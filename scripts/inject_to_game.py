import shutil
import os

def main():
    src = r"d:\Viet Hoa Game\temp_scripts\ScenarioMessageData_Chapter_1.packed"
    dest = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_Chapter_1"
    backup = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter_backup_before_MASTER_FINAL\ScenarioMessageData_Chapter_1.pre_final_backup"

    if os.path.exists(dest):
        shutil.copy2(dest, backup)
        print(f"Backed up current file to {backup}")

    shutil.copy2(src, dest)
    print(f"Successfully injected {src} into {dest}")
    print(f"Target file size: {os.path.getsize(dest)} bytes.")

if __name__ == "__main__":
    main()
