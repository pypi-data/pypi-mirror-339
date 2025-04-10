# Using `normal_modes_tools` with the normal modes of SrOPh

## Deuterate the normal modes
The `xyz` directory contains the normal modes that come from CFOUR. The normal
modes were deuterated using the deuteration tool
```bash
python -m normal_modes_tools --deuterate\
    xyz/SrOPh_normal_modes.xyz > xyz/SrOPh-5d_normal_modes.xyz
```

## Find mode symmetries and sorted them using Mulliken's convention
The `mulliken_order` directory contains scripts that find the irrpes with which
each mode transforms, assigns them to each mode, and finally sorts the modes
using the Mulliken's convention, i.e., all modes are sorted first by their
irrep, and then within each irrep they are sorted in desceding order by
frequency.


## Compare the two sets of normal modes
The `duszyński` directory contains comparison between the two sets of normal
modes.
