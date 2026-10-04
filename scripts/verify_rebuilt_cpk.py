from parse_utf_proper import parse_utf_table

def main():
    cpk_path = r"d:\Viet Hoa Game\temp_scripts\parameter.cpk.new"
    with open(cpk_path, "rb") as f:
        data = f.read(64*1024)
        
    rows = parse_utf_table(data, 2064)
    print("Total rows in rebuilt CPK:", len(rows))
    for r in rows:
        if r["FileName"] == "ScenarioMessageData_Chapter_1":
            print("Chapter 1 in rebuilt CPK:", r)
            # test reading it
            with open(cpk_path, "rb") as cf:
                cf.seek(20480 + r["FileOffset"])
                ch1_bytes = cf.read(r["FileSize"])
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.backends import default_backend
            import struct
            dec = Cipher(algorithms.AES(b"8xTD|EgD|b?07QDj"), modes.CBC(b"/]s@*CxLzM!9Qd%("), backend=default_backend()).decryptor().update(ch1_bytes)
            magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[:16])
            print(f"Decrypted Chapter 1 from rebuilt CPK: magic={hex(magic)}, rid={rid}, l2={l2}, rlen={rlen}")

if __name__ == "__main__":
    main()
