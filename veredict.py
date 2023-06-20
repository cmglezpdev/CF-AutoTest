from colorama import Back, Style

def print_veredict(veredict: str):
    if veredict == "AC":
        print(Back.GREEN + "ACCEPTED" + Style.RESET_ALL)
    elif veredict == "WA":
        print(Back.RED + "WRONG ANSWER" + Style.RESET_ALL)
    elif veredict == "TLE":
        print(Back.YELLOW + "TIME LIMIT EXCEEDED" + Style.RESET_ALL)
    elif veredict == "MLE":
        print("\033[48;2;255;165;0m" + "MEMORY LIMIT EXCEEDED" + Style.RESET_ALL)
    elif veredict == "CE":
        print(Back.LIGHTBLACK_EX + "COMPILE ERROR" + Style.RESET_ALL)
    elif veredict == "RE":
        print(Back.LIGHTBLACK_EX + "RUNTINE ERROR" + Style.RESET_ALL)
    else:
        raise Exception(f"{veredict} is not a valid veredict")