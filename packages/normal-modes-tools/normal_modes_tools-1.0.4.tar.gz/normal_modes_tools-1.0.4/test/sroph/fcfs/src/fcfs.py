import normal_modes_tools as nmt


x_nms = nmt.xyz_file_to_NormalModesList('../data/f0.xyz')
a_nms = nmt.xyz_file_to_NormalModesList('../data/f0.xyz')

for mode in x_nms:
    print(mode)
