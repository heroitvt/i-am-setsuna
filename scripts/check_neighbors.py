from parse_utf_proper import parse_utf_table

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        data = f.read(64*1024)
    rows = parse_utf_table(data, 2064)
    
    # sort rows by FileOffset
    sorted_rows = sorted(rows, key=lambda r: r["FileOffset"])
    for idx, r in enumerate(sorted_rows):
        if r["FileName"] == "ScenarioMessageData_Chapter_1":
            print("Target row:", r)
            print("Previous row:", sorted_rows[idx-1])
            print("Next row:", sorted_rows[idx+1])
            next_off = sorted_rows[idx+1]["FileOffset"]
            curr_off = r["FileOffset"]
            gap = next_off - curr_off
            print(f"Gap between current and next: {gap} bytes (curr size: {r['FileSize']})")

if __name__ == "__main__":
    main()
