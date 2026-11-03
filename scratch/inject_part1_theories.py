# -*- coding: utf-8 -*-
import json
import re

theories = {
    "p1_type_02": {
        "title": "DẠNG 02: CÂU HỎI Ý CHÍNH (MAIN IDEA QUESTIONS)",
        "definition": "Dạng câu hỏi <mark class=\"hl-keyword\">MAIN IDEA (Chủ đề chính)</mark> yêu cầu thí sinh xác định <mark class=\"hl-primary\">nội dung trung tâm hoặc chủ đề bao quát</mark> của toàn bộ đoạn hội thoại hay bài nói ngắn.<br><br>Khác với dạng <mark class=\"hl-accent\">PURPOSE (Mục đích giao tiếp)</mark> tập trung vào việc người nói muốn làm gì, dạng <mark class=\"hl-keyword\">MAIN IDEA</mark> tập trung vào việc <mark class=\"hl-highlight\">toàn bộ đoạn nghe đang nói về vấn đề gì</mark>. Nói cách khác, đây là “câu trả lời cho câu hỏi: Cả đoạn đang nói về điều gì?”.",
        "question_patterns": [
            "What is the conversation/talk <mark class=\"hl-keyword\">mainly about</mark>?",
            "What is the <mark class=\"hl-keyword\">main topic</mark> of the talk/conversation?",
            "What are the speakers <mark class=\"hl-keyword\">mainly discussing</mark>?",
            "What is the <mark class=\"hl-keyword\">main idea</mark> of the talk/conversation?"
        ],
        "strategies": [
            {
                "step": "Bước 1: Đọc kỹ câu hỏi & Nhận diện dạng bài",
                "badge": "01",
                "points": [
                    "Xác định từ khóa nhận diện câu hỏi về chủ đề chính: <mark class=\"hl-keyword\">mainly</mark>, <mark class=\"hl-keyword\">main topic</mark>, <mark class=\"hl-keyword\">main idea</mark>, <mark class=\"hl-keyword\">discussing</mark>.",
                    "Đọc lướt 4 phương án lựa chọn A, B, C, D để khoanh vùng các lĩnh vực chủ đề có thể xuất hiện."
                ]
            },
            {
                "step": "Bước 2: Tập trung mở đầu, ý lặp lại và kết luận",
                "badge": "02",
                "points": [
                    "Chủ đề chính thường xuất hiện ngay ở <mark class=\"hl-primary\">1-2 câu mở đầu</mark> và được <mark class=\"hl-accent\">phát triển, nhắc lại xuyên suốt</mark> nội dung bài nghe.",
                    "Lắng nghe câu kết luận để nắm bắt thông điệp tổng kết của người nói."
                ]
            },
            {
                "step": "Bước 3: Không bị đánh lừa bởi chi tiết nhỏ (Né bẫy)",
                "badge": "03",
                "points": [
                    "Cảnh giác bẫy: Tuyệt đối tránh chọn những phương án <mark class=\"hl-danger\">chỉ là một ví dụ minh họa hoặc thông tin phụ</mark> được nhắc thoáng qua.",
                    "Đáp án đúng phải là chủ đề <mark class=\"hl-success\">bao quát toàn bộ bài nghe</mark>, không quá hẹp cũng không quá rộng."
                ]
            },
            {
                "step": "Bước 4: Tự đặt câu hỏi kiểm tra sau khi nghe",
                "badge": "04",
                "points": [
                    "Sau khi nghe xong, tự đặt câu hỏi: <em>“Nếu phải đặt tiêu đề cho đoạn hội thoại/bài nói này, mình sẽ đặt là gì?”</em>",
                    "Đối chiếu tiêu đề đó với 4 phương án để chọn đáp án phản ánh đúng nhất ý nghĩa tổng quát."
                ]
            }
        ],
        "signals_title": "Cụm từ gợi ý chủ đề thường gặp trong bài nghe",
        "signals_subtitle": "Các mẫu câu giới thiệu chủ đề trực tiếp của người nói:",
        "signal_groups": [
            {
                "category": "Giới thiệu chủ đề trực tiếp",
                "icon": "🎙️",
                "color": "blue",
                "signals": [
                    { "en": "Today, I’d like to talk about…", "vi": "Hôm nay, tôi muốn nói về…" },
                    { "en": "We’re going to discuss… / Let's discuss...", "vi": "Chúng ta sẽ thảo luận về… / Hãy cùng thảo luận…" },
                    { "en": "Let me tell you about… / I want to talk to you about…", "vi": "Để tôi kể cho bạn về… / Tôi muốn nói với bạn về…" }
                ]
            },
            {
                "category": "Khơi gợi chủ đề / Đặt vấn đề",
                "icon": "💬",
                "color": "purple",
                "signals": [
                    { "en": "Have you heard about...?", "vi": "Bạn đã nghe về… chưa?" },
                    { "en": "What do you think about...?", "vi": "Bạn nghĩ gì về…?" }
                ]
            },
            {
                "category": "Nhấn mạnh trọng tâm / Nội dung bài",
                "icon": "🎯",
                "color": "green",
                "signals": [
                    { "en": "The main point is…", "vi": "Điểm cốt lõi / quan trọng nhất là…" },
                    { "en": "This is about… / This presentation is about...", "vi": "Bài này nói về… / Bài thuyết trình này nói về…" }
                ]
            }
        ]
    },

    "p1_type_03": {
        "title": "DẠNG 03: CÂU HỎI THÔNG TIN CHI TIẾT (DETAIL QUESTIONS)",
        "definition": "Dạng câu hỏi <mark class=\"hl-keyword\">DETAIL (Thông tin chi tiết)</mark> yêu cầu thí sinh xác định các <mark class=\"hl-primary\">thông tin cụ thể được đề cập trực tiếp</mark> trong đoạn nghe như: <mark class=\"hl-accent\">thời gian, số lượng, giá cả, tên người, lý do, hành động, kế hoạch</mark> hoặc các dữ kiện thực tế chính xác khác.",
        "question_patterns": [
            "<mark class=\"hl-keyword\">What time</mark> does the train leave? / <mark class=\"hl-keyword\">When</mark> will the meeting take place?",
            "<mark class=\"hl-keyword\">How much</mark> does the item cost? / <mark class=\"hl-keyword\">Which</mark> product is on sale?",
            "<mark class=\"hl-keyword\">What</mark> does the man/woman <mark class=\"hl-keyword\">suggest doing</mark>?",
            "<mark class=\"hl-keyword\">What</mark> does the speaker <mark class=\"hl-keyword\">plan to do first</mark>?",
            "<mark class=\"hl-keyword\">Why</mark> does the speaker <mark class=\"hl-keyword\">thank the listeners</mark>?",
            "According to the speaker, <mark class=\"hl-keyword\">what</mark> have some people <mark class=\"hl-keyword\">expressed concern about</mark>?"
        ],
        "strategies": [
            {
                "step": "Bước 1: Đọc trước câu hỏi & 4 đáp án (Bắt từ khóa)",
                "badge": "01",
                "points": [
                    "Xác định từ để hỏi (<em>What, When, Where, How much, Which...</em>) và đối tượng chính được hỏi.",
                    "Gạch chân từ khóa định hướng: số giờ, tên địa điểm, số tiền, hành động cụ thể để chủ động nghe bắt thông tin."
                ]
            },
            {
                "step": "Bước 2: Tập trung lắng nghe các dữ kiện cụ thể",
                "badge": "02",
                "points": [
                    "Chú ý cao độ đến: <mark class=\"hl-primary\">con số, danh từ riêng, cụm thời gian, mức giá, động từ chỉ hành động</mark>.",
                    "Để ý các từ đồng nghĩa (paraphrase) giữa bài nghe và các phương án trả lời."
                ]
            },
            {
                "step": "Bước 3: Loại trừ đáp án sai lệch & Gây nhiễu",
                "badge": "03",
                "points": [
                    "Loại bỏ ngay các đáp án có thông tin <mark class=\"hl-danger\">mâu thuẫn, đảo ngược sự thật</mark> hoặc <mark class=\"hl-danger\">hoàn toàn không được nhắc đến</mark>.",
                    "Cảnh giác với đáp án chứa từ vựng giống y hệt trong bài nhưng lại ghép sai ngữ cảnh hoặc sai mốc thời gian/đối tượng."
                ]
            },
            {
                "step": "Bước 4: Kiểm tra lại tính logic với câu hỏi",
                "badge": "04",
                "points": [
                    "Trong bài có thể xuất hiện nhiều con số hoặc sự kiện khác nhau, nhưng phải chọn đúng dữ kiện <mark class=\"hl-success\">trả lời trực tiếp cho câu hỏi</mark>.",
                    "Kiểm tra lại xem phương án chọn có trả lời đúng yêu cầu (ví dụ: làm gì <em>first</em>, lo lắng về điều gì...)."
                ]
            }
        ],
        "signals_title": "Từ vựng & Mẫu câu chỉ chi tiết thường gặp",
        "signals_subtitle": "Các cấu trúc báo hiệu thông tin chi tiết cần nắm bắt:",
        "signal_groups": [
            {
                "category": "Thời gian, Khởi hành & Hạn chót",
                "icon": "⏰",
                "color": "blue",
                "signals": [
                    { "en": "It starts at... / It leaves at... / The train departs at...", "vi": "Bắt đầu lúc… / Rời đi lúc… / Tàu khởi hành lúc…" },
                    { "en": "The deadline is on… / You need to submit this by… / It’s on…", "vi": "Hạn chót là vào ngày… / Bạn cần nộp trước… / Vào ngày…" }
                ]
            },
            {
                "category": "Giá cả & Số lượng cụ thể",
                "icon": "💰",
                "color": "green",
                "signals": [
                    { "en": "The price is... / It costs... / It is about…", "vi": "Giá là… / Nó có giá… / Khoảng chừng…" },
                    { "en": "There are… / We have… / A total of… / About…", "vi": "Có… / Chúng tôi có… / Tổng cộng là… / Khoảng…" }
                ]
            },
            {
                "category": "Địa điểm & Vị trí chính xác",
                "icon": "📍",
                "color": "amber",
                "signals": [
                    { "en": "Located at... / On the second floor...", "vi": "Tọa lạc tại… / Ở tầng hai…" },
                    { "en": "Next to... / Across from…", "vi": "Bên cạnh… / Đối diện với…" }
                ]
            },
            {
                "category": "Kế hoạch, Quyết định & Đề xuất",
                "icon": "💡",
                "color": "purple",
                "signals": [
                    { "en": "We're planning to... / We decided to... / We're going to...", "vi": "Chúng tôi đang lên kế hoạch để… / Chúng tôi quyết định… / Chúng tôi sẽ…" },
                    { "en": "He suggested… / We recommend that… / Let’s… / Why don’t we…?", "vi": "Anh ấy gợi ý… / Chúng tôi khuyến nghị rằng… / Hãy cùng… / Tại sao chúng ta không…?" }
                ]
            }
        ]
    },

    "p1_type_04": {
        "title": "DẠNG 04: CÂU HỎI DANH TÍNH (SPEAKER IDENTITY OR RELATIONSHIP)",
        "definition": "Dạng câu hỏi <mark class=\"hl-keyword\">SPEAKER IDENTITY OR RELATIONSHIP (Danh tính và mối quan hệ)</mark> yêu cầu thí sinh xác định <mark class=\"hl-primary\">vai trò, nghề nghiệp, mối quan hệ giữa các nhân vật</mark> trong bài nghe (chẳng hạn như <em>khách hàng – nhân viên, giáo viên – học sinh, bệnh nhân – bác sĩ</em>, hoặc nghề nghiệp cụ thể của một người).<br><br>Trong nhiều trường hợp, đáp án <mark class=\"hl-danger\">không được nói trực tiếp</mark> mà phải được <mark class=\"hl-accent\">suy luận từ ngữ cảnh, từ vựng chuyên ngành, cách xưng hô và nội dung cuộc trò chuyện</mark>.",
        "question_patterns": [
            "<mark class=\"hl-keyword\">Who is the speaker</mark>? / <mark class=\"hl-keyword\">Who are the speakers</mark>?",
            "<mark class=\"hl-keyword\">Who is the man / woman</mark>?",
            "<mark class=\"hl-keyword\">Who is most likely speaking</mark>? / <mark class=\"hl-keyword\">Who is most likely listening</mark>?",
            "<mark class=\"hl-keyword\">Who is the woman most likely talking to</mark>?",
            "<mark class=\"hl-keyword\">What is the man’s / the woman’s job</mark>?",
            "<mark class=\"hl-keyword\">What is the relationship between the speakers</mark>?"
        ],
        "strategies": [
            {
                "step": "Bước 1: Đọc câu hỏi & Xác định đối tượng cần tìm",
                "badge": "01",
                "points": [
                    "Xác định rõ câu hỏi yêu cầu tìm: vai trò người nói (speaker), người nghe (listener), người thứ ba được nhắc đến, hay mối quan hệ giữa hai người (relationship).",
                    "Chú ý đại từ chỉ giới tính (<em>the man</em> hay <em>the woman</em>) để không nhầm lẫn nhân vật."
                ]
            },
            {
                "step": "Bước 2: Lắng nghe 3 nhóm manh mối then chốt",
                "badge": "02",
                "points": [
                    "<strong>Từ vựng chuyên ngành:</strong> <em>medicine, appointment, reservation, assignment, fee, contract, inventory, prescription...</em>",
                    "<strong>Cách xưng hô:</strong> <em>Sir, Professor, Doctor, Manager, Officer, Detective...</em>",
                    "<strong>Hành động giao tiếp:</strong> <em>make a reservation, report a problem, ask for assistance, diagnose, deliver...</em>"
                ]
            },
            {
                "step": "Bước 3: Đánh giá mối quan hệ & Ngữ cảnh giao tiếp",
                "badge": "03",
                "points": [
                    "Xác định tính chất cuộc trò chuyện: trang trọng (<em>formal</em> - công việc, thủ tục) hay thân mật (<em>informal</em> - bạn bè, đồng nghiệp thân thiết).",
                    "Loại trừ những đáp án không phù hợp với thái độ và vị trí xã hội của người nói."
                ]
            },
            {
                "step": "Bước 4: Chọn phương án phản ánh đúng vai trò thực tế",
                "badge": "04",
                "points": [
                    "Chọn đáp án thể hiện nghề nghiệp hoặc mối quan hệ phù hợp nhất với hành động thực tế diễn ra trong đoạn nghe.",
                    "Tránh nhầm lẫn giữa khách hàng (customer/client) và nhân viên cung cấp dịch vụ (service provider)."
                ]
            }
        ],
        "signals_title": "Bảng từ vựng nghề nghiệp & chức vụ theo lĩnh vực",
        "signals_subtitle": "Các chức danh và nghề nghiệp phổ biến nhất trong bài thi VSTEP Listening:",
        "signal_groups": [
            {
                "category": "Lĩnh vực Giáo dục",
                "icon": "🏫",
                "color": "blue",
                "signals": [
                    { "en": "a teacher / a professor", "vi": "giáo viên / giáo sư đại học" },
                    { "en": "a tutor / a lecturer", "vi": "gia sư, người dạy kèm / giảng viên" },
                    { "en": "a principal / a dean", "vi": "hiệu trưởng / trưởng khoa" },
                    { "en": "a librarian / a teaching assistant", "vi": "thủ thư / trợ giảng (TA)" },
                    { "en": "an academic advisor / a school counselor", "vi": "cố vấn học tập / chuyên viên tư vấn học đường" }
                ]
            },
            {
                "category": "Lĩnh vực Y tế & Sức khỏe",
                "icon": "🏥",
                "color": "green",
                "signals": [
                    { "en": "a doctor / a physician / a surgeon", "vi": "bác sĩ / bác sĩ nội khoa / bác sĩ phẫu thuật" },
                    { "en": "a nurse / a paramedic / a medical assistant", "vi": "y tá / nhân viên cứu thương / trợ lý y tế" },
                    { "en": "a pharmacist / a dentist / a therapist", "vi": "dược sĩ / nha sĩ / nhà trị liệu" },
                    { "en": "a receptionist / a dietician", "vi": "nhân viên lễ tân phòng khám / chuyên gia dinh dưỡng" }
                ]
            },
            {
                "category": "Lĩnh vực Kinh doanh & Hành chính",
                "icon": "💼",
                "color": "purple",
                "signals": [
                    { "en": "a manager / a supervisor / a director", "vi": "quản lý / người giám sát / giám đốc" },
                    { "en": "an accountant / a financial advisor", "vi": "kế toán viên / cố vấn tài chính" },
                    { "en": "an executive / an assistant / a secretary", "vi": "chuyên viên điều hành / trợ lý / thư ký" },
                    { "en": "an employee / a clerk / an HR officer", "vi": "nhân viên / nhân viên văn phòng / cán bộ nhân sự" },
                    { "en": "a business analyst / a consultant", "vi": "chuyên viên phân tích kinh doanh / chuyên viên tư vấn" }
                ]
            },
            {
                "category": "Lĩnh vực Dịch vụ, Nhà hàng & Bán hàng",
                "icon": "🛒",
                "color": "amber",
                "signals": [
                    { "en": "a cashier / a salesperson / a store clerk", "vi": "thu ngân / nhân viên bán hàng / nhân viên cửa hàng" },
                    { "en": "a store owner / a caterer", "vi": "chủ cửa hàng / người cung cấp dịch vụ ăn uống tiệc" },
                    { "en": "a waiter / a waitress / a barista", "vi": "bồi bàn nam / nữ / nhân viên pha chế cà phê" },
                    { "en": "a customer service rep / a receptionist", "vi": "đại diện chăm sóc khách hàng / nhân viên lễ tân" },
                    { "en": "a housekeeper / a concierge / a delivery person", "vi": "nhân viên dọn phòng / nhân viên hỗ trợ khách sạn / nhân viên giao hàng" }
                ]
            },
            {
                "category": "Lĩnh vực Công nghệ, Truyền thông & Báo chí",
                "icon": "💻",
                "color": "blue",
                "signals": [
                    { "en": "a technician / an IT specialist", "vi": "kỹ thuật viên / chuyên viên công nghệ thông tin" },
                    { "en": "a programmer / a web developer", "vi": "lập trình viên / nhà phát triển web" },
                    { "en": "a designer / an editor / a publisher", "vi": "nhà thiết kế / biên tập viên / nhà xuất bản" },
                    { "en": "a journalist / a news reporter / a broadcaster", "vi": "nhà báo / phóng viên tin tức / phát thanh viên" },
                    { "en": "a photographer / a sound engineer", "vi": "nhiếp ảnh gia / kỹ sư âm thanh" }
                ]
            },
            {
                "category": "Lĩnh vực Xây dựng, Kỹ thuật & Giao thông",
                "icon": "🏗️",
                "color": "amber",
                "signals": [
                    { "en": "an architect / a civil engineer", "vi": "kiến trúc sư / kỹ sư xây dựng dân dụng" },
                    { "en": "a construction worker / a site supervisor", "vi": "công nhân xây dựng / người giám sát công trường" },
                    { "en": "a project manager / a building contractor", "vi": "quản lý dự án / nhà thầu xây dựng" },
                    { "en": "a plumber / an electrician / a mechanic", "vi": "thợ sửa ống nước / thợ điện / thợ cơ khí" },
                    { "en": "a pilot / a train conductor", "vi": "phi công / người soát vé, trưởng tàu" },
                    { "en": "a truck driver / a bus driver / a delivery driver", "vi": "tài xế xe tải / tài xế xe buýt / tài xế giao hàng" }
                ]
            },
            {
                "category": "Lĩnh vực Nghệ thuật, Giải trí & Du lịch",
                "icon": "🎭",
                "color": "purple",
                "signals": [
                    { "en": "an artist / an actor / an actress", "vi": "nghệ sĩ / nam diễn viên / nữ diễn viên" },
                    { "en": "a singer / a musician / a composer", "vi": "ca sĩ / nhạc công / nhạc sĩ sáng tác" },
                    { "en": "a film director / a producer", "vi": "đạo diễn phim / nhà sản xuất" },
                    { "en": "a tour guide / a travel agent / a flight attendant", "vi": "hướng dẫn viên du lịch / đại lý du lịch / tiếp viên hàng không" },
                    { "en": "a real estate agent", "vi": "môi giới bất động sản" }
                ]
            },
            {
                "category": "Lĩnh vực Luật pháp, Chính phủ & Dịch vụ công",
                "icon": "⚖️",
                "color": "green",
                "signals": [
                    { "en": "a lawyer / a judge / a politician", "vi": "luật sư / thẩm phán / chính trị gia" },
                    { "en": "a police officer / a detective / a security guard", "vi": "cảnh sát / thám tử / nhân viên bảo vệ" },
                    { "en": "a firefighter / a soldier", "vi": "lính cứu hỏa / quân nhân, người lính" },
                    { "en": "a government official / a town official / a mayor", "vi": "quan chức chính phủ / viên chức thị trấn / thị trưởng" }
                ]
            }
        ]
    },

    "p1_type_05": {
        "title": "DẠNG 05: CÂU HỎI ĐỊA ĐIỂM/BỐI CẢNH (LOCATION / SETTING QUESTIONS)",
        "definition": "Dạng câu hỏi <mark class=\"hl-keyword\">LOCATION / SETTING (Địa điểm / bối cảnh)</mark> yêu cầu thí sinh suy luận ra <mark class=\"hl-primary\">nơi diễn ra cuộc hội thoại hay bài nói</mark> dựa trên các manh mối xuất hiện trong bài nghe.<br><br>Đáp án thường <mark class=\"hl-danger\">không được nêu trực tiếp</mark> mà phải được suy ra từ: <mark class=\"hl-accent\">từ vựng gợi ý (contextual vocabulary), loại hình dịch vụ / hoạt động được đề cập, và hành động giao tiếp của người nói</mark>.",
        "question_patterns": [
            "<mark class=\"hl-keyword\">Where does the talk / conversation take place</mark>?",
            "<mark class=\"hl-keyword\">What is the most likely location</mark> of the talk / conversation?",
            "<mark class=\"hl-keyword\">What is the setting</mark> of the talk / conversation?",
            "<mark class=\"hl-keyword\">Where are the speakers</mark>? / <mark class=\"hl-keyword\">Where is the speaker</mark>?",
            "<mark class=\"hl-keyword\">Where is this announcement being made</mark>?",
            "<mark class=\"hl-keyword\">Where does the speaker most likely work</mark>?",
            "<mark class=\"hl-keyword\">Where most likely are the listeners</mark>?"
        ],
        "strategies": [
            {
                "step": "Bước 1: Đọc kỹ câu hỏi & Xác định từ khóa địa điểm",
                "badge": "01",
                "points": [
                    "Xác định từ khóa nhận diện: <mark class=\"hl-keyword\">where</mark>, <mark class=\"hl-keyword\">place</mark>, <mark class=\"hl-keyword\">location</mark>, <mark class=\"hl-keyword\">setting</mark>.",
                    "Phân biệt rõ: câu hỏi hỏi nơi diễn ra cuộc nói chuyện, nơi người nói làm việc (<em>work</em>), hay nơi người nghe đang đứng (<em>listeners</em>)."
                ]
            },
            {
                "step": "Bước 2: Lắng nghe từ vựng gợi ý đặc trưng",
                "badge": "02",
                "points": [
                    "Tập trung bắt các từ vựng gắn liền với một địa điểm cụ thể (ví dụ: nghe thấy <em>menu, order, bill</em> → nhà hàng; nghe thấy <em>flight, gate, boarding pass</em> → sân bay).",
                    "Chú ý các âm thanh nền (nếu có) hoặc thông báo qua loa phát thanh."
                ]
            },
            {
                "step": "Bước 3: Suy luận dựa vào ngữ cảnh và hành động",
                "badge": "03",
                "points": [
                    "Kết hợp hành động giao tiếp: làm thủ tục check-in, đổi hàng, hỏi đường, đặt vé, khám bệnh...",
                    "Xem xét đối tượng được trao đổi và tính chất dịch vụ để xác định địa điểm chính xác."
                ]
            },
            {
                "step": "Bước 4: Loại trừ đáp án không hợp lý (Né bẫy)",
                "badge": "04",
                "points": [
                    "Cảnh giác bẫy: Không chọn những địa điểm chỉ được người nói nhắc đến như một kế hoạch trong tương lai hoặc nơi họ sắp đến.",
                    "Đáp án phải là nơi <mark class=\"hl-success\">cuộc hội thoại hoặc sự kiện đang thực sự diễn ra</mark>."
                ]
            }
        ],
        "signals_title": "Từ vựng nhận diện địa điểm, nơi chốn & sự kiện",
        "signals_subtitle": "Các cụm từ khóa đặc trưng giúp bạn nhận diện ngay bối cảnh bài nghe:",
        "signal_groups": [
            {
                "category": "Tại nhà hàng, quán ăn (At a restaurant / cafe)",
                "icon": "🍽️",
                "color": "amber",
                "signals": [
                    { "en": "menu, waiter, customer, bill", "vi": "thực đơn, người bồi bàn, khách hàng, hóa đơn" },
                    { "en": "seat, meal, receipt, refreshment", "vi": "chỗ ngồi, bữa ăn, biên lai, đồ ăn nhẹ / nước giải khát" },
                    { "en": "reserve, order, book a table, make a reservation", "vi": "đặt chỗ, gọi món, đặt bàn trước" }
                ]
            },
            {
                "category": "Tại khách sạn (At a hotel)",
                "icon": "🏨",
                "color": "blue",
                "signals": [
                    { "en": "front desk, room key, room service, bellboy", "vi": "quầy lễ tân, chìa khóa phòng, dịch vụ phòng, nhân viên xách hành lý" },
                    { "en": "receptionist, manager, lobby, housekeeping", "vi": "lễ tân, quản lý, tiền sảnh, nhân viên dọn phòng" },
                    { "en": "register, check in, check out, guest", "vi": "đăng ký, làm thủ tục nhận/trả phòng, khách lưu trú" }
                ]
            },
            {
                "category": "Tại ngân hàng (At the bank)",
                "icon": "🏦",
                "color": "green",
                "signals": [
                    { "en": "cash, credit card, interest, transaction", "vi": "tiền mặt, thẻ tín dụng, lãi suất, giao dịch" },
                    { "en": "client, balance, ATM, transfer", "vi": "khách hàng, số dư tài khoản, máy ATM, chuyển khoản" },
                    { "en": "deposit, withdraw, account, loan", "vi": "gửi tiền, rút tiền, tài khoản, khoản vay" }
                ]
            },
            {
                "category": "Tại bưu điện (At the post office)",
                "icon": "📮",
                "color": "purple",
                "signals": [
                    { "en": "send by air, mailbox, address label", "vi": "gửi đường hàng không, hòm thư, nhãn địa chỉ" },
                    { "en": "stamp, envelope, package, postal code", "vi": "tem thư, phong bì, bưu kiện, mã bưu chính" },
                    { "en": "ship, deliver, delivery, tracking number, registered mail", "vi": "vận chuyển, giao hàng, mã vận đơn theo dõi, thư bảo đảm" }
                ]
            },
            {
                "category": "Tại phòng khám / Bệnh viện (At a medical office / hospital)",
                "icon": "🏥",
                "color": "green",
                "signals": [
                    { "en": "doctor, nurse, patient, medicine", "vi": "bác sĩ, y tá, bệnh nhân, thuốc men" },
                    { "en": "prescription, check-up, appointment, clinic", "vi": "đơn thuốc, khám tổng quát, cuộc hẹn khám, phòng khám" },
                    { "en": "treatment, examination, medical record, receptionist", "vi": "điều trị, kiểm tra y tế, bệnh án, lễ tân y tế" }
                ]
            },
            {
                "category": "Tại sân bay (At the airport)",
                "icon": "✈️",
                "color": "blue",
                "signals": [
                    { "en": "passport, boarding pass, passenger, luggage", "vi": "hộ chiếu, thẻ lên máy bay, hành khách, hành lý" },
                    { "en": "flight, gate, departure, arrival", "vi": "chuyến bay, cửa ra máy bay, giờ khởi hành, giờ đến" },
                    { "en": "terminal, security check, airline, carry-on bag", "vi": "nhà ga sân bay, kiểm tra an ninh, hãng hàng không, hành lý xách tay" }
                ]
            },
            {
                "category": "Tại cửa hàng / Siêu thị (At a shop / store / supermarket)",
                "icon": "🛍️",
                "color": "amber",
                "signals": [
                    { "en": "cashier, salesperson, item, receipt", "vi": "thu ngân, nhân viên bán hàng, món hàng, biên lai" },
                    { "en": "in stock, out of stock, refund, discount", "vi": "còn hàng, hết hàng, hoàn tiền, giảm giá" },
                    { "en": "payment, shopping bag / cart, on sale, price tag", "vi": "thanh toán, túi/xe đẩy mua hàng, đang giảm giá, mác giá" }
                ]
            },
            {
                "category": "Tại kho hàng (At a warehouse)",
                "icon": "🏬",
                "color": "purple",
                "signals": [
                    { "en": "shipment, package, inventory, storage", "vi": "lô hàng, bưu kiện, hàng tồn kho, kho lưu trữ" },
                    { "en": "loading dock, forklift, load, unload", "vi": "bãi bốc dỡ hàng, xe nâng, chất hàng, dỡ hàng" },
                    { "en": "stack, label, invoice, drop off", "vi": "xếp chồng, dán nhãn, hóa đơn xuất hàng, giao trả hàng" }
                ]
            },
            {
                "category": "Tại văn phòng công ty (At an office)",
                "icon": "🏢",
                "color": "blue",
                "signals": [
                    { "en": "manager, employee, coworker / colleague, department", "vi": "quản lý, nhân viên, đồng nghiệp, phòng ban" },
                    { "en": "interview, project, meeting, deadline", "vi": "phỏng vấn, dự án, cuộc họp, hạn chót hoàn thành" },
                    { "en": "memo, salary, CEO, contract", "vi": "thông báo nội bộ, tiền lương, tổng giám đốc, hợp đồng" }
                ]
            },
            {
                "category": "Tại nhà ga tàu / Bến xe (At a train / bus station)",
                "icon": "🚆",
                "color": "green",
                "signals": [
                    { "en": "ticket booth, schedule, platform, departure", "vi": "quầy bán vé, lịch trình, sân ga đón tàu, giờ khởi hành" },
                    { "en": "arrival, train, bus, track", "vi": "giờ đến, tàu hỏa, xe buýt, đường ray tàu" },
                    { "en": "conductor, route, stop, transfer", "vi": "người soát vé, tuyến đường, điểm dừng, chuyển tuyến xe/tàu" }
                ]
            },
            {
                "category": "Tại rạp hát / Rạp chiếu phim (At a theater / cinema)",
                "icon": "🎭",
                "color": "purple",
                "signals": [
                    { "en": "ticket, seat, showtime, curtain", "vi": "vé, chỗ ngồi, giờ chiếu/diễn, rèm sân khấu" },
                    { "en": "play, movie, performance, audience", "vi": "vở kịch, phim, buổi biểu diễn, khán giả" },
                    { "en": "actor / actress, stage, director, sold out", "vi": "diễn viên nam/nữ, sân khấu, đạo diễn, cháy vé/hết vé" }
                ]
            },
            {
                "category": "Tại văn phòng bất động sản (At a real estate agency)",
                "icon": "🏠",
                "color": "amber",
                "signals": [
                    { "en": "apartment, home, rent, landlord", "vi": "căn hộ, nhà ở, tiền thuê, chủ nhà" },
                    { "en": "tenant, lease, move in, move out", "vi": "người thuê nhà, hợp đồng thuê, dọn vào, dọn đi" },
                    { "en": "property, contract, real estate agent, listing", "vi": "bất động sản, hợp đồng mua bán, đại lý môi giới, danh mục nhà đất" }
                ]
            },
            {
                "category": "Một số nơi chốn & Cơ sở khác",
                "icon": "📍",
                "color": "blue",
                "signals": [
                    { "en": "an advertising company", "vi": "công ty quảng cáo (campaign, client, marketing, design, pitch)" },
                    { "en": "a factory / manufacturing plant", "vi": "nhà máy sản xuất (machinery, production, assembly line, workers)" },
                    { "en": "a newspaper / press office", "vi": "tòa soạn báo (reporter, article, deadline, editor, print)" },
                    { "en": "a customer service center", "vi": "trung tâm CSKH (complaint, inquiry, hotline, feedback, support)" },
                    { "en": "a car dealership", "vi": "đại lý ô tô (test drive, showroom, vehicle, salesman)" },
                    { "en": "a fitness center / gym", "vi": "phòng tập thể hình (workout, trainer, membership, treadmill)" },
                    { "en": "a university campus", "vi": "khuôn viên đại học (lecture, student ID, dorm, registrar, semester)" },
                    { "en": "a delivery hub", "vi": "trung tâm điều phối giao hàng (parcel, dispatch, logistics, courier, scan)" }
                ]
            },
            {
                "category": "Một số sự kiện đặc trưng thường xuất hiện",
                "icon": "🎉",
                "color": "purple",
                "signals": [
                    { "en": "a music festival / concert", "vi": "lễ hội âm nhạc (stage, band, crowd, soundcheck, ticket)" },
                    { "en": "a sporting event / match", "vi": "sự kiện thể thao (stadium, team, match, score, cheer)" },
                    { "en": "an orientation session", "vi": "buổi định hướng (welcome, new staff/students, schedule, policy)" },
                    { "en": "an anniversary celebration", "vi": "lễ kỷ niệm (years, invite, speech, cake, memory)" },
                    { "en": "a community fundraiser / charity", "vi": "sự kiện gây quỹ từ thiện (donation, raffle, cause, support, volunteer)" },
                    { "en": "a press conference", "vi": "buổi họp báo (media, spokesperson, announcement, live)" },
                    { "en": "a product demonstration", "vi": "buổi giới thiệu / dùng thử sản phẩm (try out, feature, benefit, sample)" },
                    { "en": "a job interview", "vi": "buổi phỏng vấn xin việc (job opening, shift preference, cover letter, resume)" }
                ]
            }
        ]
    },

    "p1_type_06": {
        "title": "DẠNG 06: CÂU HỎI SUY LUẬN/HÀM Ý (INFERENCE / IMPLICATION QUESTIONS)",
        "definition": "Dạng câu hỏi <mark class=\"hl-keyword\">INFERENCE / IMPLICATION (Suy luận / hàm ý)</mark> yêu cầu thí sinh <mark class=\"hl-primary\">rút ra một kết luận hợp lý</mark> dựa trên những thông tin được nghe.<br><br>Đáp án thường <mark class=\"hl-danger\">không được nêu trực tiếp</mark> mà phải được suy luận từ: <mark class=\"hl-accent\">ngữ cảnh, thái độ, cảm xúc, hành động hoặc lời nói gián tiếp</mark> của các nhân vật trong đoạn hội thoại hay bài nói.",
        "question_patterns": [
            "<mark class=\"hl-keyword\">What can be inferred</mark> about the man/woman?",
            "<mark class=\"hl-keyword\">What does the woman imply</mark> when she says...?",
            "<mark class=\"hl-keyword\">What does the speaker suggest</mark>?",
            "<mark class=\"hl-keyword\">What is probably true</mark> about the situation?",
            "<mark class=\"hl-keyword\">What can be concluded</mark> from the conversation?",
            "<mark class=\"hl-keyword\">What is it true</mark> about...?"
        ],
        "strategies": [
            {
                "step": "Bước 1: Đọc kỹ câu hỏi & Xác định mục tiêu suy luận",
                "badge": "01",
                "points": [
                    "Xác định rõ câu hỏi yêu cầu suy luận về điều gì: <mark class=\"hl-keyword\">thái độ, cảm xúc, hành động tiếp theo, mối quan hệ, hay một nhận định đúng (true)</mark>.",
                    "Đọc lướt 4 lựa chọn để nắm bắt các khả năng suy luận trước khi audio phát."
                ]
            },
            {
                "step": "Bước 2: Tìm kiếm manh mối ngầm và thái độ người nói",
                "badge": "02",
                "points": [
                    "Chú ý cách diễn đạt gián tiếp: các cách đồng ý ngầm, từ chối khéo léo (<em>I wish I could, but...</em>), hoặc phản ứng ngạc nhiên, thất vọng.",
                    "Lắng nghe ngữ điệu và các từ nối chuyển ý mang tính bước ngoặt (<em>actually, in fact, unfortunately, however, but...</em>)."
                ]
            },
            {
                "step": "Bước 3: Suy luận hợp lý từ bối cảnh tổng thể",
                "badge": "03",
                "points": [
                    "Kết hợp tất cả các chi tiết nghe được để đưa ra kết luận hoặc hàm ý <mark class=\"hl-primary\">hợp lý và tự nhiên nhất</mark>.",
                    "Dựa hoàn toàn vào dữ kiện trong bài nghe, <mark class=\"hl-danger\">tuyệt đối không suy diễn dựa trên cảm tính hoặc kiến thức bên ngoài</mark>."
                ]
            },
            {
                "step": "Bước 4: Loại trừ đáp án bẫy máy móc",
                "badge": "04",
                "points": [
                    "Cảnh giác bẫy: Loại ngay đáp án <mark class=\"hl-danger\">chỉ lặp lại từ ngữ nghe được một cách máy móc</mark> nhưng không trả lời đúng câu hỏi suy luận.",
                    "Loại bỏ các phương án suy đoán quá xa, thiếu căn cứ xác thực từ bài nghe."
                ]
            }
        ],
        "note": "Dạng câu hỏi này thiên về <strong>nghe hiểu và suy luận ngữ nghĩa</strong> hơn là nghe bắt từ khóa trực tiếp. Thí sinh cần nắm bắt được <strong>ý nghĩa tổng thể</strong> của cả đoạn nghe và những hàm ý được gợi mở ra từ thái độ của người nói, thay vì chỉ chăm chăm bắt từ đơn lẻ.",
        "signals_title": "Tín hiệu nhận diện hàm ý & Mẹo suy luận logic",
        "signals_subtitle": "Các cấu trúc thường gợi mở thông tin ngầm hoặc thái độ thực sự của người nói:",
        "signal_groups": [
            {
                "category": "Tín hiệu chuyển ý & Đưa ra thông tin bất ngờ / Trái ngược",
                "icon": "⚡",
                "color": "amber",
                "signals": [
                    { "en": "Actually… / In fact… / As a matter of fact…", "vi": "Trên thực tế là… / Thật ra là… (chuẩn bị đính chính hoặc đưa thông tin ngược lại)" },
                    { "en": "Unfortunately… / I’m afraid that… / Sadly...", "vi": "Thật không may là… / Tôi e rằng… (báo hiệu tin buồn, từ chối hoặc vấn đề phát sinh)" },
                    { "en": "However… / But then… / On the other hand…", "vi": "Tuy nhiên… / Nhưng rồi… (báo hiệu sự thay đổi trong kế hoạch hoặc tình huống)" }
                ]
            },
            {
                "category": "Gợi ý hành động & Đề xuất gián tiếp",
                "icon": "💡",
                "color": "blue",
                "signals": [
                    { "en": "Why don’t you / we…? / How about…?", "vi": "Tại sao bạn/chúng ta không…? / Còn về việc… thì sao? (gợi ý làm điều gì đó)" },
                    { "en": "You might want to… / It would be better if…", "vi": "Có thể bạn sẽ muốn… / Sẽ tốt hơn nếu… (khuyên nhủ một cách lịch sự)" },
                    { "en": "Maybe we should consider…", "vi": "Có lẽ chúng ta nên cân nhắc… (hành động tiếp theo nên làm)" }
                ]
            },
            {
                "category": "Biểu đạt thái độ, cảm xúc & Hoài nghi ngầm",
                "icon": "🎭",
                "color": "purple",
                "signals": [
                    { "en": "I doubt that… / Are you sure about that?", "vi": "Tôi nghi ngờ rằng… / Bạn có chắc về điều đó không? (thể hiện sự không tin tưởng/chưa đồng ý)" },
                    { "en": "That sounds great, but…", "vi": "Nghe có vẻ hay đấy, nhưng mà… (chuẩn bị từ chối khéo léo)" },
                    { "en": "I couldn’t agree more! / Exactly!", "vi": "Tôi hoàn toàn đồng ý! / Chính xác! (thể hiện sự đồng thuận cao)" }
                ]
            }
        ]
    }
}

# Now let's inject into data.js
with open('data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

# For each type (p1_type_02 to p1_type_06), find the object in data.js and insert theory_content
for type_id, theory_obj in theories.items():
    pattern = rf'(\{{\s*"id":\s*"{type_id}",\s*"title":\s*"[^"]+",)'
    match = re.search(pattern, data_js)
    if not match:
        print(f"ERROR: Could not find {type_id} in data.js")
        continue
    
    # Format theory_obj as formatted JSON with 8-space indentation
    theory_json = json.dumps(theory_obj, ensure_ascii=False, indent=8)
    # indent properly
    indented_theory = '        "theory_content": ' + theory_json.strip() + ','
    
    # Replacement
    old_header = match.group(1)
    new_header = old_header + '\n' + indented_theory
    data_js = data_js.replace(old_header, new_header, 1)
    print(f"Successfully injected theory for {type_id}")

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)

print("Finished updating data.js!")
