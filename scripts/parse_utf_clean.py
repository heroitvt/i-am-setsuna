import struct

def parse_utf(data, offset):
    magic, table_size = struct.unpack(">4sI", data[offset:offset+8])
    if magic != b"@UTF":
        return None
    raw = data[offset+8:offset+8+table_size]
    rows_offset, strings_offset, data_offset, table_name_offset, num_fields, row_length, num_rows = struct.unpack(">IIIIHHI", raw[:24])
    
    def get_str(str_off):
        end = raw.find(b"\x00", strings_offset + str_off)
        return raw[strings_offset + str_off:end].decode('ascii', errors='ignore')
        
    table_name = get_str(table_name_offset)
    print(f"Table name: {table_name}, num_fields: {num_fields}, row_len: {row_length}, num_rows: {num_rows}")
    
    cur = 24
    cols = []
    for _ in range(num_fields):
        col_type = raw[cur]; cur += 1
        name_off = struct.unpack(">I", raw[cur:cur+4])[0]; cur += 4
        cols.append((get_str(name_off), col_type))
        
    print("Cols:", cols)
    
    rows = []
    for r in range(num_rows):
        row_pos = rows_offset + r * row_length
        item = {}
        for cname, ctype in cols:
            flags = ctype & 0xF0
            type_id = ctype & 0x0F
            if flags in (0x10, 0x30): # constant or default
                pass
            val = None
            if type_id == 0:
                val = raw[row_pos]; row_pos += 1
            elif type_id == 1:
                val = struct.unpack(">b", raw[row_pos:row_pos+1])[0]; row_pos += 1
            elif type_id == 2:
                val = struct.unpack(">H", raw[row_pos:row_pos+2])[0]; row_pos += 2
            elif type_id == 3:
                val = struct.unpack(">h", raw[row_pos:row_pos+2])[0]; row_pos += 2
            elif type_id == 4:
                val = struct.unpack(">I", raw[row_pos:row_pos+4])[0]; row_pos += 4
            elif type_id == 5:
                val = struct.unpack(">i", raw[row_pos:row_pos+4])[0]; row_pos += 4
            elif type_id == 6:
                val = struct.unpack(">Q", raw[row_pos:row_pos+8])[0]; row_pos += 8
            elif type_id == 7:
                val = struct.unpack(">q", raw[row_pos:row_pos+8])[0]; row_pos += 8
            elif type_id == 8:
                val = struct.unpack(">f", raw[row_pos:row_pos+4])[0]; row_pos += 4
            elif type_id == 0xA:
                soff = struct.unpack(">I", raw[row_pos:row_pos+4])[0]; row_pos += 4
                val = get_str(soff)
            elif type_id == 0xB:
                doff = struct.unpack(">I", raw[row_pos:row_pos+4])[0]; row_pos += 4
                dlen = struct.unpack(">I", raw[row_pos:row_pos+4])[0]; row_pos += 4
                val = raw[data_offset + doff:data_offset + doff + dlen]
            item[cname] = val
        rows.append(item)
    return rows

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        data = f.read(64*1024)
    rows = parse_utf(data, 2064)
    for r in rows[:10]:
        print(r)
    for r in rows:
        fn = r.get("FileName") or r.get("DirName")
        if fn and "ScenarioMessageData_Chapter_1" in fn:
            print("Found Chapter 1:", r)

if __name__ == "__main__":
    main()
