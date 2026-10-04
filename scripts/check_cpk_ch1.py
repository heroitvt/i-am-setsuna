from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        data = f.read()

    # Search for encrypted block of ScenarioMessageData_Chapter_1 or check TOC entries
    # In TOC, we found offset 2064 has 275 rows.
    # Let's inspect the TOC rows to find the exact file offset and size of ScenarioMessageData_Chapter_1!
    pass

if __name__ == "__main__":
    main()
