import os

def main():
    p1 = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    p2 = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll.bak"
    print("Assembly-CSharp.dll:", os.path.getsize(p1))
    print("Assembly-CSharp.dll.bak:", os.path.getsize(p2))

if __name__ == "__main__":
    main()
