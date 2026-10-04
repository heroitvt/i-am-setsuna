import struct
import re

def main():
    dll = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    with open(dll, "rb") as f:
        data = f.read()

    pe_offset = struct.unpack("<I", data[0x3C:0x40])[0]
    opt_header = pe_offset + 24
    cli_rva = struct.unpack("<I", data[opt_header+208:opt_header+212])[0]
    num_sections = struct.unpack("<H", data[pe_offset+6:pe_offset+8])[0]
    section_offset = pe_offset + 24 + struct.unpack("<H", data[pe_offset+20:pe_offset+22])[0]
    sections = []
    for i in range(num_sections):
        s_name = data[section_offset+i*40:section_offset+i*40+8].rstrip(b'\x00').decode('ascii')
        v_size, v_addr, r_size, r_offset = struct.unpack("<IIII", data[section_offset+i*40+8:section_offset+i*40+24])
        sections.append((s_name, v_addr, v_size, r_offset, r_size))
        
    def rva_to_offset(rva):
        for s_name, v_addr, v_size, r_offset, r_size in sections:
            if v_addr <= rva < v_addr + v_size:
                return r_offset + (rva - v_addr)
        return None

    cli_offset = rva_to_offset(cli_rva)
    meta_rva = struct.unpack("<I", data[cli_offset+8:cli_offset+12])[0]
    meta_offset = rva_to_offset(meta_rva)
    
    ver_len = struct.unpack("<I", data[meta_offset+12:meta_offset+16])[0]
    cur = meta_offset + 16 + ver_len
    cur = (cur + 3) & ~3
    flags, num_streams = struct.unpack("<HH", data[cur:cur+4])
    cur += 4
    streams = {}
    for i in range(num_streams):
        s_off, s_size = struct.unpack("<II", data[cur:cur+8])
        cur += 8
        s_name = ""
        while data[cur] != 0:
            s_name += chr(data[cur])
            cur += 1
        cur += 1
        cur = (cur + 3) & ~3
        streams[s_name] = (meta_offset + s_off, s_size)
    
    us_offset, us_size = streams["#US"]
    target = "ScenarioMessageData_Chapter_1".encode('utf-16le')
    target_pos = data.find(target, us_offset, us_offset + us_size)
    if target_pos != -1:
        token_id = (target_pos - 1 - us_offset) | 0x70000000
        print(f"Token ID for ScenarioMessageData_Chapter_1: {hex(token_id)}")
        token_bytes = struct.pack("<I", token_id)
        ldstr = b"\x72" + token_bytes
        matches = [m.start() for m in re.finditer(re.escape(ldstr), data)]
        print(f"Matches for ldstr {hex(token_id)}: {[hex(m) for m in matches]}")
        for m in matches:
            print(f"Around match {hex(m)}: {data[max(0, m-20):min(len(data), m+40)].hex()}")

if __name__ == "__main__":
    main()
