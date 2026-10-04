import json

subquest_trans = {
    '9706_{\"NpcNm\":\"NPC_21020\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":0,\"NpcId\":0,\"QuestId\":0}}':
        'Aha!\nNgươi là <NAME=CP_0001> của bộ tộc\nmặt nạ, phải không nào!\n|\nTa có một bức thư gửi cho ngươi đây!',
    '9707_{\"NpcNm\":\"CP_0005\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":1,\"NpcId\":0,\"QuestId\":0}}':
        'Thư gửi cho <NAME=CP_0001> ư!?\nTừ ai vậy?',
    '9708_{\"NpcNm\":\"CP_0004\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":2,\"NpcId\":0,\"QuestId\":0}}':
        'Này! Nhóc con đang làm cái gì thế hả!?\nSao lại tự tiện đọc thư của người khác như vậy!',
    '9709_{\"NpcNm\":\"CP_0004\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":3,\"NpcId\":0,\"QuestId\":0}}':
        'Thế... trong thư viết gì vậy?',
    '9710_{\"NpcNm\":\"CP_0003\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":4,\"NpcId\":0,\"QuestId\":0}}':
        '*Thở dài*...',
    '9711_{\"NpcNm\":\"\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":5,\"NpcId\":0,\"QuestId\":0}}':
        'Ta để lại vật này cho ngươi vì tin rằng\nngươi có đủ năng lực để phát huy sức mạnh của nó.',
    '9712_{\"NpcNm\":\"\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":6,\"NpcId\":0,\"QuestId\":0}}':
        'Có thể ngươi đã biết, trên vùng đất này\ncó ba bệ thờ trọng yếu.\n|\nNgười ta tương truyền rằng nếu ngươi giơ viên\npháp thạch này trước những bệ thờ đó, ngươi\nsẽ nhận được sự dẫn lối cho tương lai.',
    '9713_{\"NpcNm\":\"\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":7,\"NpcId\":0,\"QuestId\":0}}':
        'Đầu tiên, hãy đến bệ thờ ở <NAME=MA_0009_01>.\n|\nTiếp theo là bệ thờ trên <NAME=MA_0021_01>.\n|\nVà cuối cùng là bệ thờ tại <NAME=MA_0100_01>.\n|\nHãy ghi nhớ kỹ thứ tự này.',
    '9714_{\"NpcNm\":\"\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":8,\"NpcId\":0,\"QuestId\":0}}':
        'Khi cần một lời chỉ dẫn cho con đường tương lai,\nhãy nhớ lại nội dung bức thư này.',
    '9715_{\"NpcNm\":\"\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":9,\"NpcId\":0,\"QuestId\":0}}':
        'Ta hy vọng trí tuệ của người xưa sẽ tiếp thêm\nsức mạnh và soi rọi ánh sáng dẫn lối cho ngươi.',
    '9716_{\"NpcNm\":\"\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":10,\"NpcId\":0,\"QuestId\":0}}':
        'Bạn nhận được <NAME=ITEM_EVT_027>.',
    '9717_{\"NpcNm\":\"CP_0005\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":11,\"NpcId\":0,\"QuestId\":0}}':
        'Gì cơ...? Ai gửi thế này?\nNgười quen của anh hả, <NAME=CP_0001>?',
    '9718_{\"NpcNm\":\"\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":12,\"NpcId\":0,\"QuestId\":0}}':
        'Ta nghĩ ta biết là ai rồi.',
    '9719_{\"NpcNm\":\"\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":13,\"NpcId\":0,\"QuestId\":0}}':
        'Chắc chỉ là trò đùa thôi.',
    '9720_{\"NpcNm\":\"CP_0005\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":14,\"NpcId\":0,\"QuestId\":0}}':
        'Thế rốt cuộc là ai?\nPhụ nữ hay đàn ông?',
    '9721_{\"NpcNm\":\"CP_0004\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":15,\"NpcId\":0,\"QuestId\":0}}':
        'Nghe giọng văn này thì không giống\nphụ nữ viết chút nào, đúng không...',
    '9722_{\"NpcNm\":\"CP_0003\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":16,\"NpcId\":0,\"QuestId\":0}}':
        '*Thở dài*...',
    '9723_{\"NpcNm\":\"CP_0005\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":17,\"NpcId\":0,\"QuestId\":0}}':
        'Ừ, chắc đúng vậy rồi...',
    '9724_{\"NpcNm\":\"CP_0002\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":18,\"NpcId\":0,\"QuestId\":0}}':
        'Anh có chắc là mình không vô tình quên ai\nđó không, <NAME=CP_0001>?\n|\nĐọc bức thư này thì rõ ràng người đó rất\nhiểu về anh mà.',
    '9725_{\"NpcNm\":\"CP_0003\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":19,\"NpcId\":0,\"QuestId\":0}}':
        'Cả cô cũng hùa theo nữa sao, <NAME=CP_0002>...',
    '9726_{\"NpcNm\":\"CP_0004\",\"QuestNm\":\"SUB_QUEST_0001\",\"Head\":{\"Type\":0,\"Id\":20,\"NpcId\":0,\"QuestId\":0}}':
        'Mọi người nghĩ chúng ta có thể thực sự tin bức\nthư này sao? Chúng ta có nhiệm vụ lớn phải làm...\n|\nChẳng lẽ lại mạo hiểm tính mạng chỉ vì thứ viết\ntrong một lá thư đáng ngờ ư?\n|\nThôi được rồi, địa điểm đầu tiên nói đến là\n<NAME=MA_0009_01>...\n|\nQuyết định thế nào là ở cậu, nhưng nếu đến đó,\nnhất định phải hết sức đề phòng.'
}

conv_trans = {
    '9347_{\"NpcNm\":\"NPC_21010\",\"QuestNm\":\"s_talkLoop\",\"Head\":{\"Type\":0,\"Id\":5265,\"NpcId\":0,\"QuestId\":0}}':
        'Hiếm khi thấy có người từ đại lục tới đây.\nThường thì người ta chỉ rời khỏi đây thôi...\n|\nThực ra hôm nay có buổi lễ khởi hành đấy.\n|\nHả? Khởi hành của ai á?\nCủa vật hiến tế chứ ai!'
}

with open('translation_export/SubQuestMessageData.json', 'r', encoding='utf-8') as f:
    sq_data = json.load(f)
for item in sq_data:
    if item['id'] in subquest_trans:
        item['vietnamese'] = subquest_trans[item['id']]
with open('translation_export/SubQuestMessageData.json', 'w', encoding='utf-8') as f:
    json.dump(sq_data, f, ensure_ascii=False, indent=2)

with open('translation_export/ScenarioMessageData_NormalConv.json', 'r', encoding='utf-8') as f:
    nc_data = json.load(f)
for item in nc_data:
    if item['id'] in conv_trans:
        item['vietnamese'] = conv_trans[item['id']]
with open('translation_export/ScenarioMessageData_NormalConv.json', 'w', encoding='utf-8') as f:
    json.dump(nc_data, f, ensure_ascii=False, indent=2)

print('Updated SubQuestMessageData and ScenarioMessageData_NormalConv JSON!')
