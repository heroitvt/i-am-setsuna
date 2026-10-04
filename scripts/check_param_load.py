import re

def main():
    dll = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    with open(dll, "rb") as f:
        data = f.read()

    # Search for "parameter.cpk" or "parameter/" or "ScenarioMessageData"
    for term in [b"parameter.cpk", b"data/parameter", b"StreamingAssets", b"parameter"]:
        pos = 0
        print(f"--- Matches for {term} ---")
        count = 0
        while True:
            idx = data.find(term, pos)
            if idx == -1 or count > 10:
                break
            # print surrounding context
            start = max(0, idx - 50)
            end = min(len(data), idx + 50)
            print(f"@{idx}: {data[start:end]}")
            pos = idx + len(term)
            count += 1

if __name__ == "__main__":
    main()
