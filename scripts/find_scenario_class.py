import re

def main():
    dll = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    with open(dll, "rb") as f:
        data = f.read()

    # Search for "ScenarioMessage" in ASCII table
    matches = [m.start() for m in re.finditer(b"ScenarioMessage", data)]
    for m in matches:
        print(f"Match at {m}: {data[max(0, m-20):min(len(data), m+60)]}")

if __name__ == "__main__":
    main()
