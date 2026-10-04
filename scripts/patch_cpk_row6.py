import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import shutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def encrypt_data(data):
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

def decrypt_data(data):
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    bak_path = r"d:\Viet Hoa Game\temp_scripts\parameter.cpk.bak_before_row6"
    
    if not os.path.exists(bak_path):
        print(f"Creating backup of parameter.cpk to {bak_path}...")
        shutil.copyfile(cpk_path, bak_path)
    else:
        print("Backup parameter.cpk.bak_before_row6 already exists.")

    orig_size = os.path.getsize(cpk_path)
    print(f"Original parameter.cpk size: {orig_size} bytes")

    # Read the 372,704 bytes at offset 9605120
    offset = 9605120
    file_size = 372704

    with open(cpk_path, "rb") as f:
        f.seek(offset)
        raw_enc = f.read(file_size)

    assert len(raw_enc) == file_size, f"Expected {file_size} bytes, got {len(raw_enc)}"

    # Decrypt
    dec = bytearray(decrypt_data(raw_enc))
    assert len(dec) == file_size

    # RID 3 is at pos = 604
    # Let's verify
    pos = 604
    import struct
    magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[pos:pos+16])
    assert rid == 3, f"Expected RID 3 at pos 604, got {rid}"
    assert l2 == 126, f"Expected l2=126, got {l2}"
    assert rlen == 362, f"Expected rlen=362, got {rlen}"

    cur = pos + 16
    n_len = dec[cur]; cur += 1 + n_len
    q_len = dec[cur]; cur += 1 + q_len
    cur += l1 # skip Japanese

    # Target Vietnamese text:
    # "Ừm... Đúng như lời đồn.\nMột lính đánh thuê bẩm sinh."
    target_text = "Ừm... Đúng như lời đồn.\nMột lính đánh thuê bẩm sinh."
    u16_bytes = target_text.encode('utf-16le')
    
    # We need exactly 124 bytes of UTF-16LE text so l2 remains 126 (1 byte page count + 1 byte len + 124 bytes)
    padding_needed = 124 - len(u16_bytes)
    assert padding_needed >= 0, f"Text too long: {len(u16_bytes)} > 124"
    assert padding_needed % 2 == 0, "Padding must be even for UTF-16LE"
    
    padded_text = target_text + (" " * (padding_needed // 2))
    padded_u16 = padded_text.encode('utf-16le')
    assert len(padded_u16) == 124

    new_s2 = bytearray()
    new_s2.append(1)    # 1 page
    new_s2.append(124)  # 124 bytes
    new_s2.extend(padded_u16)
    assert len(new_s2) == 126

    # Replace s2 in dec
    old_s2 = dec[cur:cur+126]
    print(f"Old s2 text: {repr(old_s2[2:].decode('utf-16le', errors='ignore'))}")
    dec[cur:cur+126] = new_s2
    print(f"New s2 text: {repr(new_s2[2:].decode('utf-16le'))}")

    # Verify total length
    assert len(dec) == file_size

    # Re-encrypt
    new_enc = encrypt_data(bytes(dec))
    assert len(new_enc) == file_size

    # Write back in-place to parameter.cpk
    with open(cpk_path, "r+b") as f:
        f.seek(offset)
        f.write(new_enc)

    new_size = os.path.getsize(cpk_path)
    print(f"New parameter.cpk size: {new_size} bytes (must match {orig_size})")
    assert new_size == orig_size, "File size changed!"

    # Verify by reading back and decrypting
    with open(cpk_path, "rb") as f:
        f.seek(offset)
        read_back_enc = f.read(file_size)
    read_back_dec = decrypt_data(read_back_enc)
    cur_check = pos + 16 + 1 + n_len + 1 + q_len + l1
    read_back_s2 = read_back_dec[cur_check:cur_check+126]
    print(f"Verified read-back text from CPK: {repr(read_back_s2[2:].decode('utf-16le'))}")
    print("CPK PATCH SUCCESSFUL!")

if __name__ == "__main__":
    main()
