from parse_utf_proper import parse_utf_table

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        data = f.read(64*1024)
    rows = parse_utf_table(data, 2064)
    
    print("Sample file offsets:")
    for r in rows[:10]:
        fn = r["FileName"]
        sz = r["FileSize"]
        off = r["FileOffset"]
        print(f"  {fn:<30}: FileOffset={off:<10} (hex: {hex(off)}), FileSize={sz:<8}, align={off % 2048}")

if __name__ == "__main__":
    main()
