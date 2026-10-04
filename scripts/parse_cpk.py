import struct
import io

def parse_utf_table(data, offset=0):
    if data[offset:offset+4] != b"@UTF":
        return None
    table_size = struct.unpack(">I", data[offset+4:offset+8])[0]
    table_data = data[offset+8:offset+8+table_size]
    
    rows_offset, strings_offset, data_offset, table_name_offset, num_fields, row_length, num_rows = struct.unpack(">IIIIHHI", table_data[:24])
    
    # parse schema/columns
    cur = 24
    columns = []
    for _ in range(num_fields):
        col_type = table_data[cur]
        cur += 1
        name_offset = struct.unpack(">I", table_data[cur:cur+4])[0]
        cur += 4
        col_name = ""
        str_cur = strings_offset + name_offset
        while str_cur < len(table_data) and table_data[str_cur] != 0:
            col_name += chr(table_data[str_cur])
            str_cur += 1
        columns.append((col_name, col_type))
        
    # parse rows
    rows = []
    for r in range(num_rows):
        row_cur = rows_offset + r * row_length
        row_dict = {}
        for col_name, col_type in columns:
            flags = col_type & 0xF0
            type_id = col_type & 0x0F
            if flags == 0x10 or flags == 0x30:
                pass # constant or default
            val = None
            if type_id == 0: # 1 byte
                val = table_data[row_cur]
                row_cur += 1
            elif type_id == 1: # 1 byte signed
                val = struct.unpack(">b", table_data[row_cur:row_cur+1])[0]
                row_cur += 1
            elif type_id == 2: # 2 byte
                val = struct.unpack(">H", table_data[row_cur:row_cur+2])[0]
                row_cur += 2
            elif type_id == 3: # 2 byte signed
                val = struct.unpack(">h", table_data[row_cur:row_cur+2])[0]
                row_cur += 2
            elif type_id == 4: # 4 byte
                val = struct.unpack(">I", table_data[row_cur:row_cur+4])[0]
                row_cur += 4
            elif type_id == 5: # 4 byte signed
                val = struct.unpack(">i", table_data[row_cur:row_cur+4])[0]
                row_cur += 4
            elif type_id == 6: # 8 byte
                val = struct.unpack(">Q", table_data[row_cur:row_cur+8])[0]
                row_cur += 8
            elif type_id == 7: # 8 byte signed
                val = struct.unpack(">q", table_data[row_cur:row_cur+8])[0]
                row_cur += 8
            elif type_id == 8: # float
                val = struct.unpack(">f", table_data[row_cur:row_cur+4])[0]
                row_cur += 4
            elif type_id == 0xA: # string
                str_off = struct.unpack(">I", table_data[row_cur:row_cur+4])[0]
                row_cur += 4
                s = ""
                str_c = strings_offset + str_off
                while str_c < len(table_data) and table_data[str_c] != 0:
                    s += chr(table_data[str_c])
                    str_c += 1
                val = s
            elif type_id == 0xB: # data
                d_off = struct.unpack(">I", table_data[row_cur:row_cur+4])[0]
                row_cur += 4
                d_len = struct.unpack(">I", table_data[row_cur:row_cur+4])[0]
                row_cur += 4
                val = table_data[data_offset + d_off : data_offset + d_off + d_len]
            row_dict[col_name] = val
        rows.append(row_dict)
    return rows

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        data = f.read(64*1024) # read first 64KB
        
    header_rows = parse_utf_table(data, 16) # CPK starts with CPK\xff\x00\x00\x00, then @UTF header
    if header_rows:
        print("CPK Header:", header_rows[0])
        toc_offset = header_rows[0].get("TocOffset")
        toc_size = header_rows[0].get("TocSize")
        content_offset = header_rows[0].get("ContentOffset")
        print(f"TocOffset: {toc_offset}, TocSize: {toc_size}, ContentOffset: {content_offset}")
        
        with open(cpk_path, "rb") as f:
            f.seek(toc_offset)
            toc_data = f.read(toc_size)
        
        # Toc starts with TOC\xff\x00\x00\x00, then @UTF
        if toc_data[:4] == b"TOC ":
            toc_rows = parse_utf_table(toc_data, 16)
        else:
            toc_rows = parse_utf_table(toc_data, 0)
            
        print(f"Total files in TOC: {len(toc_rows) if toc_rows else 0}")
        if toc_rows:
            for r in toc_rows:
                fname = r.get("FileName") or r.get("DirName")
                if "ScenarioMessageData_Chapter_1" in str(fname):
                    print("Found file entry in TOC:", r)

if __name__ == "__main__":
    main()
