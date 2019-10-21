#!/usr/bin/env python3

from glob import glob

import nine as N
import systems as S


cuty = []
igi = ""

j = 0
p = sorted(glob("./out/*.bel"))[j]
if True:

# for p in sorted(glob("./out/*.bel"))[2:5]:

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
               R_alpha=0,
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


# bcdef = ("b", "c", "d", "e", "f")
# log = "name:omega:theta:e:i\n"
# try:
#     for j, (c, p) in enumerate(zip(C, sorted(glob("./out_europa/*.bel")))):
#         name = p.split("/")[-1].split(".")[0].split("-0")[0]
#         log += name.replace("_", " ")
#         D = N.load_sim(p)
#         n_cnt = len(c) - 1
#         omega_fft = [0 for l in range(n_cnt)]
#         theta_fft = [0 for l in range(n_cnt)]
#         e_fft = [0 for l in range(n_cnt)]
#         i_fft = [0 for l in range(n_cnt)]
#         for k in range(n_cnt):
#             print(f"\n\t{c.name} {bcdef[k]}\n")
#             ignore = [l for l in range(n_cnt) if l != k]
#             omega_happy = False
#             theta_happy = False
#             N.plot(D, L="e", L_unit=None, R="i", R_unit=r"\degree",
#                    output=False, rasterized=True, ignore_bodies=ignore)
#             cut = float(input(f"cut: "))
#             if cut > 0:
#                 steps = int(cut * D["steps"] / 100)
#                 D["o"][k][steps:] = 0
#                 D["h"][k][steps:] = 0
#                 D["e"][k][steps:] = 0
#                 D["i"][k][steps:] = 0
#                 continue
#             while True:
#                 N.plot(D, L=r"\omega", L_unit=r"\degree", R=r"\Theta",
#                        R_unit=None, output=False, rasterized=True,
#                        ignore_bodies=ignore,
#                        L_ft=omega_fft[k] if omega_happy else None,
#                        R_ft=theta_fft[k] if theta_happy else None)
#                 if not omega_happy:
#                     omega_fft[k] = int(input(f"omega fft: "))
#                 if not theta_happy:
#                     theta_fft[k] = int(input(f"theta fft: "))
#                 N.plot(D, L=r"\omega", L_unit=r"\degree", L_ft=omega_fft[k],
#                        R=r"\Theta", R_unit=None, R_ft=theta_fft[k],
#                        output=False, rasterized=True, ignore_bodies=ignore)
#                 if not omega_happy:
#                     omega_happy = input("omega happy? (y/n): ").lower() == "y"
#                 if not theta_happy:
#                     theta_happy = input("theta happy? (y/n): ").lower() == "y"
#                 if omega_happy and theta_happy:
#                     break
#             e_happy = False
#             i_happy = False
#             while True:
#                 N.plot(D, L="e", L_unit=None, R="i", R_unit=r"\degree",
#                        output=False, rasterized=True, ignore_bodies=ignore,
#                        L_ft=e_fft[k] if e_happy else None,
#                        R_ft=i_fft[k] if i_happy else None)
#                 if not e_happy:
#                     e_fft[k] = int(input(f"e fft: "))
#                 if not i_happy:
#                     i_fft[k] = int(input(f"i fft: "))
#                 N.plot(D, L="e", L_unit=None, L_ft=e_fft[k], R="i",
#                        R_unit=r"\degree", R_ft=i_fft[k], output=False,
#                        rasterized=True, ignore_bodies=ignore)
#                 if not e_happy:
#                     e_happy = input("e happy? (y/n):").lower() == "y"
#                 if not i_happy:
#                     i_happy = input("i happy? (y/n):").lower() == "y"
#                 if e_happy and i_happy:
#                     break
#         if cut <= 0:
#             log += ":" + ",".join(map(str, omega_fft))
#             log += ":" + ",".join(map(str, theta_fft))
#             log += ":" + ",".join(map(str, e_fft))
#             log += ":" + ",".join(map(str, i_fft))
#         else:
#             log += f"--{cut}--"
#         log += "\n"
#         N.plot(D, L=r"\omega", L_unit=r"\degree",
#                L_ft=omega_fft if cut <= 0 else None,
#                R=r"\Theta", R_unit=None,
#                R_ft=theta_fft if cut <= 0 else None,
#                save_name=name+"-omega_theta.pdf")
#         N.plot(D, L="e", L_unit=None,
#                L_ft=e_fft if cut <= 0 else None,
#                R="i", R_unit=r"\degree",
#                R_ft=i_fft if cut <= 0 else None,
#                save_name=name+"-e_i.pdf")
# except KeyboardInterrupt:
#     pass
# finally:
#     with open("out.log", "a") as f:
#         f.write("\n\n\n")
#         f.write(log)


# fft = 5
# for j, (c, p) in enumerate(zip(C, sorted(glob("./out_europa/*.bel")))):
#     name = p.split("/")[-1].split(".")[0].split("-0")[0]
#     D = N.load_sim(p)
#     # for fft in (5, 10, 20, 30):
#     N.plot(D, save_name=name+"-omega_theta.pdf", L=r"\omega",
#             L_unit=r"\degree", L_ft=fft, R=r"\Theta", R_unit=None, R_ft=fft,
#             rasterized=True)
#     N.plot(D, save_name=name+"-e_i.pdf", L="e", L_unit=None, L_ft=fft,
#             R="i", R_unit=r"\degree", R_ft=fft, rasterized=True)
