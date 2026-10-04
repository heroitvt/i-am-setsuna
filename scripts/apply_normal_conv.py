import shutil
import os
import subprocess
import sys

def main():
    packed_file = r"d:\Viet Hoa Game\temp_scripts\ScenarioMessageData_NormalConversation.packed"
    loose_file = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_NormalConversation"
    backup_file = r"d:\Viet Hoa Game\temp_scripts\ScenarioMessageData_NormalConversation.orig"

    if not os.path.exists(backup_file):
        print(f"Creating backup of original loose file to {backup_file}...")
        shutil.copy2(loose_file, backup_file)

    print(f"Copying packed NormalConversation to loose file: {loose_file}...")
    shutil.copy2(packed_file, loose_file)
    print("Loose file updated successfully!")

    # Now rebuild CPK
    print("\nRebuilding parameter.cpk...")
    sys.path.append(r"d:\Viet Hoa Game\temp_scripts")
    import rebuild_cpk
    rebuild_cpk.main()

    # Now replace the parameter.cpk
    new_cpk = r"d:\Viet Hoa Game\temp_scripts\parameter.cpk.new"
    target_cpk = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    
    assert os.path.exists(new_cpk)
    new_cpk_size = os.path.getsize(new_cpk)
    print(f"New CPK size: {new_cpk_size} bytes")

    print(f"Replacing target CPK at {target_cpk}...")
    shutil.copy2(new_cpk, target_cpk)
    print("Target CPK replaced successfully!")

if __name__ == "__main__":
    main()
