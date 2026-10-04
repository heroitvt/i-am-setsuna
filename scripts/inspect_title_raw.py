from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def main():
    pdir = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter"
    for name in ["TitleMessage", "SystemMessage", "BattleMessage"]:
        p = os.path.join(pdir, name)
        with open(p, "rb") as f:
            d = f.read()
        dec = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend()).decryptor().update(d)
        print(f"\n{name} first 64 bytes:")
        print(dec[:64])
        # Find any text
        import re
        txts = re.findall(b"(?:[\x20-\x7e]\x00){3,}", dec[:500])
        print("Texts:", [t.decode('utf-16le') for t in txts[:10]])

if __name__ == "__main__":
    main()
