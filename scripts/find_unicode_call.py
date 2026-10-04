import struct

def main():
    dll = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    with open(dll, "rb") as f:
        data = f.read()

    # Search for MemberRef table in #~ to find get_Unicode
    # MemberRef token is 0x0aXXXXXX
    # Let's search for "get_Unicode" in #Strings
    str_offset = 1540364
    target = b"get_Unicode\x00"
    pos = data.find(target, str_offset)
    if pos != -1:
        str_idx = pos - str_offset
        print(f"get_Unicode string index: {hex(str_idx)}")
        
        # In MemberRef table (#~), find rows where Name == str_idx
        # Let's search MemberRef rows in tilde stream
        tilde = data[969636:969636+570728]
        # Let's search for str_idx in tilde as 2 or 4 bytes
        pattern2 = struct.pack("<H", str_idx)
        pattern4 = struct.pack("<I", str_idx)
        print("Matches in tilde:")
        for m in [i for i in range(len(tilde)-4) if tilde[i:i+4] == pattern4 or tilde[i:i+2] == pattern2]:
            pass

if __name__ == "__main__":
    main()
