import os
import sys
import struct
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Import translations
sys.path.append(os.path.dirname(__file__))
from nive_trans_batch1 import NIVE_TRANS_1
from nive_trans_batch2 import NIVE_TRANS_2

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def build_s2(vn_text):
    pages = vn_text.split("\n|\n")
    res = bytearray()
    res.append(len(pages))
    for p in pages:
        b = p.encode('utf-16le')
        assert len(b) <= 255, f"Page length {len(b)} exceeds 255: {p}"
        res.append(len(b))
        res.extend(b)
    return bytes(res)

def main():
    all_trans = {}
    all_trans.update(NIVE_TRANS_1)
    all_trans.update(NIVE_TRANS_2)
    print(f"Loaded {len(all_trans)} Nive translations (RIDs {min(all_trans)} to {max(all_trans)})")

    in_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_NormalConversation"
    with open(in_path, "rb") as f:
        encrypted_data = f.read()

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = cipher.decryptor().update(encrypted_data)

    offset = 0
    records = []
    total_records = 0
    modified_count = 0
    new_payload = bytearray()

    while offset + 16 <= len(dec):
        mtype, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if rlen == 0 or rlen > 10000:
            break
        
        rec_data = dec[offset:offset+rlen]
        cur = 16
        n_len = rec_data[cur]; cur += 1
        npc_bytes = rec_data[cur:cur+n_len]; cur += n_len
        q_len = rec_data[cur]; cur += 1
        quest_bytes = rec_data[cur:cur+q_len]; cur += q_len

        s1_bytes = rec_data[cur:cur+l1]; cur += l1
        s2_bytes = rec_data[cur:cur+l2]; cur += l2
        s3_bytes = rec_data[cur:cur+l3]; cur += l3

        if rid in all_trans:
            vn_text = all_trans[rid]
            new_s2 = build_s2(vn_text)
            new_l2 = len(new_s2)
            new_rlen = 16 + 1 + n_len + 1 + q_len + l1 + new_l2 + l3
            new_hdr = struct.pack("<ihhhhHh", mtype, rid, l1, new_l2, l3, new_rlen, npcid)

            new_rec = (
                new_hdr +
                bytes([n_len]) + npc_bytes +
                bytes([q_len]) + quest_bytes +
                s1_bytes +
                new_s2 +
                s3_bytes
            )
            assert len(new_rec) == new_rlen
            new_payload.extend(new_rec)
            modified_count += 1
        else:
            new_payload.extend(rec_data)

        total_records += 1
        offset += rlen

    print(f"Total records processed: {total_records}")
    print(f"Modified records: {modified_count}")

    # Pad to 16 bytes for AES-CBC
    pad_len = 16 - (len(new_payload) % 16)
    if pad_len != 16:
        new_payload.extend(b"\x00" * pad_len)

    # Encrypt
    c_enc = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    enc = c_enc.encryptor().update(bytes(new_payload))

    out_packed = r"d:\Viet Hoa Game\temp_scripts\ScenarioMessageData_NormalConversation.packed"
    with open(out_packed, "wb") as f:
        f.write(enc)
    print(f"Packed file written to: {out_packed} ({len(enc)} bytes)")

    # Verify
    print("\n--- Verifying packed file ---")
    c_ver = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec_ver = c_ver.decryptor().update(enc)

    v_offset = 0
    v_total = 0
    v_verified = 0
    while v_offset + 16 <= len(dec_ver):
        mtype, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec_ver[v_offset:v_offset+16])
        if rlen == 0 or rlen > 10000:
            break
        v_cur = v_offset + 16
        n_len = dec_ver[v_cur]; v_cur += 1
        npc = dec_ver[v_cur:v_cur+n_len].decode('utf-16le', errors='ignore'); v_cur += n_len
        q_len = dec_ver[v_cur]; v_cur += 1
        quest = dec_ver[v_cur:v_cur+q_len].decode('utf-16le', errors='ignore'); v_cur += q_len

        s1 = dec_ver[v_cur:v_cur+l1]; v_cur += l1
        s2 = dec_ver[v_cur:v_cur+l2]; v_cur += l2
        s3 = dec_ver[v_cur:v_cur+l3]; v_cur += l3

        if rid in all_trans:
            pages = []
            num_p = s2[0]
            cp = 1
            for _ in range(num_p):
                plen = s2[cp]; cp += 1
                pages.append(s2[cp:cp+plen].decode('utf-16le'))
                cp += plen
            reconstructed_txt = "\n|\n".join(pages)
            expected_txt = all_trans[rid]
            assert reconstructed_txt == expected_txt, f"Mismatch in RID {rid}!"
            v_verified += 1

        v_total += 1
        v_offset += rlen

    print(f"Verification successful! Verified {v_verified}/{modified_count} translated records.")
    print(f"Total records in packed file: {v_total}/{total_records}")

if __name__ == "__main__":
    main()
