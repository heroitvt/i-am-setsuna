import os
import subprocess

def main():
    dll_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\SetsunaFontFix.dll"
    if os.path.exists(dll_path):
        print(f"SetsunaFontFix.dll size: {os.path.getsize(dll_path)}")
        with open(dll_path, "rb") as f:
            data = f.read()
        # Find strings in DLL
        import re
        strings = re.findall(b"[\x20-\x7e]{4,}", data)
        print("Found strings in SetsunaFontFix.dll:")
        for s in strings:
            s_dec = s.decode('ascii', errors='ignore')
            if any(k in s_dec.lower() for k in ["setsuna", "font", "translat", "txt", "param", "load", "hook", "patch", "cpk", "auto"]):
                print("  ", s_dec)

if __name__ == "__main__":
    main()
