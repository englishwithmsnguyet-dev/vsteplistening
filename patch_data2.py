import json
import re

vocab_p2 = [
    [
        "sidewalk /ˈsaɪdwɔːk/ (n): vỉa hè, lối đi bộ",
        "do exercises /duː ˈeksərsaɪzɪz/ (v.phr): tập thể dục",
        "handrail /ˈhændreɪl/ (n): tay vịn",
        "stand to the right /stænd tuː ðə raɪt/ (v.phr): đứng về phía bên phải"
    ],
    [
        "audience /ˈɔːdiəns/ (n): khán giả",
        "moderator /ˈmɑːdəreɪtər/ (n): người điều hành, người chủ trì",
        "speech /spiːtʃ/ (n): bài phát biểu",
        "submit /səbˈmɪt/ (v): nộp, gửi",
        "written /ˈrɪtn/ (adj): bằng văn bản"
    ],
    [
        "product /ˈprɑːdʌkt/ (n): sản phẩm",
        "catalog /ˈkætəlɔːɡ/ (n): danh mục sản phẩm",
        "over the telephone /ˈoʊvər ðə ˈtelɪfoʊn/ (exp): qua điện thoại"
    ],
    [
        "business district /ˈbɪznəs ˈdɪstrɪkt/ (n): khu thương mại",
        "route /ruːt/ (n): tuyến đường",
        "subway /ˈsʌbweɪ/ (n): tàu điện ngầm"
    ],
    [
        "build /bɪld/ (v): xây dựng"
    ],
    [
        "weather /ˈweðər/ (n): thời tiết",
        "weekend /ˈwiːkend/ (n): cuối tuần",
        "sunny /ˈsʌni/ (adj): có nắng",
        "windy /ˈwɪndi/ (adj): có gió",
        "rainy /ˈreɪni/ (adj): có mưa",
        "snowy /ˈsnoʊi/ (adj): có tuyết"
    ],
    [
        "announcement /əˈnaʊnsmənt/ (n): thông báo",
        "ticket sales /ˈtɪkɪt seɪlz/ (n): việc bán vé",
        "observation window /ˌɑːbzərˈveɪʃn ˈwɪndoʊ/ (n): cửa sổ quan sát",
        "station stop /ˈsteɪʃn stɑːp/ (n): điểm dừng ở nhà ga"
    ],
    [
        "repair service /rɪˈper ˈsɜːrvɪs/ (n): dịch vụ sửa chữa",
        "politeness /pəˈlaɪtnəs/ (n): sự lịch sự",
        "location /loʊˈkeɪʃn/ (n): vị trí",
        "advertisement /ˌædvərˈtaɪzmənt/ (n): quảng cáo"
    ]
]

vocab_p3 = [
    [
        "hold a position /hoʊld ə pəˈzɪʃn/ (v.phr): giữ chức vụ",
        "current /ˈkɜːrənt/ (adj): hiện tại"
    ],
    [
        "open /ˈoʊpən/ (adj/v): mở cửa",
        "weekday /ˈwiːkdeɪ/ (n): ngày trong tuần (thứ 2 - thứ 6)",
        "weekend /ˈwiːkend/ (n): cuối tuần (thứ 7, CN)"
    ],
    [
        "section /ˈsekʃn/ (n): khu vực, phần",
        "library /ˈlaɪbreri/ (n): thư viện",
        "medical emergency /ˈmedɪkl ɪˈmɜːrdʒənsi/ (n): trường hợp khẩn cấp về y tế",
        "maintenance problem /ˈmeɪntənəns ˈprɑːbləm/ (n): vấn đề bảo trì",
        "annual meeting /ˈænjuəl ˈmiːtɪŋ/ (n): cuộc họp thường niên"
    ],
    [
        "specially discounted /ˈspeʃəli dɪsˈkaʊntɪd/ (adj): được giảm giá đặc biệt",
        "flashlight /ˈflæʃlaɪt/ (n): đèn pin",
        "battery /ˈbætəri/ (n): pin",
        "smoke detector /smoʊk dɪˈtektər/ (n): máy báo khói"
    ],
    [
        "hourly /ˈaʊərli/ (adj/adv): hàng giờ",
        "victim /ˈvɪktɪm/ (n): nạn nhân",
        "tornado /tɔːrˈneɪdoʊ/ (n): lốc xoáy",
        "natural disaster /ˈnætʃrəl dɪˈzæstər/ (n): thảm họa thiên nhiên",
        "warning /ˈwɔːrnɪŋ/ (n): lời cảnh báo"
    ],
    [
        "intended for /ɪnˈtendɪd fɔːr/ (adj): dành cho (ai)",
        "employee /ɪmˈplɔɪiː/ (n): nhân viên",
        "tow truck owner /toʊ trʌk ˈoʊnər/ (n): chủ xe cứu hộ"
    ],
    [
        "trip /trɪp/ (n): chuyến đi",
        "around /əˈraʊnd/ (prep/adv): khoảng chừng"
    ],
    [
        "available /əˈveɪləbl/ (adj): có sẵn",
        "vegetable /ˈvedʒtəbl/ (n): rau củ"
    ]
]

vocab_p4 = [
    [
        "heaviest /ˈheviɪst/ (adj): nặng nhất",
        "rainfall /ˈreɪnfɔːl/ (n): lượng mưa",
        "mainland /ˈmeɪnlænd/ (n): đất liền"
    ],
    [
        "in case of /ɪn keɪs əv/ (exp): trong trường hợp",
        "property office /ˈprɑːpərti ˈɔːfɪs/ (n): văn phòng tài sản",
        "make a statement /meɪk ə ˈsteɪtmənt/ (v.phr): đưa ra lời khai",
        "immediately /ɪˈmiːdiətli/ (adv): ngay lập tức"
    ],
    [
        "delay /dɪˈleɪ/ (v): trì hoãn",
        "unwell /ʌnˈwel/ (adj): không khỏe",
        "break down /breɪk daʊn/ (v.phr): bị hỏng"
    ],
    [
        "stolen /ˈstoʊlən/ (adj): bị đánh cắp",
        "burglary /ˈbɜːrɡləri/ (n): vụ trộm",
        "statue /ˈstætʃuː/ (n): bức tượng",
        "jewel /ˈdʒuːəl/ (n): viên ngọc",
        "antique /ænˈtiːk/ (n): đồ cổ"
    ],
    [
        "instruction /ɪnˈstrʌkʃn/ (n): lời hướng dẫn",
        "hazard lights /ˈhæzərd laɪts/ (n): đèn cảnh báo nguy hiểm",
        "flat tire /flæt ˈtaɪər/ (n): lốp xịt hơi"
    ],
    [
        "prize /praɪz/ (n): giải thưởng",
        "holiday /ˈhɑːlədeɪ/ (n): kỳ nghỉ"
    ],
    [
        "cost /kɔːst/ (v): có giá trị, tốn (tiền)"
    ],
    [
        "leave /liːv/ (v): rời đi"
    ]
]

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

def patch_practice(pid, vocab_list, content):
    start_idx = content.find(f'"id": "{pid}"')
    if start_idx == -1: return content
    
    end_idx = content.find('"id": "p1_practice_', start_idx + 100)
    if end_idx == -1: end_idx = content.find('"id": "p2_', start_idx + 100)
    
    section = content[start_idx:end_idx]
    
    question_blocks = []
    for m in re.finditer(r'"number":\s*\d+,', section):
        question_blocks.append(m.start())
        
    out_section = section
    for i in range(min(len(question_blocks), len(vocab_list))):
        q_num = i + 1
        vocab_json = json.dumps(vocab_list[i], ensure_ascii=False)
        pattern = rf'("number":\s*{q_num},\s*.*?)(?=\n\s*"options")'
        
        def replacer(match):
            return match.group(1) + f'\n            "vocabulary": {vocab_json},'
            
        out_section = re.sub(pattern, replacer, out_section, flags=re.DOTALL)
        
    return content[:start_idx] + out_section + content[end_idx:]

content = patch_practice('p1_practice_02', vocab_p2, content)
content = patch_practice('p1_practice_03', vocab_p3, content)
content = patch_practice('p1_practice_04', vocab_p4, content)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched Practice 02, 03, 04 successfully.")
