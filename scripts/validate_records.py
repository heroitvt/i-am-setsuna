from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def main():
    p = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_Chapter_1"
    with open(p, "rb") as f:
        d = f.read()
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor().update(d)
    
    offset = 0
    all_ok = True
    record_count = 0
    
    while offset + 16 <= len(dec):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if magic != -1:
            print(f"Non -1 magic at offset {offset}: {magic}")
            break
            
        cur = offset + 16
        npc_len = dec[cur]; cur += 1
        npc_bytes = dec[cur:cur+npc_len]; cur += npc_len
        
        q_len = dec[cur]; cur += 1
        q_bytes = dec[cur:cur+q_len]; cur += q_len
        
        # s1
        s1_type = dec[cur]; cur += 1
        s1_len = dec[cur]; cur += 1
        s1_bytes = dec[cur:cur+s1_len]; cur += s1_len
        if s1_len + 2 != l1:
            print(f"Record {rid} s1_len mismatch: {s1_len}+2 != {l1}")
            all_ok = False
            
        # s2
        s2_type = dec[cur]; cur += 1
        s2_len = dec[cur]; cur += 1
        s2_bytes = dec[cur:cur+s2_len]; cur += s2_len
        if s2_len + 2 != l2:
            print(f"Record {rid} s2_len mismatch: {s2_len}+2 != {l2}")
            all_ok = False
            
        # s3
        s3_type = dec[cur]; cur += 1
        s3_len = dec[cur]; cur += 1
        s3_bytes = dec[cur:cur+s3_len]; cur += s3_len
        if s3_len + 2 != l3:
            print(f"Record {rid} s3_len mismatch: {s3_len}+2 != {l3}")
            all_ok = False
            
        consumed = cur - offset
        if consumed > rlen:
            print(f"Record {rid} consumed {consumed} > rlen {rlen}")
            all_ok = False
            
        record_count += 1
        offset += rlen
        
    print(f"Verified {record_count} records. All lengths and structures match: {all_ok}")
    print(f"Final offset: {offset}, total decrypted len: {len(dec)}")

if __name__ == "__main__":
    main()
