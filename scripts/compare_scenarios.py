import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def decrypt_file(p):
    with open(p, "rb") as f:
        d = f.read()
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor()
    return dec.update(d) + dec.finalize()

def parse_records(dec):
    import struct
    offset = 0
    records = []
    while offset + 16 <= len(dec):
        magic = struct.unpack("<i", dec[offset:offset+4])[0]
        if magic != -1:
            break
        rec_id, l1, l2, l3, rec_len, npcid = struct.unpack("<hhhhHh", dec[offset+4:offset+16])
        cur = offset + 16
        n_len = dec[cur]; cur += 1
        n_str = dec[cur:cur+n_len].decode('utf-16le', errors='ignore'); cur += n_len
        q_len = dec[cur]; cur += 1
        q_str = dec[cur:cur+q_len].decode('utf-16le', errors='ignore'); cur += q_len
        
        # s1
        cur += 1
        s1 = dec[cur:cur+l1].decode('utf-16le', errors='ignore'); cur += l1
        # s2
        cur += 1
        s2 = dec[cur:cur+l2].decode('utf-16le', errors='ignore'); cur += l2
        # s3
        cur += 1
        s3 = dec[cur:cur+l3].decode('utf-16le', errors='ignore'); cur += l3
        
        records.append({'id': rec_id, 'npc': n_str, 'quest': q_str, 's1': s1, 's2': s2, 's3': s3})
        offset += rec_len
    return records

def main():
    p_orig = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter_backup_before_MASTER_FINAL\ScenarioMessageData_Chapter_1.bak_original"
    p_test = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter_backup_before_MASTER_FINAL\ScenarioMessageData_Chapter_1.backup_before_CH1_LOOSE_TEST"
    p_curr = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_Chapter_1"

    rec_orig = parse_records(decrypt_file(p_orig))
    rec_test = parse_records(decrypt_file(p_test))
    rec_curr = parse_records(decrypt_file(p_curr))

    print(f"Orig: {len(rec_orig)} records")
    print(f"Test: {len(rec_test)} records")
    print(f"Curr: {len(rec_curr)} records")

    # Count how many s2 differ from orig in test and curr
    diff_test = sum(1 for o, t in zip(rec_orig, rec_test) if o['s2'] != t['s2'])
    diff_curr = sum(1 for o, c in zip(rec_orig, rec_curr) if o['s2'] != c['s2'])
    print(f"Diffs in Test vs Orig: {diff_test}")
    print(f"Diffs in Curr vs Orig: {diff_curr}")

if __name__ == "__main__":
    main()
