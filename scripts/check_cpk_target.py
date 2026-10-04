import os

def main():
    cpk = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk, "rb") as f:
        data = f.read()
    
    target = b"ScenarioMessageData_Chapter_1"
    idx = data.find(target)
    print("Found ScenarioMessageData_Chapter_1 in parameter.cpk at:", idx)

if __name__ == "__main__":
    main()
