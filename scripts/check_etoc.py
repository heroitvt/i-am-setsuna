from parse_utf_proper import parse_utf_table

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        data = f.read(32*1024)
        
    header = parse_utf_table(data, 16)[0]
    print("Header:", header)
    etoc_off = header.get("EtocOffset")
    etoc_size = header.get("EtocSize")
    print(f"EtocOffset: {etoc_off}, EtocSize: {etoc_size}")
    if etoc_off and etoc_size:
        etoc_rows = parse_utf_table(data, etoc_off)
        print("ETOC rows:", len(etoc_rows) if etoc_rows else 0)
        if etoc_rows:
            print("ETOC sample:", etoc_rows[0])

if __name__ == "__main__":
    main()
