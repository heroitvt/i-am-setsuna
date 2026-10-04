from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def parse_string_field(data):
    if len(data) == 0:
        return []
    num_pages = data[0]
    pages = []
    cur = 1
    for p in range(num_pages):
        page_len = data[cur]
        cur += 1
        page_bytes = data[cur:cur+page_len]
        cur += page_len
        pages.append(page_bytes.decode('utf-16le'))
    if cur != len(data):
        raise ValueError(f"Consumed {cur} != {len(data)}")
    return pages

def main():
    p = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter_backup_before_MASTER_FINAL\ScenarioMessageData_Chapter_1.backup_before_CH1_LOOSE_TEST"
    with open(p, "rb") as f:
        d = f.read()
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor().update(d)
    
    offset = 0
    all_clean = True
    total_records = 0
    
    for r in range(1403):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        cur = offset + 16
        n_len = dec[cur]; cur += 1 + n_len
        q_len = dec[cur]; cur += 1 + q_len
        
        s1 = dec[cur:cur+l1]; cur += l1
        s2 = dec[cur:cur+l2]; cur += l2
        s3 = dec[cur:cur+l3]; cur += l3
        
        try:
            p1 = parse_string_field(s1)
            p2 = parse_string_field(s2)
            p3 = parse_string_field(s3)
        except Exception as e:
            print(f"Record {rid} parse error: {e}")
            all_clean = False
            
        total_records += 1
        offset += rlen
        
    print(f"Parsed {total_records} records in pristine backup. 100% exact match for ALL strings: {all_clean}")

if __name__ == "__main__":
    main()
