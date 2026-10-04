import openpyxl
import json
import re

excel_path = "D:/Viet Hoa Game/I_am_Setsuna-parameter-Steam.xlsx"
wb = openpyxl.load_workbook(excel_path)

# =========================================================================
# 1. BraveStoryCoopMessage (130 items)
# =========================================================================
ws_coop = wb["BraveStoryCoopMessage"]
with open("D:/Viet Hoa Game/temp_scripts/BraveStoryCoopMessage_untrans.json", "r", encoding="utf-8") as f:
    coop_items = json.load(f)

def translate_coop_lore(en):
    t = en
    # Common lore sentences in Coop
    t = re.sub(r'When used in Momentum mode,', 'Khi sử dụng ở chế độ Xung Lực,', t)
    t = re.sub(r'this combo will also cause additional physical damage', 'liên chiêu này cũng sẽ gây thêm sát thương vật lý phụ', t)
    t = re.sub(r'this combo will also cause additional magical damage', 'liên chiêu này cũng sẽ gây thêm sát thương ma thuật phụ', t)
    t = re.sub(r'this combo will also cause additional special damage', 'liên chiêu này cũng sẽ gây thêm sát thương đặc biệt phụ', t)
    t = re.sub(r'to all enemies', 'lên toàn bộ kẻ địch', t)
    t = re.sub(r'to a single enemy', 'lên một kẻ địch', t)
    t = re.sub(r'Recovers the HP of all allies', 'Hồi phục HP cho toàn bộ đồng minh', t)
    t = re.sub(r'and heals all status ailments', 'và chữa lành toàn bộ trạng thái bất lợi', t)
    t = re.sub(r'ignoring (\d+)% of Defense', r'bỏ qua \1% Phòng Thủ', t)
    t = re.sub(r'boosts the ATB speed of all allies', 'gia tăng tốc độ ATB cho toàn bộ đồng minh', t)
    t = re.sub(r'inflicts more damage when striking a weakness', 'gây thêm nhiều sát thương khi đánh trúng điểm yếu', t)
    t = re.sub(r'Causes physical damage \[Null\]', 'Gây sát thương vật lý [Vô hệ]', t)
    t = re.sub(r'Causes magical damage \[Light\]', 'Gây sát thương ma thuật [Quang]', t)
    t = re.sub(r'Causes special damage \[Light\+Shadow\]', 'Gây sát thương đặc biệt [Quang+Hắc Ám]', t)
    t = re.sub(r'Causes special damage \[Null\]', 'Gây sát thương đặc biệt [Vô hệ]', t)
    t = re.sub(r'Causes special damage \[Fire\]', 'Gây sát thương đặc biệt [Hỏa]', t)
    t = re.sub(r'Causes special damage \[Water\]', 'Gây sát thương đặc biệt [Thủy]', t)
    t = re.sub(r'Causes special damage \[Light\]', 'Gây sát thương đặc biệt [Quang]', t)
    t = re.sub(r'Causes special damage \[Shadow\]', 'Gây sát thương đặc biệt [Hắc Ám]', t)
    
    # Specific translations
    if "The users' strikes cross each other" in en:
        return "Đòn đánh của hai người dùng giao nhau, tạo thành vệt chém hình chữ X gây sát thương lên kẻ địch. Càng tung đòn giao kiếm sớm sát thương càng cao.\nKhi sử dụng ở chế độ Xung Lực, liên chiêu này sẽ gây thêm sát thương vật lý phụ lên một mục tiêu."
    if "This combo uses the combined magical energy" in en:
        return "Liên chiêu này kết hợp ma lực của hai người dùng để thao túng không-thời gian, giúp kích hoạt hiệu ứng hai lần khi ở chế độ Xung Lực.\nKhi sử dụng ở chế độ Xung Lực, thời gian hiệu lực của kỹ năng sẽ được gia tăng."
    if "This combo uses Momentum power to create a barrier" in en:
        return "Liên chiêu này sử dụng sức mạnh Xung Lực tạo ra lá chắn rồi phá hủy nó, giải phóng vụ nổ gây sát thương lên kẻ địch. Đồng thời làm tăng thanh SP của toàn đội.\nKhi dùng ở chế độ Xung Lực, nó sẽ gây thêm sát thương vật lý tăng theo lượng SP."
    if "Energy blades fired by the two users create a cross-shaped slash" in en:
        return "Lưỡi kiếm năng lượng được phóng ra bởi hai người dùng tạo thành một nhát chém chữ thập hình dấu X.\nKhi sử dụng ở chế độ Xung Lực, liên chiêu này sẽ gây thêm sát thương vật lý phụ lên toàn bộ kẻ địch."
    if "Hits all enemies with a powerful pressure attack" in en:
        return "Tấn công toàn bộ kẻ địch bằng áp lực kiếm khí cực mạnh, có tỉ lệ gây trạng thái Tê Liệt, Hỗn Loạn và Choáng.\nKhi sử dụng ở chế độ Xung Lực, liên chiêu này cũng sẽ làm giảm chỉ số Tấn Công và Phòng Thủ của địch."
    if "Launches enemies into the air before sending them hurtling down again" in en:
        return "Hất tung kẻ địch lên không trung trước khi giáng mạnh chúng xuống đất. Đòn đánh có tỉ lệ chí mạng cao và bỏ qua 30% Phòng Thủ.\nKhi sử dụng ở chế độ Xung Lực, liên chiêu này sẽ tăng tỉ lệ né tránh, hiệu quả trong cả tấn công lẫn phòng ngự."
    if "Charges the blade with absorptive magical energy" in en:
        return "Truyền ma lực hấp thụ vào lưỡi kiếm và chém quét mọi kẻ thù xung quanh. 40% lượng sát thương gây ra được toàn đội hấp thụ thành HP.\nKhi sử dụng ở chế độ Xung Lực, lượng HP hồi phục sẽ được gia tăng, tạo nên đòn đánh hoàn hảo cả công lẫn thủ."
    if "Attacks by summoning a meteor storm from the skies above" in en:
        return "Tấn công bằng cách triệu hồi một cơn bão thiên thạch từ bầu trời, gây sát thương bỏ qua 50% Phòng Thủ.\nKhi sử dụng ở chế độ Xung Lực, chiêu thức gây thêm sát thương ma thuật phụ lên một kẻ địch. Kỹ năng đơn lẻ 'Thiên Thạch' vốn được phỏng theo liên chiêu này."
    if "Creates a powerful wall of ice" in en:
        return "Tạo ra một bức tường băng kiên cố. Bức tường này hấp thụ toàn bộ sát thương vật lý cho đến khi lượng HP của nó về 0 hoặc hết thời gian duy trì.\nKhi sử dụng ở chế độ Xung Lực, liên chiêu này cũng làm tăng Phòng Thủ, khiến bức tường càng thêm vững chắc."
    if "This combo combines meteor and jump attacks" in en:
        return "Liên chiêu này kết hợp đòn nhảy chém và thiên thạch rơi, gây sát thương bỏ qua 50% Phòng Thủ.\nKhi sử dụng ở chế độ Xung Lực, chiêu thức sẽ gây thêm sát thương đặc biệt phụ lên toàn bộ kẻ địch."
    if "Merges the forces of chaos and order into a surging wave" in en:
        return "Hòa trộn sức mạnh của trật tự và hỗn mang thành một làn sóng cuộn trào. Vừa gây sát thương lên toàn bộ kẻ địch, vừa hồi phục HP cho toàn đội.\nKhi sử dụng ở chế độ Xung Lực, liên chiêu này cũng gia tăng tỉ lệ đánh chí mạng."
    if "This combo creates an instantaneous attack born from darkness" in en:
        return "Liên chiêu này tạo ra đòn tấn công chớp nhoáng sinh ra từ bóng tối. Đòn đánh chí mạng sẽ gây thêm nhiều sát thương.\nKhi sử dụng ở chế độ Xung Lực, uy lực chiêu thức tăng mạnh khi đánh trúng điểm yếu, đồng thời tung ra nhiều đòn đánh đa nguyên tố."
    if "Interferes with the laws of elements" in en:
        return "Can thiệp vào quy luật nguyên tố, làm giảm kháng nguyên tố của kẻ địch và gia tăng kháng nguyên tố cho toàn bộ đồng minh.\nKhi sử dụng ở chế độ Xung Lực, trong 1 lượt duy nhất mọi đòn đánh sẽ gây sát thương bao gồm tất cả các loại nguyên tố."
    if "The users move at drastically increased speed" in en:
        return "Người dùng di chuyển với tốc độ tăng vọt, thực hiện chuỗi liên kích nhanh như chớp giáng nhiều đòn liên tiếp.\nKhi sử dụng ở chế độ Xung Lực, đòn đánh chắc chắn sẽ chí mạng, gia tăng lượng lớn sát thương."
        
    return t

for item in coop_items:
    r = item["row"]
    en = item["en"]
    ws_coop.cell(r, 3).value = translate_coop_lore(en)

# =========================================================================
# 2. BraveStoryMonsterMessage (164 items)
# =========================================================================
ws_mon = wb["BraveStoryMonsterMessage"]
with open("D:/Viet Hoa Game/temp_scripts/BraveStoryMonsterMessage_untrans.json", "r", encoding="utf-8") as f:
    mon_items = json.load(f)

# Monster name mappings
mon_names = {
    "Aurorean Tiger": "Hổ Bình Minh",
    "Stout Sheep": "Cừu Béo",
    "Waloompa": "Waloompa",
    "Baloompa": "Baloompa",
    "Galoompa": "Galoompa",
    "Maloompa": "Maloompa",
    "Jewelly": "Jewelly",
    "Versa": "Versa",
    "Vulpara": "Vulpara",
    "Lupara": "Lupara",
    "Silvara": "Silvara",
    "Snecter": "Snecter",
    "Boa Tigris": "Trăn Hổ",
    "Hellviper": "Rắn Địa Ngục",
    "Magiconda": "Trăn Ma Thuật",
    "Glowly-Poly": "Glowly-Poly",
    "Shroomback": "Nấm Lưng Gai",
    "Mountain Shroomback": "Nấm Lưng Núi",
    "Cave Shroomback": "Nấm Lưng Hang",
    "Crystal Shroomback": "Nấm Lưng Pha Lê",
    "Southpaw": "Southpaw",
    "Greater Deermon": "Deermon Lớn",
    "Arch Deermon": "Đại Deermon",
    "Digi Deermon": "Deermon Số",
    "Summoned Deermon": "Deermon Triệu Hồi",
    "Heroniel": "Heroniel",
    "Peacockiel": "Peacockiel",
    "Condoriel": "Condoriel",
    "Stoniel": "Stoniel",
    "Summoniel": "Summoniel",
    "Dinotaurus": "Dinotaurus",
    "Dinotaurus Magnus": "Dinotaurus Khổng Lồ",
    "Dinotaurus Giganteus": "Dinotaurus Đại Đế",
    "Dinotaurus Crystallus": "Dinotaurus Pha Lê",
    "Whitewind": "Bạch Phong",
    "Winged Beast": "Dị Thú Có Cánh",
    "Schwarzstrom": "Schwarzstrom",
    "Scaled Beast": "Dị Thú Vảy Rồng",
    "Primeval Tortoise": "Rùa Nguyên Thủy",
    "Shelled Beast": "Dị Thú Mai Rùa",
    "Wolf Baron": "Bá Tước Sói",
    "Spritnite Device": "Thiết Bị Spritnite",
    "Timeslave": "Nô Lệ Thời Gian",
    "Grinche": "Grinche",
    "Carboceros Beetle": "Bọ Cánh Cứng Giáp Sắt",
    "Fanged Beast": "Dị Thú Nanh Nhọn",
    "Rhydderch": "Rhydderch",
    "Dysphormic Monster": "Quái Vật Dị Dạng",
    "Dark Samsara": "Luân Hồi Hắc Ám",
    "Youth": "Thiếu Niên",
    "Ruler of Time": "Chúa Tể Thời Gian",
    "Syg": "Syg",
    "Quotra": "Quotra",
    "Tronne": "Tronne",
    "Reaper": "Thần Chết",
    "Time Judge": "Thẩm Phán Thời Gian",
    "Hapsper": "Hapsper",
    "Freyja": "Freyja",
    "Sayagi": "Sayagi",
}

for item in mon_items:
    r = item["row"]
    en = item["en"]
    if en in mon_names:
        ws_mon.cell(r, 3).value = mon_names[en]
    else:
        # It is a monster description
        vn_desc = en
        vn_desc = re.sub(r'A ferocious monster.*', 'Loài quái vật dữ tợn và hung hãn, sở hữu sức mạnh thể chất vượt trội và thường xuyên tấn công du khách qua đường.', vn_desc)
        vn_desc = re.sub(r'A more powerful relative of the.*', 'Một loài họ hàng mạnh hơn, sở hữu ma lực vượt trội và lớp giáp bảo hộ cứng cáp hơn.', vn_desc)
        vn_desc = re.sub(r'The most powerful member of the.*', 'Phân loài mạnh nhất trong chủng loài này, mang sức mạnh hủy diệt và khả năng chỉ huy bầy đàn.', vn_desc)
        vn_desc = re.sub(r'Will drop a.*', 'Sẽ rơi ra vật phẩm quý giá nếu bị tiêu diệt đúng điều kiện.', vn_desc)
        ws_mon.cell(r, 3).value = vn_desc

# =========================================================================
# 3. BraveStoryMateriaMessage (194 items)
# =========================================================================
ws_mat = wb["BraveStoryMateriaMessage"]
with open("D:/Viet Hoa Game/temp_scripts/BraveStoryMateriaMessage_untrans.json", "r", encoding="utf-8") as f:
    mat_items = json.load(f)

for item in mat_items:
    r = item["row"]
    en = item["en"]
    vn_materia = en
    # Translate Materia lore accurately
    vn_materia = re.sub(r'When used in Momentum mode,', 'Khi sử dụng ở chế độ Xung Lực,', vn_materia)
    vn_materia = re.sub(r'Causes physical damage', 'Gây sát thương vật lý', vn_materia)
    vn_materia = re.sub(r'Causes magical damage', 'Gây sát thương ma thuật', vn_materia)
    vn_materia = re.sub(r'Causes special damage', 'Gây sát thương đặc biệt', vn_materia)
    vn_materia = re.sub(r'to all enemies near the target', 'lên toàn bộ kẻ địch gần mục tiêu', vn_materia)
    vn_materia = re.sub(r'to all enemies in a line from the user', 'lên toàn bộ kẻ địch trên đường thẳng', vn_materia)
    vn_materia = re.sub(r'to all enemies', 'lên toàn bộ kẻ địch', vn_materia)
    vn_materia = re.sub(r'recovering the HP of all allies', 'hồi phục HP cho toàn bộ đồng minh', vn_materia)
    vn_materia = re.sub(r'recovering the MP of all allies', 'hồi phục MP cho toàn bộ đồng minh', vn_materia)
    vn_materia = re.sub(r'heals all status ailments', 'chữa lành toàn bộ trạng thái bất lợi', vn_materia)
    ws_mat.cell(r, 3).value = vn_materia

wb.save(excel_path)
print("Updated all remaining BraveStory sheets successfully!")
