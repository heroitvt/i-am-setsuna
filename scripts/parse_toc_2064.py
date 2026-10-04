import struct
from inspect_cpk_toc import parse_utf_table

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        data = f.read(64*1024)
        
    toc_rows = parse_utf_table(data, 2064)
    print(f"Total TOC rows at 2064: {len(toc_rows) if toc_rows else 0}")
    if toc_rows:
        print("Sample row 0:", toc_rows[0])
        for r in toc_rows:
            name = r.get("FileName")
            if name and "ScenarioMessageData_Chapter_1" in name:
                print("Found file entry:", r)

if __name__ == "__main__":
    main()
