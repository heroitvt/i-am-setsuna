import os

def main():
    dll = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    with open(dll, "rb") as f:
        data = f.read()

    # Search for "ScenarioMessageData_Chapter_1"
    target = "ScenarioMessageData_Chapter_1".encode('utf-16le')
    pos = 0
    while True:
        idx = data.find(target, pos)
        if idx == -1:
            break
        print(f"Found target at offset {idx}")
        pos = idx + len(target)

if __name__ == "__main__":
    main()
