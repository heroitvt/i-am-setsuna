import os
import struct

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        header = f.read(16)
        print("Header:", header)
        f.seek(0)
        content = f.read(1024*1024) # read 1MB
        # check if file names are in header
        import re
        names = re.findall(b"[a-zA-Z0-9_-]{4,}\\.?[a-zA-Z0-9]*", content)
        print("Sample names in parameter.cpk:")
        for n in names[:30]:
            try:
                print(" ", n.decode('ascii'))
            except:
                pass

if __name__ == "__main__":
    main()
