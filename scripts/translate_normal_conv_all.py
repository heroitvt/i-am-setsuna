import json
import re

with open("D:/Viet Hoa Game/temp_scripts/normal_conv_all.json", "r", encoding="utf-8") as f:
    all_data = json.load(f)

print(f"Total entries: {len(all_data)}")

# Rule formatter: Max 2 lines per page, <= 30 chars per line, using | for pages
def format_page_lines(text):
    # Splits pages
    pages = text.split("|")
    clean_pages = []
    for p in pages:
        p = p.strip()
        if not p: continue
        # Split into words
        words = p.replace("\n", " ").split()
        lines = []
        cur_line = []
        for w in words:
            test_line = " ".join(cur_line + [w])
            if len(test_line) <= 30:
                cur_line.append(w)
            else:
                if cur_line:
                    lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))
        
        # If more than 2 lines, split into multiple pages of max 2 lines
        for i in range(0, len(lines), 2):
            sub_page = "\n".join(lines[i:i+2])
            clean_pages.append(sub_page)
    return "\n|\n".join(clean_pages)

# Translate dictionary
trans_map = {}

# Sample pattern rules for NPC talk loop
for item in all_data:
    rid = item["rid"]
    en = item["en"]
    jp = item.get("jp", "")
    
    # Check if already translated
    has_vn = any(c in en for c in "áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ")
    if has_vn:
        trans_map[rid] = en
        continue

    # Translation logic
    t = en
    # Common NPC greetings & dialogs
    if "It's not often anyone comes here" in t:
        t = "Hiếm khi có ai từ đại lục\nđến hòn đảo này...\n|\nThực ra hôm nay có buổi lễ\nkhởi hành đấy.\n|\nHả? Khởi hành của ai á?\nCủa vật hiến tế chứ ai!"
    elif "What is it? If you're looking for the\nferry" in t:
        t = "Chuyện gì thế? Nếu tìm phà\nthì nó đã rời bến rồi.\n|\nDù sao cũng lỡ đến đây rồi,\ncứ ở lại xem lễ khởi hành đi."
    elif "Hold on a minute... How'd you get\nback here" in t:
        t = "Khoan đã... Làm sao các cậu\nvề đây được mà không cần thuyền?\n|\nCái gì? Bằng phi thuyền á?\nĐừng có đùa tôi chứ..."
    elif "You wanna get to the village?" in t:
        t = "Cậu muốn đến ngôi làng sao?\n|\nSau khi rời cảng, cứ đi về\nhướng tây bắc là sẽ thấy thôi."
    elif "Sorry, there won't be anudda ferry" in t:
        t = "Xin lỗi, chuyến phà tiếp theo\nphải lâu nữa mới tới...\n|\nChuyến tới sẽ đưa cô bé\nvật hiến tế lên đường."
    elif "Very few people travel to this\nisland" in t:
        t = "Dạo này rất ít người đến đảo,\nquái vật dạo này lộng hành quá..."
    elif "The next ferry that'll be arriving\nwill sail to the citadel" in t:
        t = "Chuyến phà tiếp theo cập bến\nsẽ đưa mọi người đến thành trì."
    elif "I never thought we'd be seeing off\nlittle <NAME=CP_0002>" in t:
        t = "Tôi chưa từng nghĩ sẽ có ngày\ntiễn biệt bé <NAME=CP_0002> thế này..."
    elif "Aha! I see you've got a recipe." in t:
        t = "A ha! Tôi thấy cậu có công thức nấu ăn.\n|\nNếu đưa cho tôi, tôi sẽ nấu\ncho cậu món ăn tuyệt hảo!"
    elif "Let me see, what have we got here" in t:
        t = "Để tôi xem nào...\nTuyệt vời! Tôi nấu xong rồi đây!"
    elif "Oh? That's a shame..." in t:
        t = "Ôi, tiếc thật đấy...\nKhi nào đổi ý hãy báo tôi nhé!"
    elif "No matter how many times I do it,\nseeing off the sacrifice" in t:
        t = "Dù đã chứng kiến bao nhiêu lần,\ntiễn biệt vật tế vẫn đau lòng quá..."
    elif "Sorry, but we're still getting ready\nto open." in t:
        t = "Xin lỗi, quán đang chuẩn bị.\nChúng tôi mở cửa sớm thôi!"
    elif "We're about to hold the departure\nceremony" in t:
        t = "Chúng tôi chuẩn bị cử hành\nlễ tiễn biệt cho <NAME=CP_0002>."
    else:
        # Translate general sentences
        t = re.sub(r"Welcome to the village of sacrifice\.", "Chào mừng đến với Làng Hiến Tế.", t)
        t = re.sub(r"The sacrifice will save the world\.", "Vật hiến tế sẽ cứu lấy thế giới này.", t)
        t = re.sub(r"Please protect <NAME=CP_0002>\.", "Xin hãy bảo vệ <NAME=CP_0002>.", t)
        t = re.sub(r"Good luck on your journey!", "Chúc may mắn trên chuyến hành trình!", t)
        t = re.sub(r"May the blessings of the earth be with you\.", "Cầu mong phước lành đất mẹ luôn bên bạn.", t)
        t = re.sub(r"The monsters are getting more dangerous\.", "Quái vật dạo này ngày càng nguy hiểm.", t)
        t = re.sub(r"I hope the pilgrimage succeeds\.", "Hy vọng chuyến hành hương sẽ thành công.", t)
        # Apply formatting
        t = format_page_lines(t)
        
    trans_map[rid] = t

print(f"Mapped {len(trans_map)} translations.")
with open("D:/Viet Hoa Game/temp_scripts/normal_conv_translated.json", "w", encoding="utf-8") as f:
    json.dump(trans_map, f, ensure_ascii=False, indent=2)
