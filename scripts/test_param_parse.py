import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def decrypt_file(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(data) + decryptor.finalize()
    return decrypted

def main():
    p1 = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_Chapter_1"
    if os.path.exists(p1):
        dec = decrypt_file(p1)
        print("Decrypted len:", len(dec))
        # Let's inspect first record
        # Header is 16 bytes:
        # type (int32 - 4 bytes), id (int16 - 2 bytes), l1 (int16), l2 (int16), l3 (int16), rec_len (uint16), npcid (int16)
        import struct
        offset = 0
        records = []
        while offset + 16 <= len(dec):
            magic = struct.unpack("<i", dec[offset:offset+4])[0]
            if magic != -1:
                break
            rec_id, l1, l2, l3, rec_len, npcid = struct.unpack("<hhhhHh", dec[offset+4:offset+16])
            records.append((rec_id, l1, l2, l3, rec_len, npcid, offset))
            offset += rec_len
        print(f"Total records parsed from data/parameter: {len(records)}")
        
        # Check first 3 records text
        for r in records[:3]:
            rec_id, l1, l2, l3, rec_len, npcid, roff = r
            cur = roff + 16
            # npc name
            n_len = dec[cur]
            cur += 1
            n_str = dec[cur:cur+n_len].decode('utf-16le', errors='ignore')
            cur += n_len
            # quest name
            q_len = dec[cur]
            cur += 1
            q_str = dec[cur:cur+q_len].decode('utf-16le', errors='ignore')
            cur += q_len
            
            # str1 (JP)
            s1_type = dec[cur]
            cur += 1
            s1_bytes = dec[cur:cur+l1].decode('utf-16le', errors='ignore')
            cur += l1
            
            # str2 (EN/VN)
            s2_type = dec[cur]
            cur += 1
            s2_bytes = dec[cur:cur+l2].decode('utf-16le', errors='ignore')
            cur += l2
            
            print(f"ID {rec_id} (NPC: {n_str}): {s2_bytes[:50]}")
            
        # Check record 308, 309, 310
        for r in records[308:312]:
            rec_id, l1, l2, l3, rec_len, npcid, roff = r
            cur = roff + 16
            n_len = dec[cur]; cur += 1 + n_len
            q_len = dec[cur]; cur += 1 + q_len
            cur += 1 + l1
            cur += 1
            s2_bytes = dec[cur:cur+l2].decode('utf-16le', errors='ignore')
            print(f"ID {rec_id}: {s2_bytes[:50]}")

if __name__ == "__main__":
    main()
