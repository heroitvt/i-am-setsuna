import os
from parse_utf_proper import parse_utf_table

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        data = f.read(64*1024)
    rows = parse_utf_table(data, 2064)
    
    pdir = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter"
    missing = []
    size_diffs = []
    for r in rows:
        fn = r.get("FileName") or r.get("DirName")
        lp = os.path.join(pdir, fn)
        if not os.path.exists(lp):
            missing.append(fn)
        else:
            sz = os.path.getsize(lp)
            cpk_sz = r["FileSize"]
            if sz != cpk_sz:
                size_diffs.append((fn, sz, cpk_sz))
                
    print(f"Total files in CPK: {len(rows)}")
    print(f"Missing from data/parameter: {len(missing)}")
    print(f"Size diffs: {len(size_diffs)}")
    for d in size_diffs:
        print(" ", d)

if __name__ == "__main__":
    main()
