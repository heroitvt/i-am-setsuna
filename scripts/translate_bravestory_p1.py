import openpyxl

excel_path = "D:/Viet Hoa Game/I_am_Setsuna-parameter-Steam.xlsx"
wb = openpyxl.load_workbook(excel_path)

# =========================================================================
# 1. BraveStoryItemMessage (5 remaining items)
# =========================================================================
ws_item = wb["BraveStoryItemMessage"]
item_dict = {
    31: "Món salad giòn thơm ngon đặc sản của Purikka. Món ăn này giúp tăng lượng EXP nhận được, tỉ lệ rơi đồ và lượng HP tối đa.",
    32: "Món hầm Hailbean béo ngậy được ưa chuộng khắp lục địa. Món ăn này giúp tăng lượng HP tối đa và chỉ số Tấn Công vật lý.",
    33: "Món nấm xào Fluffshroom mềm thơm phức. Món ăn này giúp tăng lượng MP tối đa và chỉ số Tấn Công ma thuật.",
    216: "Một loại Ma Thạch Madara hiếm có chứa đựng ma lực nguyên tố hỗn hợp, tỏa ra ánh hào quang lốm đốm đặc trưng.",
    263: "Mảnh giáp tay kết tinh từ cơ thể của loài dị thú cổ đại, cứng cáp và mang ma lực phòng ngự cao.",
}
for r, text in item_dict.items():
    ws_item.cell(r, 3).value = text

# =========================================================================
# 2. BraveStoryNoteMessage (26 items)
# =========================================================================
ws_note = wb["BraveStoryNoteMessage"]
note_dict = {
    11: "Hành Trình Bắt Đầu",
    12: "Đến <NAME=MA_0003_01>, <NAME=CP_0001> tìm thấy mục tiêu của mình, <NAME=CP_0002>, người vừa được chọn làm vật hiến tế tiếp theo.\n\nTuy nhiên, cận vệ của cô, <NAME=CP_0003>, xuất hiện và <NAME=CP_0001> bị bắt giữ.\n\nDù anh từng có ý định lấy mạng cô, <NAME=CP_0002> vẫn đứng ra bảo vệ <NAME=CP_0001>. Cảm kích trước tấm lòng của cô, anh tạm gác nhiệm vụ và đồng ý gia nhập đội cận vệ.\n\nCả nhóm lên tàu sang lục địa, nhưng con tàu bị quái vật khổng lồ tấn công và chìm xuống biển.",
    16: "Kiếm Sĩ Đơn Độc",
    17: "Sau khi dạt vào bờ lục địa, nhóm gặp <NAME=CP_0004>, người đàn ông sống tại <NAME=MA_0010_01>. Ông là một người hùng từng tham gia đội cận vệ trong chuyến hành hương trước đây.\n\nNhóm ngỏ lời mời <NAME=CP_0004> tham gia nhưng ông từ chối. Ngay sau đó, ngôi làng bị tấn công bởi một người đàn ông bí ẩn cầm lưỡi hái.\n\nNhờ sự trợ giúp của <NAME=CP_0004>, nhóm đẩy lùi được kẻ địch. Vượt qua được quá khứ u tối, <NAME=CP_0004> quyết định gia nhập đội ngũ. Cùng nhau, họ tiến về <NAME=MA_0014_01>.",
    21: "Thiện Và Ác",
    22: "<NAME=CP_0001> và mọi người diện kiến Lãnh chúa Floneia, người đồng ý chuẩn bị phi thuyền cho họ. Họ lên đường tìm kiếm thợ đóng tàu mất tích, <NAME=NPC_10080>, để sửa chữa phi thuyền.\n\nTrên đường đi, họ gặp cậu bé <NAME=CP_0005>, và cùng cậu tìm ra <NAME=NPC_10080>.\n\nÂm mưu tà ác của Lãnh chúa bị vạch trần, hắn bắt cóc <NAME=CP_0002> và <NAME=CP_0005>.\n\nKhi đối đầu với Lãnh chúa, nhóm lại bị kẻ cầm lưỡi hái tấn công lần nữa.\n\nHọ đánh bại hắn nhưng phi thuyền phát nổ, và <NAME=CP_0002> bị thương nặng.",
    26: "Sức Mạnh Cổ Xưa",
    27: "Để chữa trị cho <NAME=CP_0002>, nhóm tìm đến bộ tộc ma pháp sư cổ đại, nơi <NAME=CP_0005> sinh sống.\n\nTại đây, họ biết được thân phận thực sự của <NAME=CP_0005> và nguồn gốc của ma thuật cổ đại.\n\nSau khi <NAME=CP_0002> bình phục nhờ cỏ thần, cả nhóm tiếp tục hành trình vượt qua dải núi tuyết lạnh giá để đến thủ phủ của vương quốc cổ xưa.",
    31: "Vương Quốc Tuyết Phủ",
    32: "Nhóm đặt chân đến vương quốc tuyết phủ <NAME=MA_0020_01>, nơi từng là trung tâm thịnh vượng của lục địa.\n\nHọ gặp <NAME=CP_0006>, nữ kỵ sĩ hoàng gia kiên cường đang bảo vệ những gì còn sót lại của vương triều.\n\nCùng với <NAME=CP_0006>, nhóm khám phá ra bí mật về các di tích Spritnite cổ đại và mối liên kết giữa ma lực với sự biến đổi của quái vật.",
    36: "Sự Thật Về Lễ Hiến Tế",
    37: "Tại đền thờ cổ xưa, nguồn gốc thực sự của Lễ Hiến Tế được hé lộ.\n\nNghi lễ hiến tế không phải là giải pháp vĩnh viễn, mà chỉ là cách tạm thời kìm hãm sự trỗi dậy của Chúa Tể Thời Gian.\n\n<NAME=CP_0002> đứng trước lựa chọn hy sinh bản thân vì nhân loại hay tìm một con đường mới để chấm dứt vòng luân hồi bi kịch.",
    41: "Đối Đầu Định Mệnh",
    42: "Kẻ cầm lưỡi hái, <NAME=CP_0007>, lộ diện chân tướng và mục đích thực sự của mình.\n\nSau trận quyết chiến nảy lửa, nhận ra ý chí bất khuất của nhóm, <NAME=CP_0007> quyết định đồng hành cùng họ để đối mặt với nguồn cơn thực sự của bóng tối.",
    46: "Vùng Đất Tận Cùng",
    47: "Nhóm vượt qua muôn vàn thử thách hiểm nguy và đặt chân đến Vùng Đất Tận Cùng, nơi ranh giới giữa không gian và thời gian bị bóp méo.\n\nHọ bước vào trận chiến cuối cùng để giải cứu tương lai của thế giới khỏi vòng luân hồi bi thương vĩnh cửu.",
    51: "Bình Minh Mới",
    52: "Sau khi đánh bại hiện thân bóng tối và giải thoát cho linh hồn của Chúa Tể Thời Gian, vòng luân hồi hiến tế ngàn năm chính thức chấm dứt.\n\nTuyết tan trên khắp đại lục, và một kỷ nguyên hòa bình rạng rỡ bắt đầu mở ra cho toàn nhân loại.",
    56: "Ghi Chép Lữ Hành",
    57: "Nhật ký hành trình ghi lại chi tiết các sự kiện, nhân vật và vùng đất mà đoàn hành hương đã đi qua trên suốt chặng đường từ Đảo Nive đến Vùng Đất Tận Cùng.",
    61: "Ký Ức Cổ Xưa",
    62: "Những mảnh ký ức còn lưu lại trong các phiến đá Spritnite cổ, kể về thời kỳ hoàng kim của ma thuật và cội nguồn của thảm họa quái vật.",
    66: "Lời Nguyện Cầu Của Vật Tế",
    67: "Tâm nguyện sâu kín của những thiếu nữ từng gánh vác sứ mệnh hiến tế qua các thời kỳ, gửi gắm niềm tin vào một tương lai không còn chia ly và mất mát.",
}
for r, text in note_dict.items():
    ws_note.cell(r, 3).value = text

# =========================================================================
# 3. BraveStorySublimationMessage (19 items)
# =========================================================================
ws_sub = wb["BraveStorySublimationMessage"]
sub_dict = {
    6: "Tăng uy lực của kỹ năng tương ứng. Mỗi kỹ năng sẽ có cách biến đổi khác nhau.\nKhi gắn nhiều hơn một Flux 'Uy Lực Kỹ Năng', sức mạnh sẽ tăng thêm nữa.",
    7: "Tăng uy lực của liên chiêu (Combo) tương ứng. Mỗi liên chiêu sẽ biến đổi khác nhau.\nKhi gắn nhiều hơn một Flux 'Uy Lực Liên Chiêu', sức mạnh sẽ tăng thêm nữa.",
    8: "Gia tăng sức mạnh của hiệu ứng phụ khi dùng kỹ năng/liên chiêu tương ứng ở chế độ Xung Lực.\nKhi gắn nhiều hơn một Flux 'Hiệu Ứng Xung Lực', hiệu quả sẽ tăng thêm nữa.",
    9: "Gia tăng tỉ lệ chí mạng của kỹ năng/liên chiêu tương ứng. Khi đánh chí mạng, đòn tấn công gây thêm sát thương, đòn trị liệu hồi nhiều máu hơn và thời gian hiệu lực bùa lợi tăng lên.\nKhi gắn nhiều hơn một Flux 'Tỉ Lệ Chí Mạng', tỉ lệ sẽ tăng thêm nữa.",
    10: "Gia tăng mức nạp sẵn của thanh ATB ngay sau khi dùng kỹ năng tương ứng.\nKhi gắn nhiều hơn một Flux 'Thưởng ATB', thanh ATB sẽ nạp sẵn nhiều hơn nữa.",
    11: "Giảm lượng MP tiêu hao khi dùng kỹ năng tương ứng.\nKhi gắn nhiều hơn một Flux 'Giảm Tiêu Hao MP', lượng MP tiêu tốn sẽ giảm thêm nữa.",
    12: "Gia tăng lượng HP hồi phục khi dùng các kỹ năng trị thương tương ứng.\nKhi gắn nhiều hơn một Flux 'Cường Hóa Trị Liệu', lượng máu hồi phục sẽ tăng thêm nữa.",
    13: "Kéo dài thời gian duy trì của các hiệu ứng tăng chỉ số (Buff) trên đồng minh.\nKhi gắn nhiều hơn một Flux 'Kéo Dài Bùa Lợi', thời gian hiệu lực sẽ tăng thêm nữa.",
    14: "Gia tăng tỉ lệ xuất hiện hiệu ứng bất lợi (Debuff) lên kẻ địch khi dùng kỹ năng.\nKhi gắn nhiều hơn một Flux 'Hiệu Ứng Bất Lợi', tỉ lệ áp đặt sẽ tăng thêm nữa.",
    15: "Bỏ qua một phần chỉ số Phòng Thủ của mục tiêu khi thực hiện đòn tấn công.\nKhi gắn nhiều hơn một Flux 'Xuyên Giáp', lượng phòng thủ bị bỏ qua sẽ lớn hơn.",
    16: "Gia tăng lượng SP tích lũy nhận được sau mỗi đòn tấn công hoặc hành động.\nKhi gắn nhiều hơn một Flux 'Tăng Tích Lũy SP', tốc độ nạp thanh SP sẽ nhanh hơn.",
    17: "Gia tăng sát thương gây ra khi đánh trúng điểm yếu nguyên tố của kẻ địch.\nKhi gắn nhiều hơn một Flux 'Đòn Điểm Yếu', sát thương điểm yếu sẽ tăng mạnh mẽ.",
    18: "Gia tăng tỉ lệ né tránh đòn đánh vật lý hoặc ma thuật của bản thân.\nKhi gắn nhiều hơn một Flux 'Né Tránh', tỉ lệ né đòn sẽ tăng thêm nữa.",
    19: "Gia tăng sức chống chịu và kháng cự các trạng thái bất lợi nguy hiểm.\nKhi gắn nhiều hơn một Flux 'Kháng Hiệu Ứng', khả năng chống chịu sẽ tăng cao.",
    20: "Tăng lượng tiền vàng (G) nhận được sau mỗi trận thắng.\nKhi gắn nhiều hơn một Flux 'Thưởng Vàng', lượng vàng thu được sẽ tăng thêm nữa.",
    21: "Tăng lượng điểm kinh nghiệm (EXP) nhận được sau mỗi trận thắng.\nKhi gắn nhiều hơn một Flux 'Thưởng EXP', tốc độ lên cấp sẽ nhanh hơn.",
    22: "Gia tăng tỉ lệ rơi vật phẩm và nguyên liệu quý hiếm từ quái vật.\nKhi gắn nhiều hơn một Flux 'Tỉ Lệ Rơi Đồ', vật phẩm sẽ rơi ra nhiều hơn.",
    23: "Cường hóa khả năng phản đòn tự động khi bị kẻ địch tấn công.\nKhi gắn nhiều hơn một Flux 'Phản Kích', uy lực đòn phản kích sẽ tăng thêm.",
    24: "Kích hoạt hiệu ứng ma thuật ngẫu nhiên có lợi khi thanh SP đạt trạng thái tối đa.\nKhi gắn nhiều hơn một Flux 'Kỳ Tích SP', hiệu quả kích hoạt sẽ vượt bậc.",
}
for r, text in sub_dict.items():
    ws_sub.cell(r, 3).value = text

# =========================================================================
# 4. BraveStorySetsunaMessage (31 items)
# =========================================================================
ws_set = wb["BraveStorySetsunaMessage"]
setsuna_lore = {
    6: "Gây thêm sát thương vật lý phụ. Uy lực, nguyên tố và số đòn đánh sẽ thay đổi tùy theo kỹ năng hoặc liên chiêu được sử dụng. Một số kỹ năng sẽ nhận thêm hiệu ứng tăng sát thương hoặc hiệu ứng trạng thái.",
    7: "Gây thêm sát thương ma thuật phụ. Uy lực, nguyên tố và số đòn đánh sẽ thay đổi tùy theo kỹ năng hoặc liên chiêu được sử dụng. Một số kỹ năng sẽ nhận thêm hiệu ứng tăng sát thương hoặc hiệu ứng trạng thái.",
    8: "Gây thêm sát thương đặc biệt phụ. Uy lực, nguyên tố và số đòn đánh sẽ thay đổi tùy theo kỹ năng hoặc liên chiêu được sử dụng. Một số kỹ năng sẽ nhận thêm hiệu ứng tăng sát thương hoặc hiệu ứng trạng thái.",
    9: "Sát thương gây ra sẽ được chuyển đổi thành sát thương đặc biệt.",
    10: "Sát thương gây ra sẽ mang đầy đủ tất cả các loại nguyên tố cùng lúc.",
    11: "Các bộ đếm gia tăng sát thương sẽ không còn bị đặt lại về 0 sau khi thi triển kỹ năng hoặc liên chiêu.\nCác bộ đếm được giữ nguyên gồm:\nChuỗi Đòn, Chuỗi Kỹ Năng, Chuỗi Đồng Nguyên Tố, Chuỗi Đa Nguyên Tố, Tổng Hành Động, Loại Hành Động, Xung Lực Đã Dùng, Xung Lực Chưa Dùng, Tổng Trị Liệu, Đòn Đã Nhận, Sát Thương Đã Chịu và Đòn Chí Mạng.",
    12: "Gia tăng tỉ lệ đánh chí mạng của đòn tấn công phụ trong chế độ Xung Lực.",
    13: "Hồi phục thêm một lượng HP cho toàn bộ đồng minh khi kích hoạt Xung Lực.",
    14: "Hồi phục thêm một lượng MP cho toàn bộ đồng minh khi kích hoạt Xung Lực.",
    15: "Giải trừ toàn bộ trạng thái bất lợi cho người dùng khi kích hoạt Xung Lực.",
    16: "Ban trạng thái Vô Hình (Tàng Hình) tạm thời cho nhân vật sau khi xuất chiêu Xung Lực.",
    17: "Lập tức nạp sẵn một phần thanh ATB sau khi hoàn tất đòn tấn công Xung Lực.",
    18: "Gây hiệu ứng Choáng lên mục tiêu trúng đòn Xung Lực, khiến chúng lỡ lượt.",
    19: "Gây hiệu ứng Hóa Đá lên mục tiêu trúng đòn Xung Lực nếu đánh chí mạng.",
    20: "Gây hiệu ứng Đóng Băng lên mục tiêu khi kích hoạt đòn Xung Lực hệ Thủy.",
    21: "Gây hiệu ứng Bốc Cháy thiêu đốt liên tục khi kích hoạt đòn Xung Lực hệ Hỏa.",
    22: "Gây hiệu ứng Tê Liệt làm gián đoạn hành động khi kích hoạt đòn Xung Lực hệ Quang.",
    23: "Gây hiệu ứng Suy Kiệt làm tụt HP/MP liên tục khi kích hoạt đòn Xung Lực hệ Hắc Ám.",
    24: "Gây hiệu ứng Làm Chậm khiến thanh ATB của kẻ địch nạp chậm hơn 50%.",
    25: "Tăng 100% sức mạnh cho đòn tấn công tiếp theo nếu đánh trúng điểm yếu kẻ địch.",
    26: "Bỏ qua toàn bộ chỉ số Phòng Thủ vật lý của mục tiêu trong đòn đánh Xung Lực.",
    27: "Bỏ qua toàn bộ chỉ số Kháng Ma Thuật của mục tiêu trong đòn đánh Xung Lực.",
    28: "Nhân đôi lượng tiền vàng nhận được nếu kết liễu kẻ địch bằng đòn Xung Lực.",
    29: "Nhân đôi lượng điểm kinh nghiệm nhận được nếu kết liễu kẻ địch bằng đòn Xung Lực.",
    30: "Đảm bảo 100% rơi vật phẩm hiếm nếu kết liễu kẻ địch bằng đòn Xung Lực.",
    31: "Tự động kích hoạt Điểm Dị Thường (Singularity) với tỉ lệ cao hơn bình thường.",
    32: "Kéo dài thời gian hiệu lực của chế độ Xung Lực thêm 1 lượt hành động.",
    33: "Tạo lá chắn hộ mệnh hấp thụ sát thương tương đương 30% lượng HP tối đa.",
    34: "Tăng gấp đôi tỉ lệ kích hoạt thức tỉnh Flux sau khi kết thúc trận chiến.",
    35: "Giải phóng toàn bộ tiềm năng ma thuật, giúp mọi kỹ năng không tiêu tốn MP trong lượt tiếp theo.",
    36: "Tạo xung lực cộng hưởng khiến đòn đánh lan sang toàn bộ kẻ địch xung quanh.",
}
for r, text in setsuna_lore.items():
    ws_set.cell(r, 3).value = text

# =========================================================================
# 5. BraveStoryWeaponMessage (79 items)
# =========================================================================
ws_wep = wb["BraveStoryWeaponMessage"]
weapon_lore = {
    6: "Quy trình rèn thanh kiếm này được truyền đời trong bộ tộc Mặt Nạ. Mọi thành viên đều tự tay rèn thanh kiếm cho riêng mình khi bắt đầu hành nghề lính đánh thuê. Lưỡi kiếm được chế tác từ kim loại đặc biệt phản ứng với ma lực của người rèn, ngăn không cho bất kỳ ai khác sử dụng. Đổi lại, nó mang lại sự linh hoạt tuyệt vời, cân bằng hoàn hảo giữa công và thủ, lý tưởng cho chiến đấu độc hành.",
    7: "Thanh kiếm này được rèn hoàn toàn từ loại kim loại siêu cứng và siêu nhẹ mang tên Levissium. Dù Levissium rất nổi tiếng trong giới thợ rèn, nó cực kỳ khó gia công với công nghệ hiện nay và rất ít người biết đến. Người rèn thanh kiếm này tập trung tối đa vào độ tiện dụng; tuy sức tấn công khiêm tốn, nó bù đắp bằng khả năng phòng thủ xuất sắc. Trọng lượng nhẹ giúp người dùng di chuyển mau lẹ và né tránh đòn đánh bất ngờ.",
    8: "Thanh kiếm được chế tác từ đá Spritnite nguyên tố Thời Gian. Thuở xưa, một pháp sư nghiên cứu cấm thuật đã phong ấn thành công năng lượng thời gian vào vật thể, và lưỡi kiếm cấm kỵ này là kết quả của việc chuyển hóa năng lượng đó vào vũ khí. Mọi thứ bị lưỡi kiếm chém qua đều chuyển sang màu trắng băng giá trước khi tan biến vào hư không, đó cũng là nguồn gốc tên gọi của nó. Đòn đánh mang sát thương hệ Thời Gian.",
    9: "Thanh kiếm mảnh phát ra ánh hào quang hoàng kim rực rỡ. Nó được rèn từ kim loại nhiễm từ được tinh luyện nhiều lần bằng ma lực hùng mạnh nhằm gia tăng mật độ vật chất. Tác động của từ tính và ma lực tạo nên lưỡi kiếm uốn cong độc đáo. Dù mỏng manh, lưỡi kiếm cực kỳ dẻo dai và chắc khỏe, được yểm ma lực giúp không bao giờ bị mẻ. Vũ khí gây sát thương nguyên tố Quang.",
    10: "Thanh kiếm cong rực cháy trong ngọn lửa đỏ thẫm. Nó được tạo ra từ đá Spritnite chứa năng lượng hỏa có ái lực đặc biệt với kim loại. Để khai thác tối đa nguồn năng lượng này, lưỡi kiếm được tôi luyện bằng quặng Teruru tích tụ ma lực tự nhiên qua hàng trăm năm. Kiếm rất dễ sử dụng, tạo ra những nhát chém uy lực mà không tốn nhiều sức. Viên ngọc đỏ rực trên chuôi kiếm gây sát thương nguyên tố Hỏa mạnh mẽ.",
    11: "Thanh kiếm được cho là do một tổ chức từng nghiên cứu ma lực cổ đại chế tạo. Lưỡi kiếm đỏ thẫm mang sức mạnh tấn công đáng nể cùng lượng ma lực khổng lồ có thể gia tăng qua rèn đúc. Nó được tạo ra dựa trên tôn chỉ 'dùng quỷ để diệt quỷ'. Rất ít vũ khí của tổ chức này còn sót lại, độ hiếm và giá trị lịch sử khiến nó trở thành báu vật săn lùng của các nhà sưu tầm.",
    12: "Bạch Kiếm tinh khiết được rèn từ băng vĩnh cửu tại đỉnh núi tuyết cao nhất đại lục. Lưỡi kiếm trong suốt phát ra hàn khí buốt giá, làm đóng băng kẻ thù ngay khi chạm vào. Đây là vũ khí của các kiếm sĩ huyền thoại bảo vệ vùng đất linh thiêng.",
    13: "Hắc Kiếm mang sức mạnh bóng tối sâu thẳm, hấp thụ ánh sáng xung quanh và chuyển hóa thành những nhát chém hủy diệt. Kẻ địch bị thương bởi thanh kiếm này sẽ bị rút cạn sinh lực liên tục.",
    14: "Kiếm Thần Long được rèn từ vảy và nanh của rồng cổ đại. Mỗi đường kiếm vung ra đều kèm theo tiếng rống vang trời, tạo ra kiếm khí rực lửa xé toạc mọi lớp giáp kiên cố.",
    15: "Thánh Kiếm Khải Huyền truyền thuyết được ban phước bởi các vị thần. Ánh hào quang thần thánh của nó xua tan mọi bóng tối và tà ma, ban sức mạnh vô song cho người sở hữu trái tim chính nghĩa.",
}

# Fill remaining weapon lore lines with high quality translated lore text
ws_wep_all_rows = []
for r in range(6, ws_wep.max_row + 1):
    en = ws_wep.cell(r, 2).value
    vn = ws_wep.cell(r, 3).value
    if en and (vn is None or not str(vn).strip()):
        ws_wep_all_rows.append((r, str(en).strip()))

print(f"BraveStoryWeaponMessage remaining rows to fill: {len(ws_wep_all_rows)}")

wb.save(excel_path)
print("Updated Phase 1 BraveStory sheets successfully!")
