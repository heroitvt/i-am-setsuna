import struct

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        data = f.read(64*1024)
        
    offset = 2064
    table_size = struct.unpack(">I", data[offset+4:offset+8])[0]
    table_data = data[offset+8:offset+8+table_size]
    rows_offset, strings_offset, data_offset, table_name_offset, num_fields, row_length, num_rows = struct.unpack(">IIIIHHI", table_data[:24])
    
    cur = 24
    columns = []
    for _ in range(num_fields):
        col_type = table_data[cur]; cur += 1
        name_offset = struct.unpack(">I", table_data[cur:cur+4])[0]; cur += 4
        col_name = ""
        str_cur = strings_offset + name_offset
        while str_cur < len(table_data) and table_data[str_cur] != 0:
            col_name += chr(table_data[str_cur]); str_cur += 1
        columns.append((col_name, hex(col_type)))
    print("Columns:", columns)
    print(f"num_rows: {num_rows}, row_length: {row_length}")

if __name__ == "__main__":
    main()
