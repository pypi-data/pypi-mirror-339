import argparse

from posym import SymmetryNormalModes
import normal_modes_tools as nmt
from normal_modes_tools.normal_mode import (
    NormalMode,
    normalModesList_to_xyz_file,
)


def find_mode_symmetries(normal_modes: list[NormalMode]) -> list[str]:
    """ Use posym to tell the irrep of each normal mode. """

    # Prepare input in a posym format
    geometry = normal_modes[0].at
    coordinates: list[list[float]] = list()
    symbols: list[str] = list()
    for atom in geometry.atoms:
        coordinates.append(atom.xyz)
        symbols.append(atom.name)

    posym_nmodes: list[list[list[float]]] = list()
    frequencies: list[float] = list()
    for nmode in normal_modes:
        posym_nmode: list[list[float]] = list()
        for displacement in nmode.displacement:
            posym_nmode.append(displacement.xyz)
        posym_nmodes.append(posym_nmode)
        frequencies.append(nmode.frequency)

    # Let posym do the work
    sym_modes_gs = SymmetryNormalModes(
        group='c2v',  # Hack SrOPh is C2v
        coordinates=coordinates,
        modes=posym_nmodes,
        symbols=symbols,
    )

    # Prepare the output as a list of strings
    mode_symmetries: list[str] = list()
    for i in range(len(posym_nmodes)):
        symmetry = sym_modes_gs.get_state_mode(i)
        symmetry = str(symmetry)
        # HACK: SrOPh is not Mulliken-oriented in the input
        if symmetry == 'B1':
            symmetry = 'B2'
        elif symmetry == 'B2':
            symmetry = 'B1'
        
        symmetry = symmetry.lower()

        mode_symmetries.append(str(symmetry))

    return mode_symmetries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'normal_modes',
        type=str,
        help='Normal modes stored in the xyz file format.',
    )
    args = parser.parse_args()
    xyz_path = args.normal_modes
    # xyz_path = './input/SrOPh_normal_modes.xyz'
    # xyz_path = './input/SrOPh-5d_normal_modes.xyz'

    normal_modes = nmt.xyz_file_to_NormalModesList(xyz_path)

    mode_symmetries = find_mode_symmetries(normal_modes)
    for mode, irrep in zip(normal_modes, mode_symmetries):
        mode.irrep = irrep

    normal_modes.sort(key=lambda x: (x.irrep, -x.frequency))
    print(normalModesList_to_xyz_file(normal_modes))


if __name__ == "__main__":
    main()
