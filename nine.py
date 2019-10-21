import re
import numpy as np
from matplotlib import pyplot as plt

from subprocess import call
from time import strftime, localtime
from os.path import isdir, isfile
from glob import glob


ROOT_PATH = "./"
SAVE_PATH = "/out/"


def f_num(n:float) -> str:
    r"Python float to Fortran double."
    return "{:e}".format(float(n)).replace("e", "d")


def p_num(s:str) -> float:
    r"Fortran double to Python float."
    return float(s.lower().replace("d", "e"))


def f_bool(b:bool) -> str:
    r"Python bool to Fortran bool."
    if b:
        return ".true."
    return ".false."


def p_bool(b:str) -> bool:
    r"Fortran bool to Python bool."
    return b.lower() == ".true."


def m_sol(m_j:float, i:float=None) -> float:
    r"Converts M_J or M_J * sin(i) to M_sol."
    m = m_j * 9.5458e-4
    if i is None:
        return m
    elif i <= 0:
        i += 360
    return m / np.sin(np.deg2rad(i))


def m_jup(m_s:float) -> float:
    r"Converts M_sol to M_J"
    return m_s * 1048


def theta(e:float, i:float) -> float:
    r"""
    LKE constant relation.
    theta = (1 - e^2) cos^2i = const.
    i_0 ~ 39.2 degree
    """
    return (1 - e ** 2) * (np.cos(np.deg2rad(i))) ** 2


def info_sim(file_name:str, output:bool=True) -> tuple:
    r"""
    Gives information about the result file from a simulation.
    Returns statistical information of the file: number of bodies,
        number of lines, body names
    """
    # ultra complex regexp to parse output file
    def get_line(f):
        # replace whitespace and newline with ','
        line = re.sub(r"(\s{2,}|\n)", r",", f.readline())
        # replace unit declarations [...] with ''
        line = re.sub(r"\s\[(.*?)\]", r"", line)
        # replace remaining whitespace with '_'
        line = re.sub(r"\s", r"_", line)
        # return and strip commas from start and end
        return re.split(r",", line[1:-1])
    with open(file_name, "r") as f:
        labels = get_line(f)
        names = list()
        name = get_line(f)[-1]
        n_lines = 1
        while name not in names:
            names.append(name)
            name = get_line(f)[-1]
            n_lines += 1
        n_bodies = len(names)
        for remaining in f.readlines():
            n_lines += 1
        if output:
            print()
            print("=" * (len(file_name) + 10))
            print(" " * 5 + file_name)
            print("=" * (len(file_name) + 10))
            print()
            print("Bodies:", n_bodies)
            for i, name in enumerate(names):
                print(f"{name}[{i}][:]", end=" ")
            print("\n")
            print("Datacolumns:", len(labels[:-1]))
            for i, label in enumerate(labels[:-1]):
                print(f"{label}[:][{i}]", end=" ")
            print("\n")
            print("Datalines:", n_lines)
            print()
    return n_bodies, n_lines, names


def load_sim(file_name:str, output:bool=True) -> dict:
    r"""
    Load a simulation file, detects type based on file extension.
    Currently `bel` and `bco` (partially) files are supported.
    Time prefix for scaling: dy, yr, kyr, Myr
    """
    # couple of useful options have been commentend out for better performance
    D = dict()
    D["file_name"] = file_name
    D["type"] = file_name.split(".")[-1]
    D["n"], n_lines, D["names"] = info_sim(file_name, output=output)
    D["steps"] = n_lines // D["n"]
    D["dy"] = np.zeros(D["steps"], dtype=np.float64)
    zero = np.zeros((D["n"], D["steps"]), dtype=np.float64)
    if D["type"] == "bel":
        cols = [0, 2, 3, 4, 5]
        D["a"] = zero.copy()
        D["e"] = zero.copy()
        D["i"] = zero.copy()
        D["o"] = D[r"\omega"] = zero.copy()
        D["h"] = D[r"\Theta"] = zero.copy()
    elif D["type"] == "bco":
        cols = [0, 2, 3, 4]
        D["x"] = zero.copy()
        D["y"] = zero.copy()
        D["z"] = zero.copy()
    else:
        raise Exception(f"File extension '.{D['type']}' unknown/unsupported.")
    data = np.genfromtxt(file_name, skip_header=1, usecols=cols,
                         dtype=np.float64)
    for j, t_idx in enumerate(range(0, n_lines, D["n"])):
        D["dy"][j] = data[t_idx][0]
        for n in range(D["n"]):
            if D["type"] == "bel":
                D["a"][n][j] = data[t_idx+n][1]
                D["e"][n][j] = data[t_idx+n][2]
                D["i"][n][j] = data[t_idx+n][3]
                D["o"][n][j] = data[t_idx+n][4]
                D["h"][n][j] = theta(D["e"][n][j], D["i"][n][j])
            elif D["type"] == "bco":
                D["x"][n][j] = data[t_idx+n][1]
                D["y"][n][j] = data[t_idx+n][2]
                D["z"][n][j] = data[t_idx+n][3]
    D["yr"] = D["dy"] / 365.2425
    D["kyr"] = D["yr"] / 1000
    # D["Myr"] = D["kyr"] / 1000
    return D


def sim_last(D:dict, T:str="kyr", method=np.mean) -> tuple:
    r"""
    Gives final mean values of simulation data dict.
    """
    t = int(D[T][-1])
    a = []
    e = []
    i = []
    o = []
    m = int(D["steps"] / 100)
    for n in range(D["n"]):
        a.append(method(D["a"][n][-m:-1]))
        e.append(method(D["e"][n][-m:-1]))
        i.append(method(D["i"][n][-m:-1]))
        o.append(method(D["o"][n][-m:-1]))
    return (t, a, e, i, o)


def save_file_path(name:str, file_extension:str, cnt:int=1,
                   ret_cnt:bool=False) -> str:
    r"""
    <ROOT_PATH>/<SAVE_PATH>/<name>-<cnt>.<extension>
    Overwrite file counter with cnt.
    Counter is returned if ret_cnt == True -> (str, int)
    """
    if not isdir(ROOT_PATH+SAVE_PATH):
        call(["mkdir", ROOT_PATH+SAVE_PATH])
    file_path = ROOT_PATH + SAVE_PATH + "/"
    file_path += strftime(name, localtime())
    file_path += "-%03d." + file_extension
    while isfile(file_path % cnt):
        cnt += 1
    file_path %= cnt
    if ret_cnt:
        return file_path, cnt
    return file_path


def plot(D:dict, plot_title:str=None, save_name:str=None,
         cnt:int=1, T:str="kyr", L:str="e", R:str="i", L_lim:list=None,
         R_lim:tuple=None, L_ft:list=None, R_ft:list=None,
         L_col:str="red", R_col:str="blue", L_style:str="-",
         R_style:str="-", L_unit:str=None, R_unit:str=r"\degree",
         L_alpha:float=0.3, R_alpha:float=0.3, cut_at:list=None,
         legend_off:float=1.15, grid_opt:dict=None, hspace:float=0.4,
         dpi:int=300, output:bool=True, ignore_bodies:list=None,
         **kwargs) -> None:
    r"""Do some nice plotting bro!"""
    save_path = None
    if output:
        print("loading sim")
    # left FFT cut if given as number
    if L is not None:
        if type(L_ft) is int or type(L_ft) is tuple and len(L_ft) == 2:
            L_ft = [L_ft] * D["n"]
        elif type(L_ft) is list and len(L_ft) == 1:
            L_ft *= D["n"]
    # right FFT cut if given as number
    if R is not None:
        if type(R_ft) is int or type(R_ft) is tuple and len(R_ft) == 2:
            R_ft = [R_ft] * D["n"]
        elif type(R_ft) is list and len(R_ft) == 1:
            R_ft *= D["n"]
    if output:
        print("preparing plot")
    if L_unit is None or L_unit == "" and L is not None:
        L_unit = "~"
    if R_unit is None or R_unit == "" and R is not None:
        R_unit = "~"
    if cut_at is None or (type(cut_at) in {tuple, list} and len(cut_at) == 0):
        cut_at = [0] * D["n"]
    elif type(cut_at) in {int, float}:
        cut_at = [cut_at] * D["n"]
    if type(ignore_bodies) in {tuple, list, str}:
        if len(ignore_bodies) == 0:
            ignore_bodies = None
        if type(ignore_bodies) is str:
            ignore_bodies = [le for le in ignore_bodies]
            for k, letter in enumerate("bcdefgh"):
                for bdyk in range(len(ignore_bodies)):
                    if ignore_bodies[bdyk] == letter:
                        ignore_bodies[bdyk] = k
    if L_alpha is None:
        L_alpha = 0
    if R_alpha is None:
        R_alpha = 0
    # use TeX style for plotting
    plt.rc("text", usetex=True)
    plt.rc("font", family="serif")
    plt.rcParams["text.latex.preamble"] = [r"\usepackage{siunitx}"]
    # allow the skipping of bodies
    if ignore_bodies is not None:
        will_skipp = len(ignore_bodies)
        if D["n"] - len(ignore_bodies) == 1:
            plt.rcParams["figure.figsize"] = 6.5, 2
    else:
        will_skipp = 0
    skipped = 0
    fig, ax = plt.subplots(D["n"]-will_skipp, sharex=True)
    for j in range(D["n"]):
        if ignore_bodies is not None and j in ignore_bodies:
            skipped += 1
            continue
        j_skp = j - skipped
        if output:
            print("\n\tplot body:", D["names"][j])
        # only one ax (body) doesnt allow indexing
        if D["n"] - will_skipp == 1:
            ax1 = ax
        else:
            ax1 = ax[j_skp]
        # --- head ---
        if j_skp == 0 and plot_title is not None:
            plot_title = plot_title + r"\\[1em]" + D["names"][j]
        else:
            plot_title = D["names"][j]
        plt.setp(ax1, title=plot_title.replace("_", " "))
        if grid_opt is not None:
            ax1.grid(**grid_opt)
        # --- left side ---
        if L_ft is None:
            L_D = D[L][j]
        else:
            if output:
                print(f"\t{L} FFT = {L_ft[j_skp]}")
            ft = np.fft.rfft(D[L][j])
            if type(L_ft[j_skp]) is tuple and len(L_ft[j_skp]) == 2:
                ft[L_ft[j_skp][0]:L_ft[j_skp][1]] = 0
            else:
                ft[L_ft[j_skp]:] = 0
            L_D = np.fft.irfft(ft)
        if L_lim is None:
            L_min = np.amin(D[L][j])
            L_max = np.amax(D[L][j])
        else:
            L_min, L_max = L_lim
        L_off = (L_max - L_min) / 10
        if output:
            print(f"\t{L} min/max/off = "
                  f"{L_min:3.2f}/{L_max:3.2f}/{L_off:3.2f}")
        if cut_at[j] == 0:
            L_y = L_D
        else:
            cut_steps = int(D["steps"]*cut_at[j])
            L_y = L_D[:cut_steps]
        L_x = D[T][:L_y.shape[0]]
        plt.setp(ax1, ylim=[L_min-L_off, L_max+L_off])
        ax1.set_ylabel(fr"${L}~[\si{{{L_unit}}}]$")
        ax1.plot(L_x, L_y, linestyle=L_style, c=L_col,
                 label=fr"${L}$", **kwargs)
        if 0 < L_alpha < 1 and L_ft is not None:
            if cut_at[j] == 0:
                L_y_b = D[L][j]
            else:
                L_y_b = D[L][j][:cut_steps]
            L_x_b = D[T][:L_y_b.shape[0]]
            ax1.plot(L_x_b, L_y_b, c=L_col, alpha=L_alpha, **kwargs)
        if j_skp == 0:
            ax1.legend(frameon=False, loc=10,
                       bbox_to_anchor=(0.1, legend_off))
        # --- right side ---
        if R is not None:
            ax2 = ax1.twinx()
            if R_ft is None:
                R_D = D[R][j]
            else:
                if output:
                    print(f"\t{R} FFT = {R_ft[j_skp]}")
                ft = np.fft.rfft(D[R][j])
                if type(R_ft[j_skp]) is tuple and len(R_ft[j_skp]) == 2:
                    ft[R_ft[j_skp][0]:R_ft[j_skp][1]] = 0
                else:
                    ft[R_ft[j_skp]:] = 0
                R_D = np.fft.irfft(ft)
            if R_lim is None:
                R_min = np.amin(D[R][j])
                R_max = np.amax(D[R][j])
            else:
                R_min, R_max = R_lim
            R_off = (R_max - R_min) / 10
            if output:
                print(f"\t{R} min/max/off = "
                      f"{R_min:3.2f}/{R_max:3.2f}/{R_off:3.2f}")
            if cut_at[j] == 0:
                R_y = R_D
            else:
                cut_steps = int(D["steps"]*cut_at[j])
                R_y = R_D[:cut_steps]
            R_x = D[T][:R_y.shape[0]]
            plt.setp(ax2, ylim=[R_min-R_off, R_max+R_off])
            ax2.set_ylabel(fr"${R}\, [\si{{{R_unit}}}]$")
            ax2.plot(R_x, R_y, linestyle=R_style, c=R_col,
                     label=fr"${R}$", **kwargs)
            if 0 < R_alpha < 1 and R_ft is not None:
                if cut_at[j] == 0:
                    R_y_b = D[R][j]
                else:
                    R_y_b = D[R][j][:cut_steps]
                R_x_b = D[T][:R_y_b.shape[0]]
                ax2.plot(R_x_b, R_y_b, c=R_col, alpha=R_alpha, **kwargs)
            if j_skp == 0:
                ax2.legend(frameon=False, loc=10,
                           bbox_to_anchor=(0.9, legend_off))
    if output:
        print()
    # --- bottom ---
    T_min = np.amin(D[T])
    T_max = np.amax(D[T])
    T_off = (T_max - T_min) / 20
    if output:
        print(f"t [{T}] min/max/off = "
              f"{T_min:3.2f}/{T_max:3.2f}/{T_off:3.2f}")
    plt.setp(ax1, xlim=[T_min-T_off, T_max+T_off])
    ax1.set_xlabel(fr"$t\,[\si{{{T}}}]$")
    # --- finalize ---
    plt.subplots_adjust(hspace=hspace)
    # if no save name is given, just show the plot
    if save_name is None:
        if output:
            print("showing plot")
        plt.show()
        plt.close()
    else:
        if output:
            print("saving plot to: ", end="")
        # get file extension from save_name
        save_name_split = save_name.split(".")
        extension = save_name_split.pop()
        save_name = ".".join(save_name_split)
        if extension not in {"pdf", "png", "jpg", "jpge"}:
            raise Exception(f"Unsoported file extension '.{extension}'.")
        save_path = save_file_path(save_name, extension, cnt)
        if output:
            print(save_path)
        plt.savefig(save_path, dpi=dpi, bbox_inches="tight")
        if output:
            print("done!")
    plt.close()


class NineConf:

    def __init__(self, bodies:list, name:str=r"%Y-%m-%d", timing:list=None,
                 integrator_id:int=4, candy_lie_stepsize:float=1e-1,
                 error_mark:float=1e-10, integrator_coordiantes:str="b",
                 inputformat:str="he", lie_sw:int=11, lie_st:list=[8, 14],
                 min_stepsize:float=1e-10, cutoff_radius:list=None,
                 ce_file:list=[False, 1e-1, 1e-6],
                 merging:list=[False, 1e-10, 2], limit_mass:float=6.4e-11,
                 show_progress:bool=True, outputfiles:str="bco",
                 planetoid_rings:bool=False):
        self.__bodies = bodies
        self.__name = name
        self.__timing = timing
        self.__integrator_id = integrator_id
        self.__candy_lie_stepsize = candy_lie_stepsize
        self.__error_mark = error_mark
        self.__integrator_coordiantes = integrator_coordiantes
        self.__inputformat = inputformat
        self.__lie_sw = lie_sw
        self.__lie_st = lie_st
        self.__min_stepsize = min_stepsize
        # allows cutoff radius to be a number or None
        if cutoff_radius is None:
            self.__cutoff_radius = [0, False, False]
        elif type(cutoff_radius) in {int, float}:
            self.__cutoff_radius = [cutoff_radius, False, False]
        else:
            self.__cutoff_radius = cutoff_radius
        self.__ce_file = ce_file
        self.__merging = merging
        self.__limit_mass = limit_mass
        self.__show_progress = show_progress
        self.__outputfiles = outputfiles
        self.__planetoid_rings = planetoid_rings
        self.__overwrite_timing = None  # overwrite timing in .run()
        self.__inn_file = None
        self.__inn_cnt = None  # save counter from last inn file
        self.__out_file = None

    def __str__(self) -> str:
        return self.__C

    def __len__(self) -> int:
        return len(self.__bodies)

    @property
    def __file_extensions(self) -> list:
        return self.__outputfiles.split(" ")

    @property
    def name(self) -> str:
        return self.__name

    def save(self) -> int:
        r"""
        Save .inn file.
        """
        self.__inn_file, self.__inn_cnt = \
            save_file_path(self.__name, "inn", ret_cnt=True)
        with open(self.__inn_file, "w") as f:
            f.write(self.__C)
        return self.__inn_file, self.__inn_cnt

    def run(self, overwrite_timing:list=None, inn_file:str=None,
            exe_path:str=ROOT_PATH+"/nine.exe") -> (str, str):
        r"""
        Run the simulation (saves beforehand).
        Overwrite timing lets you change the timing (nona)
        -> [start, stop, step]
        """
        self.__overwrite_timing = overwrite_timing
        if inn_file is None:
            self.save()
        else:
            self.__inn_file = inn_file
        call(["cp", self.__inn_file, ROOT_PATH+"/config.inn"])
        try:
            call(exe_path)
            for file_extension in self.__file_extensions:
                old_files = glob(ROOT_PATH+"/*."+file_extension)
                # raise error if there are other files with that extension
                # (avoid overwriting old simulations)
                if len(old_files) > 1:
                    raise FileExistsError
                old_file = old_files[0]
                new_file = save_file_path(self.__name, file_extension,
                                          cnt=self.__inn_cnt)
                call(["mv", old_file, new_file])
                self.__out_file = new_file
        except FileExistsError:
            print("Old sim files found.")
        finally:
            call(["rm", ROOT_PATH+"/config.inn"])
            return self.__inn_file, self.__out_file

    def table(self, D:dict=None, save_name:str=None, T:str="kyr") -> str:
        r"""
        The D is for comparison with the final values, if None only the
        initial values are shown.
        When save_name is provided, the table will be saved in that file, else
        the table will be returned as str.
        T... time prefix yr, kyr, Myr
        """
        sep = "&"
        eol = r"\\" + "\n"
        indent = 4 * " "
        if type(D) is str:
            D = load_sim(D)
        if D is not None:
            t, a, e, i, o = sim_last(D)
            h = [theta(ee, i[j]) for j, ee in enumerate(e)]
            tex = r"\begin{tabular}{ccccccc@{\hspace{2em}}ccccc}" + "\n"
        else:
            tex = r"\begin{tabular}{cccccc}" + "\n"
        tex += indent + r"\toprule" + "\n"
        tex += indent + 2 * sep
        if D is not None:
            tex += r"\multicolumn{5}{c}{$t=0$}" + sep
            tex += fr"\multicolumn{{5}}{{c}}{{$t=\SI{{{t}}}{{{T}}}$}}" + eol
            tex += indent + sep
        tex += r"$m[\si{M_J}]$" + sep
        tex += r"$a_0[\si{au}]$" + sep
        tex += r"$e_0[\si{~}]$" + sep
        tex += r"$i_0[\si{\degree}]$" + sep
        tex += r"$\omega_0[\si{\degree}]$"
        if D is not None:
            tex += sep
            tex += r"$\Theta_0[\si{~}]$" + sep
            tex += r"$a\,[\si{au}]$" + sep
            tex += r"$e\,[\si{~}]$" + sep
            tex += r"$i\,[\si{\degree}]$" + sep
            tex += r"$\omega\,[\si{\degree}]$" + sep
            tex += r"$\Theta\,[\si{~}]$"
        tex += eol
        tex += indent + r"\midrule" + "\n"
        for n, body in enumerate(self.__bodies[1:]):
            tex += indent + fr"{body[-1]}" + sep
            if body[6] is None:
                mass = m_sol(body[7], body[2])
            else:
                mass = body[6]
            mass = m_jup(mass)
            tex += fr"${round(mass, 2):g}$" + sep
            if D is not None:
                body_h = theta(body[1], body[2])
                en = enumerate([*body[0:4], body_h,
                                a[n], e[n], i[n], o[n], h[n]])
            else:
                en = enumerate(body[0:4])
            for j, val in en:
                tex += fr"${round(val, 2):g}$" + sep
            tex = tex[:-len(sep)] + eol  # remove last separator
        tex += indent + r"\bottomrule" + "\n"
        tex += r"\end{tabular}"
        if save_name is not None:
            save_path = save_file_path(save_name.replace(".tex", ""), "tex")
            with open(save_path, "w") as f:
                return f.write(tex)
        return tex

    @property
    def __C(self) -> str:
        #     0,   1,      2,      3,      4,      5,     6,          7,    8
        # a[au], e[], i[deg], ω[deg], Ω[deg], M[deg], M_sol, M_J*sin(i), NAME
        str_bodies = ""
        for body in self.__bodies:
            # conversion to M_sol if mass is given in M_J * sin(i)
            if body[6] is None:
                body[6] = m_sol(body[7], body[2])
            str_bodies += str(7 * "{:<12}\t").format(*map(f_num, body[:7]))
            # don't save whitspaces in name
            str_bodies += body[-1].replace(" ", "_") + "\n"
        # allow overwrite of timing with self.run()
        # either self.__timing or self.__overwrite_timing must be not None
        if self.__overwrite_timing is None:
            if self.__timing is None:
                raise Exception("No timings!")
            else:
                self.__overwrite_timing = self.__timing
        timeing = " ".join(map(f_num, self.__overwrite_timing))
        self.__overwrite_timing = None
        lie_st = " ".join(map(str, map(int, self.__lie_st)))
        cutoff_radius = " ".join([f_num(self.__cutoff_radius[0]),
                                  *map(f_bool, self.__cutoff_radius[1:])])
        ce_file = " ".join([f_bool(self.__ce_file[0]),
                            *map(f_num, self.__cutoff_radius[1:])])
        if type(self.__merging[0]) in {int, bool}:
            if self.__merging[0]:
                merging_bool = "yes"
            else:
                merging_bool = "no"
        else:
            merging_bool = self.__merging[0]
        merging = " ".join([merging_bool, *map(f_num, self.__merging[1:])])
        if self.__planetoid_rings:
            planetoid_rings = "yes"
        else:
            planetoid_rings = "no"
        return f"""{int(self.__integrator_id):<42}...id number of integrator (see end of file)
{timeing:<42}...start time / end time / outputtimes [days]
{f_num(self.__candy_lie_stepsize):<42}...stepsize for Candy and ordercontrolled Lie Series [days]
{len(self):<42}...number of bodies in this file (without counting bodies in planetoid rings)
{f_num(self.__error_mark):<42}...error mark (Lie Series: eps = local error)
{str(self.__integrator_coordiantes):<42}...coordinates during integration: barycentric only -> b)
{str(self.__inputformat):<42}...Inputformat (rv-vectors: (rv), heliocentric Keplerian elements: (he), Yarkovsky elements: (ye))
{int(self.__lie_sw):<42}...Lie-Itegrator  SW  (=Anzahl der (minimalen) Lieterme) (Lie specific: number of sequence terms) > 2!!
{lie_st:<42}...Lie-Integrator ST (order window for term control: minimum order / maximum order)
{f_num(self.__min_stepsize):<42}...minimum stepsize [days * Gaussian Gravitational Constant]
{cutoff_radius:<42}...Cutoff-radius [AU] / cutoff <= 0.d0  means no cuttoff, stop calculation when massive, massless body beyond cutoff? (.true./.false. .true./false.)
{ce_file:<42}...Close Encounter output file? (yes/no) / miminum pair distance for output[AU]
{merging:<42}...Merging? (yes/no),   minimum merging radius [AU], maximum merging radius [AU]
{f_num(self.__limit_mass):<42}...limit mass for mutual planetesimal interaction [Msun] (NICE Model)
{f_bool(self.__show_progress):<42}...show progress in terminal
{str(self.__outputfiles):<42}...Outputfiles(en=energy conservation/hel=heliocentric elements/hco=heliocentric coordinates/bco= barycentric coordinates/bbc=barycentric coordinates binary format/bhe=heliocentric elements binary output)
{planetoid_rings:<42}...Planetoid rings? (yes/no)
{str_bodies}


Input format heliocentric Keplerian elements:
a   e   i  argument of perihelion (omega)  argument ofthe ascending node (Omega)  mean anomaly (M) mass (Solar masses)

Input format heliocentric Keplerian elements:
rx   ry   rz    vx    vy    vz     mass (Solar masses)

Input format Yarkovsky elements:semi-major axis (a) [AU] eccentricity (e) [] inclination (i) [deg]  argument of perihelion (omega) [deg]argument of the ascending node (Omega) [deg]  mean anomaly (M) [deg]  mass [Solar masses]   prograde (0) / retrograde (180) rotation  thermal capacity [J/kg/K]  k_0 and k_1 parameters of the surface thermalconductivity [K(T) = k_0 + k_1 T_av^3]   density of the surface layer [kg/m^3]  radius of the body [km]  rotation frequency [Hz]  surface absorptivity=emissivity  bulk density [kg/m^3]

Integrators:

0.....Candy (symplectic 4th order, fixed stepsize)
1.....Yoshida (symplectic & symmetric 8th order, fixed stepsize)
2.....standard Lie series Integrator with adaptive stepsize control (LieSW)
3.....Bulirsch Stoer with adaptive stepsize(Mercury6)
4.....Gauss Radau with adaptive stepsize
5.....Gauss Radau with adaptive stepsize and GR (spheric heliocentric metric)
6.....Gauss Radau with adaptive stepsize, GR (spheric heliocentric metric) and Yarkovsky Thermal effect
7.....Gauss Radau with adaptive stepsize, GR (EIH barycentric metric) 
8.....Gauss Radau with adaptive stepsize, GR (EIH barycentric metric) and Yarkovsky Thermal effect"""
