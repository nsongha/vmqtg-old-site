# Đề xuất xây dựng trang web mới — Phiên bản 2

## Website Văn Miếu – Quốc Tử Giám

*Cập nhật: ngày 4 tháng 5 năm 2026 · Tài liệu đi kèm: `SITEMAP.md`, `REPORT.md`, `website_report.md`*

---

## Phần I — Xuất phát điểm: nội dung thực tế trong tay

Trước khi đề xuất cấu trúc, cần nhìn thẳng vào những gì Trung tâm đã có. Toàn bộ tư liệu số hóa hiện tại gồm **476 file**, phân bổ như sau:

| Nhóm nội dung | Số bài/tài liệu | Ghi chú |
|---|---|---|
| Lịch sử Văn Miếu | 8 | 5 bài Tiếng Việt (Lý-Trần-Hồ, Lê sơ-Mạc, Lê Trung hưng, 1802–1945, 1945–1988) + 3 bài Tiếng Anh |
| Kiến trúc | 10 | Tổng thể, Hồ Văn–Vườn Giám, Tiền án, Cổng Văn Miếu, Nhập đạo–Đại Trung, Khuê Văn Các, Vườn bia–Giếng Thiên Quang, Đại Thành Môn, Điện Đại Thành, Thái Học |
| 82 Bia Tiến sĩ | 5 | 3 bài TV (Quá trình dựng bia, Giá trị, Di sản tư liệu) + 2 bài TA |
| Hệ thống tượng thờ | 10 | Khổng Tử, Tứ phối (Nhan Tử, Tăng Tử, Tử Tư, Mạnh Tử), Chu Văn An, Lý Thánh Tông, Lý Nhân Tông, Lê Thánh Tông + giới thiệu chung |
| Danh nhân & dòng họ | 21 | Tế tửu–Tư nghiệp (11), Tiến sĩ (6), Chu Văn An – bài chuyên đề (2), Dòng họ khoa bảng (1), Tư liệu/Đền thờ (1) |
| Thăm quan | 4 | Vé, Dịch vụ tham quan, Nội quy, Các tiện ích |
| Hoạt động | 1 | Trưng bày triển lãm thường xuyên (+ 1 trang phụ lục ảnh bị tách riêng sai) |
| Giáo dục di sản | ~192 tài liệu | 9 chương trình × 4 lứa tuổi × nhiều loại tài liệu (trước–trong–sau thăm quan) |
| Về chúng tôi | 1 | Giới thiệu Trung tâm |

**Tổng: 93 trang web hiện có, nội dung chất lượng cao, thiếu cấu trúc để phát huy.**

---

## Phần II — Vấn đề cần giải quyết

Được ghi chép chi tiết trong `SITEMAP.md`. Tóm tắt bốn vấn đề lớn nhất:

### 1. Mục "Danh nhân & dòng họ" — 21 bài flat, không phân loại

21 bài xếp thẳng theo alphabet, gộp chung 5 nhóm nội dung khác hẳn nhau: Tế tửu–Tư nghiệp (10 vị), Tiến sĩ (6 vị), chuyên đề Chu Văn An, Dòng họ khoa bảng, Tư liệu & Đền thờ. Người dùng muốn tìm "các vị Tế tửu Quốc Tử Giám" phải đọc lần lượt 21 tiêu đề để nhận ra đâu là Tế tửu, đâu là Tiến sĩ.

### 2. Mục "Hoạt động" — chỉ 1 nội dung thực sự

Hai URL hiện tại (`trung-bay-trien-lam-thuong-xuyen/` và `…-chu-thich-anh/`) là **một nội dung bị tách làm đôi** do lỗi build. Mục Hoạt động của cả một di tích cấp quốc gia chỉ có đúng 1 bài — điều này không phản ánh thực tế phong phú của các hoạt động tại Văn Miếu.

### 3. Mục "Giáo dục di sản" — 9 chương trình lặp qua 4 lứa tuổi

Cùng một chương trình "Đi tìm linh vật trên kiến trúc cổ" xuất hiện ở 4 trang khác nhau (Mầm non, Lớp 1–3, Lớp 4–6, Lớp 7–12). Giáo viên muốn biết "chương trình này dành cho lứa tuổi nào, khác nhau thế nào?" phải tự mở 4 trang rồi so sánh — thao tác không cần thiết.

### 4. Nội dung mới chưa có chỗ

Website hiện tại không có vị trí cho: 360°, thuyết minh âm thanh trực tuyến, bảo tàng ảo, bán vé online, cửa hàng lưu niệm, lịch sự kiện, tin tức & báo chí. Đây đều là các tính năng cần thiết để phục vụ khách du lịch quốc tế và vận hành hiện đại.

---

## Phần III — Nguyên tắc thiết kế cấu trúc

### Nguyên tắc 1: Số mục điều hướng chính không quá 6

**Cơ sở thực tiễn:** Khảo sát 10 website bảo tàng và di sản hàng đầu thế giới:

| Website | Số mục top-level | Cách tổ chức nội dung số |
|---|---|---|
| Louvre (louvre.fr/en) | **4** | 360°, audio guide, database → gộp vào "Explore" |
| British Museum | **5** | 8 triệu hiện vật + 3D objects → gộp vào "Collection" |
| Met Museum (metmuseum.org) | **5** | Met 360°, virtual tour, audio → gộp vào "Art" |
| Rijksmuseum (rijksmuseum.nl) | **4** | 2,5 triệu ảnh Rijksstudio → gộp vào "Explore" |
| Smithsonian (si.edu) | **5** | 19 bảo tàng + thư viện + virtual tours → gộp vào "Learn & Explore" |
| National Gallery London | **5** | Audio, podcast, nghiên cứu → gộp vào "Art & Artists" |
| Natural History Museum | **5** | Data portal, bộ sưu tập số → gộp vào "Science" |
| Guggenheim | **5** | Collection, online exhibitions, digital projects → gộp vào "Art" |
| APSARA / Angkor Wat | **6** | Bản đồ, lộ trình, kiến trúc → gộp vào "Angkor Park" |
| Hội An Ancient Town | **6** | Di tích + kiến trúc + museum → gộp vào "See" |

**Kết luận:** Ngưỡng 5–6 mục là chuẩn thực tế cho heritage site có sub-menu. Logo bấm về trang chủ — không cần mục "Trang chủ" trong nav.

**Lý do kỹ thuật:** Nghiên cứu UX của Nielsen Norman Group (2024) xác nhận: menu trên 7 mục làm thời gian tìm kiếm thông tin tăng 20–30% do "cognitive load" — người dùng phải đọc và ra quyết định với mỗi mục thêm vào. Đây là lý do Louvre — với kho tàng 380.000 tác phẩm — vẫn chỉ dùng 4 mục.

### Nguyên tắc 2: Mỗi mục phục vụ một câu hỏi rõ ràng

Người dùng đến website không suy nghĩ theo cấu trúc nội bộ của Trung tâm — họ đến với câu hỏi cụ thể:

- *"Giờ mở cửa mấy giờ? Giá vé bao nhiêu?"* → **Tham quan**
- *"Khuê Văn Các được xây năm nào? Ai thờ ở đây?"* → **Di tích**
- *"Trường tôi muốn đặt chương trình cho 40 học sinh lớp 5"* → **Giáo dục di sản**
- *"Tuần này có sự kiện gì?"* → **Sự kiện**
- *"Tôi muốn xem 360° khi chưa đến được"* → **Khám phá số**
- *"Tôi muốn liên hệ đặt tour đoàn"* → **Về chúng tôi**

### Nguyên tắc 3: Không lặp nội dung ở hai chỗ

Mỗi bài chỉ có một URL chính thức. Tham chiếu chéo thì dùng link — không copy-paste.

---

## Phần IV — Cấu trúc đề xuất (6 mục)

```
[Logo] → Trang chủ
│
├── 1. Di tích
│   ├── Lịch sử                         (8 bài, TV + EN)
│   │   ├── Lý, Trần, Hồ (1010–1407)
│   │   ├── Lê sơ – Mạc (1428–1592)
│   │   ├── Lê Trung hưng (1593–1788)
│   │   ├── 1802–1945
│   │   └── 1945–nay
│   ├── Kiến trúc                        (10 bài)
│   │   ├── Tổng thể khu di tích         ← bản đồ tương tác 10 công trình
│   │   ├── Hồ Văn & Vườn Giám
│   │   ├── Khu Tiền án
│   │   ├── Cổng Văn Miếu
│   │   ├── Khu Nhập đạo & Cổng Đại Trung
│   │   ├── Khu Thành đạt & Khuê Văn Các ← điểm nhấn biểu tượng
│   │   ├── Khu Vườn bia & Giếng Thiên Quang
│   │   ├── Cổng Đại Thành
│   │   ├── Khu Điện Đại Thành
│   │   └── Khu Thái Học
│   ├── 82 Bia Tiến sĩ                   (5 bài + tính năng tra cứu tương lai)
│   │   ├── Quá trình dựng bia
│   │   ├── Giá trị Bia Tiến sĩ
│   │   └── Bia Tiến sĩ – Di sản Tư liệu Thế giới
│   ├── Hệ thống tượng thờ               (10 bài)
│   │   ├── Giới thiệu chung
│   │   ├── Khổng Tử
│   │   ├── Tứ phối (Nhan Tử, Tăng Tử, Tử Tư, Mạnh Tử)
│   │   ├── Chu Văn An
│   │   ├── Lý Thánh Tông
│   │   ├── Lý Nhân Tông
│   │   └── Lê Thánh Tông
│   └── Danh nhân khoa bảng              (21 bài, phân loại lại thành 4 nhóm)
│       ├── Tế tửu & Tư nghiệp Quốc Tử Giám   (11 bài)
│       │   Chu Văn An · Nguyễn Trực · Ngô Sĩ Liên · Phùng Khắc Khoan
│       │   Nguyễn Duy Thì · Nguyễn Công Thái · Nguyễn Trí Vị
│       │   Nguyễn Nghiễm · Nguyễn Bá Lân · Vũ Miên · (tổng quan)
│       ├── Tiến sĩ tiêu biểu                  (6 bài)
│       │   Nguyễn Quý Đức · Nhữ Đình Toản · Nguyễn Duy Hiểu
│       │   Nguyễn Công Cơ · Trần Công Xán · Nghiêm Tướng công từ
│       ├── Chu Văn An – chuyên đề              (2 bài chuyên sâu)
│       │   (link tới tượng thờ Chu Văn An; không lặp nội dung)
│       └── Dòng họ khoa bảng                   (1 bài, mở rộng tương lai)
│
├── 2. Tham quan
│   ├── Giờ mở cửa & Giá vé             ← thông tin số 1 khách cần
│   │   (gộp file Vé + bổ sung giờ mở cửa, lịch nghỉ lễ)
│   ├── Bản đồ & Hướng dẫn di chuyển    ← mới, hiện đang thiếu hoàn toàn
│   │   (xe buýt, xe máy, ô tô, đi bộ từ trung tâm; chỗ đỗ xe)
│   ├── Mua vé trực tuyến               ← mới (tính năng cần xây dựng)
│   ├── Dịch vụ tham quan               (file có sẵn: thuyết minh viên, audio guide)
│   ├── Tiện ích tại di tích            (file có sẵn: café, lưu niệm, gửi xe)
│   └── Nội quy tham quan               (file có sẵn, sửa slug bỏ "-6-2")
│
├── 3. Sự kiện
│   ├── Lịch sự kiện                    ← mới (dạng lịch tháng, lọc theo loại)
│   ├── Trưng bày thường xuyên          (gộp 2 trang hiện có thành 1)
│   │   3 không gian: Nhà Tiền đường · Nhà Hậu đường · Khu Thái Học
│   ├── Triển lãm & Sự kiện chuyên đề   ← mới (slot cho nội dung theo thời gian)
│   │   Ngoại giao · Hội thảo tọa đàm · Cuộc thi · Sự kiện cộng đồng
│   ├── Lễ hội truyền thống             ← mới
│   │   Lễ xin chữ đầu năm · Lễ tế Khổng Tử · Lễ vinh danh thủ khoa
│   └── Đăng ký tham dự                ← mới (form hoặc link đến từng sự kiện)
│
├── 4. Giáo dục di sản
│   ├── Theo chương trình               ← primary navigation (mới)
│   │   ┌─────────────────────────────────────────────────────────┐
│   │   │ Chương trình         │ MN │ 1–3 │ 4–6 │ 7–12 │ 15+ │
│   │   ├─────────────────────────────────────────────────────────┤
│   │   │ Đi tìm linh vật      │  ✓ │  ✓  │  ✓  │  ✓   │     │
│   │   │ Ô kìa con Nghê       │  ✓ │  ✓  │  ✓  │  ✓   │     │
│   │   │ Mãnh hổ hạ sơn       │  ✓ │  ✓  │     │      │     │
│   │   │ Khám phá Bia Tiến sĩ │    │  ✓  │  ✓  │  ✓   │     │
│   │   │ Khuê Văn Các & KT    │    │  ✓  │  ✓  │  ✓   │     │
│   │   │ Lớp học xưa          │    │  ✓  │  ✓  │      │     │
│   │   │ Thi Hương–Hội–Đình   │    │     │     │  ✓   │     │
│   │   │ Vinh quy bái tổ      │    │     │     │  ✓   │     │
│   │   │ Sách học & Ván khắc  │    │     │     │  ✓   │     │
│   │   │ QTG ở Thăng Long     │    │     │     │  ✓   │     │
│   │   │ VM–QTG xưa và nay    │    │     │     │  ✓   │     │
│   │   │ Môi trường           │    │     │     │  ✓   │     │
│   │   └─────────────────────────────────────────────────────────┘
│   │   Mỗi ô có link đến trang chương trình đó cho lứa tuổi đó.
│   │   Mỗi trang chương trình gồm: nội dung, tài liệu tải về
│   │   (trước/trong/sau thăm quan · dành cho GV · dành cho cha mẹ)
│   │
│   ├── Theo lứa tuổi                   ← secondary (giữ URL cũ, không xóa)
│   │   Mầm non · Lớp 1–3 · Lớp 4–6 · Lớp 7–12 · 15 tuổi+ · Gia đình
│   │
│   ├── Học sinh trải nghiệm            ← mới (ảnh, video, câu chuyện)
│   └── Đặt chương trình               ← form đặt dịch vụ online
│
├── 5. Khám phá số
│   │   (Lý do tách riêng thay vì gộp vào Di tích: đây là nhóm tính năng
│   │   mới hoàn toàn, chưa có nội dung, cần highlight để thu hút đầu tư
│   │   và truyền thông. Sau 2–3 năm khi đã đầy đủ nội dung số, có thể
│   │   gộp vào Di tích như mô hình Louvre/British Museum.)
│   │
│   ├── Tham quan 360°                  ← mới (8 điểm đặc trưng)
│   │   Cổng VM · Đại Trung Môn · Khuê Văn Các · Giếng Thiên Quang
│   │   Vườn bia · Đại Thành Môn · Điện Đại Thành · Nhà Thái Học
│   ├── Bộ sưu tập 3D                   ← mới (bia, tượng thờ, hiện vật)
│   ├── Thuyết minh âm thanh trực tuyến ← nâng cấp từ thiết bị có sẵn (8 ngôn ngữ)
│   ├── AR tại di tích                  ← mới (giơ điện thoại trước bia)
│   └── Thư viện số                     ← bài nghiên cứu, tư liệu tải về
│
└── 6. Về chúng tôi
    ├── Giới thiệu Trung tâm            (trang có sẵn)
    ├── Cơ cấu tổ chức                 ← mới
    ├── Liên hệ & Hợp tác              ← mới (email, ĐT, form liên hệ, đặt đoàn)
    ├── Tin tức & Báo chí              ← mới (thông cáo báo chí, tin hoạt động)
    └── Cửa hàng lưu niệm             ← mới (sách, catalog, đồ lưu niệm)
```

---

## Phần V — Lý do cụ thể cho từng quyết định

### 5.1. Tại sao "Danh nhân" không đứng riêng?

Góp ý của Văn Miếu đặt "Danh nhân" là mục riêng (mục 3), dẫn đến hai vấn đề ngay lập tức:

**Vấn đề 1 — Trùng lặp bắt buộc:** Bia Tiến sĩ nằm ở mục 2 "Di tích" nhưng nội dung về các vị Tiến sĩ trên bia lại nằm ở mục 3 "Danh nhân". Người dùng tra cứu về một vị Tiến sĩ cụ thể phải biết phân biệt: thông tin về tấm bia → mục 2; thông tin về người được khắc tên → mục 3. Đây là sự phân chia không tự nhiên.

**Vấn đề 2 — Nội dung chưa đủ dày:** Hiện tại mục Danh nhân có 21 bài — chủ yếu là Tế tửu và Tư nghiệp, không phải "danh nhân khoa bảng" theo nghĩa rộng. Tách thành mục riêng làm nó trông mỏng hơn thực tế.

**Giải pháp:** Gộp vào Di tích như British Museum gộp biographies vào "Collection", Louvre gộp vào "Explore". Khi nội dung được mở rộng (1.304 vị Tiến sĩ, dòng họ khoa bảng), có thể tách ra hoặc tạo trang tra cứu riêng nằm trong Di tích.

### 5.2. Tại sao "Khám phá số" đứng riêng (thay vì gộp vào Di tích)?

Đây là điểm khác với mô hình Louvre/British Museum, và có lý do cụ thể:

**Louvre gộp vào Explore** vì 360° và database *đã tồn tại* và *đã đầy đủ* khi thiết kế nav. Họ cần cất nó vào một ngăn gọn.

**Văn Miếu chưa có nội dung số** — 360°, AR, 3D, thuyết minh online đều cần đầu tư xây dựng. Đặt riêng một mục "Khám phá số" có hai tác dụng: (1) tạo điểm đến rõ ràng để người dùng sớm nhận ra tính năng mới ngay cả khi nội dung còn ít; (2) tạo áp lực tích cực để Trung tâm ưu tiên đầu tư vào nội dung số.

**Tương đương trong thực tế:** Khi Rijksmuseum ra mắt Rijksstudio (2013), họ đặt nó ở nav chính — không gộp vào "Collection" — để highlight đây là tính năng mới. Sau 5 năm khi đã có 2,5 triệu ảnh, họ mới chuyển về dưới "Explore".

### 5.3. Tại sao Giáo dục di sản cần hai view song song?

Hiện tại 192 tài liệu xếp theo lứa tuổi. Phân tích cho thấy hai nhóm người dùng khác nhau:

- **Giáo viên chọn chương trình trước** ("Tôi muốn làm chương trình Bia Tiến sĩ cho lớp 6") → cần view theo chương trình
- **Phụ huynh/học sinh chọn lứa tuổi trước** ("Con tôi lớp 3, có chương trình gì?") → cần view theo lứa tuổi

Giải pháp: primary navigation theo chương trình (mới, giúp giáo viên so sánh biến thể), secondary navigation theo lứa tuổi (giữ URL cũ, không mất SEO). Hai view chia sẻ cùng nội dung, chỉ khác cách trình bày index.

### 5.4. Tại sao "Sự kiện" tách khỏi "Di tích"?

Sự kiện là nội dung **thay đổi theo thời gian** (lịch tháng, triển lãm đặc biệt, cuộc thi), trong khi Di tích là nội dung **tĩnh** (lịch sử, kiến trúc, bia, tượng). Trộn lẫn hai loại này tạo khó khăn cho cả người dùng (tìm thông tin tĩnh bị xen kẽ tin tức) lẫn nhân viên cập nhật (hai nhịp cập nhật rất khác nhau).

Đây là cách British Museum phân chia: "Collection" (tĩnh) vs "Exhibitions & Events" (động). National Gallery: "Art & Artists" (tĩnh) vs "Exhibitions & Events" (động).

### 5.5. Tại sao không có mục "Tin tức" riêng?

Website di sản không phải báo điện tử. Tin tức ở đây chủ yếu là: (a) thông báo thay đổi giờ/giá, (b) thông cáo báo chí, (c) bài nghiên cứu mới. Loại (a) → nổi bật ở Tham quan và trang chủ. Loại (b) và (c) → gộp vào "Về chúng tôi" mục Tin tức & Báo chí. Đây là cách Louvre (Press Room), British Museum (Press), Met Museum (Press) đều làm.

---

## Phần VI — Trang chủ

Trang chủ không phải một mục trong nav (logo làm nút home), nhưng cần được thiết kế như cửa ngõ phục vụ 5 nhóm người dùng trong `website_proposal.md` (§1):

**Bố cục đề xuất:**

1. **Hero section:** Ảnh hoặc đoạn phim 30 giây (cảnh quan di tích giờ vàng, có nhạc nền trầm)
2. **4 nút hành động nhanh** nổi bật ngay dưới hero:
   - 🎟 Mua vé / Giá vé
   - 🕐 Giờ mở cửa
   - 📅 Sự kiện sắp tới
   - 🗺 Bản đồ đường đi
3. **Giới thiệu Văn Miếu** — 3 câu, đặt trước 3 số liệu nổi bật: *950+ năm lịch sử · 82 Bia Tiến sĩ · Di sản Tư liệu UNESCO*
4. **Sự kiện đang diễn ra** — hiển thị 2–3 sự kiện gần nhất (tự động cập nhật)
5. **Điểm vào 6 mục chính** — 6 ô hình ảnh lớn dẫn vào từng mục
6. **Pop-up mua vé** — hiện ở cuối trang (không tự bung lên), có nút ✕ đóng rõ ràng

---

## Phần VII — Yêu cầu giao diện & kỹ thuật

*(Giữ nguyên từ `website_proposal.md` §4 và §5, bổ sung các ý từ góp ý của Văn Miếu)*

### 7.1. Thanh điều hướng

- **Logo** → trang chủ (không có mục "Trang chủ" trong nav)
- **6 mục chính** → mỗi mục có mega-menu khi hover, hiện sub-nav
- **Ô tìm kiếm** → luôn hiện ở header, không ẩn trong menu
- **Chuyển ngôn ngữ** → góc trên phải, hiển thị tên ngôn ngữ bằng chính nó: Tiếng Việt · English · Français · 中文 · 한국어 · 日本語
- **Nút mua vé** → nổi bật ở header, màu khác biệt

### 7.2. Bài đăng & sự kiện

- Hiển thị đồng thời: ngày diễn ra sự kiện + ngày đăng bài (theo góp ý của Văn Miếu)
- Lọc sự kiện theo loại: lễ tế · triển lãm · hội thảo · cuộc thi · ngoại giao

### 7.3. Pop-up mua vé

- Không tự bung lên khi vào trang (tôn trọng người dùng)
- Luôn hiển thị ở cuối trang dưới dạng thanh nổi (sticky bottom bar) hoặc nút cố định
- Có nút ✕ để đóng rõ ràng (theo góp ý của Văn Miếu)

### 7.4. Ưu tiên điện thoại di động

Thiết kế mobile-first — trên 60% lượt truy cập du lịch là từ điện thoại. Tốc độ tải trang dưới 2 giây trên mạng 4G.

---

## Phần VIII — Lộ trình triển khai

### Giai đoạn 1 — Nền tảng (3 tháng đầu)

Đưa trang web đẹp, hiện đại ra mắt với nội dung sẵn có:

- Cấu trúc 6 mục, trang chủ mới
- Toàn bộ nội dung hiện có đưa vào đúng vị trí trong cấu trúc mới
- Sửa các lỗi hiện tại: slug sai, bài EN tách riêng, tiêu đề ALL CAPS, Danh nhân phân loại lại
- Trang Tham quan bổ sung: Giờ mở cửa, Bản đồ, Hướng dẫn di chuyển
- Mua vé trực tuyến (tích hợp VNPay, MoMo, ZaloPay, Visa/MasterCard)
- Tiếng Việt + Tiếng Anh
- Mobile-first, tốc độ tải < 2 giây
- Trang quản trị cho nhân viên cập nhật tin tức, sự kiện

### Giai đoạn 2 — Nội dung phong phú (3 tháng tiếp)

- Tham quan 360° (8 điểm)
- Thuyết minh âm thanh trực tuyến (Tiếng Việt + Tiếng Anh trước)
- Lịch sự kiện với chức năng đăng ký
- Form đặt chương trình giáo dục di sản online
- Bổ sung Tiếng Pháp, Tiếng Trung

### Giai đoạn 3 — Bảo tàng số & tính năng cao cấp (6 tháng cuối)

- AR tại di tích (quét bia, hiện bản dịch + danh sách Tiến sĩ)
- Bộ sưu tập 3D (bia, tượng thờ tiêu biểu)
- Kho dữ liệu 82 Bia Tiến sĩ với tra cứu 1.304 vị Tiến sĩ
- Cửa hàng lưu niệm trực tuyến
- Bổ sung Tiếng Hàn, Tiếng Nhật, Tiếng Tây Ban Nha, Tiếng Thái

---

## Phần IX — So sánh với góp ý của Văn Miếu (ngày 4/5/2026)

| Góp ý của Văn Miếu | Đề xuất này | Lý do |
|---|---|---|
| 7 mục top-level | 6 mục | Chuẩn quốc tế 5–6; logo thay cho "Trang chủ" |
| "Danh nhân" = mục riêng (mục 3) | Nhánh trong "Di tích" | Tránh trùng Bia Tiến sĩ; nội dung chưa đủ dày để đứng riêng |
| "Khám phá" là mục riêng | Giữ, đổi tên "Khám phá số" | Đúng — cần highlight nội dung mới |
| "Khuê Văn Các" = mục ngang hàng Bia Tiến sĩ | Nằm trong Kiến trúc | Khuê Văn Các là một công trình kiến trúc, đã có trong danh sách 10 công trình |
| Bài đăng hiện ngày diễn ra + ngày đăng | Áp dụng | Ý hay, đưa vào yêu cầu giao diện |
| Pop-up vé có nút ✕, hiện cuối trang | Áp dụng | Ý hay, đưa vào yêu cầu giao diện |
| Cover trailer trên trang chủ | Áp dụng | Đưa vào hero section trang chủ |
| Thanh tìm kiếm | Áp dụng | Luôn hiện ở header |
| Lứa tuổi 15+ trong Giáo dục di sản | Áp dụng | Thêm vào view theo lứa tuổi |

---

## Phần X — Mục tiêu đo lường (6 tháng sau ra mắt)

| Chỉ số | Mục tiêu |
|---|---|
| Lượt truy cập/tháng | ≥ 150.000 |
| Tỉ lệ khách quốc tế | ≥ 30% |
| Thời gian trung bình trên trang | ≥ 3 phút |
| Tỉ lệ mua vé online | ≥ 5% tổng lượt vào cửa |
| Người dùng trên điện thoại | ≥ 65% |
| Tốc độ tải trang (4G) | < 2 giây |
| Đạt chuẩn tiếp cận WCAG 2.1 AA | ≥ 95% |

---

*Tài liệu đi kèm: `SITEMAP.md` (phân tích hiện trạng 93 trang), `REPORT.md` (báo cáo kỹ thuật), `website_report.md` (báo cáo rà soát tư liệu). Mọi câu hỏi về nội dung nguồn xin tham khảo các tài liệu đó trước khi trao đổi thêm.*
