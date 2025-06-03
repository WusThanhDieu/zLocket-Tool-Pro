# ==================================
#!/usr/bin/env python
# coding: utf-8
# Telegram: @wus_team
# Version: 1.0.7
# Github: https://github.com/wusthanhdieu
# Description: zLocket Tool Open Sourc
# ==================================
import sys
import platform
if platform.python_version() < "3.12":
    print(f"\033[91m[!] Phiên bản python của bạn không được hỗ trợ")
    print(f"\033[93m[!] Hiện tại: Python {platform.python_version()}")
    print(f"\033[92m[+] Yêu cầu: Python 3.12 trở lên")
    sys.exit(1)
import subprocess
try:
    from colorama import Fore, Style, init
    init()
except ImportError:
    class DummyColors:
        def __getattr__(self, name):
            return ''
    Fore=Style=DummyColors()
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def itls(pkg):
    try:
        __import__(pkg)
        return True
    except ImportError:
        return False
_list_={
    'requests':
    'requests',
    'tqdm'    :
    'tqdm',
    'colorama':
    'colorama',
    'pystyle' :
    'pystyle',
    'urllib3' :
    'urllib3',
}
_pkgs=[pkg_name for pkg_name in _list_ if not itls(pkg_name)]
if _pkgs:
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] Bạn thiếu thư viện: {Fore.RED}{', '.join(_pkgs)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    install=input(f"{Fore.GREEN}[?] Bạn có muốn cài đặt thư viện này không? (y/n): {Style.RESET_ALL}")
    if install.lower()=='y':
        print(f"{Fore.BLUE}[*] Đang cài đặt thư viện...{Style.RESET_ALL}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *_pkgs])
            print(f"{Fore.GREEN}[✓] Cài đặt thành công!{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}[✗] Lỗi cài đặt, hãy thử cài tay bằng lệnh sau:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}pip install {' '.join(_pkgs)}{Style.RESET_ALL}")
            input("Nhấn Enter để thoát...")
            sys.exit(1)
    else:
        print(f"{Fore.YELLOW}[!] Cần có thư viện để tool hoạt động, cài bằng lệnh:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}pip install {' '.join(_pkgs)}{Style.RESET_ALL}")
        input("Nhấn Enter để thoát...")
        sys.exit(1)
import os, re, time, json, queue, string, random, threading, datetime
from queue import Queue
from itertools import cycle
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from requests.exceptions import ProxyError
from colorama import init, Back, Style
from typing import Optional, List
import getpass
PRINT_LOCK=threading.RLock()
def sfprint(*args, **kwargs):
    with PRINT_LOCK:
        print(*args, **kwargs)
        sys.stdout.flush()
class xColor:
    YELLOW='\033[38;2;255;223;15m'
    GREEN='\033[38;2;0;209;35m'
    RED='\033[38;2;255;0;0m'
    BLUE='\033[38;2;0;132;255m'
    PURPLE='\033[38;2;170;0;255m'
    PINK='\033[38;2;255;0;170m'
    MAGENTA='\033[38;2;255;0;255m'
    ORANGE='\033[38;2;255;132;0m'
    CYAN='\033[38;2;0;255;255m'
    PASTEL_YELLOW='\033[38;2;255;255;153m'
    PASTEL_GREEN='\033[38;2;153;255;153m'
    PASTEL_BLUE='\033[38;2;153;204;255m'
    PASTEL_PINK='\033[38;2;255;153;204m'
    PASTEL_PURPLE='\033[38;2;204;153;255m'
    DARK_RED='\033[38;2;139;0;0m'
    DARK_GREEN='\033[38;2;0;100;0m'
    DARK_BLUE='\033[38;2;0;0;139m'
    DARK_PURPLE='\033[38;2;75;0;130m'
    GOLD='\033[38;2;255;215;0m'
    SILVER='\033[38;2;192;192;192m'
    BRONZE='\033[38;2;205;127;50m'
    NEON_GREEN='\033[38;2;57;255;20m'
    NEON_PINK='\033[38;2;255;20;147m'
    NEON_BLUE='\033[38;2;31;81;255m'
    WHITE='\033[38;2;255;255;255m'
    RESET='\033[0m'
class zLocket:
    def __init__(self, device_token: str="", target_friend_uid: str="", num_threads: int=1, note_target: str=""):
        self.FIREBASE_GMPID="1:641029076083:ios:cc8eb46290d69b234fa606"
        self.IOS_BUNDLE_ID="com.locket.Locket"
        self.API_LOCKET_URL="https://api.locketcamera.com"
        self.FIREBASE_AUTH_URL="https://www.googleapis.com/identitytoolkit/v3/relyingparty"
        self.FIREBASE_API_KEY="AIzaSyCQngaaXQIfJaH0aS2l7REgIjD7nL431So"
        self.TOKEN_API_URL="https://thanhdieu.com/api/v1/locket/token"
        self.SHORT_URL="https://url.thanhdieu.com/api/v1"
        self.SV_FRQ_URL="https://thanhdieu-server.vercel.app/api/locket-friend-requests"
        self.TOKEN_FILE="token.json"
        self.TOKEN_EXPIRY_TIME=(20 + 9) * 60
        self.FIREBASE_APP_CHECK=None
        self.USE_EMOJI=True
        self.ACCOUNTS_PER_PROXY=random.randint(6,10)
        self.NAME_TOOL="zLocket Tool Pro"
        self.VERSION_TOOL="v1.0.7"
        self.TARGET_FRIEND_UID=target_friend_uid if target_friend_uid else None
        self.PROXY_LIST=[
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=20000&country=all&ssl=all&anonymity=all',
        ]
        self.print_lock=threading.Lock()
        self.successful_requests=0
        self.failed_requests=0
        self.total_proxies=0
        self.start_time=time.time()
        self.spam_confirmed=False
        self.telegram='wus_team'
        self.author='WsThanhDieu'
        self.messages=[]
        self.request_timeout=15
        self.device_token=device_token
        self.num_threads=num_threads
        self.note_target=note_target
        self.session_id=int(time.time() * 1000)
        self._init_environment()
        self.FIREBASE_APP_CHECK=self._load_token_()
        if os.name=="nt":
            os.system(
                f"title 💰 {self.NAME_TOOL} {self.VERSION_TOOL} by Api.ThanhDieu.Com 💰"
         )
    def _print(self, *args, **kwargs):
        with PRINT_LOCK:
            timestamp=datetime.datetime.now().strftime("%H:%M:%S")
            message=" ".join(map(str, args))
            sm=message
            if "[+]" in message:
                sm=f"{xColor.GREEN}{Style.BRIGHT}{message}{Style.RESET_ALL}"
            elif "[✗]" in message:
                sm=f"{xColor.RED}{Style.BRIGHT}{message}{Style.RESET_ALL}"
            elif "[!]" in message:
                sm=f"{xColor.YELLOW}{Style.BRIGHT}{message}{Style.RESET_ALL}"
            sfprint(
                f"{xColor.CYAN}[{timestamp}]{Style.RESET_ALL} {sm}", **kwargs)
    def _loader_(self, message, duration=3):
        spinner=cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        end_time=time.time() + duration
        while time.time() < end_time:
            with PRINT_LOCK:
                sys.stdout.write(f"\r{xColor.CYAN}{message} {next(spinner)} ")
                sys.stdout.flush()
            time.sleep(0.1)
        with PRINT_LOCK:
            sys.stdout.write(f"\r{xColor.GREEN}{message} ✓     \n")
            sys.stdout.flush()
    def _sequence_(self, message, duration=1.5, char_set="0123456789ABCDEF"):
        end_time=time.time() + duration
        while time.time() < end_time:
            random_hex=''.join(random.choices(char_set, k=50))
            with PRINT_LOCK:
                sys.stdout.write(f"\r{xColor.GREEN}[{xColor.WHITE}*{xColor.GREEN}] {xColor.CYAN}{message}: {xColor.GREEN}{random_hex}")
                sys.stdout.flush()
            time.sleep(0.05)
        with PRINT_LOCK:
            sys.stdout.write("\n")
            sys.stdout.flush()
    def _randchar_(self, duration=2):
        special_chars="#$%^&*()[]{}!@<>?/\\|~`-=+_"
        hex_chars="0123456789ABCDEF"
        colors=[xColor.GREEN, xColor.RED, xColor.YELLOW,
                  xColor.CYAN, xColor.MAGENTA, xColor.NEON_GREEN]
        end_time=time.time() + duration
        while time.time() < end_time:
            length=random.randint(20, 40)
            vtd=""
            for _ in range(length):
                char_type=random.randint(1, 3)
                if char_type==1:
                    vtd+=random.choice(special_chars)
                elif char_type==2:
                    vtd+=random.choice(hex_chars)
                else:
                    vtd+=random.choice("xX0")
            status=random.choice([
                f"{xColor.GREEN}[ACCESS]",
                f"{xColor.RED}[DENIED]",
                f"{xColor.YELLOW}[BREACH]",
                f"{xColor.CYAN}[DECODE]",
                f"{xColor.MAGENTA}[ENCRYPT]"
            ])
            color=random.choice(colors)
            with PRINT_LOCK:
                sys.stdout.write(
                    f"\r{xColor.CYAN}[RUNNING TOOL] {color}{vtd} {status}")
                sys.stdout.flush()
            time.sleep(0.1)
        with PRINT_LOCK:
            print()
    def _blinking_(self, text, blinks=3, delay=0.1):
        for _ in range(blinks):
            with PRINT_LOCK:
                sys.stdout.write(f"\r{xColor.WHITE}{text}")
                sys.stdout.flush()
            time.sleep(delay)
            with PRINT_LOCK:
                sys.stdout.write(f"\r{' ' * len(text)}")
                sys.stdout.flush()
            time.sleep(delay)
        with PRINT_LOCK:
            sys.stdout.write(f"\r{xColor.GREEN}{text}\n")
            sys.stdout.flush()
    def _init_environment(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        init(autoreset=True)
    def _load_token_(self):
        try:
            if not os.path.exists(self.TOKEN_FILE):
                return self.fetch_token()
            self._loader_(
                f"{xColor.YELLOW}Verifying token integrity{Style.RESET_ALL}", 0.5)
            with open(self.TOKEN_FILE, 'r') as file:
                token_data=json.load(file)
            if 'token' in token_data and 'expiry' in token_data:
                if token_data['expiry'] > time.time():
                    self._print(
                        f"{xColor.GREEN}[+] {xColor.CYAN}Loaded token from file token.json: {xColor.YELLOW}{token_data['token'][:10] + "..." + token_data['token'][-10:]}")
                    time.sleep(0.4)
                    time_left=int(token_data['expiry'] - time.time())
                    self._print(
                        f"{xColor.GREEN}[+] {xColor.CYAN}Token expires in: {xColor.WHITE}{time_left//60} minutes {time_left % 60} seconds")
                    return token_data['token']
                else:
                    self._print(
                        f"{xColor.RED}[!]{xColor.RED} Locket token expired, trying to fetch new token")
            return self.fetch_token()
        except Exception as e:
            self._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Error loading token from file: {str(e)}")
            return self.fetch_token()
    def save_token(self, token):
        try:
            token_data={
                'token': token,
                'expiry': time.time() + self.TOKEN_EXPIRY_TIME,
                'created_at': time.time()
            }
            with open(self.TOKEN_FILE, 'w') as file:
                json.dump(token_data, file, indent=4)

            self._print(
                f"{xColor.GREEN}[+] {xColor.CYAN}Token saved to {xColor.WHITE}{self.TOKEN_FILE}")
            return True
        except Exception as e:
            self._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Error saving token to file: {str(e)}")
            return False
    def fetch_token(self, retry=0, max_retries=3):
        if retry==0:
            self._print(
                f"{xColor.MAGENTA}[*] {xColor.CYAN}Initializing token authentication sequence")
            self._loader_("Establishing secure connection", 1)
        if retry >= max_retries:
            self._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Token acquisition failed after {max_retries} attempts")
            self._loader_("Emergency shutdown", 1)
            sys.exit(1)
        try:
            self._print(
                f"{xColor.MAGENTA}[*] {xColor.CYAN}Preparing to retrieve token [{retry+1}/{max_retries}]")
            response=requests.get(self.TOKEN_API_URL, timeout=self.request_timeout, proxies={
                                    "http": None, "https": None})
            response.raise_for_status()
            data=response.json()
            if not isinstance(data, dict):
                self._print(
                    f"{xColor.YELLOW}[!] {xColor.WHITE}Invalid response format, retrying...")
                time.sleep(0.5)
                return self.fetch_token(retry + 1)
            if data.get("code")==200 and "data" in data and "token" in data["data"]:
                token=data["data"]["token"]
                self._print(
                    f"{xColor.GREEN}[+] {xColor.CYAN}Token acquired successfully")
                masked_token=token[:10] + "..." + token[-10:]
                self._print(
                    f"{xColor.GREEN}[+] {xColor.WHITE}Token: {xColor.YELLOW}{masked_token}")
                self.save_token(token)
                return token
            elif data.get("code") in (403, 404, 502, 503, 504, 429, 500):
                self._print(
                    f"{xColor.YELLOW}[!] {xColor.RED}The Locket token server is no longer available, please contact us telegram @{self.author}, trying again...")
                time.sleep(1.3)
                return self.fetch_token(retry + 1)
            else:
                self._print(
                    f"{xColor.YELLOW}[!] {xColor.RED}{data.get("msg")}")
                time.sleep(1.3)
                return self.fetch_token(retry + 1)
        except requests.exceptions.RequestException as e:
            self._print(
                f"{xColor.RED}[!] Warning: {xColor.YELLOW}Token unauthorized, retrying... {e}")
            self._loader_("Attempting to reconnect", 1)
            time.sleep(1.3)
            return self.fetch_token(retry + 1)
    def headers_locket(self):
        return {
            'Host': self.API_LOCKET_URL.replace('https://', ''),
            'Accept': '*/*',
            'baggage': 'sentry-environment=production,sentry-public_key=78fa64317f434fd89d9cc728dd168f50,sentry-release=com.locket.Locket%401.121.1%2B1,sentry-trace_id=2cdda588ea0041ed93d052932b127a3e',
            'X-Firebase-AppCheck': self.FIREBASE_APP_CHECK,
            'Accept-Language': 'vi-VN,vi;q=0.9',
            'sentry-trace': '2cdda588ea0041ed93d052932b127a3e-a3e2ba7a095d4f9d-0',
            'User-Agent': 'com.locket.Locket/1.121.1 iPhone/18.2 hw/iPhone12_1',
            'Firebase-Instance-ID-Token': 'd7ChZwJHhEtsluXwXxbjmj:APA91bFoMIgxwf-2tmY9QLy82lKMEWL6S4d8vb9ctY3JxLLTQB1k6312TcgtqJjWFhQVz_J4wIFvE0Kfroztu1vbZDOFc65s0vvj68lNJM4XuJg1onEODiBG3r7YGrQLiHkBV1gEoJ5f',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
        }
    def firebase_headers_locket(self):
        base_headers=self.headers_locket()
        return {
            'Host': 'www.googleapis.com',
            'baggage': base_headers.get('baggage', ''),
            'Accept': '*/*',
            'X-Client-Version': 'iOS/FirebaseSDK/10.23.1/FirebaseCore-iOS',
            'X-Firebase-AppCheck': self.FIREBASE_APP_CHECK,
            'X-Ios-Bundle-Identifier': self.IOS_BUNDLE_ID,
            'X-Firebase-GMPID': '1:641029076083:ios:cc8eb46290d69b234fa606',
            'X-Firebase-Client': 'H4sIAAAAAAAAAKtWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA',
            'sentry-trace': base_headers.get('sentry-trace', ''),
            'Accept-Language': 'vi',
            'User-Agent': 'FirebaseAuth.iOS/10.23.1 com.locket.Locket/1.121.1 iPhone/18.2 hw/iPhone12_1',
            'Connection': 'keep-alive',
            'X-Firebase-GMPID': self.FIREBASE_GMPID,
            'Content-Type': 'application/json',
        }
    def analytics_payload(self):
        return {
            "platform": "ios",
            "experiments": {
                "flag_4": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "43",
                },
                "flag_10": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "505",
                },
                "flag_6": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "2000",
                },
                "flag_3": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "501",
                },
                "flag_22": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1203",
                },
                "flag_18": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1203",
                },
                "flag_17": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1010",
                },
                "flag_16": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "303",
                },
                "flag_15": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "501",
                },
                "flag_14": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "551",
                },
                "flag_25": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "23",
                },
            },
            "amplitude": {
                "device_id": "57A54C21-B633-418C-A6E3-4201E631178C",
                "session_id": {
                    "value": str(self.session_id),
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                },
            },
            "google_analytics": {"app_instance_id": "7E17CEB525FA4471BD6AA9CEC2C1BCB8"},
            "ios_version": "1.121.1.1",
        }
    def excute(self, url, headers=None, payload=None, thread_id=None, step=None, proxies_dict=None):
        prefix=f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}{step}{Style.RESET_ALL}]" if thread_id is not None and step else ""
        try:
            response=requests.post(
                url,
                headers=headers or self.headers_locket(),
                json=payload,
                proxies=proxies_dict,
                timeout=self.request_timeout,
                verify=False
            )
            response.raise_for_status()
            self.successful_requests+=1
            return response.json() if response.content else True
        except ProxyError:
            self._print(
                f"{prefix} {xColor.RED}[!] Proxy connection terminated")
            self.failed_requests+=1
            return "proxy_dead"
        except requests.exceptions.RequestException as e:
            self.failed_requests+=1
            if hasattr(e, 'response') and e.response is not None:
                status_code=e.response.status_code
                try:
                    error_data=e.response.json()
                    error_msg=error_data.get(
                        'error', 'Remote server rejected request')
                    self._print(
                        f"{prefix} {xColor.RED}[!] HTTP {status_code}: {error_msg}")
                except:
                    self._print(
                        f"{prefix} {xColor.RED}[!] Server connection timeout")
                if status_code==429:
                    return "too_many_requests"
            # self._print(f"{prefix} {xColor.RED}[!] Network error: {str(e)[:50]}...")
            return None
    def setup(self):
        self._zlocket_panel_()
    def _input_(self, prompt_text="", section="config"):
        print(
            f"{xColor.CYAN}┌──({xColor.NEON_GREEN}root@thanhdieu{xColor.CYAN})-[{xColor.PURPLE}{section}{xColor.CYAN}]")
        print(f"{xColor.CYAN}└─{xColor.RED}$ {xColor.WHITE}{prompt_text}")
        sys.stdout.write(f"  {xColor.YELLOW}>>> {xColor.RESET}")
        sys.stdout.flush()
        time.sleep(0.3)
        sys.stdout.write("\r" + " " * 30 + "\r")
        sys.stdout.flush()
        sys.stdout.write(f"  {xColor.GREEN}>>>{xColor.RESET} ")
        sys.stdout.flush()
        return input()
    def _zlocket_panel_(self):
        _clear_()
        print(f"\n{xColor.CYAN}╔═══════════════════════════════════════════════════════╗")
        print(f"{xColor.CYAN}║ {xColor.YELLOW}             ZLOCKET TOOL PRO PANEL {config.VERSION_TOOL}            {xColor.CYAN}║")
        print(f"{xColor.CYAN}║ {xColor.RED}                 [Telegram: @{self.telegram}]                {xColor.CYAN}║")
        print(f"{xColor.CYAN}║{xColor.WHITE}                                                       {xColor.CYAN}║")
        print(f"{xColor.CYAN}║   {xColor.WHITE}[{xColor.GREEN}01{xColor.WHITE}] {xColor.YELLOW}⭐ Tool Spam Kết Bạn                           {xColor.CYAN}║")
        print(f"{xColor.CYAN}║   {xColor.WHITE}[{xColor.GREEN}02{xColor.WHITE}] {xColor.YELLOW}⭐ Tool Xoá Yêu Cầu Kết Bạn                    {xColor.CYAN}║")
        print(f"{xColor.CYAN}║   {xColor.WHITE}[{xColor.RED}00{xColor.WHITE}] {xColor.RED}✗  Thoát Tool                                  {xColor.CYAN}║")
        print(f"{xColor.CYAN}║{xColor.WHITE}                                                       {xColor.CYAN}║")
        print(f"{xColor.CYAN}╚═══════════════════════════════════════════════════════╝")
        _cc_=self._input_(f"Hãy chọn chức năng {xColor.YELLOW}", "menu")
        if _cc_=="1" or _cc_=="01":
            return self._spam_friend_request()
        elif _cc_=="2" or _cc_=="02":
            return self._delete_friend_request()
        elif _cc_=="0" or _cc_=="00":
            print(f"{xColor.RED}[✗] Đã thoát {self.NAME_TOOL}...")
            time.sleep(2)
            sys.exit(0)
        else:
            print(f"{xColor.RED}[✗] Lựa chọn không hợp lệ!")
            time.sleep(1.5)
            return self._zlocket_panel_()
    def _spam_friend_request(self):
        while True:
            _clear_()
            self._zheader_()
            _tg_=self._input_(f"Nhập Username hoặc Link Locket {xColor.YELLOW}", "target")
            if not _tg_.strip():
                print(f"{xColor.RED}[✗] Bạn phải nhập Username hoặc Link Locket!")
                time.sleep(1.5)
                continue
            url=_tg_.strip()
            if not url.startswith(("http://", "https://")) and not url.startswith("locket."):
                url=f"https://locket.cam/{url}"
            if url.startswith("locket."):
                url=f"https://{url}"
            self._loader_(f"{xColor.YELLOW}[?] Checking URL, please wait {xColor.WHITE}{url}...", 0.3)
            self.messages=[]
            uid=self._extract_uid_locket(url)
            if uid:
                self.TARGET_FRIEND_UID=uid
                print(f"{xColor.GREEN}[✓] Successfully Locket UID: {xColor.WHITE}{uid}")
            else:
                for msg in self.messages:
                    print(f"{xColor.RED}[✗] {msg}")
                self.messages=[]
                time.sleep(1.5)
                continue
            _clear_()
            self._zheader_()
            _msg_=self._input_(f"Nhập Username Custom {xColor.YELLOW}(mặc định: {xColor.WHITE}{self.NAME_TOOL}{xColor.YELLOW}) [tối đa 20 kí tự]", "custom")
            if _msg_.strip():
                if len(_msg_.strip()) > 20:
                    print(f"{xColor.RED}[✗] Username quá dài. Vui lòng nhập lại (tối đa 20 kí tự)!")
                    time.sleep(1.5)
                    continue
                else:
                    self.NAME_TOOL=_msg_.strip()
            _clear_()
            self._zheader_()
            _e_=self._input_(
                f'Kích Hoạt Random Emoji {xColor.YELLOW}(mặc định: '
                f'{xColor.GREEN if self.USE_EMOJI else xColor.RED}{"ON" if self.USE_EMOJI else "OFF"}'
                f'{xColor.YELLOW}) {xColor.WHITE}[y/n]',
                "emoji"
            )
            if _e_.strip().lower() in ('y', 'yes', '1'):
                self.USE_EMOJI=True
            elif _e_.strip().lower() in ('n', 'no', '0'):
                self.USE_EMOJI=False
            self._blinking_(f"{xColor.YELLOW}[-] Waiting for connection to launch...", blinks=5)
            _clear_()
            self._zheader_()
            print(f"{xColor.GREEN}● Target UID     : {xColor.WHITE}{self.TARGET_FRIEND_UID}")
            print(f"{xColor.GREEN}● Custom Username: {xColor.WHITE}{self.NAME_TOOL}")
            print(f"{xColor.GREEN}● Random Emoji   : {xColor.GREEN if self.USE_EMOJI else xColor.RED}{'ON' if self.USE_EMOJI else 'OFF'}{xColor.WHITE}")
            _cf_=self._input_(
                f'Xác Nhận Chạy Tool {xColor.RED}{xColor.WHITE}[y/n]',
                "config"
            )
            if _cf_.strip().lower() in ('y', 'yes', '1'):
                self._cf_=True
                break
            else:
                print(f"{xColor.RED}[✗] Đã huỷ chạy {self.NAME_TOOL}...")
                time.sleep(2)
                return self._zlocket_panel_()
        return
    def _delete_friend_request(self):
        while True:
            _clear_()
            self._xheader_()
            while True:
                _clear_()
                self._xheader_()
                email=self._input_("Nhập email Locket của bạn", "login")
                if not email:
                    print(f"{xColor.RED}[✗] Email không được để trống!")
                    time.sleep(1.5)
                    continue
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    print(f"{xColor.RED}[✗] Email không đúng định dạng!")
                    print(f"{xColor.YELLOW}[!] Ví dụ: thanhdieu@email.com")
                    time.sleep(2)
                    continue
                while True:
                    _clear_()
                    self._xheader_()
                    print(f"{xColor.GREEN}[+] Email: {xColor.WHITE}{email}")
                    _pw_=self._input_("Nhập mật khẩu", "login")
                    if not _pw_:
                        print(f"{xColor.RED}[✗] Mật khẩu không được để trống!")
                        time.sleep(1.5)
                        continue
                    print(f"{xColor.YELLOW}[*] Đang đăng nhập vào tài khoản...")
                    _sb_=False
                    try:
                        _res_=requests.post(
                            f"{self.FIREBASE_AUTH_URL}/verifyPassword?key={self.FIREBASE_API_KEY}",
                            headers=self.firebase_headers_locket(),
                            json={
                                "email": email,
                                "password": _pw_,
                                "clientType": "CLIENT_TYPE_IOS",
                                "returnSecureToken": True
                            },
                            timeout=self.request_timeout,
                            verify=False
                        )
                        if _res_.status_code==400:
                            try:
                                _d_=_res_.json()
                                _e_=_d_.get('message', '')
                                if not _e_ and 'error' in _d_:
                                    _e_=_d_['error'].get('message', 'Unknown error')
                                _clear_()
                                self._xheader_()
                                print(f"{xColor.GREEN}[+] Email: {xColor.WHITE}{email}")
                                if _e_=='INVALID_EMAIL' or _e_=='EMAIL_NOT_FOUND':
                                    print(f"{xColor.RED}[✗] Tài khoản không tồn tại!")
                                    time.sleep(2)
                                    _sb_=True
                                    break
                                elif _e_=='INVALID_PASSWORD':
                                    print(f"{xColor.RED}[✗] Mật khẩu không chính xác!")
                                    time.sleep(2)
                                    continue
                                else:
                                    print(f"{xColor.RED}[✗] {_e_}")
                                    time.sleep(2)
                                    continue
                            except ValueError:
                                _clear_()
                                self._xheader_()
                                print(f"{xColor.GREEN}[+] Email: {xColor.WHITE}{email}")
                                print(f"{xColor.RED}[✗] Không thể đăng nhập tài khoản, hãy thử lại sau!")
                                time.sleep(2)
                                continue
                        _res_.raise_for_status()
                        _auth_=_res_.json()
                        if not _auth_:
                            print(f"{xColor.RED}[✗] Something went wrong, please try again later!")
                            time.sleep(2)
                            continue
                        if 'idToken' not in _auth_ or 'localId' not in _auth_:
                            error_msg=_auth_.get('error', {}).get('message')
                            print(f"{xColor.RED}[✗] {error_msg}")
                            time.sleep(2)
                            continue
                        break
                    except requests.exceptions.RequestException as e:
                        print(f"{xColor.RED}[✗] Warning: {str(e)}")
                        time.sleep(2)
                        continue
                if _sb_:
                    continue
                break
            _clear_()
            self._xheader_()
            if _auth_.get('displayName', 'Unknown'):
                print(f"{xColor.GREEN}[+] Tên Tài Khoản: {xColor.WHITE}{_auth_.get('displayName', '')}")
                print(f"{xColor.GREEN}[+] Email: {xColor.WHITE}{email}")
            print(f"{xColor.CYAN}{'=' * 40}")
            loader_stop=threading.Event()
            vtd_loader=threading.Thread(
                target=self._cc_loader_,
                args=(f"{xColor.YELLOW}Đang lấy danh sách Y/C kết bạn, hãy kiên nhẫn chờ đợi...", loader_stop)
            )
            vtd_loader.daemon=True
            vtd_loader.start()
            try:
                vtd=requests.post(
                    self.SV_FRQ_URL,
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    data={
                        "action": 'thanhdieu_get_friends',
                        "idToken": _auth_['idToken'],
                        "localId": _auth_['localId']
                    },
                    timeout=self.request_timeout+200,
                    verify=True
                )
                cmm=vtd.json()
                loader_stop.set()
                vtd_loader.join()
                _clear_()
                self._xheader_()
                if _auth_.get('displayName', 'Unknown'):
                    print(f"{xColor.GREEN}[+] Tên Tài Khoản: {xColor.WHITE}{_auth_.get('displayName', '')}")
                    print(f"{xColor.GREEN}[+] Email: {xColor.WHITE}{email}")
                print(f"{xColor.CYAN}{'=' * 40}")
                if cmm.get('code') != 200:
                    print(f"{xColor.RED}[✗] {cmm.get('msg')}")
                    time.sleep(4)
                    continue
                friend_list=cmm['data']['list']
                total_friends=cmm['total']
                print(f"{xColor.GREEN}[✓] Đã tìm thấy {xColor.RED}{total_friends} {xColor.GREEN}lượt yêu cầu kết bạn")
                if total_friends < 0:
                    input(f"\n{xColor.YELLOW}Nhấn Enter để quay lại menu chính...")
                    return self._zlocket_panel_()
                self._frc_=friend_list
            except requests.exceptions.RequestException as e:
                loader_stop.set()
                vtd_loader.join()
                print(f"{xColor.RED}[✗] Warning: {str(e)}")
                time.sleep(4)
                continue
            except Exception as e:
                loader_stop.set()
                vtd_loader.join()
                print(f"{xColor.RED}[✗] Unexpected: {str(e)}")
                time.sleep(4)
                continue
            confirm=self._input_(f"Bạn có muốn tiếp tục xoá Y/C kết bạn locket? (y/n)", "confirm")
            if confirm.lower() not in ['y', 'yes', '1']:
                print(f"{xColor.YELLOW}[!] Đã hủy xóa yêu cầu kết bạn")
                time.sleep(3)
                return self._zlocket_panel_()
            _o_=None
            while True:
                _clear_()
                self._xheader_()
                if _auth_.get('displayName', 'Unknown'):
                    print(f"{xColor.GREEN}[+] Tên Tài Khoản: {xColor.WHITE}{_auth_.get('displayName', '')}")
                    print(f"{xColor.GREEN}[+] Email: {xColor.WHITE}{email}")
                print(f"{xColor.CYAN}{'=' * 40}")
                print(f"{xColor.GREEN}[✓] Đã tìm thấy {xColor.RED}{total_friends} {xColor.GREEN}lượt yêu cầu kết bạn")
                print(f"{xColor.CYAN}{'=' * 40}")
                print(f"{xColor.CYAN}[1] {xColor.YELLOW}(Destroy) - {xColor.GREEN}Khắc Chế Cứng {xColor.WHITE}(Xóa không tì vết)")
                print(f"{xColor.CYAN}[2] {xColor.BLUE}(Limit) - {xColor.GREEN}Xoá Sương Sương {xColor.WHITE}(Xóa theo nhu cầu)")
                if not _o_:
                    _o_=self._input_("Nhập lựa chọn", "option").lower()
                if _o_ not in ['1', '2','destroy', 'limit']:
                    print(f"{xColor.RED}[✗] Hãy nhập lựa chọn 1 hoặc 2!")
                    time.sleep(1.5)
                    _o_=None
                    continue
                break
            limit=total_friends
            if _o_ in ['2', 'limit']:
                while True:
                    try:
                        _limit_=self._input_(f"Nhập số lượng muốn xóa (tối đa {total_friends})", "limit")
                        limit=int(_limit_)
                        if 0 < limit <= total_friends:
                            break
                        print(f"{xColor.RED}[✗] Hãy nhập từ 1 đến {total_friends}!")
                    except ValueError:
                        print(f"{xColor.RED}[✗] Hãy nhập số lượng hợp lệ!")
            while True:
                try:
                    _num_=int(self._input_(f"Nhập Threads (1-1000)", "threads"))
                    if 1 <= _num_ <= 1000:
                        break
                    print(f"{xColor.RED}[✗] Hãy nhập threads 1 đến 1000!")
                except ValueError:
                    print(f"{xColor.RED}[✗] Hãy nhập threads hợp lệ!")
            _clear_()
            print(f"{xColor.YELLOW}[*] Bắt đầu xóa yêu cầu kết bạn...")
            deleted_count=0
            thread_semaphore=threading.Semaphore(_num_)
            delete_lock=threading.Lock()
            active_threads=[]
            def delete_friend_request(friend):
                nonlocal deleted_count
                with thread_semaphore:
                    if deleted_count >= limit:
                        return
                    headers=self.headers_locket()
                    headers['Authorization']=f"Bearer {_auth_['idToken']}"
                    _payload={
                        "data": {
                            "analytics": self.analytics_payload(),
                            "direction": "incoming",
                            "user_uid": friend['userId']
                        }
                    }
                    result=self.excute(
                        f"{self.API_LOCKET_URL}/deleteFriendRequest",
                        headers=headers,
                        payload=_payload
                    )
                    with delete_lock:
                        if result and deleted_count < limit:
                            deleted_count += 1
                            remaining=limit - deleted_count
                            progress_percent=min((deleted_count/limit*100), 100)
                            name_display=friend['userId'] if friend['fullname']=='Tạm Ẩn' else friend['fullname']
                            print(f"""{xColor.CYAN}[{xColor.WHITE}✓{xColor.CYAN}] {xColor.YELLOW}TK/UserID   {xColor.CYAN}:{xColor.NEON_PINK} {name_display}{' ' * (28 - len(name_display))}
{xColor.CYAN}[{xColor.WHITE}+{xColor.CYAN}] {xColor.YELLOW}Đã Xoá      {xColor.CYAN}:{xColor.WHITE} {deleted_count:,}/{xColor.ORANGE}{limit} {xColor.NEON_GREEN}({progress_percent:.0f}%){' ' * (15 - len(str(int(progress_percent))))}
{xColor.CYAN}[{xColor.WHITE}!{xColor.CYAN}] {xColor.YELLOW}Còn Lại     {xColor.CYAN}:{xColor.RED} {max(remaining, 0):,}
{xColor.CYAN}{'=' * 46}""")
            for i in range(0, min(limit, len(self._frc_)), _num_):
                if deleted_count >= limit:
                    break
                batch=self._frc_[i:i + _num_]
                threads=[]
                for friend in batch:
                    if deleted_count >= limit:
                        break
                    thread=threading.Thread(target=delete_friend_request, args=(friend,))
                    threads.append(thread)
                    thread.start()
                    active_threads.append(thread)
                for thread in threads:
                    thread.join()
                    active_threads.remove(thread)
                if deleted_count >= limit:
                    break
            for thread in active_threads:
                thread.join()
            print(f"\n{xColor.GREEN}[✓] Đã xóa thành công {xColor.RED}{deleted_count:,} {xColor.GREEN}Y/C kết bạn")
            input(f"\n{xColor.YELLOW}Nhấn Enter để quay lại menu chính...")
            return self._zlocket_panel_()
    def _extract_uid_locket(self, url: str) -> Optional[str]:
        real_url=self._convert_url(url)
        if not real_url:
            self.messages.append(
                f"Locket account not found, please try again.")
            return None
        parsed_url=urlparse(real_url)
        if parsed_url.hostname != "locket.camera":
            self.messages.append(
                f"Locket URL không hợp lệ: {parsed_url.hostname}")
            return None
        if not parsed_url.path.startswith("/invites/"):
            self.messages.append(
                f"Link Locket Sai Định Dạng: {parsed_url.path}")
            return None
        parts=parsed_url.path.split("/")
        if len(parts) > 2:
            full_uid=parts[2]
            uid=full_uid[:28]
            return uid
        self.messages.append("Không tìm thấy UID trong Link Locket")
        return None
    def _convert_url(self, url: str) -> str:
        if url.startswith("https://locket.camera/invites/"):
            return url
        if url.startswith("https://locket.cam/"):
            try:
                resp=requests.get(
                    url,
                    headers={
                        "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
                    },
                    timeout=self.request_timeout,
                )
                if resp.status_code==200:
                    match=re.search(
                        r'window\.location\.href\s*=\s*"([^"]+)"', resp.text)
                    if match:
                        parsed=urlparse(match.group(1))
                        query=parse_qs(parsed.query)
                        enc_link=query.get("link", [None])[0]
                        if enc_link:
                            return enc_link
                        else:
                            return None
                    else:
                        return None
                else:
                    return None
            except Exception as e:
                self.messages.append(
                    f"Failed to connect to the Locket server.")
                return ""
        payload={"type": "toLong", "kind": "url.thanhdieu.com", "url": url}
        headers={
            "Accept": "*/*",
            "Accept-Language": "vi",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
            "X-Requested-With": "XMLHttpRequest",
        }
        try:
            response=requests.post(
                self.SHORT_URL,
                headers=headers,
                data=urlencode(payload),
                timeout=self.request_timeout,
                verify=True,
            )
            response.raise_for_status()
            _res=response.json()
            if _res.get("status")==1 and "url" in _res:
                return _res["url"]
            self.messages.append("Lỗi kết nối tới API Url.ThanhDieu.Com")
            return ""
        except requests.exceptions.RequestException as e:
            self.messages.append(
                "Lỗi kết nối tới API Url.ThanhDieu.Com " + str(e))
            return ""
        except ValueError:
            self.messages.append("Lỗi kết nối tới API Url.ThanhDieu.Com")
            return ""
    def _cc_loader_(self, message, stop_event):
        spinner=cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        while not stop_event.is_set():
            with PRINT_LOCK:
                sys.stdout.write(f"\r{xColor.CYAN}{message} {next(spinner)} ")
                sys.stdout.flush()
            time.sleep(0.1)
        with PRINT_LOCK:
            sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
            sys.stdout.flush()
    def _xheader_(self):
        print(f"\n{xColor.CYAN}╔═══════════════════════════════════════════════════════╗")
        print(f"{xColor.CYAN}║ {xColor.YELLOW}             TOOL KHẮC CHẾ SPAM Y/C KẾT BẠN           {xColor.CYAN}║")
        print(f"{xColor.CYAN}║ {xColor.RED}                 [Telegram: @{self.telegram}]                {xColor.CYAN}║")
        print(f"{xColor.CYAN}╚═══════════════════════════════════════════════════════╝")
    def _zheader_(self):
        print(f"\n{xColor.CYAN}╔═══════════════════════════════════════════════════════╗")
        print(f"{xColor.CYAN}║ {xColor.YELLOW}              SPAM KẾT BẠN LOCKET WIDGET              {xColor.CYAN}║")
        print(f"{xColor.CYAN}║ {xColor.RED}                 [Telegram: @{self.telegram}]                {xColor.CYAN}║")
        print(f"{xColor.CYAN}╚═══════════════════════════════════════════════════════╝\n")
def _print(*args, **kwargs):
    return config._print(*args, **kwargs)
def _loader_(message, duration=3):
    return config._loader_(message, duration)
def _sequence_(message, duration=1.5, char_set="0123456789ABCDEF"):
    return config._sequence_(message, duration, char_set)
def _randchar_(duration=2):
    return config._randchar_(duration)
def _blinking_(text, blinks=3, delay=0.1):
    return config._blinking_(text, blinks, delay)
def _rand_str_(length=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))
def _rand_name_():
    return _rand_str_(8, chars=string.ascii_lowercase)
def _rand_email_():
    return f"{_rand_str_(15)}@thanhdieu.com"
def _rand_pw_():
    return 'zlocket' + _rand_str_(7)
def _clear_():
    try:
        os.system('cls' if os.name=='nt' else 'clear')
    except:
        with PRINT_LOCK:
            print("\033[2J\033[H", end="")
            sys.stdout.flush()
def typing_print(text, delay=0.02):
    with PRINT_LOCK:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
def _flush_():
    sys.stdout.write('\033[F\033[K') 
    sys.stdout.write('\033[F\033[K')
    sys.stdout.flush()
def _matrix_():
    matrix_chars="01"
    lines=5
    columns=os.get_terminal_size().columns
    with PRINT_LOCK:
        for _ in range(lines):
            line=""
            for _ in range(columns - 5):
                if random.random() > 0.9:
                    line+=xColor.GREEN + random.choice(matrix_chars)
                else:
                    line+=" "
            print(line)
        time.sleep(0.2)
def _banner_():
    try:
        wterm=os.get_terminal_size().columns
    except:
        wterm=80
    banner=[
        f"{xColor.RED}███████╗{xColor.GREEN}░░░░░░{xColor.RED}██{xColor.GREEN}║░░░░░{xColor.RED}░█████╗{xColor.GREEN}░{xColor.RED}░█████╗{xColor.GREEN}░{xColor.RED}██{xColor.GREEN}║░░{xColor.RED}██{xColor.GREEN}║{xColor.RED}███████╗{xColor.RED}████████╗",
        f"{xColor.RED}╚════██{xColor.GREEN}║░░░░░░{xColor.RED}██{xColor.GREEN}║░░░░░{xColor.RED}██{xColor.GREEN}╔═{xColor.RED}═██{xColor.GREEN}╗{xColor.RED}██{xColor.GREEN}╔═{xColor.RED}═██{xColor.GREEN}╗{xColor.RED}██{xColor.GREEN}║░{xColor.RED}██{xColor.GREEN}╔╝{xColor.RED}██{xColor.GREEN}╔════╝{xColor.RED}╚══██{xColor.GREEN}╔══╝",
        f"{xColor.RED}░░███╔═{xColor.GREEN}╝{xColor.RED}█████{xColor.GREEN}╗{xColor.RED}██{xColor.GREEN}║░░░░░{xColor.RED}██{xColor.GREEN}║░░{xColor.RED}██{xColor.GREEN}║{xColor.RED}██{xColor.GREEN}║░░{xColor.RED}╚═{xColor.GREEN}╝{xColor.RED}█████═{xColor.GREEN}╝░{xColor.RED}█████{xColor.GREEN}╗░░░░░{xColor.RED}██{xColor.GREEN}║░░░",
        f"{xColor.RED}██╔══╝{xColor.GREEN}░░{xColor.RED}╚════{xColor.GREEN}╝{xColor.RED}██{xColor.GREEN}║░░░░░{xColor.RED}██{xColor.GREEN}║░░{xColor.RED}██{xColor.GREEN}║{xColor.RED}██{xColor.GREEN}║░░{xColor.RED}██{xColor.GREEN}╗{xColor.RED}██{xColor.GREEN}╔═{xColor.RED}██{xColor.GREEN}╗░{xColor.RED}██{xColor.GREEN}╔══╝░░░░░{xColor.RED}██{xColor.GREEN}║░░░",
        f"{xColor.RED}███████{xColor.GREEN}╗░░░░░░{xColor.RED}███████{xColor.GREEN}╗{xColor.RED}╚█████╔{xColor.GREEN}╝{xColor.RED}╚█████╔{xColor.GREEN}╝{xColor.RED}██{xColor.GREEN}║░{xColor.RED}╚██{xColor.GREEN}╗{xColor.RED}███████{xColor.GREEN}╗░░░{xColor.RED}██{xColor.GREEN}║░░░",
        f"{xColor.RED}╚══════{xColor.GREEN}╝░░░░░░{xColor.RED}╚══════{xColor.GREEN}╝░{xColor.RED}╚════╝{xColor.GREEN}░░{xColor.RED}╚════╝{xColor.GREEN}░{xColor.RED}╚═{xColor.GREEN}╝░░{xColor.RED}╚═{xColor.GREEN}╝{xColor.RED}╚══════{xColor.GREEN}╝░░░{xColor.RED}╚═{xColor.GREEN}╝░░░",
        f"{xColor.WHITE}[ {xColor.YELLOW}Author: @{config.author} {xColor.RED}|{xColor.WHITE} {xColor.GREEN}zLocket Tool {config.VERSION_TOOL}{xColor.WHITE} ]"
    ]
    def visible_length(text):
        clean=re.sub(r'\033\[[0-9;]+m', '', text)
        return len(clean)
    centered=[]
    for line in banner:
        line_length=visible_length(line)
        padding=(wterm - line_length) // 2
        if padding > 0:
            center=" " * padding + line
        else:
            center=line
        centered.append(center)
    banner="\n" + "\n".join(centered) + "\n"
    with PRINT_LOCK:
        sfprint(banner)
def _stats_():
    elapsed=time.time() - config.start_time
    hours, remainder=divmod(int(elapsed), 3600)
    minutes, seconds=divmod(remainder, 60)
    elapsed_str=f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    success_rate=(config.successful_requests / (config.successful_requests + config.failed_requests)
                    ) * 100 if (config.successful_requests + config.failed_requests) > 0 else 0
    stats=f"""
{xColor.CYAN}┌──{xColor.YELLOW}[ {xColor.WHITE}SESSION STATISTICS {xColor.YELLOW}]{xColor.CYAN}─────────────────────────────────────┐
{xColor.GREEN} ● Runtime      : {xColor.WHITE}{elapsed_str}
{xColor.GREEN} ● Success Rate : {xColor.WHITE}{success_rate:.1f}%
{xColor.GREEN} ● Successful   : {xColor.WHITE}{config.successful_requests} requests
{xColor.RED} ● Failed       : {xColor.WHITE}{config.failed_requests} attempts
{xColor.BLUE} ● Proxies      : {xColor.WHITE}{config.total_proxies} loaded
{xColor.CYAN}└─────────────────────────────────────────────────────────────┘{xColor.CYAN}
"""
    return stats
def load_proxies():
    proxies=[]
    proxy_urls=config.PROXY_LIST
    config._print(
        f"{xColor.MAGENTA}{Style.BRIGHT}[*] {xColor.CYAN}Initializing proxy collection system...")
    try:
        with open('proxy.txt', 'r', encoding='utf-8', errors='ignore') as f:
            file_proxies=[line.strip() for line in f if line.strip()]
            config._print(
                f"{xColor.MAGENTA}[+] {xColor.GREEN}Found {xColor.WHITE}{len(file_proxies)} {xColor.GREEN}proxies in local storage (proxy.txt)")
            config._loader_("Processing local proxies", 1)
            proxies.extend(file_proxies)
    except FileNotFoundError:
        config._print(
            f"{xColor.YELLOW}[!] {xColor.RED}No local proxy file detected, trying currently available proxies...")
    for url in proxy_urls:
        try:
            config._print(
                f"{xColor.MAGENTA}[*] {xColor.CYAN}Fetching proxies from {xColor.WHITE}{url}")
            config._loader_(f"Connecting to {url.split('/')[2]}", 1)
            response=requests.get(url, timeout=config.request_timeout)
            response.encoding='utf-8'
            response.raise_for_status()
            url_proxies=[line.strip() for line in response.text.splitlines() if line.strip()]
            proxies.extend(url_proxies)
            config._print(
                f"{xColor.MAGENTA}[+] {xColor.GREEN}Harvested {xColor.WHITE}{len(url_proxies)} {xColor.GREEN}proxies from {url.split('/')[2]}")
        except requests.exceptions.RequestException as e:
            config._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Connection failed: {url.split('/')[2]} - {str(e)}")
        except UnicodeDecodeError:
            config._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Encoding error while reading proxies from {url.split('/')[2]}")
            try:
                response.encoding='latin-1'
                url_proxies=[line.strip() for line in response.text.splitlines() if line.strip()]
                proxies.extend(url_proxies)
                config._print(
                    f"{xColor.MAGENTA}[+] {xColor.GREEN}Harvested {xColor.WHITE}{len(url_proxies)} {xColor.GREEN}proxies from {url.split('/')[2]} (using alternative encoding)")
            except:
                config._print(
                    f"{xColor.RED}[!] {xColor.YELLOW}Failed to decode proxies from {url.split('/')[2]}")
    proxies=list(set(proxies)) 
    valid_proxies=[p for p in proxies if re.match(r'^(\d{1,3}\.){3}\d{1,3}:\d+$', p)]
    if not valid_proxies:
        config._print(
            f"{xColor.RED}[!] Warning: No valid proxies available for operation")
        return []
    config.total_proxies=len(valid_proxies)
    config._print(
        f"{xColor.GREEN}[+] {xColor.CYAN}Proxy harvesting complete{xColor.WHITE} {len(valid_proxies)} {xColor.CYAN}unique proxies loaded")
    return valid_proxies
def init_proxy():
    proxies=load_proxies()
    if not proxies:
        config._print(f"{xColor.RED}[!] {xColor.YELLOW}Note: Please add proxies to continue running the tool.")
        config._loader_("Shutting down system", 1)
        sys.exit(1)
    if len(proxies) < 200:
        config._print(f"{xColor.RED}[!] {xColor.YELLOW}Warning: Insufficient proxies ({len(proxies)} proxies found, minimum 200 required)")
        config._print(f"{xColor.RED}[!] Please add more proxies to proxy.txt or check proxy sources")
        config._loader_("Shutting down system", 1)
        sys.exit(1)
    config._print(f"{xColor.MAGENTA}[*] {xColor.CYAN}Randomizing proxy sequence for optimal distribution")
    random.shuffle(proxies)
    config._loader_("Optimizing proxy rotation algorithm", 1)
    proxy_queue=Queue()
    for proxy in proxies:
        proxy_queue.put(proxy)
    num_threads=len(proxies)
    config._print(f"{xColor.GREEN}[+] {xColor.CYAN}Proxy system initialized with {xColor.WHITE}{num_threads} {xColor.CYAN}endpoints")
    return proxy_queue, num_threads
def format_proxy(proxy_str):
    if not proxy_str:
        return None
    try:
        if not proxy_str.startswith(('http://', 'https://')):
            proxy_str=f"http://{proxy_str}"
        return {"http": proxy_str, "https": proxy_str}
    except Exception as e:
        config._print(
            f"{xColor.RED}[!] {xColor.YELLOW}Proxy format error: {e}")
        return None
def get_proxy(proxy_queue, thread_id, stop_event=None):
    try:
        if stop_event is not None and stop_event.is_set():
            return None
        proxy_str=proxy_queue.get_nowait()
        return proxy_str
    except queue.Empty:
        if stop_event is None or not stop_event.is_set():
            config._print(
                f"{xColor.RED}[Thread-{thread_id:03d}] {xColor.YELLOW}Proxy pool exhausted")
        return None
def excute(url, headers=None, payload=None, thread_id=None, step=None, proxies_dict=None):
    return config.excute(url, headers, payload, thread_id, step, proxies_dict)
def step1b_sign_in(email, password, thread_id, proxies_dict):
    if not email or not password:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failed: Invalid credentials")
        return None, None
    payload={
        "email": email,
        "password": password,
        "clientType": "CLIENT_TYPE_IOS",
        "returnSecureToken": True
    }
    vtd=excute(
        f"{config.FIREBASE_AUTH_URL}/verifyPassword?key={config.FIREBASE_API_KEY}",
        headers=config.firebase_headers_locket(),
        payload=payload,
        thread_id=thread_id,
        step="Auth",
        proxies_dict=proxies_dict
    )
    if vtd and 'idToken' in vtd and 'localId' in vtd:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.GREEN}[✓] Authentication successful")
        return vtd.get('idToken'), vtd.get('localId')
    config._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failed")
    return None, None
def step2_finalize_user(id_token, thread_id, proxies_dict):
    if not id_token:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.RED}[✗] Profile creation failed: Invalid token")
        return False
    first_name=config.NAME_TOOL
    last_name=' '.join(random.sample([
        '😀', '😂', '😍', '🥰', '😊', '😇', '😚', '😘', '😻', '😽', '🤗',
        '😎', '🥳', '😜', '🤩', '😢', '😡', '😴', '🙈', '🙌', '💖', '🔥', '👍',
        '✨', '🌟', '🍎', '🍕', '🚀', '🎉', '🎈', '🌈', '🐶', '🐱', '🦁',
        '😋', '😬', '😳', '😷', '🤓', '😈', '👻', '💪', '👏', '🙏', '💕', '💔',
        '🌹', '🍒', '🍉', '🍔', '🍟', '☕', '🍷', '🎂', '🎁', '🎄', '🎃', '🔔',
        '⚡', '💡', '📚', '✈️', '🚗', '🏠', '⛰️', '🌊', '☀️', '☁️', '❄️', '🌙',
        '🐻', '🐼', '🐸', '🐝', '🦄', '🐙', '🦋', '🌸', '🌺', '🌴', '🏀', '⚽', '🎸'
    ], 5))
    username=_rand_name_()
    payload={
        "data": {
            "username": username,
            "last_name": last_name,
            "require_username": True,
            "first_name": first_name
        }
    }
    headers=config.headers_locket()
    headers['Authorization']=f"Bearer {id_token}"
    result=excute(
        f"{config.API_LOCKET_URL}/finalizeTemporaryUser",
        headers=headers,
        payload=payload,
        thread_id=thread_id,
        step="Profile",
        proxies_dict=proxies_dict
    )
    if result:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.GREEN}[✓] Profile created: {xColor.YELLOW}{username}")
        return True
    config._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.RED}[✗] Profile creation failed")
    return False
def step3_send_friend_request(id_token, thread_id, proxies_dict):
    if not id_token:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.RED}[✗] Connection failed: Invalid token")
        return False
    payload={
        "data": {
            "user_uid": config.TARGET_FRIEND_UID,
            "source": "signUp",
            "platform": "iOS",
            "messenger": "Messages",
            "invite_variant": {"value": "1002", "@type": "type.googleapis.com/google.protobuf.Int64Value"},
            "share_history_eligible": True,
            "rollcall": False,
            "prompted_reengagement": False,
            "create_ofr_for_temp_users": False,
            "get_reengagement_status": False
        }
    }
    headers=config.headers_locket()
    headers['Authorization']=f"Bearer {id_token}"
    result=excute(
        f"{config.API_LOCKET_URL}/sendFriendRequest",
        headers=headers,
        payload=payload,
        thread_id=thread_id,
        step="Friend",
        proxies_dict=proxies_dict
    )
    if result:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.GREEN}[✓] Connection established with target")
        return True
    config._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.RED}[✗] Connection failed")
    return False
def _cd_(message, count=5, delay=0.2):
    for i in range(count, 0, -1):
        binary=bin(i)[2:].zfill(8)
        sys.stdout.write(
            f"\r{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.GREEN}{message} {xColor.RED}{binary}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(
        f"\r{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.GREEN}{message} {xColor.GREEN}READY      \n")
    sys.stdout.flush()
def step1_create_account(thread_id, proxy_queue, stop_event):
    while not stop_event.is_set():
        current_proxy=get_proxy(proxy_queue, thread_id, stop_event)
        proxies_dict=format_proxy(current_proxy)
        proxy_usage_count=0
        failed_attempts=0
        max_failed_attempts=10
        if not current_proxy:
            config._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Proxy pool depleted, waiting for refill (1s)")
            time.sleep(1)
            continue
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.GREEN}● Thread activated with proxy: {xColor.YELLOW}{current_proxy}")
        if thread_id < 3:
            _cd_(f"Thread-{thread_id:03d} initialization", count=3)
        while not stop_event.is_set() and proxy_usage_count < config.ACCOUNTS_PER_PROXY and failed_attempts < max_failed_attempts:
            if stop_event.is_set():
                return
            if not current_proxy:
                current_proxy=get_proxy(proxy_queue, thread_id, stop_event)
                proxies_dict=format_proxy(current_proxy)
                if not current_proxy:
                    config._print(
                        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Proxy unavailable, will try again")
                    break
                config._print(
                    f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.GREEN}● Switching to new proxy: {xColor.YELLOW}{current_proxy}")

            prefix=f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Register{Style.RESET_ALL}]"
            email=_rand_email_()
            password=_rand_pw_()
            config._print(
                f"{prefix} {xColor.CYAN}● Initializing new identity: {xColor.YELLOW}{email[:8]}...@...")
            payload={
                "data": {
                    "email": email,
                    "password": password,
                    "client_email_verif": True,
                    "client_token": _rand_str_(40, chars=string.hexdigits.lower()),
                    "platform": "ios"
                }
            }
            if stop_event.is_set():
                return
            response_data=excute(
                f"{config.API_LOCKET_URL}/createAccountWithEmailPassword",
                headers=config.headers_locket(),
                payload=payload,
                thread_id=thread_id,
                step="Register",
                proxies_dict=proxies_dict
            )
            if stop_event.is_set():
                return
            if response_data=="proxy_dead":
                config._print(
                    f"{prefix} {xColor.RED}[!] Proxy terminated, acquiring new endpoint")
                current_proxy=None
                failed_attempts += 1
                continue
            if response_data=="too_many_requests":
                config._print(
                    f"{prefix} {xColor.RED}[!] Connection throttled, switching endpoint")
                current_proxy=None
                failed_attempts += 1
                continue
            if isinstance(response_data, dict) and response_data.get('result', {}).get('status')==200:
                config._print(
                    f"{prefix} {xColor.GREEN}[✓] Identity created: {xColor.YELLOW}{email}")
                proxy_usage_count += 1
                failed_attempts=0
                if stop_event.is_set():
                    return
                id_token, local_id=step1b_sign_in(
                    email, password, thread_id, proxies_dict)
                if stop_event.is_set():
                    return
                if id_token and local_id:
                    if step2_finalize_user(id_token, thread_id, proxies_dict):
                        if stop_event.is_set():
                            return
                        first_request_success=step3_send_friend_request(
                            id_token, thread_id, proxies_dict)
                        if first_request_success:
                            config._print(
                                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Boost{Style.RESET_ALL}] {xColor.YELLOW}🚀 Boosting friend requests: Sending 15 more requests")
                            for _ in range(15):
                                if stop_event.is_set():
                                    return
                                step3_send_friend_request(
                                    id_token, thread_id, proxies_dict)
                            config._print(
                                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Boost{Style.RESET_ALL}] {xColor.GREEN}[✓] Boost complete: 101 total requests sent")
                    else:
                        config._print(
                            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failure")
                else:
                    config._print(
                        f"{prefix} {xColor.RED}[✗] Identity creation failed")
                failed_attempts += 1
        if failed_attempts >= max_failed_attempts:
            config._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Thread restarting: Excessive failures ({failed_attempts})")
        else:
            config._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.YELLOW}● Proxy limit reached ({proxy_usage_count}/{config.ACCOUNTS_PER_PROXY}), getting new proxy")

def main():
    config.start_time=time.time()
    config.setup()
    _clear_()
    _banner_()
    config._randchar_(duration=1)
    config._blinking_("Preparing to connect to the server", blinks=3)
    typing_print(
        f"-----------------[zLocket Tool Pro {config.VERSION_TOOL}]-----------------", delay=0.01)
    config._print(
        f"{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.GREEN}System ready. {xColor.WHITE}Target: {xColor.YELLOW}{config.TARGET_FRIEND_UID}")
    config._print(f"{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.GREEN}Locket token: {xColor.WHITE}{'[' + xColor.GREEN + 'ACTIVE' + xColor.WHITE + ']' if config.FIREBASE_APP_CHECK else '[' + xColor.RED + 'FAILED' + xColor.WHITE + ']'}")
    config._print(
        f"{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.GREEN}Resource limit: {xColor.WHITE}{config.ACCOUNTS_PER_PROXY} {xColor.GREEN}accounts per proxy")
    config._print(
        f"{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.GREEN}Running mode: {xColor.WHITE}PREMIUM SPAMMER {xColor.GREEN}(NO TIME LIMIT)")
    config._loader_("Initializing security protocol", 1)
    config._print(f"{xColor.CYAN}{Style.BRIGHT}{'=' * 65}{Style.RESET_ALL}")
    if not config.FIREBASE_API_KEY:
        config._print(
            f"{xColor.RED}[!] {xColor.YELLOW}Critical error: Missing locket api key, please contact to telegram @{config.author}")
        config._loader_("Emergency shutdown initiated", 1.2)
        sys.exit(1)
    if not config.FIREBASE_APP_CHECK:
        config._print(
            f"{xColor.RED}[!] {xColor.YELLOW}Critical error: Missing locket token, please contact to telegram @{config.author}")
        config._loader_("Emergency shutdown initiated", 1.2)
        sys.exit(1)
    try:
        stop_event=threading.Event()
        all_threads=[]
        try:
            proxy_queue, num_threads=init_proxy()
            config._loader_("Setting up encryption layer", 1)
            config._print(
                f"{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.GREEN}Initializing {xColor.WHITE}{num_threads} {xColor.GREEN}parallel threads")
            config._loader_("Activating distributed network", 1.2)
            threads=[]
            for i in range(num_threads):
                thread=threading.Thread(
                    target=step1_create_account,
                    args=(i, proxy_queue, stop_event)
                )
                threads.append(thread)
                all_threads.append(thread)
                thread.daemon=False
                thread.start()
                if i % 10==0 and i > 0:
                    config._print(
                        f"{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.GREEN}Activated {xColor.WHITE}{i} {xColor.GREEN}threads...")
            config._print(
                f"{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.GREEN}All threads activated. {xColor.WHITE}Spam is running in continuous mode. Press Ctrl+C to stop.")
            config._print(
                f"{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.YELLOW}Waiting for threads to terminate (max 5s)...")
            active_threads=[]
            for t in threads:
                t.join(timeout=0.1)
                if t.is_alive():
                    active_threads.append(t)
            if active_threads:
                config._print(
                    f"{xColor.CYAN}[{xColor.WHITE}*{xColor.CYAN}] {xColor.YELLOW}Waiting for {len(active_threads)} remaining threads...")
                for t in active_threads:
                    t.join(timeout=1.0)
        except KeyboardInterrupt:
            stop_event.set()
            config._print(
                f"\n{xColor.RED}[!] {xColor.YELLOW}User interrupt detected")
        stop_event.set()
    except KeyboardInterrupt:
        stop_event.set()
        config._print(
            f"\n{xColor.RED}[!] {xColor.YELLOW}User interrupt detected")
    time.sleep(0.5)
    end_time=time.time()
    config._sequence_("Destroying Terminal", duration=2)
    config._loader_("Executing graceful shutdown", 2)
    elapsed=end_time - config.start_time
    hours, remainder=divmod(int(elapsed), 3600)
    minutes, seconds=divmod(remainder, 60)
    config._print(
        f"{xColor.GREEN}[+] {xColor.CYAN}Operation complete. Runtime: {xColor.WHITE}{hours:02d}:{minutes:02d}:{seconds:02d}")
    config._print(f"{xColor.CYAN}{Style.BRIGHT}{'=' * 65}{Style.RESET_ALL}")
    config._blinking_("TOOL HAS BEEN SHUT DOWN", blinks=20)
    sys.stdout.flush()
    os._exit(0)
if __name__=="__main__":
    config=zLocket()
    main()
