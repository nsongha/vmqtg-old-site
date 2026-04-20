# Sơ đồ trang — Hiện trạng & Đề xuất

Nguồn dữ liệu: build `site/` ngày 2026-04-20, 93 trang, 5 chuyên mục.
Sơ đồ tương tác live: [/so-do-trang/](https://nsongha.github.io/vmqtg-old-site/so-do-trang/)

---

## 1. Sơ đồ hiện tại

```
Trang chủ
├── Di tích                            (54 bài)
│   ├── Kiến trúc                      (10)   Cổng · Đại Thành Môn · Hồ Văn · Khuê Văn Các · Thái Học · Tiền án · Vườn bia · …
│   ├── Lịch sử                        ( 5)   Lý-Trần-Hồ · Lê sơ-Mạc · Lê Trung hưng · 1802-1945 · 1945-1988
│   ├── 82 Bia Tiến sĩ                 ( 3)   + 1 trang bản tiếng Anh tách riêng
│   ├── Hệ thống tượng thờ             (10)   Khổng Tử · Á Thánh · Phục Thánh · Thuật Thánh · Tông Thánh · Chu Văn An · 2 vua Lý · …
│   └── Danh nhân & dòng họ            (21)   Flat list — trộn Tế tửu, Tiến sĩ, Dòng họ, Tư liệu ghi chép
├── Tham quan                          ( 4)   Vé · Dịch vụ tham quan · Nội quy · Các tiện ích
├── Hoạt động                          ( 2)   Trưng bày triển lãm thường xuyên · Chú thích ảnh (tách riêng)
├── Giáo dục di sản                    (28)   Theo lứa tuổi
│   ├── Mầm non                        ( 3)   Linh vật · Mãnh hổ hạ sơn · Ô kìa con nghê
│   ├── Lớp 1–3                        ( 6)   + Bia Tiến sĩ, Khuê Văn Các, Lớp học xưa
│   ├── Lớp 4–6                        ( 5)   − Mãnh hổ; + Kiến trúc nội thất KVC
│   └── Lớp 7–12                       (10)   Thi Hương-Hội-Đình · Sách học · Vinh quy · Kiến trúc cổ · QTG Thăng Long · VM xưa-nay · Môi trường
└── Về chúng tôi                       ( 1)   Chỉ 1 trang giới thiệu Trung tâm
```

---

## 2. Vấn đề nhận diện

### 2.1. `Danh nhân & dòng họ` — flat 21 bài, khó tra cứu

Nội dung trộn **5 nhóm khác nhau** nhưng cùng một cấp:

| Nhóm | Bài hiện có |
|---|---|
| Tế tửu – Tư nghiệp Quốc Tử Giám | Nguyễn Bá Lân, Nguyễn Công Thái, Nguyễn Trí Vị, Nguyễn Trực (Tế tửu), Phùng Khắc Khoan, Vũ Miên, Nguyễn Trực (Trạng nguyên), Ngô Sĩ Liên (Tư nghiệp), Chu Văn An (Tư nghiệp), Quan Tế tửu - Tư nghiệp (giới thiệu) |
| Tiến sĩ / Quận công | Nguyễn Công Cơ, Trần Công Xán, Đại tư đồ Nguyễn Nghiễm, Nguyễn Quý Đức |
| Danh nhân Chu Văn An | Ảnh hưởng với đương thời, Các hình thức tôn vinh |
| Dòng họ khoa bảng | 1 bài tổng quan |
| Tư liệu / Đền thờ / Hoàng giáp | Nguyễn Duy Thì (2 bài), Nguyễn Duy Hiểu, Nghiêm Tướng công từ, Nhữ Đình Toản |

**Hệ quả:** trang `/di-tich/danh-nhan/` hiển thị 21 link theo alphabet, không có ngữ cảnh. Slug lỗi: `10te-tuu-quoc-tu-giam-nguyen-ba-lan-...` (prefix "10" thừa).

### 2.2. `Hoạt động` — chỉ 2 trang, 1 trang là "Chú thích ảnh" tách riêng

`/hoat-dong/trung-bay-trien-lam-thuong-xuyen/` và `…-chu-thich-anh/` là **một nội dung bị tách làm đôi** (nội dung chính + phụ lục ảnh). Không ai click vào "Chú thích ảnh" như một mục riêng.

### 2.3. `Tham quan` — tên trang sai/lỗi thời

- `noi-quy-tham-quan-6-2` — có "6-2" lạc trong slug (tên file nguồn: `Nội quy tham quan 6-2.docx`).
- `ve` — slug quá ngắn, SEO kém. Nên là `gia-ve` hoặc `ve-tham-quan`.
- Thiếu: **giờ mở cửa**, **bản đồ**, **hướng dẫn di chuyển** — những thông tin khách cần nhất khi vào trang này.

### 2.4. `Giáo dục di sản` — 6 chương trình lặp qua 4 lứa tuổi, khó so sánh

Hiện tại xếp theo lứa tuổi → mỗi chương trình xuất hiện 2-4 lần ở các trang khác nhau:

| Chương trình | MN | 1–3 | 4–6 | 7–12 |
|---|:-:|:-:|:-:|:-:|
| Đi tìm linh vật | ✓ | ✓ | ✓ | ✓ |
| Ô kìa con Nghê  | ✓ | ✓ | ✓ | ✓ |
| Khám phá Bia Tiến sĩ | | ✓ | ✓ | ✓ |
| Mãnh hổ hạ sơn | ✓ | ✓ | | |
| Khám phá Khuê Văn Các | | ✓ | ✓ | |
| Lớp học xưa | | ✓ | ✓ | |
| *(chỉ 7–12)* Thi Hương-Hội-Đình, Vinh quy bái tổ, Sách học & ván khắc, QTG Thăng Long, VM xưa-nay, Kiến trúc cổ, Môi trường | | | | ✓ |

Giáo viên/phụ huynh muốn biết "chương trình X dành cho độ tuổi nào?" → phải mở 4 trang.

### 2.5. Title ALL CAPS

Tiêu đề trang được kéo thẳng từ `.docx` dạng `TẾ TỬU QUỐC TỬ GIÁM NGUYỄN TRỰC (1417-1473)`, hiển thị chói trong listing và sitemap. Dễ fix bằng title-case ở tầng build.

### 2.6. Song ngữ thiếu nhất quán

- Hầu hết trang bilingual dùng `<details>English version</details>` trong cùng trang.
- Riêng `bia-tien-si-di-san-tu-lieu-the-gioi` có **bản EN tách thành trang riêng** (`the-stone-stelae-a-world-documentary-heritage/`). Là glitch của build logic khi gặp cấu trúc folder `VN/EN`.

### 2.7. `Về chúng tôi` quá mỏng

Chỉ 1 bài giới thiệu Trung tâm. Thiếu **liên hệ**, **đội ngũ**, **lịch sử Trung tâm**, **báo chí/tin tức**, **tuyển dụng** — những nội dung institutional site thường có.

### 2.8. Home conflate với Di tích

Trang chủ đặt tiêu đề `Khám phá di tích` → dễ nhầm là trang Di tích. Nên đổi thành `Khám phá Văn Miếu – Quốc Tử Giám`.

---

## 3. Đề xuất sơ đồ mới

**Nguyên tắc:** giữ 5 chuyên mục hàng đầu (ít cost migration, khách quen URL cũ), tái cấu trúc bên trong + thêm 1 tầng phân loại cho 2 chuyên mục nặng nhất (`Danh nhân`, `Giáo dục`).

```
Trang chủ  ← đổi heading thành "Khám phá Văn Miếu – Quốc Tử Giám"
│
├── Di tích
│   ├── Lịch sử                       (5 → giữ nguyên)
│   ├── Kiến trúc                     (10 → giữ nguyên)
│   ├── 82 Bia Tiến sĩ                (3 + gộp bản EN vào <details>)
│   ├── Tượng thờ                     (10 → đổi tên "Hệ thống tượng thờ")
│   └── Danh nhân khoa bảng            ★ tái cấu trúc
│       ├── Tế tửu – Tư nghiệp QTG    (10)
│       ├── Tiến sĩ – Quan lại        (4)
│       ├── Chu Văn An                (2 + link tới tượng thờ)
│       ├── Dòng họ khoa bảng         (1 + mở rộng tương lai)
│       └── Tư liệu & Đền thờ         (5)
│
├── Tham quan                          ★ bổ sung
│   ├── Giờ mở cửa & Giá vé           (gộp "ve" + thêm giờ)
│   ├── Hướng dẫn & Bản đồ             (mới)
│   ├── Nội quy tham quan              (bỏ "-6-2")
│   ├── Dịch vụ tham quan
│   └── Tiện ích tại di tích
│
├── Hoạt động                          ★ gộp + mở rộng
│   ├── Trưng bày thường xuyên         (gộp 2 trang hiện có)
│   └── Sự kiện & Triển lãm chuyên đề  (mới — chỗ cho sự kiện theo thời gian)
│
├── Giáo dục di sản                    ★ 2 view
│   ├── Theo chương trình             (mới — primary navigation)
│   │   ├── Đi tìm linh vật          (MN, 1–3, 4–6, 7–12)
│   │   ├── Khám phá Bia Tiến sĩ     (1–3, 4–6, 7–12)
│   │   ├── Ô kìa con Nghê           (MN, 1–3, 4–6, 7–12)
│   │   ├── Mãnh hổ hạ sơn           (MN, 1–3)
│   │   ├── Khuê Văn Các & Kiến trúc  (1–3, 4–6, 7–12)
│   │   ├── Lớp học xưa              (1–3, 4–6)
│   │   ├── Khoa cử: Thi Hương–Hội–Đình · Vinh quy bái tổ   (7–12)
│   │   ├── Sách học & Ván khắc      (7–12)
│   │   └── QTG Thăng Long · VM xưa-nay · Môi trường (7–12)
│   └── Theo lứa tuổi                 (view phụ — URL cũ giữ cho SEO)
│       ├── Mầm non · Lớp 1–3 · Lớp 4–6 · Lớp 7–12
│
└── Về chúng tôi                       ★ mở rộng
    ├── Giới thiệu Trung tâm           (trang hiện có)
    ├── Liên hệ                        (mới — email, ĐT, địa chỉ, form)
    ├── Đội ngũ                        (mới — không bắt buộc)
    └── Tin tức & Báo chí              (mới — trống ban đầu cũng OK)
```

---

## 4. Lý do thay đổi — theo chuyên mục

### Di tích → chia `Danh nhân` thành 5 nhóm
- **Vấn đề:** 21 bài flat, người dùng phải scroll/đoán.
- **Lợi ích:** người tìm "Tế tửu Quốc Tử Giám là ai?" có nhóm riêng 10 vị. Chu Văn An có trang hub kết nối Danh nhân + Tượng thờ.
- **Cost:** build.py cần thêm phân loại (có thể manual — chỉ 21 bài).

### Di tích → gộp bản EN của Bia Tiến sĩ vào `<details>`
- **Vấn đề:** 1 trang EN tách riêng → trùng lặp, sitemap có entry lạ `THE STONE STELAE…`.
- **Lợi ích:** nhất quán với 82 trang bilingual khác đã dùng `<details>`.
- **Cost:** sửa logic `collect_articles_recursive` để không tạo page cho folder EN khi đã merge.

### Tham quan → bổ sung Giờ mở cửa + Bản đồ, sửa tên
- **Vấn đề:** thông tin khách cần nhất (giờ, bản đồ) đang nằm ở footer hoặc không có.
- **Lợi ích:** Tham quan thực sự hữu ích cho first-time visitor.
- **Cost:** 2 trang nội dung mới, cần ảnh bản đồ.

### Hoạt động → gộp 2 trang trưng bày + chừa chỗ sự kiện
- **Vấn đề:** "Chú thích ảnh" là phụ lục không nên là page riêng.
- **Lợi ích:** section này hiện chỉ 2 bài → yếu. Chừa slot cho triển lãm chuyên đề tương lai.
- **Cost:** gộp 2 file `.docx` thành 1 khi build.

### Giáo dục di sản → **pivot sang chương trình làm primary**
- **Vấn đề:** chương trình lặp qua 4 lứa tuổi. Giáo viên muốn biết chương trình "Đi tìm linh vật" khác nhau thế nào giữa MN và 7–12 → hiện tại phải mở 4 trang rời rạc.
- **Lợi ích:** mỗi chương trình có 1 trang hub liệt kê các biến thể theo lứa tuổi, có bảng so sánh. Giữ URL cũ `/lop-1-3/...` cho SEO.
- **Cost:** thêm layer index theo theme. Không phải xóa trang nào.

### Về chúng tôi → mở rộng thành institutional landing
- **Vấn đề:** 1 trang quá mỏng cho "đầu não" của site.
- **Lợi ích:** người muốn hợp tác/liên hệ/đặt đoàn có điểm đến rõ.
- **Cost:** cần nội dung — có thể bắt đầu chỉ với trang Liên hệ.

---

## 5. Quick wins — làm được ngay, không cần thêm nội dung

| # | Việc | File | Thời gian |
|---|---|---|---|
| 1 | Đổi `Khám phá di tích` → `Khám phá Văn Miếu – Quốc Tử Giám` ở home | `build.py:build_home` | 2 phút |
| 2 | Title-case cho tiêu đề ALL CAPS khi render listing & sitemap | `build.py:text_to_html` | 10 phút |
| 3 | Strip prefix số lạc (`10te-tuu-…`, `noi-quy-…-6-2`) | `build.py:strip_lead_num` mở rộng | 5 phút |
| 4 | Gộp 2 trang `hoat-dong/trung-bay-trien-lam-*` thành 1 | Gộp file nguồn `.docx` | 10 phút |
| 5 | Fix bản EN Bia Tiến sĩ tách riêng | `build.py:collect_articles_recursive` | 20 phút |
| 6 | Rename slug `ve` → `gia-ve`, thêm redirect | `build_tham_quan` + `vercel.json` rewrites | 10 phút |

---

## 6. Thay đổi cấu trúc — cần bàn trước khi làm

| # | Việc | Ảnh hưởng |
|---|---|---|
| A | Chia `Danh nhân & dòng họ` thành 5 nhóm | URL mới, cần redirect từ URL cũ |
| B | Pivot Giáo dục di sản theo chương trình | Thêm trang, URL cũ giữ |
| C | Bổ sung Tham quan: giờ, bản đồ, hướng dẫn | Cần nội dung nguồn |
| D | Mở rộng Về chúng tôi | Cần nội dung nguồn |

Đề xuất: làm Quick wins (§5) trước → xem lại §6 sau khi có nội dung cho C & D.
