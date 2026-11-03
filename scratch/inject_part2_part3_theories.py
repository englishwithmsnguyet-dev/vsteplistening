# -*- coding: utf-8 -*-
import json
import re

part2_theory = {
    "title": "CHIẾN LƯỢC & LÝ THUYẾT: PART 02 - LONG CONVERSATIONS (HỘI THOẠI DÀI)",
    "overview": {
        "desc": "PART 02 của bài thi VSTEP LISTENING đánh giá khả năng <mark class=\"hl-primary\">nghe hiểu các cuộc hội thoại dài</mark> giữa 2 người nói trong nhiều bối cảnh quen thuộc của học tập, công việc và đời sống hằng ngày. Mỗi đoạn hội thoại kéo dài từ <mark class=\"hl-keyword\">02 đến 03 phút</mark> và đi kèm <mark class=\"hl-accent\">04 câu hỏi trắc nghiệm A-B-C-D</mark>.",
        "core_skills": [
            "Nhận diện ý chính và mục đích của cuộc trò chuyện",
            "Xác định chi tiết quan trọng: thời gian, địa điểm, vấn đề phát sinh, giải pháp",
            "Hiểu mạch phát triển của cuộc hội thoại và sự chuyển đổi giữa các nội dung thảo luận",
            "Suy luận thái độ, quan điểm, hàm ý từ ngữ điệu hoặc cách diễn đạt của người nói"
        ],
        "contexts": [
            {
                "title": "Tư vấn học vụ & Học đường",
                "icon": "🎓",
                "detail": "Trao đổi giữa sinh viên và cố vấn học tập, giải đáp thắc mắc với giảng viên, đăng ký tín chỉ, lịch thi, bảo lưu..."
            },
            {
                "title": "Thảo luận công việc & Văn phòng",
                "icon": "💼",
                "detail": "Trao đổi giữa đồng nghiệp, giữa nhân viên với khách hàng, thảo luận dự án, phân công nhiệm vụ, xử lý thủ tục hành chính..."
            },
            {
                "title": "Tình huống dịch vụ công cộng",
                "icon": "🛎️",
                "detail": "Giao dịch tại ngân hàng, nhà sách, phòng khám, cửa hàng mua sắm, bến xe, sân bay, nhà hàng, khách sạn..."
            },
            {
                "title": "Giao tiếp sinh hoạt hằng ngày",
                "icon": "☕",
                "detail": "Hỏi thăm thông tin, sắp xếp lịch hẹn, nhờ vả hỗ trợ, thảo luận kế hoạch cá nhân, thuê nhà ở..."
            }
        ]
    },
    "question_types": {
        "desc": "Các dạng câu hỏi trong PART 02 có hình thức tương tự PART 01 nhưng mang tính tương tác cao hơn:",
        "highlight": "Trong PART 02, <strong>dạng câu hỏi chi tiết (Detail) là chủ đạo</strong>, vì các đoạn hội thoại thường chứa rất nhiều dữ kiện cụ thể liên quan đến hành động, mốc thời gian, địa điểm, vấn đề gặp phải hoặc giải pháp khắc phục.",
        "patterns": [
            "What are the speakers mainly discussing? (Chủ đề chính)",
            "What problem does the woman / man mention? (Vấn đề phát sinh)",
            "Where does the conversation most likely take place? (Địa điểm)",
            "What does the man suggest the woman do? (Giải pháp / Lời khuyên)",
            "What will the speakers probably do next? (Hành động tiếp theo)"
        ]
    },
    "strategies": [
        {
            "step": "Bước 1: Đọc nhanh các câu hỏi & Gạch chân từ khóa",
            "badge": "01",
            "points": [
                "Tận dụng thời gian chuẩn bị trước khi audio phát để đọc lướt cả 4 câu hỏi.",
                "Gạch chân từ khóa định hướng để xác định nội dung cần tập trung và chuẩn bị tâm lý nghe đúng chỗ."
            ]
        },
        {
            "step": "Bước 2: Tập trung vào các thông tin cụ thể",
            "badge": "02",
            "points": [
                "Đặc biệt lắng nghe: <mark class=\"hl-primary\">thời gian, địa điểm, hành động, vấn đề, giải pháp</mark>.",
                "Luyện phản xạ với các cụm từ diễn đạt chi tiết: <em>The reason is that…, He plans to…, It happened at…</em>"
            ]
        },
        {
            "step": "Bước 3: Nghe bám sát theo trình tự câu hỏi",
            "badge": "03",
            "points": [
                "Các đáp án trong PART 02 <mark class=\"hl-success\">thường xuất hiện tuần tự theo thứ tự câu hỏi</mark> từ câu 1 đến câu 4.",
                "Khi người nói đã chuyển sang nội dung mới, hãy quyết định ngay và chuyển sự chú ý sang câu hỏi tiếp theo, không quay lại lưu luyến nội dung cũ."
            ]
        },
        {
            "step": "Bước 4: Chọn theo dữ kiện thực tế, không suy đoán chủ quan",
            "badge": "04",
            "points": [
                "Chỉ chọn đáp án dựa trên đúng thông tin được nghe từ miệng nhân vật.",
                "Tránh chọn những phương án nghe có vẻ 'hợp lý trong đời thực' nhưng hoàn toàn không xuất hiện trong bài nghe."
            ]
        }
    ],
    "common_mistakes": [
        {
            "title": "Không đọc trước câu hỏi và từ khóa",
            "impact": "Khiến người nghe rơi vào thế bị động, dễ bị choáng ngợp và bỏ lỡ các điểm mốc thông tin quan trọng."
        },
        {
            "title": "Chỉ nghe ý chính, bỏ qua các chi tiết nhỏ",
            "impact": "Trong PART 02, chi tiết cụ thể mới là yếu tố then chốt để quyết định đáp án đúng cho phần lớn câu hỏi."
        },
        {
            "title": "Bị phân tâm bởi thông tin gây nhiễu (Bẫy ban đầu)",
            "impact": "Nhiều đoạn hội thoại cố tình đưa ra thông tin lệch/thay đổi ban đầu (ví dụ: định đi xe buýt nhưng sau đó đổi sang đi tàu) để đánh lừa thí sinh chọn quá vội."
        },
        {
            "title": "Nghe xong mới chọn đáp án, không quyết định ngay",
            "impact": "Đoạn hội thoại kéo dài 2-3 phút chứa lượng thông tin lớn, nếu không đánh dấu ngay sẽ rất dễ quên khi phải trả lời liên tiếp 4 câu."
        },
        {
            "title": "Suy đoán dựa vào kiến thức cá nhân",
            "impact": "Nhiều thí sinh chọn đáp án vì thấy nó 'hợp lý theo lẽ thường' nhưng người nói trong bài lại không hề đề cập đến."
        }
    ],
    "vocabulary_topics": [
        { "name": "University", "icon": "🎓", "desc": "Từ vựng học vụ, khuôn viên, môn học, giáo sư, bài tập, tín chỉ" },
        { "name": "Jobs & Workplace", "icon": "💼", "desc": "Việc làm thêm, phỏng vấn, đồng nghiệp, hợp đồng, ca làm" },
        { "name": "Travel & Transportation", "icon": "✈️", "desc": "Đặt vé máy bay, tàu xe, du lịch, lịch trình, hành lý" },
        { "name": "Booking & Services", "icon": "📞", "desc": "Đặt bàn, dịch vụ khách hàng, khiếu nại, hỗ trợ kỹ thuật" },
        { "name": "Accommodation", "icon": "🏠", "desc": "Thuê nhà, ký túc xá, chủ nhà, hợp đồng thuê, tiện ích" },
        { "name": "Shopping & Products", "icon": "🛍️", "desc": "Mua sắm, đổi trả hàng, bảo hành, hóa đơn, hoàn tiền" },
        { "name": "Events & Activities", "icon": "🎉", "desc": "Lễ hội, buổi hòa nhạc, triển lãm, sự kiện thể thao" },
        { "name": "Medical", "icon": "🏥", "desc": "Khám bệnh, đơn thuốc, triệu chứng, bảo hiểm y tế" }
    ]
}

part3_theory = {
    "title": "CHIẾN LƯỢC & LÝ THUYẾT: PART 03 - LONG TALKS (ĐỘC THOẠI DÀI / BÀI GIẢNG HỌC THUẬT)",
    "overview": {
        "desc": "PART 03 của bài thi VSTEP LISTENING bao gồm <mark class=\"hl-primary\">03 đoạn độc thoại dài</mark>, mỗi bài nói thường kéo dài từ <mark class=\"hl-keyword\">03 đến 04 phút</mark>. Đây là phần có dung lượng nghe dài nhất trong toàn bộ bài thi, đòi hỏi thí sinh phải duy trì khả năng tập trung cao độ và kỹ năng ghi nhớ thông tin theo trình tự.",
        "core_skills": [
            "Nắm bắt được logic triển khai nội dung của bài nói (theo thứ tự thời gian, theo bước, nguyên nhân – kết quả)",
            "Phân biệt rõ ràng đâu là ý chính (main ideas) – đâu là ý phụ/ví dụ minh họa (supporting details)",
            "Lọc bỏ các thông tin mở rộng không cần thiết để không bị quá tải não bộ",
            "Ghi chú ngắn gọn (take note) có hệ thống để theo dõi diễn tiến của đoạn nói",
            "Nhận diện được các tín hiệu chuyển ý (transitions) và mối liên hệ logic giữa các phần thông tin"
        ],
        "contexts": [
            {
                "title": "Giới thiệu bảo tàng / Khu triển lãm",
                "icon": "🏛️",
                "detail": "Bài thuyết minh về các phòng trưng bày, di tích lịch sử, tác phẩm nghệ thuật, quy định tham quan..."
            },
            {
                "title": "Hướng dẫn sử dụng thiết bị hoặc quy trình",
                "icon": "⚙️",
                "detail": "Quy trình vận hành máy móc, thủ tục đăng ký, hướng dẫn an toàn lao động hoặc hướng dẫn học tập..."
            },
            {
                "title": "Hiện tượng tự nhiên, môi trường & xã hội",
                "icon": "🌱",
                "detail": "Thuyết trình về biến đổi khí hậu, bảo tồn động vật hoang dã, sự phát triển đô thị, xu hướng cộng đồng..."
            },
            {
                "title": "Khái niệm khoa học hoặc sự kiện lịch sử",
                "icon": "🔬",
                "detail": "Giải thích nguồn gốc phát minh, các lý thuyết khoa học phổ thông, mốc lịch sử quan trọng..."
            },
            {
                "title": "Bài nói của hướng dẫn viên, thông báo, diễn giả",
                "icon": "🎙️",
                "detail": "Thông báo quy chế hội nghị, bài phát biểu của giáo sư tại giảng đường đại học, hướng dẫn du lịch..."
            }
        ]
    },
    "question_types": {
        "desc": "Mỗi đoạn độc thoại đi kèm với 05 câu hỏi trắc nghiệm (tổng cộng 15 câu cho Part 3), kiểm tra toàn diện:",
        "highlight": "Các bài nói Part 3 có <strong>mức độ học thuật cao hơn, nội dung dài hơn và được tổ chức chặt chẽ hơn</strong> so với Part 1 & 2. Các chi tiết liên kết móc xích đòi hỏi thí sinh phải theo dõi mạch bài liên tục thay vì chỉ nghe bắt keyword đơn lẻ.",
        "characteristics": [
            "Thông tin được trình bày theo logic rõ ràng và hệ thống (thứ tự thời gian, các bước, nguyên nhân – kết quả...).",
            "Các chi tiết liên kết chặt chẽ, tạo thành mạch lập luận thống nhất.",
            "Một số câu hỏi yêu cầu hiểu cách tổ chức bài nói (Organization) hoặc thái độ/quan điểm của diễn giả."
        ]
    },
    "strategies": [
        {
            "step": "Bước 1: Đọc nhanh 5 câu hỏi trước khi nghe (Bắt từ khóa)",
            "badge": "01",
            "points": [
                "Tận dụng tối đa thời gian chuẩn bị để đọc lướt cả 5 câu hỏi.",
                "Gạch chân từ khóa chính của từng câu để tạo 'bản đồ định vị' trước khi bài nói bắt đầu."
            ]
        },
        {
            "step": "Bước 2: Ghi chú có hệ thống (Take Notes thông minh)",
            "badge": "02",
            "points": [
                "Ưu tiên ghi nhanh các ý chính, dấu mốc thời gian, số liệu, các bước thực hiện hoặc tên riêng.",
                "Sử dụng ký hiệu viết tắt (+, -, →, =, vs...) để bắt kịp tốc độ nói của diễn giả, tuyệt đối không chép nguyên câu."
            ]
        },
        {
            "step": "Bước 3: Bám sát các từ nối logic (Transitions)",
            "badge": "03",
            "points": [
                "Chú ý cao độ đến các từ liên kết: <em>firstly, secondly, then, in contrast, on the other hand, however, as a result, finally...</em>",
                "Các từ nối này chính là 'biển báo giao thông' chỉ ra người nói đang chuyển sang ý tiếp theo tương ứng với câu hỏi kế tiếp."
            ]
        },
        {
            "step": "Bước 4: Nắm bắt ý nghĩa tổng thể, không kẹt lại ở từ lạ",
            "badge": "04",
            "points": [
                "Khi gặp một từ vựng chuyên ngành hoặc từ mới chưa biết, đừng dừng lại suy nghĩ vì sẽ bị lỡ mất cả đoạn sau.",
                "Hãy dựa vào các từ xung quanh và ngữ cảnh chung để phán đoán ý nghĩa."
            ]
        },
        {
            "step": "Bước 5: Áp dụng kỹ thuật loại trừ sắc bén",
            "badge": "05",
            "points": [
                "Loại bỏ các phương án có thông tin mâu thuẫn hoặc không được bài nói xác nhận.",
                "Cảnh giác với đáp án dùng từ ngữ giống y hệt trong bài nhưng lại bóp méo mối quan hệ nguyên nhân – kết quả."
            ]
        },
        {
            "step": "Bước 6: Luyện nghe chủ động & Dự đoán liên tục",
            "badge": "06",
            "points": [
                "Trong lúc nghe, liên tục suy đoán diễn biến tiếp theo dựa vào dấu hiệu từ vựng và ngữ điệu của người nói.",
                "Duy trì sự tập trung cao độ xuyên suốt cả 3-4 phút của bài nói."
            ]
        }
    ]
}

# Load data.js
with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Inject theory_guide into part2
p2_theory_json = json.dumps(part2_theory, ensure_ascii=False, indent=6)
p2_pattern = r'("part2":\s*\{\s*)("practice":)'
p2_replacement = r'\1"theory_guide": ' + p2_theory_json + ',\n    \\2'
content = re.sub(p2_pattern, p2_replacement, content, count=1)

# Inject theory_guide into part3
p3_theory_json = json.dumps(part3_theory, ensure_ascii=False, indent=6)
p3_pattern = r'("part3":\s*\{\s*)("practice":)'
p3_replacement = r'\1"theory_guide": ' + p3_theory_json + ',\n    \\2'
content = re.sub(p3_pattern, p3_replacement, content, count=1)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected theory_guide into part2 and part3 in data.js!")
