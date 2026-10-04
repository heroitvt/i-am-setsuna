from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct
import json

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def main():
    p = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_NormalConversation"
    with open(p, "rb") as f:
        d = f.read()
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor().update(d)
    
    offset = 0
    records = []
    while offset + 16 <= len(dec):
        mtype, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if rlen == 0 or rlen > 5000:
            break
        cur = offset + 16
        n_len = dec[cur]; cur += 1
        npc = dec[cur:cur+n_len].decode('utf-16le', errors='ignore'); cur += n_len
        q_len = dec[cur]; cur += 1
        quest = dec[cur:cur+q_len].decode('utf-16le', errors='ignore'); cur += q_len
        
        s1 = dec[cur:cur+l1]; cur += l1
        s2 = dec[cur:cur+l2]; cur += l2
        s3 = dec[cur:cur+l3]; cur += l3
        
        # parse s1 (JP)
        p1 = []
        if len(s1) > 0:
            num_p = s1[0]; c_p = 1
            for _ in range(num_p):
                plen = s1[c_p]; c_p += 1
                p1.append(s1[c_p:c_p+plen].decode('utf-16le', errors='ignore'))
                c_p += plen
        jp_txt = "\n|\n".join(p1)

        # parse s2 (EN/VN)
        p2 = []
        if len(s2) > 0:
            num_p = s2[0]; c_p = 1
            for _ in range(num_p):
                plen = s2[c_p]; c_p += 1
                p2.append(s2[c_p:c_p+plen].decode('utf-16le', errors='ignore'))
                c_p += plen
        en_txt = "\n|\n".join(p2)
        
        records.append({
            'rid': rid,
            'npc': npc,
            'quest': quest,
            'jp': jp_txt,
            'en': en_txt,
            'mtype': mtype,
            'l1': l1,
            'l2': l2,
            'l3': l3,
            'rlen': rlen,
            'npcid': npcid
        })
        offset += rlen
        
    print(f"Total parsed records: {len(records)}")
    
    # Save all records to JSON
    out_json = r"d:\Viet Hoa Game\temp_scripts\normal_conv_all.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"Saved all records to {out_json}")

if __name__ == "__main__":
    main()
