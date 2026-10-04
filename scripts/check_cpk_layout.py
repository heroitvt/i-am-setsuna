from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def decrypt_data(data):
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        cpk_data = f.read()

    # Find ScenarioMessageData_Chapter_1 in TOC or find AES encrypted block starting with -1 (0xFFFFFFFF)
    # Let's search for encrypted blocks:
    # Actually, in parameter.cpk, files are stored sequentially.
    # Let's see how files are stored in parameter.cpk.
    print("CPK length:", len(cpk_data))

if __name__ == "__main__":
    main()
