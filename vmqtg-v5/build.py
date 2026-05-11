#!/usr/bin/env python3
"""Văn Miếu – Quốc Tử Giám · Website V5 (sitemap 09.05.2026)
Style: monochrome minimalist · wireframe with real data
Nav: hover dropdowns, mega-menu for Về di tích
"""
import json
import shutil
import unicodedata
from pathlib import Path

import translations as TR

ROOT = Path(__file__).resolve().parent
OLD_IMGS = ROOT.parent / "site" / "assets" / "images"


def _strip_diacritics(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower()

# ─── DATA: SITEMAP ────────────────────────────────────────────────────────────

# Each item: id, label, slug, optional img, optional content
# Hierarchy: section → group → item

SITEMAP = [
    {
        "id": "A", "label": "Tham quan", "slug": "tham-quan", "type": "single",
        "sub": "Vé, giờ mở cửa, nội quy, đường đến và các tiện ích.",
    },
    {
        "id": "B", "label": "Về di tích", "slug": "ve-di-tich", "type": "mega",
        "sub": "Lịch sử, phân khu, kiến trúc, danh nhân, tượng thờ và thư viện.",
        "groups": [
            {"id": "B1", "label": "Lịch sử", "slug": "lich-su",
             "sub": "Hình thành và phát triển qua các triều đại.",
             "items": [
                {"id": "B1.1", "label": "Thời Lý",     "slug": "thoi-ly",
                 "img": "lich-su/1-toan-canh-van-mieu-quoc-tu-giam-dau-the-ky-xx-copy.jpg"},
                {"id": "B1.2", "label": "Thời Trần",   "slug": "thoi-tran",
                 "img": "lich-su/2-tu-tru-va-ho-van-phia-truoc-van-mieu-quoc-tu-giam.jpg"},
                {"id": "B1.3", "label": "Thời Lê",     "slug": "thoi-le",
                 "img": "lich-su/10-nha-bia-tien-si-ben-tay.jpg"},
                {"id": "B1.4", "label": "Thời Nguyễn", "slug": "thoi-nguyen",
                 "img": "lich-su/12-bia-tien-si.jpg"},
            ]},
            {"id": "B2", "label": "Các phân khu", "slug": "phan-khu",
             "sub": "Ba phân khu chính của di tích.",
             "items": [
                {"id": "B2.1", "label": "Nội tự",     "slug": "noi-tu",
                 "img": "kien-truc/san-dai-bai-va-nha-dai-bai.jpg"},
                {"id": "B2.2", "label": "Vườn Giám",  "slug": "vuon-giam",
                 "img": "kien-truc/nha-bat-giac-vuon-giam.jpg"},
                {"id": "B2.3", "label": "Hồ Văn",     "slug": "ho-van",
                 "img": "kien-truc/ho-van.jpg"},
            ]},
            {"id": "B3", "label": "Công trình kiến trúc", "slug": "kien-truc",
             "sub": "12 công trình tiêu biểu trong khuôn viên di tích.",
             "items": [
                {"id": "B3.1",  "label": "Bia Hạ mã",       "slug": "bia-ha-ma",
                 "img": "lich-su/5-bia-ha-ma.jpg"},
                {"id": "B3.2",  "label": "Cổng Văn Miếu",   "slug": "cong-van-mieu",
                 "img": "kien-truc/cong-vm-mat-truoc.jpg"},
                {"id": "B3.3",  "label": "Cổng Đại Trung",  "slug": "cong-dai-trung",
                 "img": "kien-truc/cong-dai-trung-1.jpg"},
                {"id": "B3.4",  "label": "Khuê Văn Các",    "slug": "khue-van-cac",
                 "img": "kien-truc/kvc-va-gieng-thien-quang.jpg"},
                {"id": "B3.5",  "label": "Nhà che bia",     "slug": "nha-che-bia",
                 "img": "kien-truc/khu-vuon-bia-ts-ben-dong.jpg"},
                {"id": "B3.6",  "label": "Cổng Đại Thành",  "slug": "cong-dai-thanh",
                 "img": "kien-truc/cong-dai-thanh.jpg"},
                {"id": "B3.7",  "label": "Bái đường",       "slug": "bai-duong",
                 "img": "kien-truc/toa-bai-duong.jpg"},
                {"id": "B3.8",  "label": "Cổng Thái học",   "slug": "cong-thai-hoc",
                 "img": "kien-truc/cong-thai-hoc-2.jpg"},
                {"id": "B3.9",  "label": "Thái học",        "slug": "thai-hoc",
                 "img": "lich-su/30-cong-thai-hoc.jpg"},
                {"id": "B3.10", "label": "Nhà chuông, nhà trống", "slug": "nha-chuong-trong",
                 "img": "kien-truc/lau-trong.jpg"},
                {"id": "B3.11", "label": "Nhà Bát Giác",    "slug": "nha-bat-giac",
                 "img": "kien-truc/nha-bat-giac-vuon-giam.jpg"},
                {"id": "B3.12", "label": "Phương đình",     "slug": "phuong-dinh",
                 "img": "kien-truc/gieng-thien-quang.jpg"},
            ]},
            {"id": "B4", "label": "Danh nhân", "slug": "danh-nhan",
             "sub": "Các vua, thầy giáo và danh nhân khoa bảng.",
             "items": [
                {"id": "B4.1", "label": "Vua Lý Thánh Tông",       "slug": "vua-ly-thanh-tong",
                 "img": "tuong-tho/7-ly-thanh-tong.jpg"},
                {"id": "B4.2", "label": "Vua Lý Nhân Tông",        "slug": "vua-ly-nhan-tong",
                 "img": "tuong-tho/8-ly-nhan-tong.jpg"},
                {"id": "B4.3", "label": "Vua Lê Thánh Tông",       "slug": "vua-le-thanh-tong",
                 "img": "tuong-tho/9-lethanhtong.jpg"},
                {"id": "B4.5", "label": "Tư nghiệp Chu Văn An",    "slug": "chu-van-an",
                 "img": "tuong-tho/6-chu-van-an.jpg"},
                {"id": "B4.6", "label": "Danh nhân khoa bảng",     "slug": "khoa-bang",
                 "img": "danh-nhan/1-nha-tho-trang-nguyen-nguyen-truc-xa-tam-hung-thanh-oai-ha-noi-anh-p-ncst.jpg"},
            ]},
            {"id": "B5", "label": "Tượng thờ", "slug": "tuong-tho",
             "sub": "Khổng Tử, Tứ Phối và các vị Thánh nho.",
             "items": [
                {"id": "B5.1", "label": "Khổng Tử", "slug": "khong-tu",
                 "img": "tuong-tho/1-khongtu.jpg"},
                {"id": "B5.2", "label": "Nhan Tử",  "slug": "nhan-tu",
                 "img": "tuong-tho/2-phuc-thanh-nhan-hoi.jpg"},
                {"id": "B5.3", "label": "Tử Tư",    "slug": "tu-tu",
                 "img": "tuong-tho/3-thuat-thanh-tu-tu.jpg"},
                {"id": "B5.4", "label": "Tăng Tử",  "slug": "tang-tu",
                 "img": "tuong-tho/4-tong-thanh-tang-sam.jpg"},
                {"id": "B5.5", "label": "Mạnh Tử",  "slug": "manh-tu",
                 "img": "tuong-tho/5-a-thanh-manh-tu.jpg"},
            ]},
            {"id": "B6", "label": "Thư viện", "slug": "thu-vien",
             "sub": "Tư liệu ảnh và video về di tích.",
             "items": [
                {"id": "B6.1", "label": "Thư viện ảnh", "slug": "thu-vien-anh"},
                {"id": "B6.2", "label": "Video",        "slug": "video"},
            ]},
        ],
    },
    {
        "id": "C", "label": "Trưng bày, triển lãm", "slug": "trung-bay-trien-lam", "type": "dropdown",
        "sub": "Trưng bày cố định, chuyên đề và các triển lãm.",
        "groups": [
            {"id": "C1", "label": "Trưng bày cố định", "slug": "co-dinh",
             "sub": "Ba khu trưng bày thường xuyên trong khu Thái Học.",
             "items": [
                {"id": "C1.1", "label": "Quốc Tử Giám – Trường quốc học đầu tiên", "slug": "truong-quoc-hoc",
                 "img": "hoat-dong/toan-canh.jpg"},
                {"id": "C1.2", "label": "Khơi nguồn đạo học", "slug": "khoi-nguon-dao-hoc",
                 "img": "hoat-dong/trung-bay.jpg"},
                {"id": "C1.3", "label": "Sử đá lưu danh", "slug": "su-da-luu-danh",
                 "img": "lich-su/bia.jpg"},
            ]},
            {"id": "C2", "label": "Trưng bày chuyên đề", "slug": "chuyen-de",
             "sub": "Các chuyên đề thay đổi theo thời điểm trong năm.",
             "items": []},
            {"id": "C3", "label": "Triển lãm", "slug": "trien-lam",
             "sub": "Các triển lãm hợp tác và sự kiện đặc biệt.",
             "items": []},
        ],
    },
    {
        "id": "D", "label": "Các hoạt động", "slug": "cac-hoat-dong", "type": "dropdown",
        "sub": "Sự kiện, giáo dục di sản, trải nghiệm văn hoá và workshop.",
        "groups": [
            {"id": "D1", "label": "Sự kiện", "slug": "su-kien",
             "sub": "Lịch sự kiện văn hoá và lễ hội.",
             "items": [
                {"id": "D1.1", "label": "Sự kiện sắp diễn ra", "slug": "sap-dien-ra"},
                {"id": "D1.2", "label": "Sự kiện đang diễn ra", "slug": "dang-dien-ra"},
            ]},
            {"id": "D2", "label": "Giáo dục di sản", "slug": "giao-duc-di-san",
             "sub": "Chương trình cho học sinh từ mầm non đến THPT.", "items": []},
            {"id": "D3", "label": "Hoạt động trải nghiệm", "slug": "trai-nghiem",
             "sub": "Trải nghiệm thư pháp, in dập bia và trò chơi dân gian.", "items": []},
            {"id": "D4", "label": "Hoạt động văn hoá nghệ thuật", "slug": "van-hoa-nghe-thuat",
             "sub": "Biểu diễn nhạc cổ, hát ca trù và chương trình nghệ thuật.", "items": []},
            {"id": "D5", "label": "Hội thảo – Toạ đàm", "slug": "hoi-thao",
             "sub": "Hội thảo khoa học về di sản, lịch sử và giáo dục.", "items": []},
            {"id": "D6", "label": "Đón đoàn ngoại giao", "slug": "doan-ngoai-giao",
             "sub": "Tiếp đón đoàn ngoại giao và khách quốc tế.", "items": []},
            {"id": "D7", "label": "Workshop", "slug": "workshop",
             "sub": "Workshop sáng tạo, thư pháp và di sản.", "items": []},
        ],
    },
    {
        "id": "E", "label": "Dịch vụ", "slug": "dich-vu", "type": "dropdown",
        "sub": "Tour đêm, thuyết minh, quà lưu niệm và dịch vụ tại điểm.",
        "groups": [
            {"id": "E1", "label": "Tour đêm Văn Miếu", "slug": "tour-dem",
             "sub": "Trải nghiệm di tích dưới ánh đèn đêm.", "items": []},
            {"id": "E2", "label": "Thuyết minh tự động", "slug": "audio-guide",
             "sub": "Audio guide 8 ngôn ngữ.", "items": []},
            {"id": "E3", "label": "Thuyết minh tại điểm", "slug": "huong-dan-vien",
             "sub": "Hướng dẫn viên tiếng Việt, Anh, Pháp, Trung.", "items": []},
            {"id": "E4", "label": "Quà lưu niệm", "slug": "qua-luu-niem",
             "sub": "Sách, ấn phẩm, đồ thủ công mỹ nghệ.", "items": []},
            {"id": "E5", "label": "Viết chữ thư pháp", "slug": "thu-phap",
             "sub": "Trải nghiệm viết thư pháp tại Văn Miếu.", "items": []},
            {"id": "E6", "label": "Nước uống", "slug": "nuoc-uong",
             "sub": "Quầy nước giải khát trong khuôn viên.", "items": []},
        ],
    },
]

# ─── CONTENT (rich text for selected pages) ───────────────────────────────────

CONTENT = {
    # ── A. Tham quan ─────────────────────────────────────────────────────────
    "tham-quan": """
<h2>Giờ mở cửa</h2>
<table class="info-table">
  <tr><th>Mùa hè (T4 – T10)</th><td>07:30 – 18:00 (mở hằng ngày)</td></tr>
  <tr><th>Mùa đông (T11 – T3)</th><td>08:00 – 17:00 (mở hằng ngày)</td></tr>
  <tr><th>Quầy bán vé</th><td>Đóng trước giờ đóng cửa 30 phút</td></tr>
</table>

<h2>Giá vé</h2>
<div class="price-table">
  <div class="price-row"><div class="price-cat"><p>Người lớn (từ 16 tuổi)</p></div><p class="price-val">30.000đ</p></div>
  <div class="price-row"><div class="price-cat"><p>Học sinh, sinh viên (có thẻ)</p></div><p class="price-val">15.000đ</p></div>
  <div class="price-row"><div class="price-cat"><p>Người cao tuổi (60+)</p></div><p class="price-val">15.000đ</p></div>
  <div class="price-row"><div class="price-cat"><p>Trẻ em dưới 15 tuổi</p></div><p class="price-val">Miễn phí</p></div>
</div>

<h2>Đường đến</h2>
<table class="info-table">
  <tr><th>Địa chỉ</th><td>58 Phố Quốc Tử Giám, Phường Văn Miếu, Quận Đống Đa, Hà Nội</td></tr>
  <tr><th>Xe buýt</th><td>Tuyến 02, 23, 38 — dừng tại Văn Miếu</td></tr>
  <tr><th>Bãi đỗ xe</th><td>Ô tô: phố Văn Miếu · Xe máy/xe đạp: Vườn Giám</td></tr>
</table>

<h2>Nội quy tham quan</h2>
<ol>
  <li>Quý khách phải mua vé và xuất trình tại nơi soát vé.</li>
  <li>Bảo vệ di tích, giữ gìn vệ sinh môi trường. Không sờ, viết, vẽ lên hiện vật, bia đá, công trình kiến trúc. Không giẫm cỏ, hái hoa, bẻ cành.</li>
  <li>Tuân thủ quy định phòng chống cháy nổ. Không hút thuốc trong khuôn viên.</li>
  <li>Trang phục lịch sự khi vào nơi thờ tự. Giữ yên tĩnh tại các nơi tôn nghiêm.</li>
  <li>Nghiêm cấm các hành vi mê tín, cờ bạc, lừa đảo.</li>
  <li>Khách chịu trách nhiệm pháp lý đối với tổn thất gây ra.</li>
  <li>Bảo vệ có quyền chấm dứt tham quan với khách vi phạm nội quy.</li>
  <li>Liên hệ phản ánh: 024.3747.1322 / 024.3211.5793.</li>
</ol>

<h2>Tiện ích</h2>
<ul>
  <li>Bãi đỗ xe ô tô (phố Văn Miếu) và xe máy/xe đạp (Vườn Giám)</li>
  <li>Café, quầy giải khát trong khuôn viên</li>
  <li>Quầy đồ lưu niệm tại lối ra</li>
  <li>Wifi miễn phí, ghế đá nghỉ chân, nhà vệ sinh công cộng</li>
</ul>
""",

    # ── B1. Lịch sử ──────────────────────────────────────────────────────────
    "ve-di-tich/lich-su/thoi-ly": """
<p>Văn Miếu được lập dưới thời Lý Thánh Tông, năm Canh Tuất, niên hiệu Thần Vũ thứ 2 (1070), là nơi thờ Khổng Tử, Chu Công và Tứ Phối. Đây là dấu mốc khởi đầu cho hệ thống giáo dục Nho học chính quy của Đại Việt.</p>
<h2>Sự kiện chính</h2>
<ul>
  <li><strong>1070</strong> — Lý Thánh Tông cho lập Văn Miếu thờ Khổng Tử</li>
  <li><strong>1076</strong> — Lý Nhân Tông lập Quốc Tử Giám — trường đại học đầu tiên của Việt Nam</li>
  <li><strong>1156</strong> — Lý Anh Tông cho tu sửa Văn Miếu, đặt riêng để thờ Khổng Tử</li>
</ul>
<p>Quốc Tử Giám ban đầu chỉ dành cho hoàng tử và con em quý tộc. Đến năm 1253, vua Trần Thái Tông mở rộng cho cả thường dân ưu tú vào học.</p>
""",
    "ve-di-tich/lich-su/thoi-tran": """
<p>Thời Trần (1225–1400), Văn Miếu – Quốc Tử Giám tiếp tục được duy trì và phát triển. Năm 1253, vua Trần Thái Tông cho mở rộng Quốc Tử Giám, đổi tên thành Quốc học viện, cho phép cả thường dân ưu tú vào học.</p>
<h2>Cải cách giáo dục</h2>
<ul>
  <li><strong>1253</strong> — Đổi Quốc Tử Giám thành Quốc học viện, mở cửa cho thường dân</li>
  <li><strong>1272</strong> — Lê Văn Hưu hoàn thành <em>Đại Việt sử ký</em> — bộ chính sử đầu tiên</li>
  <li><strong>1370</strong> — Tư nghiệp Chu Văn An được thờ tại Văn Miếu sau khi qua đời</li>
</ul>
<p>Chu Văn An — người thầy lớn của thời Trần — là vị danh nho đầu tiên được phối thờ tại Văn Miếu cùng Khổng Tử và Tứ Phối.</p>
""",
    "ve-di-tich/lich-su/thoi-le": """
<p>Sau khi đánh đuổi quân Minh (1428), triều Lê chính thức kiến lập và xây dựng lại Văn Miếu – Quốc Tử Giám với quy mô lớn hơn. Thời Lê là giai đoạn vàng son của khoa cử Nho học Việt Nam.</p>
<h2>82 Bia Tiến sĩ</h2>
<p>Từ năm 1484, theo lệnh vua Lê Thánh Tông, các bia Tiến sĩ bắt đầu được dựng. Trong 300 năm (1484–1780), 82 bia đá được lập, ghi danh 1.304 Tiến sĩ qua 82 kỳ thi Đình.</p>
<h2>Mốc lịch sử quan trọng</h2>
<ul>
  <li><strong>1442</strong> — Khoa thi Đình đầu tiên do Nhà nước Lê tổ chức</li>
  <li><strong>1484</strong> — Lê Thánh Tông cho dựng bia Tiến sĩ</li>
  <li><strong>1645</strong> — Khu kiến trúc đạt quy mô tương đối hoàn chỉnh thời Lê Trung hưng</li>
  <li><strong>1780</strong> — Bia Tiến sĩ cuối cùng được dựng (khoa Cảnh Hưng 40)</li>
</ul>
""",
    "ve-di-tich/lich-su/thoi-nguyen": """
<p>Dưới thời Nguyễn (1802–1945), Thăng Long không còn là Kinh đô. Quốc Tử Giám Hà Nội dần thu hẹp chức năng giáo dục — Quốc Tử Giám của triều Nguyễn được lập tại Huế. Văn Miếu Hà Nội chuyển thành nơi thờ tự là chính.</p>
<h2>Các cải biến kiến trúc</h2>
<ul>
  <li><strong>1805</strong> — Khuê Văn Các được xây dựng dưới thời Gia Long</li>
  <li><strong>1863</strong> — Tu sửa lớn dưới thời Tự Đức</li>
  <li><strong>1947</strong> — Pháp ném bom phá huỷ một phần kiến trúc Quốc Tử Giám cũ</li>
  <li><strong>1962</strong> — Văn Miếu được xếp hạng Di tích lịch sử văn hoá quốc gia</li>
  <li><strong>2010</strong> — UNESCO công nhận 82 Bia Tiến sĩ là Di sản tư liệu thế giới</li>
  <li><strong>2014</strong> — Văn Miếu – Quốc Tử Giám được công nhận Di tích Quốc gia đặc biệt</li>
</ul>
""",

    # ── B2. Phân khu ─────────────────────────────────────────────────────────
    "ve-di-tich/phan-khu/noi-tu": """
<p>Khu Nội tự là khu vực chính của di tích, kéo dài theo trục Bắc–Nam từ Cổng Văn Miếu đến khu Thái Học. Bao gồm 5 lớp sân, mỗi lớp có ý nghĩa riêng trong hệ thống biểu tượng Nho giáo.</p>
<h2>5 lớp sân</h2>
<ol>
  <li>Sân thứ nhất: Cổng Văn Miếu đến Đại Trung Môn</li>
  <li>Sân thứ hai: Đại Trung Môn đến Khuê Văn Các</li>
  <li>Sân thứ ba: Khuê Văn Các – Vườn bia Tiến sĩ – Giếng Thiên Quang</li>
  <li>Sân thứ tư: Đại Thành Môn – khu thờ chính (Đại Bái và Thượng Điện)</li>
  <li>Sân thứ năm: Khu Thái Học</li>
</ol>
""",
    "ve-di-tich/phan-khu/vuon-giam": """
<p>Vườn Giám là khu vườn cây xanh nằm phía bên trái khu Nội tự, tạo không gian thoáng đãng và là nơi đặt một số kiến trúc phụ trợ như Nhà Bát Giác.</p>
<p>Đây cũng là nơi bố trí bãi đỗ xe máy và xe đạp cho khách tham quan.</p>
<h2>Đặc điểm</h2>
<ul>
  <li>Nhiều cây cổ thụ tạo bóng mát quanh năm</li>
  <li>Nhà Bát Giác — kiến trúc 8 cạnh đặc trưng</li>
  <li>Không gian tổ chức các sự kiện văn hoá ngoài trời</li>
</ul>
""",
    "ve-di-tich/phan-khu/ho-van": """
<p>Hồ Văn nằm phía trước Văn Miếu Môn, ngăn cách với khu Nội tự bởi phố Quốc Tử Giám. Giữa hồ là gò Kim Châu — trên gò có đình Phán Thuỷ.</p>
<h2>Vai trò</h2>
<ul>
  <li>Theo phong thuỷ, Hồ Văn là tấm gương trí tuệ phản chiếu Văn Miếu</li>
  <li>Không gian tổ chức Hội thơ, Hội chữ Tết Nguyên đán hằng năm</li>
  <li>Địa điểm tổ chức sự kiện văn hoá ngoài trời</li>
</ul>
""",

    # ── B3. Kiến trúc (highlights) ────────────────────────────────────────────
    "ve-di-tich/kien-truc/bia-ha-ma": """
<p>Bia Hạ mã đặt ở hai bên cổng Văn Miếu, ghi dòng chữ Hán "Hạ mã" (下馬) — yêu cầu mọi người, kể cả vua chúa quan lại, phải xuống ngựa khi đi qua đây để tỏ lòng tôn kính nơi thờ Khổng Tử và Quốc Tử Giám.</p>
<h2>Đặc điểm</h2>
<ul>
  <li>Hai tấm bia đá cổ đặt ở vị trí cổng vào</li>
  <li>Khắc chữ Hán "Hạ mã" — hạ ngựa</li>
  <li>Biểu tượng tinh thần "tôn sư trọng đạo"</li>
</ul>
""",
    "ve-di-tich/kien-truc/cong-van-mieu": """
<p>Cổng Văn Miếu (Văn Miếu Môn) là cổng chính ở phía Nam, kiểu tam quan 3 cửa với 2 tầng mái. Cổng được xây thời Lê, trùng tu nhiều lần qua các thời kỳ.</p>
<h2>Đặc điểm kiến trúc</h2>
<ul>
  <li>Tam quan 3 cửa, 2 tầng mái cong</li>
  <li>Trên cổng có 4 chữ Hán "Văn Miếu Môn"</li>
  <li>Hai bên có Tứ trụ — bốn cột trụ cao</li>
  <li>Biểu tượng quen thuộc của di tích</li>
</ul>
""",
    "ve-di-tich/kien-truc/cong-dai-trung": """
<p>Cổng Đại Trung là cổng thứ hai, ngăn giữa sân thứ nhất và sân thứ hai. Cổng có 3 gian, mái cong kiểu truyền thống.</p>
<p>Hai bên cổng có hai cổng phụ: Đạt Tài (bên trái) và Thành Đức (bên phải) — tượng trưng cho hai phẩm chất cốt lõi của người quân tử.</p>
""",
    "ve-di-tich/kien-truc/khue-van-cac": """
<p>Khuê Văn Các được xây dựng năm 1805 dưới thời Gia Long, là biểu tượng tiêu biểu của Văn Miếu – Quốc Tử Giám và là biểu tượng văn hoá của Hà Nội.</p>
<h2>Kiến trúc đặc trưng</h2>
<ul>
  <li>Gác vuông 2 tầng, 8 mái</li>
  <li>Tầng dưới là 4 trụ gạch vuông</li>
  <li>Tầng trên có 4 cửa tròn — tượng trưng cho vầng sáng văn học</li>
  <li>Treo biển 4 chữ Hán "Khuê Văn Các"</li>
</ul>
<p>Năm 2012, Khuê Văn Các được chọn làm biểu tượng chính thức của Thủ đô Hà Nội.</p>
""",
    "ve-di-tich/kien-truc/nha-che-bia": """
<p>Hai dãy nhà che bia nằm hai bên giếng Thiên Quang, mỗi bên có 41 tấm bia đá Tiến sĩ — tổng cộng 82 tấm. Nhà che bia được xây để bảo vệ bia khỏi mưa nắng, gồm hai tầng mái lợp ngói.</p>
<h2>82 Bia Tiến sĩ</h2>
<ul>
  <li>Dựng từ 1484 đến 1780 — kéo dài 300 năm</li>
  <li>Ghi danh 1.304 Tiến sĩ qua 82 kỳ thi Đình</li>
  <li>Năm 2010 — UNESCO công nhận là Di sản tư liệu thế giới</li>
  <li>Năm 2015 — Bảo vật quốc gia</li>
</ul>
""",
    "ve-di-tich/kien-truc/cong-dai-thanh": """
<p>Cổng Đại Thành (Đại Thành Môn) là cổng vào khu thờ chính — Đại Bái Đường và Thượng Điện. Cổng 3 cửa, mái cong kiểu cung đình.</p>
<h2>Ý nghĩa tên gọi</h2>
<p>"Đại Thành" lấy từ câu của Mạnh Tử ca ngợi Khổng Tử: "Khổng Tử là tập đại thành" — người tổng kết toàn bộ tinh hoa của các bậc Thánh trước đó.</p>
""",
    "ve-di-tich/kien-truc/bai-duong": """
<p>Bái đường (Đại Bái Đường) là toà nhà chính trong khu thờ tự, nơi tổ chức các nghi lễ tế Khổng Tử và Tứ Phối. Toà nhà 9 gian rộng lớn, mái lợp ngói âm dương.</p>
<h2>Bố trí thờ tự</h2>
<ul>
  <li>Gian giữa: bàn thờ chính</li>
  <li>Hai bên: bàn thờ Tứ Phối — Nhan Hồi, Tăng Sâm, Tử Tư, Mạnh Tử</li>
  <li>Trong cùng là Thượng Điện — nơi đặt tượng Khổng Tử</li>
</ul>
""",
    "ve-di-tich/kien-truc/cong-thai-hoc": """
<p>Cổng Thái Học là cổng dẫn vào khu Thái Học — khu vực phía sau cùng của di tích, vốn là nơi đặt Quốc Tử Giám xưa.</p>
""",
    "ve-di-tich/kien-truc/thai-hoc": """
<p>Khu Thái Học được xây dựng lại vào năm 2000 trên nền cũ của trường Quốc Tử Giám. Khu vực gồm:</p>
<ul>
  <li><strong>Tiền Đường</strong> — thờ ba vị vua có công với Văn Miếu (Lý Thánh Tông, Lý Nhân Tông, Lê Thánh Tông) và Tư nghiệp Chu Văn An</li>
  <li><strong>Hậu Đường</strong> — không gian trưng bày thường xuyên</li>
  <li><strong>Nhà Đông Vũ – Tây Vũ</strong> — không gian triển lãm và sự kiện</li>
</ul>
""",
    "ve-di-tich/kien-truc/nha-chuong-trong": """
<p>Hai bên sân thứ hai của khu Nội tự đặt hai lầu đối xứng: Nhà Chuông (bên trái) và Nhà Trống (bên phải). Đây là kiến trúc chuông trống truyền thống của các đền miếu Việt Nam.</p>
""",
    "ve-di-tich/kien-truc/nha-bat-giac": """
<p>Nhà Bát Giác là kiến trúc 8 cạnh đặc trưng đặt trong khu Vườn Giám. Mái hình bát giác, 8 cột chống tạo không gian thoáng đãng.</p>
""",
    "ve-di-tich/kien-truc/phuong-dinh": """
<p>Phương đình là kiến trúc đình vuông nhỏ, đặt trong khuôn viên di tích, có chức năng nghỉ chân và thưởng cảnh.</p>
""",

    # ── B4. Danh nhân ────────────────────────────────────────────────────────
    "ve-di-tich/danh-nhan/vua-ly-thanh-tong": """
<p>Lý Thánh Tông (1023–1072) là vị vua thứ ba của triều Lý. Năm Canh Tuất (1070), vua cho lập Văn Miếu — đặt nền móng cho hệ thống giáo dục Nho học chính quy của Đại Việt.</p>
<h2>Đóng góp</h2>
<ul>
  <li>Lập Văn Miếu năm 1070 — thờ Khổng Tử, Chu Công, Tứ Phối</li>
  <li>Đặt nền móng cho việc học Nho học chính quy</li>
  <li>Mở rộng lãnh thổ và củng cố quốc gia Đại Việt</li>
</ul>
""",
    "ve-di-tich/danh-nhan/vua-ly-nhan-tong": """
<p>Lý Nhân Tông (1066–1128) là con trai Lý Thánh Tông. Năm 1076, vua cho lập Quốc Tử Giám trong khuôn viên Văn Miếu — trường đại học đầu tiên của Việt Nam.</p>
<h2>Đóng góp</h2>
<ul>
  <li>Lập Quốc Tử Giám năm 1076 — trường đại học đầu tiên của nước Việt</li>
  <li>Mở khoa thi Tam trường năm 1075 — kỳ thi đầu tiên chọn nhân tài cho triều đình</li>
  <li>Phát triển nền giáo dục và học thuật thời Lý</li>
</ul>
""",
    "ve-di-tich/danh-nhan/vua-le-thanh-tong": """
<p>Lê Thánh Tông (1442–1497) là vị vua thứ năm triều Lê sơ — một trong những vị vua xuất sắc nhất trong lịch sử Việt Nam.</p>
<h2>Đóng góp với Văn Miếu</h2>
<ul>
  <li>Năm 1484 — ban chiếu dựng bia Tiến sĩ tại Văn Miếu</li>
  <li>Khuyến khích Nho học và khoa cử phát triển mạnh</li>
  <li>Soạn thảo bộ luật Hồng Đức — bộ luật toàn diện đầu tiên của Việt Nam</li>
  <li>Mở rộng lãnh thổ về phương Nam</li>
</ul>
""",
    "ve-di-tich/danh-nhan/chu-van-an": """
<p>Chu Văn An (1292–1370) là nhà giáo lỗi lạc thời Trần, được xem là "ông tổ" của nền giáo dục Việt Nam. Ông giữ chức Tư nghiệp Quốc Tử Giám — phụ trách giáo dục quốc gia.</p>
<h2>Sự nghiệp</h2>
<ul>
  <li>Tư nghiệp Quốc Tử Giám — dạy thái tử và quan lại</li>
  <li>Soạn thảo "Thất trảm sớ" — đề nghị chém 7 nịnh thần</li>
  <li>Tác giả "Tứ thư thuyết ước" — chú giải Tứ thư</li>
</ul>
<p>Sau khi qua đời, Chu Văn An được phối thờ tại Văn Miếu cùng Khổng Tử và Tứ Phối — vinh dự hiếm có dành cho một người Việt.</p>
""",
    "ve-di-tich/danh-nhan/khoa-bang": """
<p>Trong 300 năm (1442–1779), 1.304 vị Tiến sĩ đỗ qua 82 kỳ thi Đình được khắc tên trên 82 bia đá tại vườn bia. Đây là di sản nhân lực và trí tuệ quý báu của Đại Việt.</p>
<h2>Các danh nhân tiêu biểu</h2>
<ul>
  <li><strong>Nguyễn Trãi</strong> — đỗ Thái học sinh năm 1400, anh hùng dân tộc, nhà văn hoá lớn</li>
  <li><strong>Lê Quý Đôn</strong> — đỗ Tiến sĩ 1752, bác học lớn nhất thế kỷ 18</li>
  <li><strong>Nguyễn Bỉnh Khiêm</strong> — đỗ Trạng nguyên 1535, nhà tiên tri Trạng Trình</li>
  <li><strong>Ngô Sĩ Liên</strong> — đỗ Tiến sĩ 1442, soạn <em>Đại Việt sử ký toàn thư</em></li>
</ul>
<h2>Các dòng họ khoa bảng</h2>
<ul>
  <li>Dòng họ Nguyễn Quán Nho (Thanh Hoá)</li>
  <li>Dòng họ Phan Huy (Hà Tĩnh)</li>
  <li>Dòng họ Ngô Thì (Hà Nội)</li>
</ul>
""",

    # ── B5. Tượng thờ ────────────────────────────────────────────────────────
    "ve-di-tich/tuong-tho/khong-tu": """
<p>Khổng Tử (孔子, 551–479 TCN) là nhà tư tưởng, nhà giáo dục lớn nhất Trung Quốc cổ đại — người sáng lập Nho giáo. Tượng Khổng Tử được đặt ở vị trí trung tâm của Thượng Điện trong khu Đại Thành.</p>
<h2>Vị trí tại Văn Miếu</h2>
<ul>
  <li>Tượng đặt tại Thượng Điện (Đại Thành Điện) — vị trí trung tâm</li>
  <li>Là đối tượng thờ chính tại Văn Miếu từ năm 1070</li>
  <li>Lễ tế Khổng Tử (Tế Khổng) tổ chức hằng năm vào mùa Xuân và mùa Thu</li>
</ul>
""",
    "ve-di-tich/tuong-tho/nhan-tu": """
<p>Nhan Tử (顔子) — tên thật Nhan Hồi (顔回), tự Tử Uyên — là học trò xuất sắc nhất của Khổng Tử. Ông được phong là Phục Thánh — một trong Tứ Phối thờ cùng Khổng Tử.</p>
<p>Nhan Tử nổi tiếng là người ham học, sống thanh đạm. Khổng Tử từng khen: "Hiền tai, Hồi dã!" (Hiền tài thay, Hồi vậy!)</p>
""",
    "ve-di-tich/tuong-tho/tu-tu": """
<p>Tử Tư (子思, 483–402 TCN) — tên thật Khổng Cấp — là cháu nội Khổng Tử, học trò Tăng Tử. Ông được phong là Thuật Thánh — một trong Tứ Phối.</p>
<p>Tử Tư là tác giả <em>Trung Dung</em> (中庸) — một trong Tứ Thư của Nho giáo.</p>
""",
    "ve-di-tich/tuong-tho/tang-tu": """
<p>Tăng Tử (曾子, 505–435 TCN) — tên thật Tăng Sâm — là học trò trẻ tuổi và xuất sắc của Khổng Tử. Ông được phong là Tông Thánh — một trong Tứ Phối.</p>
<p>Tăng Tử là tác giả <em>Đại Học</em> (大學) — một trong Tứ Thư của Nho giáo. Ông cũng là thầy của Tử Tư — cháu nội Khổng Tử.</p>
""",
    "ve-di-tich/tuong-tho/manh-tu": """
<p>Mạnh Tử (孟子, 372–289 TCN) — tên thật Mạnh Kha — là nhà tư tưởng lớn của Nho giáo, sống sau Khổng Tử khoảng 100 năm. Ông được phong là Á Thánh — vị trí thứ hai sau Khổng Tử.</p>
<p>Mạnh Tử là tác giả <em>Mạnh Tử</em> — một trong Tứ Thư. Ông phát triển học thuyết "tính bản thiện" — bản chất con người vốn thiện.</p>
""",

    # ── B6. Thư viện ─────────────────────────────────────────────────────────
    "ve-di-tich/thu-vien/thu-vien-anh": """
<p>Bộ sưu tập ảnh tư liệu về Văn Miếu – Quốc Tử Giám qua các thời kỳ. Bao gồm ảnh tư liệu lịch sử, ảnh kiến trúc và ảnh các sự kiện văn hoá tại di tích.</p>
<div class="gallery">
  <div class="gallery-item"><img src="../../../assets/images/lich-su/hero.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/lich-su/ho-van.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/lich-su/bia.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/lich-su/nha-bia.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/kien-truc/cong-dai-thanh.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/kien-truc/cong-dai-trung.jpg" alt="" loading="lazy"></div>
</div>
""",
    "ve-di-tich/thu-vien/video": """
<p>Tư liệu video về di tích Văn Miếu – Quốc Tử Giám: phim tài liệu lịch sử, video giới thiệu và các chương trình truyền hình về di sản.</p>
<div class="note">Liên hệ Phòng Truyền thông để được cung cấp tư liệu phục vụ nghiên cứu, học tập và truyền thông.</div>
<h2>Các chủ đề video</h2>
<ul>
  <li>Phim tài liệu "Văn Miếu – Hơn 950 năm" (2020)</li>
  <li>Phim ngắn "82 Bia Tiến sĩ — Di sản tư liệu thế giới" (2018)</li>
  <li>Tour ảo Văn Miếu – Quốc Tử Giám (2022)</li>
  <li>Series về kiến trúc và nghệ thuật trang trí</li>
</ul>
""",

    # ── C1. Trưng bày cố định ─────────────────────────────────────────────────
    "trung-bay-trien-lam/co-dinh/truong-quoc-hoc": """
<p>Khu trưng bày "Quốc Tử Giám – Trường quốc học đầu tiên" giới thiệu lịch sử hình thành, phát triển và vai trò của Quốc Tử Giám trong nền giáo dục Việt Nam thời phong kiến.</p>
<h2>Nội dung trưng bày</h2>
<ul>
  <li>Lịch sử thành lập Quốc Tử Giám (1076 – nay)</li>
  <li>Hệ thống tổ chức và bộ máy quản lý</li>
  <li>Chương trình đào tạo qua các thời kỳ</li>
  <li>Những danh nhân tiêu biểu của Quốc Tử Giám</li>
</ul>
""",
    "trung-bay-trien-lam/co-dinh/khoi-nguon-dao-hoc": """
<p>Khu trưng bày "Khơi nguồn đạo học" tập trung giới thiệu hệ thống Nho học Việt Nam — từ tư tưởng Khổng Tử đến các thế hệ học trò Việt Nam tiêu biểu.</p>
<h2>Nội dung trưng bày</h2>
<ul>
  <li>Tư tưởng và triết lý Nho học</li>
  <li>Hệ thống thờ tự và lễ nghi</li>
  <li>Các tác phẩm kinh điển và sách giáo khoa</li>
  <li>Văn phòng tứ bảo (bút, mực, nghiên, giấy) qua các thời kỳ</li>
</ul>
""",
    "trung-bay-trien-lam/co-dinh/su-da-luu-danh": """
<p>Khu trưng bày "Sử đá lưu danh" giới thiệu hệ thống 82 Bia Tiến sĩ — Di sản tư liệu thế giới được UNESCO công nhận năm 2010.</p>
<h2>Nội dung trưng bày</h2>
<ul>
  <li>Lịch sử dựng bia Tiến sĩ (1484 – 1780)</li>
  <li>Bản dập bia gốc và phiên bản nghệ thuật</li>
  <li>Nội dung văn bia và ý nghĩa</li>
  <li>Quá trình bảo tồn và phát huy giá trị di sản</li>
</ul>
""",

    # ── E. Dịch vụ ───────────────────────────────────────────────────────────
    "dich-vu/tour-dem": """
<p>Tour đêm Văn Miếu – Quốc Tử Giám mang đến trải nghiệm khám phá di tích dưới ánh đèn nghệ thuật, kết hợp công nghệ ánh sáng hiện đại với nghệ thuật trình diễn truyền thống.</p>
<h2>Thông tin tour</h2>
<table class="info-table">
  <tr><th>Thời gian</th><td>19:30 – 21:30 (Thứ 6, 7, Chủ nhật)</td></tr>
  <tr><th>Quy mô</th><td>Tối đa 30 người/tour</td></tr>
  <tr><th>Ngôn ngữ</th><td>Tiếng Việt; tiếng Anh theo yêu cầu</td></tr>
  <tr><th>Đặt trước</th><td>Tối thiểu 2 ngày</td></tr>
</table>
<h2>Chương trình</h2>
<ul>
  <li>Tham quan 5 khu vực dưới ánh đèn nghệ thuật</li>
  <li>Hướng dẫn viên kể chuyện lịch sử và truyền thuyết</li>
  <li>Biểu diễn nghệ thuật truyền thống tại Khuê Văn Các</li>
  <li>Trải nghiệm viết thư pháp dưới ánh nến</li>
</ul>
""",
    "dich-vu/audio-guide": """
<p>Thuyết minh tự động giúp Quý khách tham quan theo tốc độ riêng với nội dung chuyên sâu tại từng điểm di tích.</p>
<h2>Ngôn ngữ</h2>
<p>Có sẵn 8 ngôn ngữ: Việt, Anh, Pháp, Tây Ban Nha, Hàn, Nhật, Trung, Thái.</p>
<h2>Giá thuê thiết bị</h2>
<div class="price-table">
  <div class="price-row"><div class="price-cat"><p>Tiếng Việt</p></div><p class="price-val">30.000đ</p></div>
  <div class="price-row"><div class="price-cat"><p>Tiếng nước ngoài</p></div><p class="price-val">50.000đ</p></div>
</div>
<div class="note">Liên hệ cán bộ tại quầy bán vé để thuê thiết bị.</div>
""",
    "dich-vu/huong-dan-vien": """
<p>Đội ngũ hướng dẫn viên chuyên nghiệp được đào tạo về lịch sử, văn hoá và kiến trúc Văn Miếu — phục vụ thuyết minh chuyên sâu tại từng điểm di tích.</p>
<h2>Ngôn ngữ</h2>
<ul>
  <li>Tiếng Việt</li>
  <li>Tiếng Anh</li>
  <li>Tiếng Pháp</li>
  <li>Tiếng Trung Quốc</li>
</ul>
<h2>Đặt dịch vụ</h2>
<table class="info-table">
  <tr><th>Điện thoại</th><td>024.3823.5601</td></tr>
  <tr><th>Đặt trước</th><td>Tối thiểu 1 ngày</td></tr>
  <tr><th>Nhóm tối thiểu</th><td>5 người</td></tr>
</table>
""",
    "dich-vu/qua-luu-niem": """
<p>Quầy quà lưu niệm cung cấp các sản phẩm mang bản sắc văn hoá Văn Miếu — Quốc Tử Giám.</p>
<h2>Sản phẩm tiêu biểu</h2>
<ul>
  <li>Sách, ấn phẩm về Văn Miếu, di sản Hà Nội và Nho học</li>
  <li>Bản dập bia Tiến sĩ (phiên bản nghệ thuật)</li>
  <li>Đồ gốm, đồ đồng phong cách truyền thống</li>
  <li>Văn phòng phẩm phong cách cổ — bút, mực, nghiên, giấy</li>
  <li>Áo dài, phụ kiện mang hoạ tiết Văn Miếu</li>
</ul>
<table class="info-table">
  <tr><th>Vị trí</th><td>Lối ra chính và khu Thái Học</td></tr>
  <tr><th>Giờ mở cửa</th><td>Theo giờ tham quan di tích</td></tr>
</table>
""",
    "dich-vu/thu-phap": """
<p>Trải nghiệm viết chữ thư pháp tại Văn Miếu — kết hợp giữa nghệ thuật và di sản, mang lại không gian thư thái và ý nghĩa văn hoá sâu sắc cho Quý khách.</p>
<h2>Hoạt động</h2>
<ul>
  <li>Hướng dẫn viết chữ thư pháp Việt và Hán</li>
  <li>Xin chữ đầu năm — phong tục truyền thống</li>
  <li>Lớp học thư pháp ngắn hạn (cuối tuần)</li>
  <li>Workshop thư pháp cho nhóm</li>
</ul>
<table class="info-table">
  <tr><th>Vị trí</th><td>Khu Hồ Văn (đặc biệt dịp Tết)</td></tr>
  <tr><th>Liên hệ</th><td>024.3747.1322</td></tr>
</table>
""",
    "dich-vu/nuoc-uong": """
<p>Quầy nước giải khát phục vụ Quý khách trong khuôn viên di tích.</p>
<h2>Sản phẩm</h2>
<ul>
  <li>Nước suối đóng chai</li>
  <li>Nước trà thảo mộc, trà sen</li>
  <li>Cà phê, trà sữa</li>
  <li>Nước trái cây tự nhiên</li>
</ul>
<table class="info-table">
  <tr><th>Vị trí</th><td>Sân Tiền Đường khu Thái Học, lối ra</td></tr>
  <tr><th>Giờ mở cửa</th><td>Theo giờ tham quan di tích</td></tr>
</table>
""",

    # ── D. Hoạt động ─────────────────────────────────────────────────────────
    "cac-hoat-dong/giao-duc-di-san": """
<p>Chương trình giáo dục di sản dành cho học sinh từ mầm non đến THPT — giúp các em trải nghiệm và hiểu về di sản văn hoá dân tộc.</p>
<h2>Chương trình theo cấp học</h2>
<ul>
  <li><strong>Mầm non (3–5 tuổi)</strong> — Tham quan, kể chuyện, vẽ và tô màu</li>
  <li><strong>Tiểu học lớp 1–3</strong> — Trò chơi dân gian, thực hành viết chữ</li>
  <li><strong>Tiểu học lớp 4–6</strong> — Tìm hiểu bia Tiến sĩ, thực hành in dập</li>
  <li><strong>THCS, THPT (lớp 7–12)</strong> — Nghiên cứu chuyên sâu, hội thảo học sinh</li>
</ul>
<table class="info-table">
  <tr><th>Liên hệ</th><td>0369.087.468 (Phòng Giáo dục – Truyền thông)</td></tr>
  <tr><th>Đặt trước</th><td>Tối thiểu 3 ngày</td></tr>
  <tr><th>Nhóm tối thiểu</th><td>15 học sinh</td></tr>
</table>
""",
    "cac-hoat-dong/trai-nghiem": """
<p>Các hoạt động trải nghiệm thực tế dành cho khách tham quan và nhóm học tập.</p>
<h2>Các hoạt động chính</h2>
<ul>
  <li>Trải nghiệm in dập bia Tiến sĩ</li>
  <li>Viết thư pháp Việt – Hán</li>
  <li>Trò chơi dân gian truyền thống</li>
  <li>Tham quan có hướng dẫn theo chủ đề</li>
  <li>Tìm hiểu nghi lễ Nho giáo</li>
</ul>
""",
    "cac-hoat-dong/van-hoa-nghe-thuat": """
<p>Các chương trình văn hoá nghệ thuật tổ chức tại Văn Miếu — giới thiệu nghệ thuật truyền thống Việt Nam đến công chúng.</p>
<h2>Các loại hình</h2>
<ul>
  <li>Nhạc cổ truyền — ca trù, chầu văn, quan họ</li>
  <li>Múa cung đình</li>
  <li>Hát xẩm, hát chèo</li>
  <li>Biểu diễn áo dài</li>
</ul>
""",
    "cac-hoat-dong/hoi-thao": """
<p>Các hội thảo khoa học và toạ đàm tổ chức tại Văn Miếu — Quốc Tử Giám về di sản, lịch sử và giáo dục.</p>
<h2>Các chủ đề</h2>
<ul>
  <li>Bảo tồn và phát huy di sản Hán – Nôm</li>
  <li>Lịch sử khoa cử Nho học Việt Nam</li>
  <li>Bia Tiến sĩ và giá trị di sản tư liệu thế giới</li>
  <li>Giáo dục di sản trong nhà trường</li>
  <li>Du lịch di sản và phát triển bền vững</li>
</ul>
""",
    "cac-hoat-dong/doan-ngoai-giao": """
<p>Văn Miếu – Quốc Tử Giám là điểm đến quan trọng trong các chương trình tiếp đón đoàn ngoại giao và lãnh đạo các nước đến thăm Việt Nam.</p>
<h2>Dịch vụ tiếp đón</h2>
<ul>
  <li>Tham quan có hướng dẫn viên ngoại ngữ chuyên nghiệp</li>
  <li>Lễ tiếp đón theo nghi thức truyền thống</li>
  <li>Quà lưu niệm văn hoá đặc biệt</li>
  <li>Phối hợp với cơ quan ngoại giao</li>
</ul>
""",
    "cac-hoat-dong/workshop": """
<p>Các workshop sáng tạo và trải nghiệm văn hoá tại Văn Miếu.</p>
<h2>Các workshop tiêu biểu</h2>
<ul>
  <li>Workshop thư pháp Hán – Nôm</li>
  <li>Workshop in dập bia Tiến sĩ</li>
  <li>Workshop làm bút lông truyền thống</li>
  <li>Workshop làm sách Nho học</li>
  <li>Workshop nghệ thuật cắt giấy</li>
</ul>
<table class="info-table">
  <tr><th>Đối tượng</th><td>Mọi lứa tuổi (theo từng workshop)</td></tr>
  <tr><th>Đặt trước</th><td>Tối thiểu 5 ngày</td></tr>
</table>
""",
    "cac-hoat-dong/su-kien/sap-dien-ra": """
<p>Lịch các sự kiện sắp diễn ra tại Văn Miếu – Quốc Tử Giám.</p>
<div class="note">Lịch sự kiện được cập nhật theo từng tháng. Liên hệ 024.3747.1322 để biết thông tin chi tiết.</div>
<h2>Sự kiện thường niên</h2>
<ul>
  <li><strong>Tết Nguyên đán</strong> — Lễ khai bút, dâng hương Khổng Tử, Hội chữ Xuân</li>
  <li><strong>Rằm tháng Giêng</strong> — Ngày Thơ Việt Nam, hội thơ tại Khuê Văn Các</li>
  <li><strong>Tháng 9</strong> — Lễ tế Khổng Tử mùa Thu</li>
  <li><strong>23/11</strong> — Ngày Di sản Văn hoá Việt Nam</li>
</ul>
""",
    "cac-hoat-dong/su-kien/dang-dien-ra": """
<p>Các sự kiện đang diễn ra tại Văn Miếu – Quốc Tử Giám.</p>
<div class="note">Cập nhật theo thời gian thực. Vui lòng kiểm tra lại thông tin trước khi tham gia.</div>
""",
}

# ─── CSS ──────────────────────────────────────────────────────────────────────

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px;-webkit-text-size-adjust:100%}
body{
  font-family:'Inter',ui-sans-serif,system-ui,-apple-system,sans-serif;
  background:#f7f7f5;color:#111110;line-height:1.65;
}
a{color:inherit;text-decoration:none}
img{display:block;max-width:100%}
ul,ol{list-style:none}

.container{max-width:1200px;margin:0 auto;padding:0 1.5rem}

/* ── HEADER ── */
.site-header{
  background:#111110;color:#fff;
  position:sticky;top:0;z-index:100;
  border-bottom:1px solid #222;
}
.header-inner{
  display:flex;align-items:center;gap:2rem;
  max-width:1200px;margin:0 auto;padding:0 1.5rem;
  height:60px;
}
.brand{display:flex;align-items:center;gap:.7rem;flex-shrink:0}
.brand-mark{
  width:34px;height:34px;
  border:1.5px solid rgba(255,255,255,.35);
  display:flex;align-items:center;justify-content:center;
  font-size:.7rem;font-weight:700;letter-spacing:.05em;
}
.brand-text{display:flex;flex-direction:column}
.brand-name{font-size:.8rem;font-weight:600;line-height:1.2;color:#fff}
.brand-sub{font-size:.58rem;color:rgba(255,255,255,.4);letter-spacing:.06em;text-transform:uppercase}

/* ── NAV ── */
.main-nav{display:flex;align-items:center;flex:1}
.nav-item{position:relative;display:flex;align-items:center}
.nav-item > a{
  font-size:.78rem;color:rgba(255,255,255,.65);
  padding:.5rem .85rem;font-weight:400;white-space:nowrap;
  display:block;height:60px;line-height:46px;
}
.nav-item > a:hover,.nav-item.active > a{color:#fff}
.nav-item.has-menu > a::after{
  content:' ▾';font-size:.65rem;opacity:.6;margin-left:.15rem;
}
.nav-cta{
  margin-left:auto;
  border:1px solid rgba(255,255,255,.4);
  padding:.4rem 1rem;
  color:#fff;font-size:.76rem;font-weight:500;
  flex-shrink:0;
}
.nav-cta:hover{background:#fff;color:#111110}

/* ── DROPDOWN ── */
.dropdown{
  display:none;
  position:absolute;top:100%;left:0;
  background:#fff;color:#111110;
  border:1px solid #e4e4df;
  min-width:240px;padding:.6rem 0;
  box-shadow:0 8px 24px rgba(0,0,0,.04);
  z-index:50;
}
.nav-item:hover .dropdown,.nav-item:focus-within .dropdown{display:block}
.dropdown a{
  display:block;
  padding:.55rem 1.25rem;
  font-size:.8rem;color:#444;
  white-space:nowrap;
}
.dropdown a:hover{background:#f7f7f5;color:#111110}
.dropdown-num{
  display:inline-block;
  font-size:.6rem;color:#bbb;font-weight:600;
  margin-right:.5rem;letter-spacing:.04em;
  min-width:1.8rem;
}

/* ── MEGA MENU ── */
.dropdown.mega{
  display:none;left:50%;transform:translateX(-50%);
  width:1100px;max-width:calc(100vw - 2rem);
  padding:1.5rem;
  grid-template-columns:repeat(6,1fr);
  gap:1.5rem;
}
.nav-item:hover .dropdown.mega{display:grid}
.mega-col{}
.mega-col-title{
  font-size:.68rem;font-weight:700;color:#111110;
  letter-spacing:.04em;margin-bottom:.55rem;
  padding-bottom:.4rem;border-bottom:1px solid #e4e4df;
}
.mega-col-title a{color:#111110}
.mega-col ul{display:flex;flex-direction:column;gap:.05rem;margin-top:.3rem}
.mega-col li a{
  display:block;font-size:.74rem;color:#666;
  padding:.3rem 0;line-height:1.4;
}
.mega-col li a:hover{color:#111110}

/* Dropdown for sub-groups (C, D, E) */
.dropdown.simple{padding:.5rem 0}
.dropdown.simple .group-title{
  display:block;padding:.5rem 1.25rem .15rem;
  font-size:.62rem;font-weight:700;color:#bbb;
  letter-spacing:.06em;text-transform:uppercase;
}

/* ── BREADCRUMB ── */
.breadcrumb{
  background:#fff;border-bottom:1px solid #e4e4df;
  padding:.6rem 0;font-size:.73rem;color:#999;
}
.breadcrumb a{color:#666}
.breadcrumb a:hover{color:#111110}
.breadcrumb .sep{margin:0 .4rem;color:#ccc}

/* ── HERO ── */
.hero{position:relative;overflow:hidden;background:#ddd}
.hero-img{
  width:100%;height:420px;object-fit:cover;display:block;
  filter:grayscale(100%) contrast(.85) brightness(1.08);
}
.hero-overlay{
  position:absolute;inset:0;
  background:linear-gradient(to top,rgba(0,0,0,.55) 0%,rgba(0,0,0,.1) 55%,transparent 100%);
}
.hero-content{
  position:absolute;bottom:0;left:0;right:0;
  padding:2.5rem 3rem;color:#fff;
  max-width:1260px;margin:0 auto;
}
.hero-title{font-size:2.2rem;font-weight:700;letter-spacing:-.02em;line-height:1.15;margin-bottom:.5rem}
.hero-sub{font-size:.95rem;opacity:.75;max-width:560px}

/* ── QUICK INFO ── */
.quick-bar{background:#fff;border-bottom:1px solid #e4e4df}
.quick-bar-inner{display:flex;max-width:1200px;margin:0 auto;padding:0 1.5rem}
.quick-item{flex:1;padding:1.2rem 1rem;border-right:1px solid #e4e4df}
.quick-item:first-child{padding-left:0}
.quick-item:last-child{border-right:none;padding-right:0}
.quick-label{font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;color:#aaa;margin-bottom:.25rem;font-weight:500}
.quick-value{font-size:.88rem;font-weight:500;color:#111110}

/* ── PAGE HEADER ── */
.page-hd{background:#fff;border-bottom:1px solid #e4e4df;padding:2.5rem 0 2rem}
.page-title{font-size:1.95rem;font-weight:700;letter-spacing:-.02em;color:#111110;margin-bottom:.5rem}
.page-sub{font-size:.95rem;color:#777;max-width:640px;line-height:1.65}

/* ── CONTENT ── */
.content{padding:2.5rem 0 4rem}
.content-inner{display:grid;grid-template-columns:1fr 280px;gap:3rem;align-items:start}

/* ── GRID ── */
.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:1.25rem}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:1.25rem}

/* ── CARD ── */
.card{display:block;background:#fff;border:1px solid #e4e4df;overflow:hidden}
.card:hover{border-color:#bbb}
.card-img{aspect-ratio:16/9;background:#ebebE8;overflow:hidden;position:relative}
.card-img img{width:100%;height:100%;object-fit:cover;filter:grayscale(100%) contrast(.85) brightness(1.06)}
.card-img-ph{width:100%;height:100%;background:#e8e8e4;display:flex;align-items:center;justify-content:center}
.card-img-ph span{font-size:.65rem;color:#bbb;text-transform:uppercase;letter-spacing:.06em}
.card-body{padding:1.2rem}
.card-num{font-size:.62rem;color:#bbb;font-weight:600;letter-spacing:.06em;margin-bottom:.5rem}
.card-title{font-size:.92rem;font-weight:600;color:#111110;margin-bottom:.4rem;line-height:1.4}
.card-desc{font-size:.78rem;color:#777;line-height:1.55}
.card-arrow{display:inline-block;margin-top:.8rem;font-size:.72rem;color:#aaa}

/* Compact card for many items */
.card.compact .card-img{aspect-ratio:4/3}
.card.compact .card-body{padding:.85rem 1rem 1rem}
.card.compact .card-title{font-size:.83rem;margin-bottom:.2rem}
.card.compact .card-desc{font-size:.72rem;line-height:1.5}

/* ── ARTICLE ── */
.article{max-width:720px}
.article h1{font-size:1.7rem;font-weight:700;letter-spacing:-.02em;margin-bottom:1.5rem}
.article h2{font-size:1.2rem;font-weight:600;margin:2rem 0 .65rem;letter-spacing:-.01em}
.article h3{font-size:1rem;font-weight:600;margin:1.5rem 0 .45rem}
.article p{margin-bottom:.95rem;color:#444;line-height:1.8}
.article li{color:#444;line-height:1.7;margin-bottom:.4rem;padding-left:.25rem}
.article ul{list-style:disc;margin:.5rem 0 1rem 1.25rem}
.article ol{list-style:decimal;margin:.5rem 0 1rem 1.4rem}
.article strong{color:#111110;font-weight:600}
.article em{font-style:italic}
.article-hero{margin:0 0 2rem;aspect-ratio:16/9;background:#e8e8e4;overflow:hidden;border:1px solid #e4e4df}
.article-hero img{width:100%;height:100%;object-fit:cover;filter:grayscale(100%) contrast(.85) brightness(1.06)}

/* ── INFO TABLE ── */
.info-table{width:100%;border-collapse:collapse;margin:1.5rem 0;border:1px solid #e4e4df}
.info-table th,.info-table td{padding:.75rem 1rem;text-align:left;border-bottom:1px solid #e4e4df;font-size:.875rem}
.info-table tr:last-child th,.info-table tr:last-child td{border-bottom:none}
.info-table th{font-weight:600;background:#f7f7f5;width:35%;color:#444}
.info-table td{color:#444}

/* ── PRICE TABLE ── */
.price-table{border:1px solid #e4e4df;margin:1.5rem 0;background:#fff}
.price-row{display:flex;align-items:center;border-bottom:1px solid #e4e4df;padding:1rem 1.25rem;gap:1.5rem}
.price-row:last-child{border:none}
.price-cat{flex:1;font-size:.9rem;color:#444}
.price-val{font-size:1.1rem;font-weight:600;color:#111110;white-space:nowrap}

/* ── SIDEBAR ── */
.sidebar-box{border:1px solid #e4e4df;background:#fff;padding:1.25rem;margin-bottom:1rem}
.sidebar-title{font-size:.65rem;text-transform:uppercase;letter-spacing:.08em;color:#aaa;margin-bottom:.75rem;font-weight:600}
.sidebar-links li{padding:.4rem 0;border-bottom:1px solid #f0f0ec}
.sidebar-links li:last-child{border:none}
.sidebar-links a{font-size:.8rem;color:#444;display:block}
.sidebar-links a:hover{color:#111110}
.sidebar-links a.active{font-weight:600;color:#111110}
.sidebar-cta{display:block;background:#111110;color:#fff;padding:.95rem 1.25rem;text-align:center;font-size:.8rem;font-weight:500}

/* ── HOME SECTIONS ── */
.sections-overview{padding:2.5rem 0 3.5rem}
.sections-title{font-size:.7rem;font-weight:600;color:#888;letter-spacing:.1em;text-transform:uppercase;margin-bottom:1.25rem}
.sections-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:#e4e4df;border:1px solid #e4e4df}
.section-block{background:#fff;padding:1.75rem 1.5rem;display:flex;flex-direction:column;gap:.6rem}
.section-block:hover{background:#fafaf8}
.section-block-num{font-size:.62rem;font-weight:700;color:#ccc;letter-spacing:.1em}
.section-block-name{font-size:.95rem;font-weight:600;color:#111110;line-height:1.35}
.section-block-sub{font-size:.74rem;color:#999;line-height:1.6}
.section-block-count{margin-top:auto;padding-top:.85rem;border-top:1px solid #f0f0ec;font-size:.66rem;color:#bbb;letter-spacing:.04em}

/* ── GALLERY ── */
.gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#e4e4df;border:1px solid #e4e4df;margin:1.5rem 0}
.gallery-item{background:#fff;aspect-ratio:4/3;overflow:hidden}
.gallery-item img{width:100%;height:100%;object-fit:cover;filter:grayscale(100%) contrast(.85) brightness(1.06)}

/* ── FOOTER ── */
.site-footer{background:#111110;color:rgba(255,255,255,.55);padding:3rem 0 2rem}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:2rem;margin-bottom:2rem}
.footer-brand{font-size:.85rem;font-weight:600;color:#fff;margin-bottom:.6rem}
.footer-address{font-size:.76rem;line-height:1.85}
.footer-col-title{font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;color:rgba(255,255,255,.3);margin-bottom:.85rem;font-weight:600}
.footer-links li{padding:.3rem 0}
.footer-links a{font-size:.76rem;color:rgba(255,255,255,.5)}
.footer-links a:hover{color:rgba(255,255,255,.85)}
.footer-copy{border-top:1px solid rgba(255,255,255,.08);padding-top:1.5rem;font-size:.72rem;color:rgba(255,255,255,.25)}

/* ── UTILITY ── */
.label{display:inline-block;font-size:.62rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;border:1px solid #ddd;padding:.2rem .55rem;color:#888;margin-bottom:.75rem}
.note{background:#fff;border-left:2px solid #ccc;padding:.9rem 1.1rem;font-size:.82rem;color:#666;line-height:1.65;margin:1.25rem 0;border-top:1px solid #e4e4df;border-right:1px solid #e4e4df;border-bottom:1px solid #e4e4df}

/* ── HEADER TOOLS (search + language) ── */
.header-tools{display:flex;align-items:center;gap:.6rem;flex-shrink:0;margin-left:auto}
.search-wrap{position:relative}
.search-input{
  background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.18);
  color:#fff;font:inherit;font-size:.74rem;
  padding:.4rem .7rem .4rem .7rem;
  width:180px;height:30px;outline:none;
  transition:width .25s ease,background .2s,border-color .2s;
}
.search-input::placeholder{color:rgba(255,255,255,.45)}
.search-input:focus{width:260px;background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.4)}
.search-results{
  position:absolute;top:calc(100% + 6px);right:0;
  background:#fff;color:#111110;
  width:360px;max-height:60vh;overflow-y:auto;
  border:1px solid #e4e4df;
  box-shadow:0 12px 32px rgba(0,0,0,.08);
  display:none;z-index:200;
}
.search-results.open{display:block}
.search-result{
  display:block;padding:.6rem .9rem;
  border-bottom:1px solid #f0f0ec;
  font-size:.78rem;color:#444;
}
.search-result:last-child{border:none}
.search-result:hover,.search-result.selected{background:#f7f7f5}
.search-result .sr-id{
  display:inline-block;font-size:.62rem;color:#bbb;font-weight:600;
  letter-spacing:.04em;margin-right:.5rem;min-width:2.4rem;
}
.search-result .sr-title{font-weight:500;color:#111110}
.search-result .sr-sub{display:block;font-size:.7rem;color:#999;margin-top:.15rem;margin-left:2.9rem}
.search-result mark{background:#fff3a3;color:#111110;padding:0 .1rem;border-radius:1px}
.search-empty{padding:.85rem 1rem;font-size:.78rem;color:#999;text-align:center}

.lang-switch{display:flex;border:1px solid rgba(255,255,255,.18);height:30px;overflow:hidden}
.lang-btn{
  background:transparent;color:rgba(255,255,255,.55);
  border:none;cursor:pointer;font:inherit;
  font-size:.7rem;font-weight:600;letter-spacing:.06em;
  padding:0 .55rem;height:100%;
  border-right:1px solid rgba(255,255,255,.12);
  transition:background .15s,color .15s;
}
.lang-btn:last-child{border-right:none}
.lang-btn:hover{color:#fff}
.lang-btn.active{background:#fff;color:#111110}

/* ── PAGE TRANSITIONS ── */
/* html bg = body bg → no white flash between pages */
html{background:#f7f7f5}

/* Header & footer paint instantly (persistent feel).
   Content sections cascade in from top → bottom with a light stagger.
   Pure opacity, ease-out, short — should feel like a fast load, not an animation. */
@keyframes pageFadeIn{from{opacity:0}to{opacity:1}}

.breadcrumb,.hero,.page-hd,.quick-bar,.sections-overview,.content,.site-footer{
  animation:pageFadeIn .22s ease-out both
}
.breadcrumb       {animation-delay:0ms}
.hero,.page-hd    {animation-delay:60ms}
.quick-bar        {animation-delay:120ms}
.sections-overview,.content {animation-delay:160ms}
.site-footer      {animation-delay:240ms}

/* Inside content / overview, stagger immediate children for a softer cascade.
   nth-child up to 8 — beyond that, items appear together (cap stagger). */
.sections-overview > *, .content > *{
  animation:pageFadeIn .22s ease-out both;
  animation-delay:200ms
}
.sections-overview > *:nth-child(1),.content > *:nth-child(1){animation-delay:200ms}
.sections-overview > *:nth-child(2),.content > *:nth-child(2){animation-delay:240ms}
.sections-overview > *:nth-child(3),.content > *:nth-child(3){animation-delay:280ms}
.sections-overview > *:nth-child(4),.content > *:nth-child(4){animation-delay:320ms}
.sections-overview > *:nth-child(5),.content > *:nth-child(5){animation-delay:360ms}
.sections-overview > *:nth-child(6),.content > *:nth-child(6){animation-delay:400ms}
.sections-overview > *:nth-child(n+7),.content > *:nth-child(n+7){animation-delay:440ms}

@media(prefers-reduced-motion:reduce){
  .breadcrumb,.hero,.page-hd,.quick-bar,.sections-overview,.content,.site-footer,
  .sections-overview > *,.content > *{animation:none!important}
}

/* ── LANG TRANSITION (directional split) ──
   Header/menu slides left→right; everything else slides top→bottom.
   Both run in parallel, same easing, capped stagger so total < 600ms. */
@keyframes slideFromLeft{
  from{opacity:0;transform:translate3d(-12px,0,0)}
  to  {opacity:1;transform:translate3d(0,0,0)}
}
@keyframes slideFromTop{
  from{opacity:0;transform:translate3d(0,-8px,0)}
  to  {opacity:1;transform:translate3d(0,0,0)}
}
/* Menu animation: only top-level nav bar items, NOT submenu contents
   (user doesn't see closed dropdowns, and indexing them makes nav bar uneven). */
.lang-entering .site-header [data-i18n]:not(.dropdown [data-i18n]){
  animation:slideFromLeft .35s cubic-bezier(.2,.8,.2,1) both;
  animation-delay:calc(min(var(--i,0), 15) * 30ms);
  will-change:transform,opacity;
}
/* Content animation: ONLY text nodes ([data-i18n] / [data-i18n-html]).
   Images, backgrounds, card frames stay static. Stagger by parent section
   so text reveals top-down, section by section. */
.lang-entering :is(.breadcrumb,.hero,.quick-bar,.page-hd,.sections-overview,.content,.site-footer) :is([data-i18n],[data-i18n-html]){
  animation:slideFromTop .35s cubic-bezier(.2,.8,.2,1) both;
  will-change:transform,opacity;
}
.lang-entering .breadcrumb        :is([data-i18n],[data-i18n-html]){animation-delay:  0ms}
.lang-entering .hero              :is([data-i18n],[data-i18n-html]){animation-delay: 80ms}
.lang-entering .quick-bar         :is([data-i18n],[data-i18n-html]){animation-delay:160ms}
.lang-entering .page-hd           :is([data-i18n],[data-i18n-html]){animation-delay:160ms}
.lang-entering .sections-overview :is([data-i18n],[data-i18n-html]){animation-delay:240ms}
.lang-entering .content           :is([data-i18n],[data-i18n-html]){animation-delay:240ms}
.lang-entering .site-footer       :is([data-i18n],[data-i18n-html]){animation-delay:320ms}

@media (prefers-reduced-motion: reduce){
  .lang-entering [data-i18n],
  .lang-entering [data-i18n-html]{animation:none !important}
}

@media (max-width:900px){
  .search-input{width:120px}
  .search-input:focus{width:160px}
  .search-results{width:280px}
}
"""

# ─── TEMPLATE ─────────────────────────────────────────────────────────────────

def t(key, vi):
    """Render a span with data-i18n key + Vietnamese fallback text."""
    return f'<span data-i18n="{key}">{vi}</span>'

def build_nav(active_section_id="", b=""):
    """Build top nav with hover dropdowns + search + lang switcher."""
    out = ['<nav class="main-nav">']
    for sec in SITEMAP:
        active = "active" if sec["id"] == active_section_id else ""
        slug = sec["slug"]
        sec_url = f'{b}{slug}/index.html'
        sec_label = t(f'label.{sec["id"]}', sec["label"])
        if sec["type"] == "single":
            out.append(f'<div class="nav-item {active}"><a href="{sec_url}">{sec_label}</a></div>')
        elif sec["type"] == "mega":
            cols = []
            for grp in sec["groups"]:
                grp_url = f'{b}{slug}/{grp["slug"]}/index.html'
                grp_label = t(f'label.{grp["id"]}', grp["label"])
                items_html = ""
                for it in grp["items"]:
                    it_url = f'{b}{slug}/{grp["slug"]}/{it["slug"]}/index.html'
                    it_label = t(f'label.{it["id"]}', it["label"])
                    items_html += f'<li><a href="{it_url}"><span class="dropdown-num">{it["id"]}</span>{it_label}</a></li>'
                cols.append(f'''<div class="mega-col">
                    <div class="mega-col-title"><a href="{grp_url}">{grp_label}</a></div>
                    <ul>{items_html}</ul>
                </div>''')
            out.append(f'''<div class="nav-item has-menu {active}">
                <a href="{sec_url}">{sec_label}</a>
                <div class="dropdown mega">{"".join(cols)}</div>
            </div>''')
        else:  # dropdown
            items_html = ""
            for grp in sec["groups"]:
                grp_url = f'{b}{slug}/{grp["slug"]}/index.html'
                grp_label = t(f'label.{grp["id"]}', grp["label"])
                items_html += f'<a href="{grp_url}"><span class="dropdown-num">{grp["id"]}</span>{grp_label}</a>'
            out.append(f'''<div class="nav-item has-menu {active}">
                <a href="{sec_url}">{sec_label}</a>
                <div class="dropdown simple">{items_html}</div>
            </div>''')
    out.append('</nav>')

    # Tools: search + language switcher + CTA
    tools = f'''<div class="header-tools">
      <div class="search-wrap">
        <input type="search" class="search-input" id="site-search"
               placeholder="Tìm kiếm…" data-i18n-attr="placeholder:ui.search_ph"
               autocomplete="off" aria-label="Search">
        <div class="search-results" id="search-results" role="listbox"></div>
      </div>
      <div class="lang-switch" role="group" aria-label="Language">
        <button type="button" class="lang-btn" data-lang="vi">VI</button>
        <button type="button" class="lang-btn" data-lang="en">EN</button>
        <button type="button" class="lang-btn" data-lang="fr">FR</button>
      </div>
      <a href="{b}tham-quan/index.html#mua-ve" class="nav-cta" data-i18n="ui.buy_ticket">Mua vé</a>
    </div>'''
    return "\n".join(out) + tools

def build_footer(b=""):
    cols = []
    for sec in SITEMAP[:5]:
        sec_label = t(f'label.{sec["id"]}', sec["label"])
        if sec["type"] == "single":
            inner = f'<li><a href="{b}{sec["slug"]}/index.html">{sec_label}</a></li>'
        else:
            parts = []
            for g in sec["groups"][:5]:
                glabel = t(f'label.{g["id"]}', g["label"])
                parts.append(f'<li><a href="{b}{sec["slug"]}/{g["slug"]}/index.html">{glabel}</a></li>')
            inner = "".join(parts)
        cols.append(f'<div><p class="footer-col-title">{sec_label}</p><ul class="footer-links">{inner}</ul></div>')
    return "\n".join(cols)

def page(title, meta, section_id, crumbs, body, depth=0):
    """crumbs: list of tuples (label, href) or (label, href, i18n_key)."""
    b = "../" * depth
    nav_html = build_nav(section_id, b)
    crumb_html = ""
    for i, c in enumerate(crumbs):
        lbl, href = c[0], c[1]
        i18n_key = c[2] if len(c) > 2 else None
        if i: crumb_html += '<span class="sep">›</span>'
        lbl_html = t(i18n_key, lbl) if i18n_key else lbl
        if href and i < len(crumbs) - 1:
            crumb_html += f'<a href="{b}{href}">{lbl_html}</a>'
        else:
            crumb_html += f'<span>{lbl_html}</span>'
    footer_cols = build_footer(b)
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Văn Miếu Quốc Tử Giám</title>
<meta name="description" content="{meta}">
<link rel="stylesheet" href="{b}assets/css/style.css">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{b}index.html">
      <span class="brand-mark">VM</span>
      <span class="brand-text">
        <span class="brand-name" data-i18n="ui.site_name">Văn Miếu – Quốc Tử Giám</span>
        <span class="brand-sub" data-i18n="ui.site_sub">Di tích Quốc gia đặc biệt</span>
      </span>
    </a>
    {nav_html}
  </div>
</header>
<nav class="breadcrumb"><div class="container">{crumb_html}</div></nav>
{body}
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <p class="footer-brand" data-i18n="ui.footer_brand">Văn Miếu – Quốc Tử Giám</p>
        <p class="footer-address" data-i18n-html="ui.footer_addr">
          58 Phố Quốc Tử Giám, Phường Văn Miếu<br>
          Quận Đống Đa, Hà Nội<br>
          Điện thoại: 024.3747.1322<br>
          Email: vanmieuqtg@hanoi.gov.vn
        </p>
      </div>
      {footer_cols}
    </div>
    <p class="footer-copy" data-i18n="ui.footer_copy">© Trung tâm Hoạt động Văn hóa Khoa học Văn Miếu – Quốc Tử Giám</p>
  </div>
</footer>
<script src="{b}assets/js/data.js"></script>
<script src="{b}assets/js/app.js"></script>
</body>
</html>"""

def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")

# ─── PAGE BUILDERS ────────────────────────────────────────────────────────────

def img_or_ph(img, depth, label="Ảnh"):
    if img:
        return f'<img src="{"../"*depth}assets/images/{img}" alt="" loading="lazy">'
    return f'<div class="card-img-ph"><span>{label}</span></div>'

def render_card(num, title, desc, href, img, depth, compact=False,
                title_key=None, desc_key=None):
    img_html = (f'<img src="{"../"*depth}assets/images/{img}" alt="" loading="lazy">'
                if img else '<div class="card-img-ph"><span>Ảnh</span></div>')
    cls = "card compact" if compact else "card"
    title_html = t(title_key, title) if title_key else title
    desc_html  = t(desc_key, desc) if desc_key else desc
    return f'''<a href="{href}" class="{cls}">
  <div class="card-img">{img_html}</div>
  <div class="card-body">
    <p class="card-num">{num}</p>
    <h3 class="card-title">{title_html}</h3>
    <p class="card-desc">{desc_html}</p>
  </div>
</a>'''

def render_sidebar(section_slug, group_slug, current_item_slug, items, depth):
    b = "../" * depth
    links = []
    for it in items:
        href = f'{b}{section_slug}/{group_slug}/{it["slug"]}/index.html'
        cls = "active" if it["slug"] == current_item_slug else ""
        lbl = t(f'label.{it["id"]}', it["label"])
        links.append(f'<li><a href="{href}" class="{cls}">{lbl}</a></li>')
    return f'''<aside>
  <div class="sidebar-box">
    <p class="sidebar-title" data-i18n="ui.in_section">Trong mục này</p>
    <ul class="sidebar-links">{"".join(links)}</ul>
  </div>
  <a href="{b}tham-quan/index.html" class="sidebar-cta" data-i18n="ui.buy_ticket_arrow">Mua vé →</a>
</aside>'''

def render_group_sidebar(section_slug, current_group_slug, groups, depth):
    b = "../" * depth
    links = []
    for g in groups:
        href = f'{b}{section_slug}/{g["slug"]}/index.html'
        cls = "active" if g["slug"] == current_group_slug else ""
        lbl = t(f'label.{g["id"]}', g["label"])
        links.append(f'<li><a href="{href}" class="{cls}">{lbl}</a></li>')
    return f'''<aside>
  <div class="sidebar-box">
    <p class="sidebar-title" data-i18n="ui.in_section">Trong mục này</p>
    <ul class="sidebar-links">{"".join(links)}</ul>
  </div>
  <a href="{b}tham-quan/index.html" class="sidebar-cta" data-i18n="ui.buy_ticket_arrow">Mua vé →</a>
</aside>'''

# ─── HOME PAGE ────────────────────────────────────────────────────────────────

def build_home():
    blocks = []
    counts = {"A":"Vé · Giờ · Đường đến","B":"6 mục","C":"3 mục","D":"7 mục","E":"6 mục"}
    count_keys = {"A":"ui.count_a","B":"ui.count_b","C":"ui.count_c","D":"ui.count_d","E":"ui.count_e"}
    for sec in SITEMAP:
        href = f'{sec["slug"]}/index.html'
        sec_label = t(f'label.{sec["id"]}', sec["label"])
        sec_sub   = t(f'sub.{sec["id"]}', sec["sub"])
        sec_count = t(count_keys[sec["id"]], counts[sec["id"]])
        blocks.append(f'''<a href="{href}" class="section-block">
  <span class="section-block-num">{sec["id"]}</span>
  <span class="section-block-name">{sec_label}</span>
  <span class="section-block-sub">{sec_sub}</span>
  <span class="section-block-count">{sec_count}</span>
</a>''')
    body = f'''
<div class="hero">
  <img class="hero-img" src="assets/images/hero.jpg" alt="">
  <div class="hero-overlay"></div>
  <div class="hero-content container">
    <h1 class="hero-title" data-i18n="ui.hero_title">Văn Miếu – Quốc Tử Giám</h1>
    <p class="hero-sub" data-i18n="ui.hero_sub">Di tích Quốc gia đặc biệt · Trường đại học đầu tiên của Việt Nam · 82 Bia Tiến sĩ — Di sản tư liệu UNESCO</p>
  </div>
</div>
<div class="quick-bar"><div class="quick-bar-inner">
  <div class="quick-item"><p class="quick-label" data-i18n="ui.hours">Giờ mở cửa</p><p class="quick-value">07:30 – 18:00</p></div>
  <div class="quick-item"><p class="quick-label" data-i18n="ui.address">Địa chỉ</p><p class="quick-value" data-i18n="ui.addr_short">58 Quốc Tử Giám, Đống Đa, Hà Nội</p></div>
  <div class="quick-item"><p class="quick-label" data-i18n="ui.phone">Điện thoại</p><p class="quick-value">024.3747.1322</p></div>
  <div class="quick-item"><p class="quick-label" data-i18n="ui.price">Giá vé</p><p class="quick-value" data-i18n="ui.price_val_adult">30.000đ / người lớn</p></div>
</div></div>
<main>
<div class="container sections-overview">
  <p class="sections-title" data-i18n="ui.discover">Khám phá Văn Miếu – Quốc Tử Giám</p>
  <div class="sections-grid">{"".join(blocks)}</div>
</div>
</main>'''
    return page("Trang chủ", "Di tích Quốc gia đặc biệt Văn Miếu – Quốc Tử Giám.", "",
                [("Trang chủ","","ui.home")], body, 0)

# ─── SECTION A: THAM QUAN (single page) ───────────────────────────────────────

def build_section_a():
    body_inner = CONTENT["tham-quan"]
    body = f'''
<div class="page-hd"><div class="container">
  <p class="label" data-i18n="label.A">Tham quan</p>
  <h1 class="page-title" data-i18n="ui.page_a_title">Thông tin tham quan</h1>
  <p class="page-sub" data-i18n="ui.page_a_sub">Vé, giờ mở cửa, nội quy, đường đến và các tiện ích tại Văn Miếu – Quốc Tử Giám.</p>
</div></div>
<div class="content"><div class="container">
  <div class="article" id="mua-ve" data-i18n-html="content.tham-quan">{body_inner}</div>
</div></div>'''
    return page("Tham quan", "Thông tin tham quan Văn Miếu – Quốc Tử Giám.",
                "A", [("Trang chủ","index.html","ui.home"),("Tham quan","","label.A")], body, 1)

# ─── SECTION HUB (B/C/D/E top-level) ──────────────────────────────────────────

def build_section_hub(section):
    cards = []
    for grp in section["groups"]:
        href = f'{grp["slug"]}/index.html'
        img = None
        if grp.get("items"):
            for it in grp["items"]:
                if it.get("img"):
                    img = it["img"]
                    break
        cards.append(render_card(
            grp["id"], grp["label"], grp["sub"],
            href, img, depth=1,
            title_key=f'label.{grp["id"]}',
            desc_key=f'sub.{grp["id"]}',
        ))
    grid_class = "grid-3" if len(section["groups"]) > 4 else "grid-2"
    body = f'''
<div class="page-hd"><div class="container">
  <p class="label">{section["id"]}</p>
  <h1 class="page-title" data-i18n="label.{section["id"]}">{section["label"]}</h1>
  <p class="page-sub" data-i18n="sub.{section["id"]}">{section["sub"]}</p>
</div></div>
<div class="content"><div class="container">
  <div class="{grid_class}">{"".join(cards)}</div>
</div></div>'''
    return page(section["label"], section["sub"], section["id"],
                [("Trang chủ","index.html","ui.home"),
                 (section["label"],"",f'label.{section["id"]}')],
                body, 1)

# ─── GROUP HUB (B1, B2, ..., C1, ..., E1, ...) ────────────────────────────────

def build_group_hub(section, group):
    """Hub page for a group (e.g. B1 Lịch sử, B3 Kiến trúc)."""
    if group["items"]:
        cards = []
        compact = len(group["items"]) > 6
        for it in group["items"]:
            href = f'{it["slug"]}/index.html'
            cards.append(render_card(
                it["id"], it["label"],
                f'Chi tiết về {it["label"].lower()}.',
                href, it.get("img"), depth=2, compact=compact,
                title_key=f'label.{it["id"]}',
            ))
        grid = "grid-4" if compact else "grid-3"
        if len(group["items"]) <= 3:
            grid = "grid-3"
        body_inner = f'<div class="{grid}">{"".join(cards)}</div>'
    else:
        key = f'{section["slug"]}/{group["slug"]}'
        content = CONTENT.get(key, f'<p>Thông tin chi tiết về <strong>{group["label"]}</strong> đang được cập nhật.</p>')
        content_attr = f' data-i18n-html="content.{key}"'
        body_inner = f'<div class="content-inner"><div class="article"{content_attr}>{content}</div>{render_group_sidebar(section["slug"], group["slug"], section["groups"], depth=2)}</div>'
    body = f'''
<div class="page-hd"><div class="container">
  <p class="label"><span data-i18n="label.{section["id"]}">{section["label"]}</span> · {group["id"]}</p>
  <h1 class="page-title" data-i18n="label.{group["id"]}">{group["label"]}</h1>
  <p class="page-sub" data-i18n="sub.{group["id"]}">{group["sub"]}</p>
</div></div>
<div class="content"><div class="container">
  {body_inner}
</div></div>'''
    return page(group["label"], group["sub"], section["id"],
                [("Trang chủ","index.html","ui.home"),
                 (section["label"],f'{section["slug"]}/index.html',f'label.{section["id"]}'),
                 (group["label"],"",f'label.{group["id"]}')],
                body, 2)

# ─── ITEM PAGE (B1.1, B3.4, etc.) ─────────────────────────────────────────────

def build_item_page(section, group, item):
    key = f'{section["slug"]}/{group["slug"]}/{item["slug"]}'
    content = CONTENT.get(key)
    if not content:
        content = f'''<p>Trang chi tiết về <strong>{item["label"]}</strong> trong mục {group["label"]}.</p>
<p>Nội dung chi tiết đang được biên soạn. Quý khách vui lòng liên hệ Phòng Truyền thông để biết thêm thông tin: 024.3747.1322.</p>'''
    img_html = ""
    if item.get("img"):
        img_html = f'<div class="article-hero"><img src="../../../assets/images/{item["img"]}" alt="{item["label"]}" loading="lazy"></div>'
    body = f'''
<div class="page-hd"><div class="container">
  <p class="label"><span data-i18n="label.{section["id"]}">{section["label"]}</span> · <span data-i18n="label.{group["id"]}">{group["label"]}</span> · {item["id"]}</p>
  <h1 class="page-title" data-i18n="label.{item["id"]}">{item["label"]}</h1>
</div></div>
<div class="content"><div class="container">
  <div class="content-inner">
    <div class="article">{img_html}<div data-i18n-html="content.{key}">{content}</div></div>
    {render_sidebar(section["slug"], group["slug"], item["slug"], group["items"], depth=3)}
  </div>
</div></div>'''
    return page(item["label"], f'{item["label"]} — {group["label"]}, {section["label"]}.',
                section["id"],
                [("Trang chủ","index.html","ui.home"),
                 (section["label"], f'{section["slug"]}/index.html', f'label.{section["id"]}'),
                 (group["label"], f'{section["slug"]}/{group["slug"]}/index.html', f'label.{group["id"]}'),
                 (item["label"], "", f'label.{item["id"]}')],
                body, 3)

# ─── IMAGE COPY ───────────────────────────────────────────────────────────────

def copy_imgs():
    img_out = ROOT / "assets" / "images"
    img_out.mkdir(parents=True, exist_ok=True)

    # Special images
    pairs = [
        ("hero.jpg", "hero.jpg"),
        ("di-tich/lich-su/12-bia-tien-si.jpg", "lich-su/bia.jpg"),
        ("di-tich/lich-su/2-tu-tru-va-ho-van-phia-truoc-van-mieu-quoc-tu-giam.jpg", "lich-su/ho-van.jpg"),
        ("di-tich/lich-su/1-toan-canh-van-mieu-quoc-tu-giam-dau-the-ky-xx-copy.jpg", "lich-su/hero.jpg"),
        ("di-tich/lich-su/10-nha-bia-tien-si-ben-tay.jpg", "lich-su/nha-bia.jpg"),
        ("hoat-dong/1-toan-canh-van-mieu-quoc-tu-giam-dau-the-ky-xx.jpg", "hoat-dong/toan-canh.jpg"),
        ("hoat-dong/10-du-khach-tham-quan-phong-trung-bay.jpg", "hoat-dong/trung-bay.jpg"),
    ]
    for src_rel, dst_rel in pairs:
        src = OLD_IMGS / src_rel
        dst = img_out / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dst)

    # All images referenced in SITEMAP. Try OLD_IMGS/img first, then OLD_IMGS/di-tich/img
    for sec in SITEMAP:
        for grp in sec.get("groups", []):
            for it in grp.get("items", []):
                if it.get("img"):
                    candidates = [OLD_IMGS / it["img"], OLD_IMGS / "di-tich" / it["img"]]
                    src = next((c for c in candidates if c.exists()), None)
                    if src:
                        dst = img_out / it["img"]
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src, dst)
                    else:
                        print(f"  ! missing image: {it['img']}")

# ─── DATA.JS (i18n + search index) ────────────────────────────────────────────

def build_search_index():
    """Build a flat list of every page with VI/EN/FR labels for search."""
    idx = []
    # home
    idx.append({"id":"home","url":"index.html",
                "vi":"Trang chủ","en":"Home","fr":"Accueil",
                "sub_vi":"Văn Miếu – Quốc Tử Giám",
                "sub_en":"Temple of Literature","sub_fr":"Temple de la Littérature",
                "section":""})
    for sec in SITEMAP:
        sec_url = f'{sec["slug"]}/index.html'
        en = TR.LABELS.get(sec["id"], {}).get("en", sec["label"])
        fr = TR.LABELS.get(sec["id"], {}).get("fr", sec["label"])
        sub_en = TR.SUBS.get(sec["id"], {}).get("en", sec["sub"])
        sub_fr = TR.SUBS.get(sec["id"], {}).get("fr", sec["sub"])
        idx.append({"id":sec["id"],"url":sec_url,
                    "vi":sec["label"],"en":en,"fr":fr,
                    "sub_vi":sec["sub"],"sub_en":sub_en,"sub_fr":sub_fr,
                    "section":sec["id"]})
        for grp in sec.get("groups", []):
            grp_url = f'{sec["slug"]}/{grp["slug"]}/index.html'
            gen = TR.LABELS.get(grp["id"], {}).get("en", grp["label"])
            gfr = TR.LABELS.get(grp["id"], {}).get("fr", grp["label"])
            gsub_en = TR.SUBS.get(grp["id"], {}).get("en", grp["sub"])
            gsub_fr = TR.SUBS.get(grp["id"], {}).get("fr", grp["sub"])
            idx.append({"id":grp["id"],"url":grp_url,
                        "vi":grp["label"],"en":gen,"fr":gfr,
                        "sub_vi":grp["sub"],"sub_en":gsub_en,"sub_fr":gsub_fr,
                        "section":sec["id"]})
            for it in grp.get("items", []):
                it_url = f'{sec["slug"]}/{grp["slug"]}/{it["slug"]}/index.html'
                ien = TR.LABELS.get(it["id"], {}).get("en", it["label"])
                ifr = TR.LABELS.get(it["id"], {}).get("fr", it["label"])
                idx.append({"id":it["id"],"url":it_url,
                            "vi":it["label"],"en":ien,"fr":ifr,
                            "sub_vi":grp["label"],"sub_en":gen,"sub_fr":gfr,
                            "section":sec["id"]})
    return idx

def build_i18n_dict():
    """Build {key → {vi,en,fr}} dict consumed by JS."""
    out = {}
    # UI strings
    for k, v in TR.UI.items():
        out[f"ui.{k}"] = v
    # Labels (id → translated label)
    for k, v in TR.LABELS.items():
        out[f"label.{k}"] = v
    # Subs
    for k, v in TR.SUBS.items():
        out[f"sub.{k}"] = v
    # Long content (HTML)
    for k, v in TR.CONTENT.items():
        out[f"content.{k}"] = v
    return out

DATA_JS_TEMPLATE = """// Auto-generated. Do not edit by hand.
window.I18N = %s;
window.SEARCH_INDEX = %s;
"""

def write_data_js():
    i18n = build_i18n_dict()
    idx = build_search_index()
    out = DATA_JS_TEMPLATE % (
        json.dumps(i18n, ensure_ascii=False, separators=(",",":")),
        json.dumps(idx,  ensure_ascii=False, separators=(",",":")),
    )
    p = ROOT / "assets" / "js" / "data.js"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out, encoding="utf-8")

# ─── APP.JS (search + i18n + animation) ───────────────────────────────────────

APP_JS = r"""
(function(){
  'use strict';
  var I18N = window.I18N || {};
  var INDEX = window.SEARCH_INDEX || [];
  var STORAGE_KEY = 'vmqtg_lang';
  var DEFAULT = 'vi';

  // ─── helpers ────────────────────────────────────────────────────────────
  function stripDiacritics(s){
    return (s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
  }
  function getLang(){
    var saved = localStorage.getItem(STORAGE_KEY);
    if(saved && (saved==='vi'||saved==='en'||saved==='fr')) return saved;
    var nav = (navigator.language||'').slice(0,2).toLowerCase();
    if(nav==='en'||nav==='fr') return nav;
    return DEFAULT;
  }
  function setLang(lang){
    localStorage.setItem(STORAGE_KEY, lang);
    document.documentElement.setAttribute('lang', lang);
  }
  function lookup(key, lang){
    var entry = I18N[key];
    if(!entry) return null;
    return entry[lang] || null;
  }

  // ─── i18n apply ─────────────────────────────────────────────────────────
  function applyI18n(lang){
    // text nodes
    var nodes = document.querySelectorAll('[data-i18n]');
    nodes.forEach(function(el){
      var key = el.getAttribute('data-i18n');
      // store original VI text once
      if(!el.hasAttribute('data-vi-text')) el.setAttribute('data-vi-text', el.textContent);
      var txt = (lang==='vi') ? el.getAttribute('data-vi-text') : lookup(key, lang);
      el.textContent = txt || el.getAttribute('data-vi-text');
    });
    // html nodes
    var htmlNodes = document.querySelectorAll('[data-i18n-html]');
    htmlNodes.forEach(function(el){
      var key = el.getAttribute('data-i18n-html');
      if(!el.hasAttribute('data-vi-html')) el.setAttribute('data-vi-html', el.innerHTML);
      var html = (lang==='vi') ? el.getAttribute('data-vi-html') : lookup(key, lang);
      el.innerHTML = html || el.getAttribute('data-vi-html');
    });
    // attribute swaps: data-i18n-attr="placeholder:ui.search_ph"
    var attrNodes = document.querySelectorAll('[data-i18n-attr]');
    attrNodes.forEach(function(el){
      var spec = el.getAttribute('data-i18n-attr');
      spec.split(',').forEach(function(pair){
        var parts = pair.trim().split(':');
        var attr = parts[0], key = parts[1];
        var orig = el.getAttribute('data-vi-attr-'+attr);
        if(orig===null){ el.setAttribute('data-vi-attr-'+attr, el.getAttribute(attr)||''); orig = el.getAttribute(attr)||''; }
        var v = (lang==='vi') ? orig : lookup(key, lang);
        el.setAttribute(attr, v || orig);
      });
    });
    // update active button
    document.querySelectorAll('.lang-btn').forEach(function(b){
      b.classList.toggle('active', b.getAttribute('data-lang')===lang);
    });
    // update <title> by extracting current page title text node
    var h1 = document.querySelector('.page-title, .hero-title');
    if(h1){
      var t = h1.textContent.trim();
      if(t) document.title = t + ' — ' + (lookup('ui.site_name', lang) || 'Văn Miếu Quốc Tử Giám');
    }
  }

  // Index translatable elements into 2 regions for staggered animation.
  // Sets CSS var --i so .lang-entering rules can offset animation-delay.
  // Re-run after every applyI18n() because innerHTML swap creates new children.
  // Menu indexing: only top-level nav bar items get a stagger index.
  // Content sections use static delays in CSS (per parent section), so no
  // JS indexing is needed there — only text animates, never images/bg.
  var MENU_SEL = '.site-header [data-i18n]:not(.dropdown [data-i18n])';
  function indexElements(){
    document.querySelectorAll(MENU_SEL).forEach(function(el,i){
      el.style.setProperty('--i', i);
    });
  }

  function transitionLang(lang){
    applyI18n(lang);
    indexElements();
    // toggle .lang-entering off→on to restart animation; force reflow between
    document.body.classList.remove('lang-entering');
    void document.body.offsetWidth;
    document.body.classList.add('lang-entering');
    setTimeout(function(){
      document.body.classList.remove('lang-entering');
    }, 900);
    setLang(lang);
  }

  // ─── search ─────────────────────────────────────────────────────────────
  function highlight(text, query){
    if(!query) return text;
    var q = stripDiacritics(query);
    var src = stripDiacritics(text);
    var i = src.indexOf(q);
    if(i<0) return text;
    return text.slice(0,i)+'<mark>'+text.slice(i,i+q.length)+'</mark>'+text.slice(i+q.length);
  }
  function score(entry, query, lang){
    var q = stripDiacritics(query);
    if(!q) return 0;
    var fields = [entry[lang]||'', entry.vi||'', entry.en||'', entry.fr||'',
                  entry['sub_'+lang]||'', entry.sub_vi||''];
    var best = -1, hit=0;
    for(var i=0;i<fields.length;i++){
      var s = stripDiacritics(fields[i]);
      var idx = s.indexOf(q);
      if(idx>=0){
        hit = 1;
        // weight: earlier match + primary lang first = better
        var w = (i===0?100:i===1?80:50) - idx;
        if(w>best) best=w;
      }
    }
    return hit ? best : -1;
  }
  function runSearch(query, lang){
    if(!query.trim()) return [];
    var ranked = [];
    INDEX.forEach(function(e){
      var s = score(e, query, lang);
      if(s>=0) ranked.push({e:e, s:s});
    });
    ranked.sort(function(a,b){return b.s-a.s});
    return ranked.slice(0,10).map(function(x){return x.e});
  }
  function renderResults(results, query, lang){
    var box = document.getElementById('search-results');
    if(!box) return;
    if(!results.length){
      box.innerHTML = '<div class="search-empty">'+(lookup('ui.search_no',lang)||'Không có kết quả')+'</div>';
      box.classList.add('open'); return;
    }
    // build URL prefix from current depth
    var depth = (location.pathname.match(/\//g)||[]).length - 1;
    // Better: count slashes after the site root. Use relative trick:
    // figure out how many "../" we need by finding base of href in <link rel=stylesheet>
    var css = document.querySelector('link[rel=stylesheet]');
    var prefix = '';
    if(css){
      var href = css.getAttribute('href')||'';
      var m = href.match(/^((?:\.\.\/)+)/);
      if(m) prefix = m[1];
    }
    var html = results.map(function(r){
      var title = r[lang] || r.vi;
      var sub = r['sub_'+lang] || r.sub_vi || '';
      var url = prefix + r.url;
      return '<a class="search-result" href="'+url+'">'+
             '<span class="sr-id">'+r.id+'</span>'+
             '<span class="sr-title">'+highlight(title, query)+'</span>'+
             (sub?'<span class="sr-sub">'+highlight(sub, query)+'</span>':'')+
             '</a>';
    }).join('');
    box.innerHTML = html;
    box.classList.add('open');
  }

  // ─── init ───────────────────────────────────────────────────────────────
  function init(){
    var lang = getLang();
    setLang(lang);
    applyI18n(lang);
    indexElements();

    document.querySelectorAll('.lang-btn').forEach(function(b){
      b.addEventListener('click', function(){
        var l = b.getAttribute('data-lang');
        if(l===getLang()) return;
        transitionLang(l);
      });
    });

    var input = document.getElementById('site-search');
    var box = document.getElementById('search-results');
    if(input){
      var debounce;
      input.addEventListener('input', function(){
        clearTimeout(debounce);
        debounce = setTimeout(function(){
          var q = input.value;
          if(!q.trim()){ box.classList.remove('open'); box.innerHTML=''; return; }
          renderResults(runSearch(q, getLang()), q, getLang());
        }, 80);
      });
      input.addEventListener('focus', function(){
        if(input.value.trim()) box.classList.add('open');
      });
      document.addEventListener('click', function(e){
        if(!e.target.closest('.search-wrap')) box.classList.remove('open');
      });
      // keyboard
      input.addEventListener('keydown', function(e){
        var items = box.querySelectorAll('.search-result');
        if(!items.length) return;
        var sel = box.querySelector('.search-result.selected');
        var idx = sel ? Array.prototype.indexOf.call(items, sel) : -1;
        if(e.key==='ArrowDown'){ e.preventDefault(); idx=(idx+1)%items.length; }
        else if(e.key==='ArrowUp'){ e.preventDefault(); idx=(idx-1+items.length)%items.length; }
        else if(e.key==='Enter' && sel){ e.preventDefault(); window.location.href = sel.getAttribute('href'); return; }
        else if(e.key==='Escape'){ box.classList.remove('open'); input.blur(); return; }
        else return;
        items.forEach(function(i){i.classList.remove('selected')});
        if(items[idx]) items[idx].classList.add('selected');
      });
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  // Page transitions are pure CSS (.18s fade-in on content area only).
  // No JS interceptor — browser navigates instantly, new page paints fast.
})();
"""

def write_app_js():
    p = ROOT / "assets" / "js" / "app.js"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(APP_JS, encoding="utf-8")

# ─── BUILD ────────────────────────────────────────────────────────────────────

def main():
    print("Building VMQTG V5 (sitemap 09.05.2026)...")

    # Clear old generated dirs (keep build.py and assets/images)
    for sec in SITEMAP:
        d = ROOT / sec["slug"]
        if d.exists():
            shutil.rmtree(d)
    for old in ["trung-bay-trien-lam", "cac-hoat-dong"]:
        d = ROOT / old
        if d.exists() and old not in [s["slug"] for s in SITEMAP]:
            shutil.rmtree(d)

    # CSS
    css_path = ROOT / "assets" / "css" / "style.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(CSS, encoding="utf-8")
    print("  ✓ CSS")

    # JS (data + app)
    write_data_js()
    write_app_js()
    print("  ✓ JS (data + app)")

    # Images
    copy_imgs()
    print("  ✓ Images copied")

    # Home
    write(ROOT / "index.html", build_home())
    print("  ✓ index.html")

    # A. Tham quan (single page)
    write(ROOT / "tham-quan/index.html", build_section_a())
    print("  ✓ tham-quan/")

    # B-E. Each section
    page_count = 2
    for sec in SITEMAP:
        if sec["type"] == "single":
            continue
        write(ROOT / sec["slug"] / "index.html", build_section_hub(sec))
        page_count += 1
        for grp in sec["groups"]:
            write(ROOT / sec["slug"] / grp["slug"] / "index.html", build_group_hub(sec, grp))
            page_count += 1
            for it in grp.get("items", []):
                write(ROOT / sec["slug"] / grp["slug"] / it["slug"] / "index.html",
                      build_item_page(sec, grp, it))
                page_count += 1
        print(f"  ✓ {sec['slug']}/  ({sum(1+len(g['items']) for g in sec['groups'])} pages)")

    print(f"\nDone. {page_count} pages generated.")

if __name__ == "__main__":
    main()
