import os
import sys
import struct
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def build_s2(vn_text):
    pages = vn_text.split("\n|\n")
    res = bytearray()
    res.append(len(pages))
    for p in pages:
        p_clean = p.strip()
        b = p_clean.encode('utf-16le')
        if len(b) > 255:
            b = b[:254]
            if len(b) % 2 != 0:
                b = b[:-1]
        res.append(len(b))
        res.extend(b)
    return bytes(res)

def main():
    json_path = r"D:\Viet Hoa Game\temp_scripts\normal_conv_translated.json"
    with open(json_path, "r", encoding="utf-8") as f:
        all_trans = json.load(f)
    print(f"Loaded {len(all_trans)} translations.")

    in_path = r"D:\Viet Hoa Game\temp_scripts\ScenarioMessageData_NormalConversation.orig"
    with open(in_path, "rb") as f:
        encrypted_raw = f.read()

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = cipher.decryptor().update(encrypted_raw)
    print(f"Decrypted orig size: {len(dec)} bytes.")

    offset = 0
    total_records = 0
    modified_count = 0
    new_payload = bytearray()

    while offset + 16 <= len(dec):
        mtype, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if rlen == 0 or rlen > 10000:
            break
        
        rec = dec[offset:offset+rlen]
        cur = 16
        n_len = rec[cur]; cur += 1
        npc_bytes = rec[cur:cur+n_len]; cur += n_len
        q_len = rec[cur]; cur += 1
        q_bytes = rec[cur:cur+q_len]; cur += q_len
        
        s1_bytes = rec[cur:cur+l1]; cur += l1
        cur += l2 # old s2
        s3_bytes = rec[cur:cur+l3]; cur += l3

        rid_str = str(rid)
        if rid_str in all_trans:
            vn_text = all_trans[rid_str]
            new_s2 = build_s2(vn_text)
            new_l2 = len(new_s2)
            new_rlen = 16 + 1 + n_len + 1 + q_len + l1 + new_l2 + l3
            
            new_hdr = struct.pack("<ihhhhHh", mtype, rid, l1, new_l2, l3, new_rlen, npcid)
            new_payload.extend(new_hdr)
            new_payload.append(n_len)
            new_payload.extend(npc_bytes)
            new_payload.append(q_len)
            new_payload.extend(q_bytes)
            new_payload.extend(s1_bytes)
            new_payload.extend(new_s2)
            new_payload.extend(s3_bytes)
            modified_count += 1
        else:
            new_payload.extend(rec)

        total_records += 1
        offset += rlen

    print(f"Processed {total_records} records, modified {modified_count} records.")
    
    # Save .dec
    out_dec_path = r"D:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_NormalConversation.dec"
    with open(out_dec_path, "wb") as f:
        f.write(new_payload)
    print(f"Saved .dec ({len(new_payload)} bytes) to {out_dec_path}")

    # Pad to 16 bytes and encrypt
    pad_len = 16 - (len(new_payload) % 16)
    if pad_len < 16:
        new_payload.extend(b"\x00" * pad_len)

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    enc = cipher.encryptor().update(bytes(new_payload))

    out_enc_path = r"D:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_NormalConversation"
    with open(out_enc_path, "wb") as f:
        f.write(enc)
    print(f"Saved encrypted loose file ({len(enc)} bytes) to {out_enc_path}")

    packed_path = r"D:\Viet Hoa Game\temp_scripts\ScenarioMessageData_NormalConversation.packed"
    with open(packed_path, "wb") as f:
        f.write(enc)
    print(f"Saved packed backup to {packed_path}")

if __name__ == "__main__":
    main()
