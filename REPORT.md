# Báo cáo Audit Dữ liệu

Website cũ Văn Miếu – Quốc Tử Giám
*Ngày tổng hợp: 2026-04-20 · Live: [nsongha.github.io/vmqtg-old-site](https://nsongha.github.io/vmqtg-old-site/)*

---

## 1. Tổng quan coverage

| Section | Docx nguồn | Docx dùng | % | Ảnh nguồn | Ảnh dùng | % |
|---|---:|---:|---:|---:|---:|---:|
| **Trang 1 – Di tích** | 65 | 58 | 89% | 144 | 129 | 90% |
| **Trang 2 – Tham quan** | 4 | 4 | **100%** | 0 | 0 | — |
| **Trang 3 – Hoạt động** | 2 | 2 | **100%** | 13 | 13 | **100%** |
| **Trang 4 – Giáo dục DS** | 192 | 189 | 98% | 51 | 42 | 82% |
| **Trang 5 – Về chúng tôi** | 1 | 1 | **100%** | 0 | 0 | — |
| **TỔNG** | **264** | **254** | **96%** | **208** | **184** | **88%** |

**Đánh giá tổng**: 96% nội dung văn bản được render; 88% ảnh được dùng. Sites 2, 3, 5 đạt 100%. Thất thoát tập trung ở Trang 1 (Di tích — do cấu trúc EN không đồng nhất) và Trang 4 (Giáo dục — do tên folder ảnh tuỳ biến).

---

## 2. Nội dung KHÔNG được sử dụng — phân loại theo nguyên nhân

### 2.1. Bản dịch Tiếng Anh không được ghép với bản Tiếng Việt (5 docx + 6 ảnh)

**Phạm vi**: thư mục `Trang 1 Trang di tich/Danh nhân và dòng họ/Tế tửu - Tư nghiệp/Tiếng Anh/Chu Van An/`

Nguyên nhân: cấu trúc bên VN và EN **không đối xứng**:
- VN: `Tieng Viet/2. Tư nghiep Chu Van An/Bài viết và ảnh/<N.ARTICLE>/...` (có wrapper folder "Bài viết và ảnh")
- EN: `Tiếng Anh/Chu Van An/<N.ARTICLE>/...` (không wrapper)

Script merge bilingual hiện tại tìm VN/EN ở cùng một cấp — không match được do chênh 1 tầng thư mục.

Các bài bị bỏ:
- `9. CHU VAN AN AND HIS CONTRIBUTIONS TO VIETNAMESE CULTURE`
- `4. CHU VAN AN – THE GOD OF HAPPINESS – IN TRADITIONAL BELIEF`
- `8. THE INFLUENCE OF CHU VAN AN TO THE CONTEMPORARY`
- `10. WHAT MADE CHU VAN AN BECOME A GREAT MAN`
- `3. THE WAYS TO EXPRESS GRATITUDE TOWARDS CHU VAN AN`

Kèm theo là 6 ảnh trong các folder EN nói trên.

**→ Đây là LỖI CODE có thể fix** (chỉnh merge logic để handle bất đối xứng). Content đã sẵn sàng, chỉ cần pipeline pick up.

### 2.2. File docx là "Chú thích ảnh" (caption), không phải bài viết (2 docx)

- `Trang 1 Trang di tich/82 bia Tiên sĩ/Tiếng Việt/3.BIA TIẾN SĨ – DI SẢN TƯ LIỆU THẾ GIỚI/ảnh/Chú thích ảnh.docx`
- `Trang 1 Trang di tich/82 bia Tiên sĩ/Tieng Anh/THE STONE STELAE – A WORLD DOCUMENTARY HERITAGE/ảnh/Chú thích ảnh.docx`

Các file này nằm trong subfolder `ảnh/` và chứa caption cho từng ảnh (không phải bài độc lập). Script hiện bỏ qua do `ảnh/` được đánh dấu là image folder.

**→ CÓ THỂ GỘP** vào bài cha như phần "Chú thích hình ảnh" nếu cần. Hoặc giữ nguyên nếu chấp nhận mất caption (hiện tại ảnh không có alt text / chú thích).

### 2.3. Ảnh orphan — nằm cạnh folder không có .docx (8 ảnh trong Trang 1)

Các folder có ảnh nhưng không có bài viết tương ứng:
- `Danh nhân/…/Nguyen Duy Thi/2. HOÀNG GIÁP NGUYỄN DUY THÌ VỚI VM-QTG THĂNG LONG/` → 1 ảnh
- `Danh nhân/…/Nguyen Duy Thi/1. HOÀNG GIÁP TẾ TỬU NGUYỄN DUY THÌ CON NGƯỜI VÀ SỰ NGHIỆP/` → 2 ảnh
- `Tư nghiep Chu Van An/Bài viết và ảnh/` folders #1, #2, #6, #11 → 4 ảnh
- `82 bia Tiên sĩ/…/4. 82 BIA TIẾN SĨ – NGUỒN SỬ LIỆU QUÍ GIÁ…/ảnh/` → 1 ảnh

Những folder này trong nguồn **thiếu file .docx** — chỉ có mỗi ảnh (hoặc ảnh + tiêu đề folder). Không có nội dung bài để render.

**→ LỖI THIẾU CONTENT tại nguồn**. Website vẫn dựng được nhưng ảnh không có article để gắn vào. Cần content writer bổ sung 7 bài viết:
| # | Bài viết cần viết | Mục |
|---|---|---|
| 1 | Tư nghiệp Quốc Tử Giám Chu Văn An (1292–1370) | Danh nhân |
| 2 | Tư nghiệp QTG Chu Văn An với Văn Miếu – QTG Thăng Long | Danh nhân |
| 3 | Thân thế, sự nghiệp CVA qua chính sử và tư sử | Danh nhân |
| 4 | CVA trong tâm thức người dân Thanh Trì | Danh nhân |
| 5 | Hoàng giáp Tế tửu Nguyễn Duy Thì — con người & sự nghiệp | Danh nhân |
| 6 | Hoàng giáp Nguyễn Duy Thì với VM-QTG Thăng Long | Danh nhân |
| 7 | 82 Bia Tiến sĩ — nguồn sử liệu quí giá về lịch sử giáo dục VN thời quân chủ | 82 Bia |

### 2.4. Trang 4 — Tên folder ảnh không chuẩn (9 ảnh)

Trong Giáo dục di sản cấp lớp 7-12, các chương trình dùng tên image folder tuỳ biến thay vì `ảnh/`:
- `ảnh Môi trường/` (thay vì `ảnh/`)
- `Ảnh Kiến trúc cổ lớp 7-12/`
- `Ảnh tìm hiểu trường QTG lớp 7-12/`
- `Ảnh thi Hương, hội, đình lớp 7-12/`

Script hiện chỉ bắt đúng tên `ảnh` / `Ảnh` / `anh` → bỏ qua các biến thể trên. 9 ảnh trong 5 chương trình bị miss.

**→ LỖI CODE** dễ fix (thêm prefix match "bắt đầu bằng 'ảnh '") hoặc chuẩn hoá tên folder tại nguồn.

### 2.5. Trang 4 — docx "dành cho cha mẹ" (3 docx)

- `lớp 1-lớp 3/Khám phá Công trình KTNT Khuê Văn Các lớp 1-3/Trước Thăm quan/danh cho cha mẹ.docx`
- `lớp 4-lớp 6/khám phá công trình KTNT KVC lớp 4-6/Trước Thăm quan/danh cho cha mẹ.docx`
- `lớp 7-lớp 12/VM-QTG xưa và nay lớp 7-12/Trước Thăm quan/dành cho giáo viên và học sinh.docx`

Khác biệt naming (có dấu / không dấu, "cha mẹ" vs "giáo viên và học sinh") làm render_program không nhận diện đúng. Nội dung các bài khác trong cùng chương trình có load thành công.

**→ LỖI CODE** — cần chuẩn hoá label matching.

---

## 3. Vấn đề dịch thuật (Tiếng Anh, Tiếng Pháp)

### 3.1. Không có Tiếng Pháp trong nguồn

Đã search toàn bộ filename + content với từ khoá `franc/french/bienvenue/visiter/...` — **không có file tiếng Pháp**. Nguồn chỉ có VN và EN.

### 3.2. EN coverage rất không đồng đều

| Section | VN docx | EN docx | EN/VN |
|---|---:|---:|---:|
| Trang 1 – Di tích | 39 | 15 | **38%** |
| Trang 2, 3, 4, 5 | 199+ | 0 | **0%** |

**Chi tiết trong Trang 1**:

| Phân mục | VN | EN | Nhận xét |
|---|---:|---:|---|
| Lịch sử VM | 5 | 3 | Thiếu EN cho "Lê sơ – Mạc" và "Lê Trung hưng" |
| 82 bia Tiến sĩ | 4 (+ 2 empty) | 2 | Thiếu EN cho "Quá trình dựng bia" và "Giá trị bia" |
| Hệ thống tượng thờ | 10 | 5 | Thiếu EN cho Nhan Tử, Tăng Tử, Tử Tư, Mạnh Tử, Lý Thánh Tông |
| Danh nhân – Tiến sĩ | 6 | 0 | Không có EN nào |
| Danh nhân – Tế tửu | 15 | 10 | Tập trung ở Chu Văn An (5 bài EN bị lỗi link) |
| Dòng họ khoa bảng | 1 | 0 | Không có EN |
| Kiến trúc | 10 | 0 | **Không có EN nào** |

### 3.3. Trang 2 (Tham quan) — song ngữ trong cùng file

File `Nội quy tham quan 6-2.docx` và `Vé.docx` có cả VN + EN trong cùng document (EN ở nửa dưới). Hiện script render nguyên văn → trang hiển thị lẫn lộn 2 ngôn ngữ xen kẽ, chưa tách được.

**→ LỖI CODE** — cần detect language boundary trong docx và split thành 2 blocks.

---

## 4. Nội dung thiếu hoàn toàn (không có trong nguồn) — đề xuất bổ sung nếu làm site mới

### 4.1. Ưu tiên cao (cần cho site nghiêm túc)

| # | Hạng mục | Lý do |
|---|---|---|
| 1 | **Thông tin thực tế du khách**: giờ mở cửa, địa chỉ (58 QTG), bản đồ, hotline | Site thăm quan mà không có thông tin cơ bản → mất công năng chính |
| 2 | **Trang chủ (hero, intro, tổng quan)** | Hiện tôi viết placeholder; cần content chính thức |
| 3 | **Cơ sở dữ liệu 82 bia Tiến sĩ** (danh sách 1.304 vị Tiến sĩ, năm thi, khoa thi, quê quán) | Đây là hạt nhân của di tích — hiện site chỉ có 3 bài tổng quan |
| 4 | **Bản dịch EN cho Kiến trúc** (10 khu quan trọng: Khuê Văn Các, Đại Thành Môn, vườn bia…) | Khách quốc tế chủ yếu quan tâm kiến trúc |
| 5 | **EN cho toàn bộ Tham quan** (vé, dịch vụ, tiện ích, nội quy tách riêng) | Đối tượng khách quốc tế |

### 4.2. Ưu tiên trung bình

| # | Hạng mục | Lý do |
|---|---|---|
| 6 | Trang tin tức / sự kiện | Thường xuyên update (triển lãm, lễ tế) |
| 7 | Bổ sung EN cho Lịch sử (Lê sơ – Mạc, Lê Trung hưng) | Hoàn thiện chuỗi lịch sử song ngữ |
| 8 | Hệ thống tượng thờ — EN cho Nhan Tử, Tăng Tử, Tử Tư, Mạnh Tử | Các vị trong hệ thống Tứ Phối |
| 9 | 7 bài viết CVA & Nguyễn Duy Thì thiếu docx (xem §2.3) | Có ảnh nhưng không có nội dung |
| 10 | Phần "Hoạt động" hiện chỉ có 1 mục (Trưng bày thường xuyên) | Còn có các hoạt động khác (lễ tế Khổng Tử, vinh danh thủ khoa…) |

### 4.3. Ưu tiên thấp (nâng chất lượng nếu còn budget)

| # | Hạng mục |
|---|---|
| 11 | Ảnh 360° / virtual tour từng khu |
| 12 | Tiếng Pháp, tiếng Trung, tiếng Hàn, tiếng Nhật |
| 13 | Video giới thiệu |
| 14 | Audio guide mỗi khu |
| 15 | Câu chuyện của các dòng họ khoa bảng (hiện chỉ có 1 bài về truyền thống hiếu học) |

---

## 5. Đề xuất sửa chữa — theo thứ tự ưu tiên

### Fix ngay trong scope "old site" (không cần thêm content mới)

| # | Việc | Tác động | Effort |
|---|---|---|:---:|
| A | **Sửa merge EN/VN bất đối xứng** → pick up 5 bài EN Chu Văn An + 6 ảnh | +5 EN bài, tăng coverage 96→98% | M |
| B | **Recognize image folder tuỳ biến** (prefix "ảnh ", "Ảnh ") → pick up 9 ảnh Trang 4 | +9 ảnh | S |
| C | **Sửa label matching cho Trang 4** → pick up 3 docx "dành cho cha mẹ" còn thiếu | +3 bài | S |
| D | **Tách VN/EN trong Trang 2** (vé, nội quy) → 2 phiên bản riêng biệt | Trang 2 có EN chuẩn | M |
| E | **Gộp "Chú thích ảnh" vào bài chính** → có caption cho ảnh | Accessibility + SEO | S |

Sau 5 fix trên: coverage đạt **~100% cho dữ liệu có sẵn**.

### Cần content mới (ngoài scope "old site", dành cho site mới)

| # | Việc | Ưu tiên |
|---|---|:---:|
| F | Viết 7 bài CVA + Nguyễn Duy Thì còn thiếu (xem §2.3) | Cao |
| G | Thông tin thực tế du khách (giờ, vé, map, contact) | **Rất cao** |
| H | Database 82 bia + 1.304 Tiến sĩ | Cao |
| I | EN toàn diện (Kiến trúc, Tham quan, Giáo dục) | Cao |
| J | Trang chủ chính thức (hero, intro, mission) | Cao |

---

## 6. Kết luận

- **Site hiện tại sử dụng ~96% văn bản và ~88% ảnh** trong tư liệu được giao.
- **~4% còn lại** chia thành 3 nhóm: (a) lỗi code sửa được, (b) file caption phụ trợ, (c) content nguồn thiếu docx.
- **Dịch thuật**: EN coverage mới ~10% toàn dự án (chỉ Trang 1 có, và trong Trang 1 cũng mới 38%).
- **Khoảng trống lớn nhất**: thông tin thực tế (giờ/vé/bản đồ), database 82 bia, và EN cho 4 trong 5 trang.

Với scope "old site" (không thêm content mới), khuyến nghị fix 5 mục A-E — đều là sửa code, không đụng vào dữ liệu gốc. Sau đó coverage sẽ chạm trần của nguồn dữ liệu hiện có.

Khi làm **site mới**, nên tập trung trước vào hạng mục G (thông tin thực tế) vì đây là gap lớn nhất ảnh hưởng công năng, rồi mới đến H (82 bia database) và I (EN toàn diện).
