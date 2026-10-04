import openpyxl
import json
import re

def main():
    wb = openpyxl.load_workbook(r"d:\Viet Hoa Game\I_am_Setsuna-parameter-Steam.xlsx", data_only=True)
    ws = wb["ScenarioMessageData_Chapter_1"]
    
    rows = []
    for r in range(3, 1406):
        id_val = ws.cell(r, 1).value
        en_val = ws.cell(r, 2).value
        vn_val = ws.cell(r, 3).value
        
        # parse id from ID cell: e.g. 4211_{"NpcNm":"NPC_10031","QuestNm":"","Head":{"Type":-1,"Id":123,"NpcId":2,"QuestId":0}}
        # or rid can be extracted from regex: "Id":(\d+)
        m = re.search(r'"Id":(\d+)', str(id_val))
        if not m:
            print(f"Row {r} no Id: {id_val}")
            continue
        rid = int(m.group(1))
        
        rows.append((rid, en_val, vn_val))
        
    print(f"Loaded {len(rows)} rows from Excel.")
    
    # Check page encoding
    encode_errors = []
    for rid, en, vn in rows:
        if vn is None or str(vn).strip() == "":
            encode_errors.append((rid, "Empty VN"))
            continue
        vn_str = str(vn)
        # Check if page breaks exist
        # In Excel, is it \n|\n or | or \r\n|\r\n?
        # Let's split by regex \r?\n?\|\r?\n? or \|
        if "|" in vn_str:
            # Let's see how EN splits vs how VN splits
            en_pages = re.split(r'\n?\|\n?', str(en))
            vn_pages = re.split(r'\n?\|\n?', vn_str)
            if len(en_pages) != len(vn_pages):
                encode_errors.append((rid, f"Page count mismatch: EN {len(en_pages)} vs VN {len(vn_pages)}"))
            for p_idx, p in enumerate(vn_pages):
                p_bytes = p.encode('utf-16le')
                if len(p_bytes) > 255:
                    encode_errors.append((rid, f"Page {p_idx} byte len > 255: {len(p_bytes)}"))
        else:
            p_bytes = vn_str.encode('utf-16le')
            if len(p_bytes) > 255:
                encode_errors.append((rid, f"Single page byte len > 255: {len(p_bytes)}"))
                
    print(f"Encode errors: {len(encode_errors)}")
    if encode_errors:
        for err in encode_errors[:10]:
            print(" ", err)

if __name__ == "__main__":
    main()
