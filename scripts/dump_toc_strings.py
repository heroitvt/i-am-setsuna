import struct

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        data = f.read(64*1024)
        
    offset = 2064
    magic, table_size = struct.unpack(">4sI", data[offset:offset+8])
    raw = data[offset+8:offset+8+table_size]
    rows_offset, strings_offset, data_offset, table_name_offset, num_fields, row_length, num_rows = struct.unpack(">IIIIHHI", raw[:24])
    
    print(f"strings_offset: {strings_offset}, data_offset: {data_offset}, rows_offset: {rows_offset}")
    
    # print all strings in strings table
    strings_data = raw[strings_offset:data_offset]
    parts = strings_data.split(b"\x00")
    print("Strings in CpkTocInfo:")
    for p in parts:
        if p:
            print(" ", p.decode('ascii', errors='ignore'))

if __name__ == "__main__":
    main()
