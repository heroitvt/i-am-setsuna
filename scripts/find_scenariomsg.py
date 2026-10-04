import re

def main():
    dll = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    with open(dll, "rb") as f:
        data = f.read()

    # Search for "ScenarioData" in strings
    matches = [m.start() for m in re.finditer(b"ScenarioMessage", data)]
    print("ScenarioMessage matches:", len(matches))
    for m in matches:
        print(f"  {m}: {data[m:m+50]}")

if __name__ == "__main__":
    main()
