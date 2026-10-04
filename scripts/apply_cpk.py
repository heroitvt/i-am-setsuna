import shutil
import os

def main():
    target = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    backup = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk.bak_original"
    new_cpk = r"d:\Viet Hoa Game\temp_scripts\parameter.cpk.new"

    if not os.path.exists(backup):
        shutil.copy2(target, backup)
        print(f"Created backup: {backup}")
        
    shutil.copy2(new_cpk, target)
    print(f"Updated {target} with new CPK (size: {os.path.getsize(target)} bytes)!")

if __name__ == "__main__":
    main()
