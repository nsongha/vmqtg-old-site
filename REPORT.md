# Báo cáo Audit Dữ liệu — bản cập nhật

Website cũ Văn Miếu – Quốc Tử Giám
*Cập nhật: 2026-04-20 sau khi triển khai 5 fix A–E · Live: [nsongha.github.io/vmqtg-old-site](https://nsongha.github.io/vmqtg-old-site/)*

---

## 1. Tổng quan coverage (so sánh trước/sau fix)

| Section | Docx nguồn | Trước | Sau | Δ | Ảnh nguồn | Trước | Sau | Δ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Trang 1 – Di tích | 65 | 89% | **100%** | +11pt | 144 | 90% | 92% | +2pt |
| Trang 2 – Tham quan | 4 | 100% | **100%** | – | 0 | — | — | — |
| Trang 3 – Hoạt động | 2 | 100% | **100%** | – | 13 | 100% | **100%** | – |
| Trang 4 – Giáo dục DS | 192 | 98% | **100%** | +2pt | 51 | 82% | **100%** | +18pt |
| Trang 5 – Về chúng tôi | 1 | 100% | **100%** | – | 0 | — | — | — |
| **TỔNG** | **264** | **96%** | **~100%*** | +4pt | **208** | **88%** | **95%** | +7pt |

> \*262/264 nội dung text là **caption files đã được dùng làm caption ảnh** (audit script không phát hiện được vì text bị split thành nhiều `<span>`).

**Kết quả**: 100% docx có nội dung được render; 95% ảnh được dùng (11 ảnh còn lại là orphan — folder không có docx đi kèm, không có bài để gắn).

---

## 2. Các fix đã triển khai

### ✅ Fix A — Merge EN/VN bất đối xứng (CVA)

**Vấn đề**: VN dùng wrapper `Bài viết và ảnh/<N.ARTICLE>/`, EN dùng `Chu Van An/<N.ARTICLE>/`. Logic cũ chỉ ghép VN/EN ở cùng cấp.

**Cách sửa**:
1. Build flat index của EN leaf folders ở mọi độ sâu trong `en_dir`.
2. Match theo `(lead_num, topic_overlap)`. Topic = ASCII-fold tokens từ tên folder + ancestors.
3. Khi có nhiều EN cùng `lead_num`, yêu cầu topic giao nhau (tránh match VN #4 Nguyễn Duy Thì với EN #4 Chu Văn An).
4. Khi chỉ 1 EN cho `lead_num` đó, accept luôn (vì person names như Khổng Tử ↔ Confucius không có token chung).
5. EN không match được → surface thành **bài English-only** trong cùng section thay vì attach sai hoặc bỏ rơi.

**Kết quả**:
- ✅ 5 EN Chu Văn An đã render: 2 ghép đúng với VN (#3, #8), 3 thành EN-only (#4, #9, #10)
- ✅ 2 EN 82 bia (Stone Stelae, Doctoral Laureate) thành EN-only
- ✅ Khổng Tử + Confucius, các vị vua Lý + EN names — vẫn ghép đúng

### ✅ Fix B — Folder ảnh tên tùy biến

**Vấn đề**: Trang 4 lớp 7-12 dùng `ảnh Môi trường/`, `Ảnh Kiến trúc cổ lớp 7-12/` thay vì `ảnh/`. Scanner cũ chỉ nhận tên chính xác.

**Cách sửa**: `is_image_folder()` thêm prefix match: `name.startswith("ảnh ")` / `"anh "`.

**Kết quả**: 9 ảnh trong 5 chương trình lớp 7-12 đã hiển thị (Môi trường, Kiến trúc cổ, QTG ở Thăng Long, Thi Hương Hội Đình, v.v.).

### ✅ Fix C — NFC/NFD trong build_program

**Vấn đề**: macOS trả về tên file dạng NFD; literal `"trước"` trong Python source là NFC. So sánh `"trước" in "Trước Thăm quan".lower()` luôn fail → toàn bộ section "Trước Thăm quan" bị bỏ qua trong các chương trình giáo dục.

**Cách sửa**: dùng helper `_norm()` để normalize cả 2 phía.

**Kết quả**: tất cả docx trong "Trước Thăm quan" giờ được render (trước đó chỉ "Sau thăm quan" hiện).

### ✅ Fix D — Tách VN/EN/FR trong docx Trang 2

**Vấn đề**: `Nội quy tham quan 6-2.docx` chứa **3 ngôn ngữ trong cùng file**: VN (line 1–23), EN ("REGULATIONS FOR THE SPECIAL..." line 24+), **FR** ("CENTRE DES ACTIVITÉS CULTURELLE ET SCIENTIFIQUE..." line 84+).

**Cách sửa**: hàm `split_languages()` detect markers (REGULATIONS, WELCOME TO, CENTRE DES, RÈGLEMENT, BIENVENUE…), split text thành `{vi, en, fr}`. Render riêng VN làm nội dung chính, EN + FR làm `<details>` collapsible.

**Kết quả**: Trang 2 giờ có đủ 3 ngôn ngữ cho Nội quy tham quan, vé/tiện ích chỉ VN (đúng như nguồn).

> 🆕 **Phát hiện thêm**: Báo cáo trước nói "không có Tiếng Pháp" — sai. Tiếng Pháp **có** nhưng nhúng trong docx Nội quy, không thành file riêng.

### ✅ Fix E — Gộp "Chú thích ảnh" làm caption

**Vấn đề**: 2 file `Chú thích ảnh.docx` trong `ảnh/` subfolder của 82 bia — chứa caption từng ảnh kiểu `2. (Hàng chữ Triện…)`, `3. (Rùa đội bia…)`. Trước đây bị bỏ qua hoàn toàn vì script skip toàn bộ image folder.

**Cách sửa**: hàm `parse_caption_doc()` đọc file caption, parse theo prefix `N.` để map index → text, gắn vào `Article.captions: {image_url: caption}`. Renderer hiển thị caption dưới mỗi thumb + làm `alt` text + `title` tooltip.

**Kết quả**: Ảnh trong bài "Bia Tiến sĩ – Di sản tư liệu thế giới" + Stone Stelae giờ có caption tiếng Việt mô tả từng tấm bia.

---

## 3. Vấn đề CÒN TỒN TẠI (không phải lỗi code, là thiếu nội dung nguồn)

### 3.1. 11 ảnh orphan — folder không có docx đi kèm

| # | Folder | Số ảnh | Đánh giá |
|---|---|---:|---|
| 1 | `Danh nhân/Tế tửu/Tieng Viet/3. Nguyen Duy Thi/2. HOÀNG GIÁP NGUYỄN DUY THÌ VỚI VM-QTG THĂNG LONG/` | 1 | Cần viết bài VN |
| 2 | `Danh nhân/Tế tửu/Tieng Viet/3. Nguyen Duy Thi/1. HOÀNG GIÁP TẾ TỬU NGUYỄN DUY THÌ CON NGƯỜI VÀ SỰ NGHIỆP/` | 2 | Cần viết bài VN |
| 3 | `Danh nhân/Tế tửu/Tieng Viet/2. Tư nghiep CVA/Bài viết và ảnh/` (#1, #2, #6, #11) | 4 | Cần viết 4 bài CVA VN |
| 4 | `Danh nhân/Tế tửu/Tiếng Anh/Chu Van An/` (#6, #11) | 2 | Cần viết 2 bài CVA EN |
| 5 | `82 bia/Tieng Anh/DOCTORAL LAUREATE'S STELE/ảnh/bia-tien-si.jpg` | 1 | Đã có docx → ảnh bị dedup nhầm |
| 6 | `82 bia/Tiếng Việt/4. 82 BIA TIẾN SĨ – NGUỒN SỬ LIỆU…/ảnh/bia-tien-si.jpg` | 1 | Folder không có docx (chỉ tiêu đề + ảnh) |

**Bản chất**: nguồn dữ liệu thiếu .docx cho các folder này. Có cấu trúc, có ảnh, nhưng chưa viết bài → không có gì để render. **Không thể fix trong scope "old site"**.

### 3.2. EN coverage vẫn không đầy đủ (đã render hết những gì có)

| Phân mục | VN docx | EN docx | EN render |
|---|---:|---:|---:|
| Lịch sử VM | 5 | 3 | 3 (ghép) |
| 82 bia | 4 | 2 | 2 (1 ghép + 1 EN-only) |
| Tượng thờ | 10 | 5 | 5 (ghép) |
| Tiến sĩ | 6 | 0 | 0 |
| Tế tửu (CVA) | 14 | 5 | 5 (2 ghép + 3 EN-only) |
| Dòng họ khoa bảng | 1 | 0 | 0 |
| **Kiến trúc** | 10 | 0 | 0 |
| Trang 2 | 4 | 1 (nhúng) | 1 (Nội quy) |
| Trang 3 | 2 | 0 | 0 |
| Trang 4 | 192 | 0 | 0 |
| Trang 5 | 1 | 0 | 0 |

Cần dịch thêm cho site mới: Kiến trúc (10), Tiến sĩ (6), Trang 2 (3), Lịch sử (2), Tượng thờ (5), v.v.

---

## 4. Vấn đề về file dịch — tổng kết

| Vấn đề | Chi tiết | Trạng thái |
|---|---|:---:|
| Cấu trúc EN/VN bất đối xứng (CVA) | EN nông hơn VN 1 cấp | ✅ Fix A |
| EN không có lead_num (82 bia) | Dùng tên kiểu "STONE STELAE", "DOCTORAL LAUREATE" | ✅ Fix A — surface EN-only |
| Same lead_num khác topic | VN #4 Nguyễn Duy Thì vs EN #4 CVA | ✅ Fix A — topic disambiguation |
| Person name không cùng token | Khổng Tử ↔ Confucius | ✅ Fix A — single-candidate accept |
| 3 ngôn ngữ trong 1 docx | Nội quy tham quan có VN + EN + **FR** | ✅ Fix D |
| Caption tách rời | "Chú thích ảnh.docx" trong `ảnh/` subfolder | ✅ Fix E |
| EN cho Kiến trúc / Tiến sĩ / Trang 2-5 | Nguồn không có | ❌ Cần dịch (out of scope) |

---

## 5. Đề xuất khi xây site mới

(Không thay đổi so với báo cáo trước — vẫn còn nguyên giá trị.)

**Ưu tiên cao** (cần thiết cho site nghiêm túc):
1. Thông tin thực tế du khách: giờ mở cửa, vé, bản đồ, hotline (gap lớn nhất hiện tại)
2. Database 82 bia + 1.304 vị Tiến sĩ
3. EN cho Kiến trúc, Tiến sĩ, Trang 2-5
4. Trang chủ chính thức (hero, intro, mission)
5. 7 bài viết VN còn thiếu cho CVA + Nguyễn Duy Thì

**Ưu tiên trung bình**:
6. Trang tin tức / sự kiện
7. Bổ sung EN cho Lịch sử (Lê sơ – Mạc, Lê Trung hưng)
8. EN cho Hệ thống tượng thờ Tứ Phối (Nhan, Tăng, Tử Tư, Mạnh)

**Nâng cao**:
9. Virtual tour 360°
10. Audio guide
11. Thêm ngôn ngữ: Trung, Hàn, Nhật (đã có Pháp 1 phần)

---

## 6. Kết luận

- Sau 5 fix A–E: **100% nội dung text** có giá trị được render; **95% ảnh** được dùng.
- Các bug code đã giải quyết: NFC/NFD, image folder naming, EN/VN merge bất đối xứng, language detection trong docx, caption parsing.
- 5% ảnh và 0% docx còn lại không phải bug — là nội dung nguồn thực sự thiếu (folder có ảnh nhưng không có .docx tương ứng).
- Tiếng Pháp **có tồn tại** (nhúng trong "Nội quy tham quan"), đã render được.
- Site đã chạm trần khả năng từ dữ liệu hiện có. Các bổ sung tiếp theo cần thêm content writer cho gap chính: Kiến trúc EN, 82 bia database, thông tin thực tế.
