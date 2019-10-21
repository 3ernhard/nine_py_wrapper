from nine import NineConf, m_sol


YR = 365.2425  # [dy]
MON = YR / 12  # [dy]


def SOL_JUP(a=3.4, e=0.30, i=48.00, o=300, tons=1000, name="Asteroid"):
    # source:   wikipedia
    return NineConf(
        bodies=[
          # [a[au], e[], i[deg], ω[deg], Ω[deg], M[deg],     M_sol, M_J*sin(i),      NAME],
            [    0,   0,      0,      0,      0,      0,         1,       None,     "Sun"],
            [  5.2,   0,      0,      0,      0,      0,    1/1047,       None, "Jupiter"],
            [    a,   e,      i,      o,      0,      0, tons/5e28,       None,      name],
        ],
        timing=[0, YR*1e5, MON*6],
        name=f"SOL_JUP_{name.upper()}",
        outputfiles="bel",
    )


def TRAPPIST_1():
    # source:   private
    return NineConf(
        bodies=[
          # [    a[au],        e[],  i[deg], ω[deg], Ω[deg], M[deg],      M_sol, M_J*sin(i),           NAME],  # periods[days]
            [        0,          0,       0,      0,      0,      0,       0.08,       None, "TRAPPIST 1 a"],  #             0
            [1.150e-02, 0.6973e-02,   89.65,    306,      0,      0, 4.7728e-06,       None, "TRAPPIST 1 b"],  #       1.59254
            [1.576e-02, 0.5663e-02,   89.67,    255,      0,      0, 6.0496e-06,       None, "TRAPPIST 1 c"],  #       2.55491
            [2.219e-02, 1.1389e-02,   89.75,    204,      0,      0, 2.0672e-06,       None, "TRAPPIST 1 d"],  #       4.26863
            [2.916e-02, 1.0885e-02,   89.86,    153,      0,      0, 3.6480e-06,       None, "TRAPPIST 1 e"],  #       6.43027
            [3.836e-02, 1.4185e-02,   89.68,    102,      0,      0, 2.6144e-06,       None, "TRAPPIST 1 f"],  #       9.70216
            [4.670e-02, 0.6053e-02,   89.71,     51,      0,      0, 6.7488e-06,       None, "TRAPPIST 1 g"],  #       13.0321
            [6.170e-02, 0.7747e-02,   89.80,      0,      0,      0, 3.0400e-06,       None, "TRAPPIST 1 h"],  #       19.7914
        ],
        timing=[0, YR*1e5, YR*30],
        name="TRAPPIST_1",
        outputfiles="bel",
    )


def HD_12661(i_b=0, i_c=0):
    # source:   http://exoplanet.eu/catalog/hd_12661_b/
    #           http://exoplanet.eu/catalog/hd_12661_c/
    # doi:      10.1051/0004-6361:200810843
    # pdf:      2009AA-LT.pdf
    return NineConf(
        bodies=[
          # [a[au],   e[], i[deg], ω[deg], Ω[deg], M[deg], M_sol, M_J*sin(i),         NAME],
            [    0,     0,      0,      0,      0,      0,  1.07,       None, "HD 12661 a"],
            [ 0.83, 0.377,    i_b,    296,      0,      0,  None,       2.30, "HD 12661 b"],
            [ 2.56, 0.031,    i_c,    165,      0,      0,  None,       1.57, "HD 12661 c"],
        ],
        timing=[0, YR*1e5, YR],
        name=f"HD_12661",
        outputfiles="bel",
    )


def HD_169830(i_b=0, i_c=0):
    # source:   http://exoplanet.eu/catalog/hd_169830_b/
    #           http://exoplanet.eu/catalog/hd_169830_c/
    # doi:      10.1051/0004-6361:200810843
    # pdf:      2009AA-LT.pdf
    return NineConf(
        bodies=[
          # [a[au],   e[], i[deg], ω[deg], Ω[deg], M[deg], M_sol, M_J*sin(i),          NAME],
            [    0,     0,      0,      0,      0,      0,  1.40,       None, "HD 169830 a"],
            [ 0.81, 0.310,    i_b,    148,      0,      0,  None,       2.88, "HD 169830 b"],
            [ 3.60, 0.330,    i_c,    252,      0,      0,  None,       4.04, "HD 169830 c"],
        ],
        timing=[0, YR*1e5, YR],
        name=f"HD_169830",
        outputfiles="bel",
    )


def HD_74156(i_b=0, i_c=0, i_d=0):
    # source:   http://exoplanet.eu/catalog/hd_74156_b/
    #           http://exoplanet.eu/catalog/hd_74156_c/
    #           http://exoplanet.eu/catalog/hd_74156_d/
    # doi:      10.1051/0004-6361:200810843
    # pdf:      2009AA-LT.pdf
    return NineConf(
        bodies=[
          # [ a[au],    e[], i[deg], ω[deg], Ω[deg], M[deg],        M_sol, M_J*sin(i),         NAME],
            [     0,      0,      0,      0,      0,      0,         1.24,       None, "HD 74156 a"],
            [0.2916, 0.6380,    i_b, 175.35,      0,      0,         None,      1.778, "HD 74156 b"],
            [3.8200, 0.3829,    i_c, 268.90,      0,      0,         None,      7.997, "HD 74156 c"],
            [1.0100, 0.2500,    i_d, 166.50,      0,      0, m_sol(0.396),       None, "HD 74156 d"],
        ],
        timing=[0, YR*1e5, YR*3],
        name=f"HD_74156",
        outputfiles="bel",
    )


def HD_155358(i_b=0, i_c=0):
    # source:   http://exoplanet.eu/catalog/hd_155358_b/
    #           http://exoplanet.eu/catalog/hd_155358_c/
    # doi:      10.1051/0004-6361:200810843
    # pdf:      2009AA-LT.pdf
    return NineConf(
        bodies=[
          # [a[au],   e[], i[deg], ω[deg], Ω[deg], M[deg], M_sol, M_J*sin(i),          NAME],
            [    0,     0,      0,      0,      0,      0,  0.92,       None, "HD 155358 a"],
            [ 0.64, 0.170,    i_b, 143.00,      0,      0,  None,       0.85, "HD 155358 b"],
            [ 1.02, 0.160,    i_c, 180.00,      0,      0,  None,       0.82, "HD 155358 c"],
        ],
        timing=[0, YR*1e5, YR],
        name=f"HD_155358",
        outputfiles="bel",
    )


def HD_82943(i_d=0, o_d=0):
    # source:   http://exoplanet.eu/catalog/hd_82943_b/
    #           http://exoplanet.eu/catalog/hd_82943_c/
    #           http://exoplanet.eu/catalog/hd_82943_d/
    # doi:      doi:10.1111/j.1365-2966.2009.15532.x
    # pdf:      2009MNRAS-LT.pdf
    return NineConf(
        bodies=[
          # [a[au],   e[], i[deg], ω[deg], Ω[deg], M[deg],         M_sol, M_J*sin(i),         NAME],
            [    0,     0,      0,      0,      0,      0,          1.18,       None, "HD 82943 a"],
            [ 1.19, 0.203,   19.4, 107.00,      0,      0,   m_sol(14.5),       None, "HD 82943 b"],
            [0.746, 0.425,   19.4, 133.00,      0,      0,   m_sol(4.78),       None, "HD 82943 c"],
            [2.145, 0.000,    i_d,    o_d,      0,      0,          None,       0.29, "HD 82943 d"],
        ],
        timing=[0, YR*1e5, YR],
        name=f"HD_82943",
        outputfiles="bel",
    )


def HD_60532():
    # source:   http://exoplanet.eu/catalog/hd_60532_b/
    #           http://exoplanet.eu/catalog/hd_60532_c/
    # doi:      doi:10.1111/j.1365-2966.2009.15532.x
    # pdf:      2009MNRAS-LT.pdf
    return NineConf(
        bodies=[
          # [a[au],   e[], i[deg], ω[deg], Ω[deg], M[deg],         M_sol, M_J*sin(i),          NAME],
            [    0,     0,      0,      0,      0,      0,          1.44,       None, "HD 60532 a"],
            [ 0.77, 0.278,     20, 352.83,      0,      0,   m_sol(9.21),       None, "HD 60532 b"],
            [ 1.58, 0.038,     20, 119.49,      0,      0,  m_sol(21.81),       None, "HD 60532 c"],
        ],
        timing=[0, YR*1e5, YR],
        name=f"HD_60532",
        outputfiles="bel",
    )


def Uma_47(i_b=0, i_c=0, i_d=0):
    # source:   http://exoplanet.eu/catalog/47_uma_b/
    #           http://exoplanet.eu/catalog/47_uma_c/
    #           http://exoplanet.eu/catalog/47_uma_d/
    # doi:      doi:10.1111/j.1365-2966.2009.15532.x
    # pdf:      2009MNRAS-LT.pdf
    return NineConf(
        bodies=[
          # [a[au],   e[], i[deg], ω[deg], Ω[deg], M[deg], M_sol, M_J*sin(i),       NAME],
            [    0,     0,      0,      0,      0,      0,  1.03,       None, "47 Uma a"],
            [  2.1, 0.032,    i_b,  334.0,      0,      0,  None,       2.53, "47 Uma b"],
            [  3.6, 0.098,    i_c,  295.0,      0,      0,  None,       0.54, "47 Uma c"],
            [ 11.6, 0.160,    i_d,  110.0,      0,      0,  None,       1.64, "47 Uma d"],
        ],
        timing=[0, YR*1e5, YR],
        name=f"47_Uma",
        outputfiles="bel",
    )



def GJ_876():
    # source:   http://exoplanet.eu/catalog/gj_876_b/
    #           http://exoplanet.eu/catalog/gj_876_c/
    #           http://exoplanet.eu/catalog/gj_876_d/
    #           http://exoplanet.eu/catalog/gj_876_e/
    # doi:      10.1007/s10569-011-9372-0
    # pdf:      2011CeMDA-LT.pdf
    return NineConf(
        bodies=[
          # [     a[au],   e[], i[deg], ω[deg], Ω[deg], M[deg],        M_sol, M_J*sin(i),       NAME],
            [         0,     0,      0,      0,      0,      0,        0.334,       None, "GJ 876 a"],
            [  0.208317,   0.0,   84.0,  116.7,      0,      0, m_sol(1.938),       None, "GJ 876 b"],
            [   0.12959, 0.002,  48.07,  225.2,      0,      0, m_sol(0.856),       None, "GJ 876 c"],
            [0.02080665, 0.081,   50.0,  157.4,      0,      0, m_sol(0.022),       None, "GJ 876 d"],
            [    0.3343, 0.073,   59.5,  360.0,      0,      0, m_sol(0.045),       None, "GJ 876 e"],
        ],
        timing=[0, YR*1e5, YR],
        name=f"GJ_876",
        outputfiles="bel",
    )
