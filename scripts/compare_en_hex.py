import openpyxl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def main():
    wb = openpyxl.load_workbook(r"d:\Viet Hoa Game\I_am_Setsuna-parameter-Steam.xlsx", data_only=True)
    ws = wb["ScenarioMessageData_Chapter_1"]
    en = ws.cell(126, 2).value
    
    p = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter_backup_before_MASTER_FINAL\ScenarioMessageData_Chapter_1.backup_before_CH1_LOOSE_TEST"
    with open(p, "rb") as f:
        d = f.read()
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor().update(d)
    
    offset = 0
    for r in range(1403):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if rid == 123:
            cur = offset + 16
            cur += 1 + dec[cur]
            cur += 1 + dec[cur]
            s1 = dec[cur:cur+l1]; cur += l1
            s2 = dec[cur:cur+l2]; cur += l2
            print("RID 123 l2:", l2)
            print("s2 raw (hex):", s2.hex())
            print("en bytes (hex):", en.encode('utf-16le').hex())
            break
        offset += rlen

if __name__ == "__main__":
    main()
