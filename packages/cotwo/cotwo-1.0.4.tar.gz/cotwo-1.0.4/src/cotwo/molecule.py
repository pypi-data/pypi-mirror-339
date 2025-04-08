"""High-level class"""

from itertools import combinations
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from cotwo.io import Xyz
from cotwo.rendering.atom import Atom
from cotwo.rendering.bond import Bond
from cotwo.rendering.isosurface import Isosurface
from cotwo.resources.bond_types import BondType


class Molecule:
    LAYOUT = dict(
        scene=dict(
            aspectmode="data",
            xaxis_visible=False,
            yaxis_visible=False,
            zaxis_visible=False,
            bgcolor="whitesmoke",
            dragmode="orbit",  # Ensures orbital rotation mode is active
        ),
        scene_camera=dict(
            up=dict(x=0, y=0, z=2),
            eye=dict(x=0, y=2.5, z=0),
            center=dict(x=0, y=0, z=0),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(dict(yanchor="top", y=0.99, xanchor="left", x=0.01)),
    )

    def __init__(self, atoms: list[Atom]) -> None:
        self.atoms = atoms
        assert len(self.atoms) != 0, "No atoms supplied!"
        self.bonds = self._detect_bonds_by_radius_overlap()

    @classmethod
    def from_file(cls, file: str | Path) -> "Molecule":
        """Create a Molecule from an .xyz or an .out file"""
        xyz = Xyz.from_file(Path(file))
        return cls(xyz.atoms)

    @classmethod
    def from_smiles(cls, smiles: str) -> "Molecule":
        xyz = Xyz.from_smiles(smiles)
        return cls(xyz.atoms)

    def _detect_bonds_by_radius_overlap(self, scale: float = 0.5) -> list[Bond]:
        bonds: list[Bond] = []
        for i, j in combinations(self.atoms, 2):
            bond_type = BondType.SINGLE
            bond_threshold = (
                i.element["atomic_radius"][0] + j.element["atomic_radius"][0]
            ) / 100
            bond_threshold *= scale

            # Coordination bonds are usually longer (same for hydrogen bonds etc)
            if i.is_metal or j.is_metal:
                bond_threshold *= BondType.COORDINATION.value.detection_threshold
                bond_type = BondType.COORDINATION

            distance = np.linalg.norm(j.coords.as_vec - i.coords.as_vec)

            if distance <= bond_threshold:
                bonds.append(Bond((i, j), bond_type))
        return bonds

    def create_fig(self) -> go.Figure:
        fig = go.Figure()

        for atom in self.atoms:
            mesh = atom.to_mesh()
            fig.add_trace(mesh)

        for bond in self.bonds:
            mesh = bond.to_mesh()
            fig.add_trace(mesh)

        fig.update_layout(self.LAYOUT)
        return fig

    def create_fig_with_isosurface(
        self,
        file: str | Path,
        isovalue: float = 0.005,
        colors: tuple[str, str] = ("#1E88E5", "#004D40"),
        smoothness_factor: float = 1.0,
    ) -> go.Figure:
        fig = self.create_fig()
        isosurface_meshes = Isosurface(file).to_meshes(
            isovalue, colors, smoothness_factor
        )
        for mesh in isosurface_meshes:
            fig.add_trace(mesh)
        return fig

    def show(self) -> None:
        fig = self.create_fig()
        fig.show()

    def show_with_isosurface(
        self,
        file: str | Path,
        isovalue: float = 0.005,
        colors: tuple[str, str] = ("#1E88E5", "#004D40"),
        smoothness_factor: float = 1.0,
    ) -> None:
        fig = self.create_fig_with_isosurface(file, isovalue, colors, smoothness_factor)
        fig.show()
