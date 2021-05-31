from .convert import bjerrum, debye, potential
from .consts import Na
from .misc import lbin


def str2dic(text):
    """
    str -> dict(str : str)
    Hypothesis : text look like "key = value\\n"
    Read the text and convert it into a dictionary
    """
    # split the text into lines
    lines = text.split("\n")

    # Here we use a list comprehension
    # if the line is not a commentary and it contains an equal
    # split the line at the "="
    # and remove the blank space arround the relevent data
    # dict convert that list of list into a dictionnary
    values = dict(
        [
            [seg.strip() for seg in line.split("=")]
            for line in lines
            if "#" not in line and "=" in line
        ]
    )

    return values


def dic2str(dic):
    """
    dict(str : str) -> str
    Hypothesis : ø
    Convert the dictionary into a text that look like "key = value\\n"
    """
    # We use a list comprehension to generate a list of line
    # that link the key to the value and we join thoses lines
    # with a new line symbol \n
    return "\n".join([f"{i} = {dic[i]}" for i in dic.keys()])


def read_infile(file_path):
    """
    str -> dict(str: str)
    Hypothesis : file_path is a valid path and the file is valid
    Read the file and parse it into a dictionary
    """
    with open(file_path, "r") as lines:
        values = str2dic(lines.read())
    return values


def write_infile(dic, file_path):
    """
    dict(str :str) * str -> None
    Hypothesis : file_path is valid
    write in a file the text
    """
    with open(file_path, "w") as file:
        file.write(dic2str(dic))


def ph2lb(phys, lbin=lbin):
    """
    dict(str : str) -> dict(str : str)
    Hypothesis : phys have correct input
    Read the physical units and converts them into LBM units
    """
    dx = float(phys["dx"])
    Lx = float(phys["Lx"])
    Ly = float(phys["Ly"])
    Lz = float(phys["Lz"])
    SN = int(phys["solid nodes"])
    Potup = float(phys["Potential up"])
    Potwn = float(phys["Potential down"])
    epsilon_r = float(phys["epsilon_r"])
    T = float(phys["Temp"])
    C_inf = float(phys["C_inf"]) * 1e3 * Na

    bj = bjerrum(epsilon_r, T)
    lbda = debye(C_inf, bj)

    Pup = potential(Potup, T)
    Pwn = potential(Potwn, T)

    lbin["lx"] = f"{int(Lx/dx)}"
    lbin["ly"] = f"{int(Ly/dx)}"
    lbin["lz"] = f"{int(2*SN + Lz/dx)}"
    lbin["bjl"] = f"{bj/dx}"
    lbin["lambda_D"] = f"{lbda/dx}"
    lbin["SolidSheetsEachSideOfSlit"] = f"{int(SN)}"
    lbin["FixedPotentialUP"] = f"{Pup}"
    lbin["FixedPotentialDOWN"] = f"{Pwn}"
    lbin["UB1"] = f"{int(Lx/dx + 1)}"
    lbin["UB2"] = f"{int(Lx/dx + 1)}"

    return lbin
