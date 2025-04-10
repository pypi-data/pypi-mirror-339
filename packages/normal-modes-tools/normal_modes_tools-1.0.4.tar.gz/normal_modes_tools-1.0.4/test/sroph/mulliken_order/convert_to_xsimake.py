import normal_modes_tools as nmt

import json


# xyz_file = './output/SrOPh_nmodes_Mulliken.xyz'
xyz_file = './output/SrOPh-5d_nmodes_Mulliken.xyz'
nmodes = nmt.xyz_file_to_NormalModesList(xyz_file)

outpack = list()
for idx, mode in enumerate(nmodes, start=1):
    nickname = {
        'Mulliken': {
            'number': idx,
            'symmetry': mode.irrep,
        },
        'frequency, cm-1': float(f'{mode.frequency:.2f}'),
    }
    outpack.append(nickname)

print(json.dumps(outpack))
