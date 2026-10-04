import json
import struct
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def decrypt_data(data):
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()

def encrypt_data(data):
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

# Tutorial translations dictionary
TUTORIAL_TRANSLATIONS = {
    # Titles
    "SYS142": "Thương Hội Ma Đạo",
    "SYS143": "Đầu Bếp & Nấu Ăn",
    "SYS144": "Rèn Cường Hóa Vũ Khí",
    "SYS145": "Biến Chuyển Flux",
    "SYS146": "Biến Chuyển Hỗ Trợ",
    "SYS147": "Chạm Trán Quái Vật",
    "SYS148": "Chiến Đấu Thời Gian Thực (ATB)",
    "SYS149": "Pháp Thạch Spritnite",
    "SYS150": "Chế Độ Xung Lực (Momentum)",
    "SYS151": "Hiệu Ứng Xung Lực & Dị Thường",
    "SYS152": "Điểm Lưu Game",
    
    # Contents
    "SYS173": (
        "Thành viên của Thương Hội Ma Đạo có mặt tại các thị trấn và làng mạc trên khắp đại lục.\r\n\r\n"
        "Họ sẽ thu mua những nguyên liệu mà quái vật đánh rơi. Ngoài việc nhận được tiền vàng, bạn còn có thể đổi lấy các viên pháp thạch Spritnite tùy thuộc vào những loại nguyên liệu bạn đã từng bán. Quái vật sẽ rơi ra các vật phẩm khác nhau tùy thuộc vào cách bạn tiêu diệt chúng (chẳng hạn như dùng đòn tấn công thuộc tính nhất định, dùng liên chiêu combo, dùng đòn đánh Xung Lực, tiêu diệt khi chúng đang dính trạng thái bất lợi, tiêu diệt với lượng sát thương vượt trội Over Kill, hoặc tiêu diệt với lượng sát thương vừa vặn Exact Kill).\r\n\r\n"
        "Các viên pháp thạch Spritnite bạn có thể nhận được hiển thị tại mục 'Nhận Spritnite'. Càng tiến sâu vào hành trình, càng có thêm nhiều pháp thạch mới, vì vậy hãy thường xuyên quay lại kiểm tra nhé!"
    ),
    
    "SYS174": (
        "Đầu bếp có mặt tại các thị trấn và làng mạc trên khắp đại lục.\r\n\r\n"
        "Bằng cách trò chuyện với họ, bạn có thể mua các món ăn bồi bổ. Thức ăn chỉ có thể dùng từ menu và sẽ phát huy tác dụng tăng chỉ số trong trận chiến tiếp theo. Sau trận chiến đó, hiệu quả sẽ kết thúc.\r\n\r\n"
        "Bạn có thể mở rộng danh sách món ăn bằng cách thu thập đủ các nguyên liệu cần thiết để nhận công thức nấu nướng. Nguyên liệu có thể nhặt được tại các điểm phát sáng lấp lánh trên bản đồ thế giới và trong các khu vực. Khi có đủ nguyên liệu, trò chuyện với các NPC nhất định sẽ giúp bạn nhận được công thức món ăn mới."
    ),
    
    "SYS175": (
        "Trên suốt chuyến hành trình, đôi khi bạn sẽ tìm thấy những loại kim loại đặc biệt.\r\n\r\n"
        "Bằng cách kết hợp những kim loại này với vũ khí của bạn, bạn có thể gia tăng các chỉ số tấn công và phòng thủ của chúng. Bạn có thể thực hiện việc này ngay từ menu Vũ Khí.\r\n\r\n"
        "Càng tiến xa trong game, bạn cũng sẽ có thể mua thêm những kim loại quý này tại các thương gia và tiệm vũ khí."
    ),
    
    "SYS176": (
        "Nếu một nhân vật trang bị bùa hộ mệnh Talisman có dòng thưởng Flux, hiệu ứng Biến Chuyển Flux đôi khi sẽ ngẫu nhiên xuất hiện khi nhân vật đó sử dụng kỹ năng hoặc liên chiêu ở chế độ Xung Lực (Momentum). Điều này cho phép bạn cường hóa pháp thạch Spritnite tương ứng bằng cách khắc thêm các thuộc tính 'Flux' vào viên đá.\r\n\r\n"
        "Có rất nhiều loại thưởng Flux khác nhau: tăng uy lực kỹ năng, giảm lượng MP tiêu hao, nạp sẵn thanh ATB sau khi hành động, và nhiều hiệu ứng khác. Loại thưởng nhận được sẽ phụ thuộc vào bùa hộ mệnh mà bạn đang trang bị.\r\n\r\n"
        "Khi Biến Chuyển Flux xuất hiện trong trận đấu, các thuộc tính nhận được sẽ hiển thị trên màn hình sau khi trận chiến kết thúc. Bạn có thể chọn có khắc các thuộc tính này vào pháp thạch Spritnite hay không để tùy biến sức mạnh theo ý thích."
    ),
    
    "SYS177": (
        "Bên cạnh Pháp Thạch Mệnh Lệnh (Command Spritnite), Biến Chuyển Flux đôi khi cũng xuất hiện trên Pháp Thạch Hỗ Trợ (Support Spritnite).\r\n\r\n"
        "Nếu một nhân vật trang bị bùa hộ mệnh có dòng thưởng 'Thưởng Hỗ Trợ' (Support Bonus), đồng thời trang bị nhiều hơn một Pháp Thạch Hỗ Trợ, hiện tượng Biến Chuyển Flux đôi khi sẽ ngẫu nhiên xuất hiện trên một trong các viên pháp thạch khi kích hoạt chế độ Xung Lực.\r\n\r\n"
        "Khi điều này xảy ra, hiệu ứng của một viên Pháp Thạch Hỗ Trợ sẽ được khắc ghép sang viên đá kia. Tuy nhiên, hiệu ứng ghép thêm này sẽ chỉ mang 1/10 sức mạnh gốc của nó."
    ),
    
    "SYS178": (
        "Khi bạn di chuyển lại gần quái vật trong một khoảng cách nhất định, trận chiến sẽ bắt đầu.\r\n\r\n"
        "Nếu bạn tiếp cận quái vật từ phía trước, chúng sẽ vào thế phòng thủ sẵn sàng. Tuy nhiên, nếu bạn lén tiếp cận chúng từ phía sau lưng, chúng sẽ bị bất ngờ sơ hở. Khi đó, bạn sẽ bắt đầu trận chiến với thanh ATB và thanh SP được nạp đầy 100%, cho phép tung ra đòn tấn công phủ đầu chớp nhoáng.\r\n\r\n"
        "Cả hai thanh ATB và SP đều đóng vai trò sống còn trong chiến đấu, và sẽ được giải thích chi tiết ở các phần tiếp theo."
    ),
    
    "SYS179": (
        "Khi trận chiến bắt đầu, thanh đo ATB (Active Time Battle) của các nhân vật hiển thị ở góc dưới màn hình sẽ bắt đầu nạp dần. Khi thanh ATB của một nhân vật đầy, bảng lệnh chiến đấu của nhân vật đó sẽ xuất hiện. Hãy chọn một mệnh lệnh (Tấn công, Kỹ năng, Vật phẩm) và mục tiêu, nhân vật sẽ thực hiện hành động đó ngay lập tức.\r\n\r\n"
        "Khi có nhiều hơn một nhân vật đầy thanh ATB, bạn có thể nhấn phím điều hướng trái/phải hoặc gạt cần analog trái sang hai bên để chuyển đổi giữa các nhân vật.\r\n\r\n"
        "Dù không hiển thị trên màn hình, quái vật cũng sở hữu thanh đo ATB riêng và sẽ ra đòn ngay khi thanh của chúng đầy."
    ),
    
    "SYS180": (
        "Spritnite là những viên đá chứa đầy ma lực huyền bí. Trang bị chúng cho phép các nhân vật sở hữu vô vàn sức mạnh đặc biệt.\r\n\r\n"
        "Có hai loại pháp thạch: Pháp Thạch Mệnh Lệnh cho phép nhân vật sử dụng các kỹ năng khác nhau trong trận chiến và từ menu Kỹ Năng; trong khi Pháp Thạch Hỗ Trợ mang lại các hiệu ứng bổ trợ tự động kích hoạt trong suốt trận chiến.\r\n\r\n"
        "Pháp thạch có thể được trang bị từ menu chính. Thao tác này được thực hiện bằng cách khảm chúng vào các 'ô chứa' (slots) trên bùa hộ mệnh Talisman. Ban đầu nhân vật chỉ có 1 ô chứa, nhưng sẽ mở thêm nhiều ô hơn khi thăng cấp và khi trang bị các loại bùa hộ mệnh cao cấp khác nhau. Có ba loại ô chứa: ô dành riêng cho Pháp Thạch Mệnh Lệnh, ô dành riêng cho Pháp Thạch Hỗ Trợ, và ô đa năng có thể khảm bất kỳ loại pháp thạch nào."
    ),
    
    "SYS181": (
        "Khi thanh ATB của nhân vật đã đầy nhưng bạn chưa chọn mệnh lệnh, thanh đo SP (Special Power) hình tròn ở bên phải sẽ bắt đầu được tích lũy. Thanh này cũng sẽ được nạp khi nhân vật thực hiện hành động hoặc phải chịu sát thương. Khi đầy, thanh sẽ nhấp nháy phát sáng và một điểm SP màu vàng sẽ xuất hiện ở trên đỉnh. Sau đó thanh đo sẽ được thiết lập lại và bắt đầu tích lũy tiếp từ dưới lên. Số điểm SP tối đa có thể tích lũy là 3 điểm.\r\n\r\n"
        "Khi nhân vật có ít nhất 1 điểm SP, bạn có thể kích hoạt 'Chế độ Xung Lực' (Momentum mode) để bổ sung thêm nhiều hiệu ứng uy lực cho các đòn đánh và kỹ năng. Ngay khoảnh khắc nhân vật chuẩn bị ra đòn, một vệt sáng sẽ bừng lên trên đầu họ; nhấn phím <ICON_SQUARE> <BUTTON> (phím H trên bàn phím) đúng vào thời khắc đó sẽ kích hoạt Chế độ Xung Lực."
    ),
    
    "SYS182": (
        "Kích hoạt Chế độ Xung Lực sẽ bổ sung thêm nhiều hiệu ứng uy lực đặc biệt cho các kỹ năng và liên chiêu combo của bạn.\r\n\r\n"
        "Kích hoạt khi tấn công sẽ gây thêm sát thương phụ, chắc chắn gây đòn chí mạng, hoặc áp đặt trạng thái bất lợi lên kẻ địch. Kích hoạt khi dùng kỹ năng trị thương hoặc hỗ trợ sẽ hồi thêm HP/MP, mở rộng phạm vi tác dụng, hoặc kéo dài thời gian duy trì của bùa lợi.\r\n\r\n"
        "Trong trận chiến, các phần thưởng đặc biệt ảnh hưởng lên toàn đội đôi khi cũng ngẫu nhiên xuất hiện. Hiện tượng này được gọi là 'Điểm Dị Thường' (Singularity). Có rất nhiều loại dị thường khác nhau và xuất hiện ngẫu nhiên. Càng sử dụng chế độ Xung Lực nhiều lần, tỉ lệ kích hoạt Điểm Dị Thường càng cao. Trong các trận đánh boss kéo dài, hãy tận dụng chế độ Xung Lực càng nhiều càng tốt!"
    ),
    
    "SYS183": (
        "Điểm Lưu Game (Save Points) là những quầng sáng ma thuật xuất hiện trên các bản đồ khu vực, cho phép bạn ghi lại tiến trình chơi game hiện tại. Nếu bước vào trong quầng sáng này và nhấn phím <ICON_CIRCLE> <BUTTON>, bạn sẽ được hỏi có muốn lưu game hay không. Ngoài ra, bạn cũng có thể mở menu chính khi đang đứng trong quầng sáng và chọn mục Lưu Game.\r\n\r\n"
        "Điểm Lưu Game chỉ xuất hiện ở một số vị trí nhất định trong các khu vực. Tuy nhiên, khi ở trên Bản Đồ Thế Giới (World Map), bạn sẽ có thể lưu tiến trình chơi bất cứ lúc nào trực tiếp từ menu chính.\r\n\r\n"
        "Xin lưu ý rằng trò chơi này không tự động lưu game (No Auto-Save). Hãy luôn chủ động lưu game thường xuyên để đảm bảo hành trình của bạn luôn an toàn và thuận lợi."
    ),
}

def main():
    p_path = r"D:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\SystemMessage"
    with open(p_path, "rb") as f:
        encrypted_raw = f.read()

    dec = bytearray(decrypt_data(encrypted_raw))
    print(f"Decrypted SystemMessage: {len(dec)} bytes.")

    num_records = struct.unpack("<h", dec[2:4])[0]
    print(f"Records count: {num_records}")

    offset = 4
    new_data = bytearray()
    new_data.extend(dec[:4])

    updated_count = 0

    for i in range(num_records):
        id_bytes = dec[offset:offset+8]
        msg_id = id_bytes.split(b"\x00")[0].decode("ascii", errors="ignore")
        str_size = struct.unpack("<h", dec[offset+8:offset+10])[0]
        offset += 10

        # Read 3 languages: 0: JP, 1: EN, 2: FR
        jp_len = struct.unpack("<h", dec[offset:offset+2])[0]; offset += 2
        jp_bytes = dec[offset:offset+jp_len]; offset += jp_len

        en_len = struct.unpack("<h", dec[offset:offset+2])[0]; offset += 2
        en_bytes = dec[offset:offset+en_len]; offset += en_len

        fr_len = struct.unpack("<h", dec[offset:offset+2])[0]; offset += 2
        fr_bytes = dec[offset:offset+fr_len]; offset += fr_len

        # Check if we have translation for EN slot (game loads EN slot for English setting)
        if msg_id in TUTORIAL_TRANSLATIONS:
            vn_text = TUTORIAL_TRANSLATIONS[msg_id]
            new_en_bytes = vn_text.encode("utf-16le")
            new_en_len = len(new_en_bytes)
            updated_count += 1
        else:
            new_en_bytes = en_bytes
            new_en_len = en_len

        # Recalculate record
        # In header: MessageData struct is (id [8 bytes], stringSize [2 bytes])
        # Write MessageData
        new_data.extend(id_bytes)
        new_data.extend(struct.pack("<h", str_size))

        # Write JP
        new_data.extend(struct.pack("<h", jp_len))
        new_data.extend(jp_bytes)

        # Write EN (Vietnamese translation)
        new_data.extend(struct.pack("<h", new_en_len))
        new_data.extend(new_en_bytes)

        # Write FR
        new_data.extend(struct.pack("<h", fr_len))
        new_data.extend(fr_bytes)

    print(f"Updated {updated_count} tutorial entries!")
    print(f"New raw decrypted size: {len(new_data)} bytes.")

    # Save decrypted backup
    with open(p_path + ".dec", "wb") as f:
        f.write(new_data)

    # Pad to 16 bytes for AES
    pad_len = 16 - (len(new_data) % 16)
    if pad_len < 16:
        new_data.extend(b"\x00" * pad_len)

    encrypted = encrypt_data(bytes(new_data))
    with open(p_path, "wb") as f:
        f.write(encrypted)
    print(f"Encrypted and saved ({len(encrypted)} bytes) to {p_path}")

    # Also update in patch folder
    patch_p = r"D:\Viet Hoa Game\Setsuna_VietHoa_Patch\SETSUNA_Data\StreamingAssets\data\parameter\SystemMessage"
    os.makedirs(os.path.dirname(patch_p), exist_ok=True)
    with open(patch_p, "wb") as f:
        f.write(encrypted)
    with open(patch_p + ".dec", "wb") as f:
        f.write(new_data)
    print("Updated patch folder with new SystemMessage!")

if __name__ == "__main__":
    main()
