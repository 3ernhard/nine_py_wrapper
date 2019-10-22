#!/usr/bin/env python3

from glob import glob

import nine as N
import systems as S


N.ROOT_PATH = "../nine/"
N.SAVE_PATH = "../plot/"


cuty = []
igi = ""

# j = 0
# p = sorted(glob("./out/*.bel"))[j]
# if True:

for p in sorted(glob("../sim/*.bel")):

    name = p.split("/")[-1].split(".")[0].split("-0")[0]
    D = N.load_sim(p)
    if 1:
        N.plot(D, save_name=name+"-e_i.pdf",
               L="e", L_unit=None, L_col="red",
               R="i", R_unit=r"\degree", R_col="dodgerblue",
               # L_alpha=0, R_alpha=0,
               L_ft=None,
               R_ft=None,
               ignore_bodies=igi,
               cut_at=cuty,
               # legend_off=1.075,
               rasterized=True)
    if 1:
        N.plot(D, save_name=name+"-omega_theta.pdf",
               L=r"\omega", L_unit=r"\degree", L_col="limegreen",
               R=r"\Theta", R_unit=None, R_col="purple",
               R_alpha=0.3,
               L_ft=None,
               R_ft=10,
               ignore_bodies=igi,
               cut_at=cuty,
               # legend_off=1.075,
               rasterized=True)


# C = [

#     S.Uma_47(i_b=10, i_c=20, i_d=30),

#     S.GJ_876(),

#     S.HD_12661(-10, 10),
#     S.HD_12661(-20, 20),
#     S.HD_12660(-40, 40),

#     S.HD_155358(-10, 10),
#     S.HD_155358(-20, 20),
#     S.HD_155358(-40, 40),

#     S.HD_169830(-10, 10),
#     S.HD_169830(-20, 20),
#     S.HD_169830(-40, 40),

#     S.HD_60532(),

#     S.HD_74156(-10,  5, 10),
#     S.HD_74156(-20, 10, 20),
#     S.HD_74156(-40, 20, 40),

#     S.HD_82943(i_d=50, o_d=180),

#     S.SOL_JUP(),

# ]


# for c in C:
#     c.run()

# for c, p in zip(C, sorted(glob("../sim/*.bel"))):
#     D = N.load_sim(p)
#     c.table(D)
