# Website Văn Miếu – Quốc Tử Giám
## Báo cáo audit dữ liệu + đề xuất website mới

*Cập nhật: 2026-04-20 · Tác giả: team xây dựng site cũ*

> Tài liệu này **không** phải là báo cáo về site cũ. Đây là báo cáo về **bộ dữ liệu Văn Miếu đã gửi qua email** — dùng làm đầu vào cho việc xây website mới.

---

## 1. Bộ dữ liệu hiện có

### 1.1. Tổng quan

| Hạng mục | Số lượng | Ghi chú |
|---|---:|---|
| File tài liệu `.docx` | **264** | Toàn bộ bài viết |
| Ảnh (`.jpg`, `.png`, `.tif`) | **208** | ~700MB, chưa tối ưu web |
| Thư mục | **220** | Chia theo 5 khu vực chính |
| Tổng dung lượng thô | **~1.2 GB** | |

### 1.2. Cấu trúc thư mục

```
Website VMQTG/
├── Trang 1 Trang di tich/          (65 docx, 144 ảnh) — nội dung lõi
│   ├── Kiến trúc/                  (10 docx, VN only) — 10 khu công trình
│   ├── Lich su VM/                 (5 VN + 3 EN) — lịch sử qua các triều đại
│   ├── 82 bia Tiên sĩ/             (4 VN + 2 EN) — tổng quan hệ thống bia
│   ├── Hệ thống tượng thờ/         (10 VN + 5 EN) — 10 vị được thờ
│   └── Danh nhân và dòng họ/       (26 docx) — Tiến sĩ, Tế tửu, dòng họ khoa bảng
├── Trang 2 Thăm quan/              (4 docx) — vé, nội quy, dịch vụ, tiện ích
├── Trang 3 các hoạt động/          (2 docx + 13 ảnh) — trưng bày thường xuyên
├── trang 4 Trang Giáo dục di sản/  (192 docx, 51 ảnh) — chương trình học 4 cấp
└── Trang 5 Về chúng tôi/           (1 docx) — giới thiệu Trung tâm
```

### 1.3. Phân bố theo ngôn ngữ

| Ngôn ngữ | Số bài | % | Phạm vi |
|---|---:|---:|---|
| Tiếng Việt | 249 | **94%** | Toàn bộ 5 khu vực |
| Tiếng Anh | 15 | **6%** | Chỉ Trang 1 (Lịch sử, 82 bia, Tượng thờ, CVA) |
| Tiếng Pháp | 1 (nhúng) | **<1%** | Nhúng trong Nội quy tham quan |
| Trung / Hàn / Nhật | 0 | **0%** | (Hotline nói có audio guide 8 ngôn ngữ — nhưng tư liệu văn bản chưa có) |

### 1.4. Phân bố theo loại nội dung

| Loại | Bài | Đặc điểm |
|---|---:|---|
| Lịch sử kiến trúc | 15 | 10 bài Kiến trúc + 5 bài Lịch sử VN |
| 82 bia Tiến sĩ | 6 | Tổng quan (quá trình dựng, giá trị, UNESCO) — **không có per-stele data** |
| Danh nhân | 26 | Nguyễn Quý Đức, Nguyễn Trực, CVA (11 bài), Nguyễn Duy Thì, Phùng Khắc Khoan… |
| Hệ thống tượng thờ | 15 | Khổng Tử + Tứ Phối + Tứ Thánh + vua Lý Thánh Tông, Lý Nhân Tông, Lê Thánh Tông, CVA |
| Giáo dục di sản | 192 | 4 cấp × 3-6 chương trình × {nội dung, trước/sau thăm quan × cha mẹ/GV-HS} |
| Tham quan | 4 | Vé, nội quy, dịch vụ, tiện ích |
| Hoạt động | 2 | Trưng bày thường xuyên + caption ảnh |
| Về trung tâm | 1 | Lịch sử Trung tâm 30 năm |

---

## 2. Hiện trạng — Thừa, Thiếu, Trùng lặp

### 2.1. Thừa

- **11 ảnh orphan** — có folder có ảnh nhưng không có `.docx` bài viết:
  - 4 ảnh Chu Văn An (folder #1, #2, #6, #11)
  - 2 ảnh Nguyễn Duy Thì
  - 2 ảnh EN Chu Văn An (folder #6, #11 EN)
  - 2 ảnh "bia-tien-si.jpg" (dùng làm icon, folder không có bài)
  - 1 ảnh caption 82 bia

- **Chú thích ảnh rời rạc** — 2 file `Chú thích ảnh.docx` nằm ngoài bài viết chính, chỉ chứa mô tả từng ảnh, không có liên kết rõ ràng với hình.

### 2.2. Thiếu

#### 🔴 Cực kỳ quan trọng (chặn chức năng cơ bản)

| # | Hạng mục thiếu | Tác động |
|---|---|---|
| 1 | **Thông tin thực tế**: giờ mở cửa hiện hành, bản đồ, địa chỉ chi tiết | Site thăm quan không có mục đích chính |
| 2 | **Giá vé cập nhật** — file hiện có 30.000đ chưa chắc đúng 2026 | Khách không biết giá thật |
| 3 | **Trang chủ**: hero, giới thiệu ngắn, tin nổi bật | Không có landing page |
| 4 | **Lịch sự kiện** — lễ tế Khổng Tử, vinh danh thủ khoa, triển lãm đặc biệt | Không có "present" — chỉ có "past" |
| 5 | **Database 82 bia Tiến sĩ**: 1.304 vị Tiến sĩ với năm thi, khoa thi, quê quán, trạng nguyên/bảng nhãn/thám hoa | Hạt nhân của di tích — hiện chỉ có bài tổng quan |

#### 🟡 Quan trọng (chất lượng)

| # | Hạng mục | Hiện trạng |
|---|---|---|
| 6 | EN cho Kiến trúc (10 công trình) | 0/10 |
| 7 | EN cho các vị Tiến sĩ (6 bài VN) | 0/6 |
| 8 | EN cho Trang 2 Tham quan | Chỉ 1/4 (Nội quy) |
| 9 | EN cho toàn bộ Giáo dục di sản | 0/192 |
| 10 | EN cho Lịch sử giai đoạn Lê sơ + Lê Trung hưng | 2 giai đoạn thiếu |
| 11 | EN cho Tứ Phối (Nhan Tử, Tăng Tử, Tử Tư, Mạnh Tử) | 4 bài thiếu |
| 12 | 7 bài VN thiếu docx (CVA, Nguyễn Duy Thì — có ảnh) | Phải viết mới |
| 13 | Tiếng Trung / Hàn / Nhật / Pháp đầy đủ | Chưa có (dù audio guide đã hỗ trợ 8 ngôn ngữ) |

#### 🟢 Nâng chất (nice-to-have)

- Video giới thiệu (drone footage, timelapse lễ tế…)
- Ảnh HDR hoặc 360° cho virtual tour
- Audio guide bản viết (hiện chỉ có thiết bị tự động)
- Infographic về kiến trúc, lịch sử
- Tài liệu nghiên cứu học thuật, bibliography

### 2.3. Trùng lặp

| # | Trùng lặp | Mô tả |
|---|---|---|
| 1 | Folder naming inconsistent | `Tiếng Việt` / `Tieng Viet` / `tieng viet` — cả 3 biến thể |
| 2 | Nguyễn Trực có 2 bài sát nhau | "Trạng nguyên Nguyễn Trực" + "Tế tửu QTG Nguyễn Trực" — gần như cùng nhân vật, 2 bài |
| 3 | Chu Văn An có **11 bài** | Nhiều góc độ: tiểu sử, đóng góp giáo dục, tín ngưỡng, ảnh hưởng đương thời, v.v. Có thể hợp nhất thành 1 hub chính + subsections |
| 4 | Chương trình Khuê Văn Các | Lớp 1-3 + lớp 4-6 có chương trình rất giống (tên gần trùng, nội dung lặp) |
| 5 | Nguyễn Duy Thì có 4 bài sub-article | Có thể gộp thành 1 hub danh nhân |
| 6 | Nội dung CVA xuất hiện ở **3 vị trí**: Tượng thờ, Danh nhân/Tế tửu, và có thể Lịch sử | Cần canonical page + cross-link |

---

## 3. Đề xuất cấu trúc website mới

### 3.1. Đối tượng sử dụng

| Đối tượng | % ước tính | Nhu cầu chính |
|---|---:|---|
| **Khách du lịch quốc tế** | 35% | Mua vé, bản đồ, ngôn ngữ nước mình, audio guide, virtual tour preview, timeline lịch sử dễ hiểu |
| **Khách du lịch Việt Nam** | 40% | Giá vé, giờ mở cửa, sự kiện, chụp ảnh check-in, mang theo app audio |
| **Học sinh, sinh viên, gia đình** | 15% | Chương trình giáo dục, workshop, học liệu trước/sau tour, quiz |
| **Nhà nghiên cứu, báo chí** | 5% | Database 82 bia + 1.304 Tiến sĩ, bibliography, download ảnh res cao |
| **Người Hà Nội ghé thăm lễ tết** | 5% | Lịch lễ tế, đăng ký xin chữ, dâng hương |

### 3.2. Information Architecture (sitemap đề xuất)

```
🏠  Trang chủ                        Hero ấn tượng · Quick actions · Tin nổi bật
│
├── 🏛  KHÁM PHÁ (Discover)
│   ├── Tổng quan di tích             Giới thiệu chung, thống kê, video 60s
│   ├── Timeline lịch sử              (INTERACTIVE) Lý → Trần → Hồ → Lê → Nguyễn → nay
│   ├── Kiến trúc                     10 công trình, map tương tác click-to-zoom
│   ├── 82 Bia Tiến sĩ                (INTERACTIVE) Filter 1.304 vị theo năm/khoa/quê
│   ├── Hệ thống tượng thờ            Khổng Tử + Tứ Phối + vua + CVA
│   └── Danh nhân khoa bảng            Grid các tiến sĩ, tế tửu, dòng họ
│
├── 🎫  THĂM QUAN (Visit)
│   ├── Kế hoạch chuyến đi             Giờ mở cửa, giá vé, map, hướng dẫn đi
│   ├── Mua vé online                 (INTERACTIVE) Chọn giờ, số lượng, thanh toán
│   ├── Nội quy tham quan              VN/EN/FR
│   ├── Dịch vụ tại chỗ               Thuyết minh 8 ngôn ngữ, thuê audio guide
│   ├── Tiện ích                       Đỗ xe, café, đồ lưu niệm
│   └── Tour theo chủ đề               "Hành trình Tiến sĩ", "Kiến trúc 1h", "Đặc biệt đêm"
│
├── 🌐  BẢO TÀNG SỐ (Virtual Museum)   — mới hoàn toàn
│   ├── Virtual tour 360°             8 điểm + hotspot thông tin
│   ├── AR trên điện thoại             Scan bia → xem dịch + tên các vị
│   ├── Bộ sưu tập 3D                  Bia đá, tượng thờ, hiện vật
│   └── Audio guide                    Stream trực tuyến + download offline
│
├── 🎭  SỰ KIỆN & HOẠT ĐỘNG (What's On)
│   ├── Sự kiện sắp tới                (CALENDAR) Lễ tế Khổng Tử, triển lãm, vinh danh
│   ├── Trưng bày thường xuyên
│   ├── Triển lãm đặc biệt             Hiện tại + sắp diễn ra
│   ├── Lễ hội truyền thống            Xin chữ đầu năm, tế Khổng Tử, vinh danh thủ khoa
│   └── Đặt chỗ sự kiện                Form đăng ký
│
├── 📚  GIÁO DỤC DI SẢN (Education)
│   ├── Chương trình cho mầm non
│   ├── Chương trình cho tiểu học (lớp 1-3 / 4-6)
│   ├── Chương trình cho THCS-THPT (lớp 7-12)
│   ├── Workshop cuối tuần cho gia đình
│   ├── Học liệu tải về                PDF trước/sau tour, bài tập, quiz
│   └── Đặt chương trình                Form dành cho trường + nhóm
│
├── 📰  TIN TỨC & BLOG
│   ├── Tin mới nhất
│   ├── Thông báo
│   └── Bài nghiên cứu
│
├── 🛍  CỬA HÀNG LƯU NIỆM               — mới
│   ├── Sách, cataloge triển lãm
│   ├── Đồ lưu niệm handmade
│   └── Bản dập bia Tiến sĩ (replica)
│
└── ℹ️  VỀ CHÚNG TÔI
    ├── Trung tâm Hoạt động VHKH
    ├── Cơ cấu tổ chức
    ├── Tuyển dụng
    ├── Liên hệ + hợp tác
    └── Tin báo chí
```

### 3.3. Language switcher

- **VN** (default) / **EN** / **FR** / **中文** / **한국어** / **日本語** — 6 ngôn ngữ match audio guide
- Auto-detect `Accept-Language` header cho visitor mới
- Preserve chọn trong localStorage + cookie
- Hiển thị tên gốc mỗi ngôn ngữ (không translate), có cờ nhỏ

---

## 4. Sản phẩm số hóa (digital products) — tính năng mới

### 4.1. Timeline lịch sử tương tác 🕰
> *Cứu cánh cho "6% EN coverage" — timeline visual ít text hơn, dễ bản địa hoá.*

- Scroll-based, parallax ảnh
- Các mốc: 1070 dựng Văn Miếu → 1076 lập Quốc Tử Giám → 1484 bắt đầu dựng bia → các triều đại chính → 2010 công nhận Di tích QG đặc biệt → 2011 bia Tiến sĩ vào UNESCO
- Mỗi mốc: 1 ảnh, 1-2 câu, link "Đọc thêm" mở panel
- Filter theo: triều đại · loại sự kiện (xây dựng / khoa thi / lịch sử lớn)
- Export PNG để HS in ra

### 4.2. Timeline + Database 82 Bia Tiến sĩ 📜
> *Core feature — phải làm đúng, tôn vinh 1.304 vị Tiến sĩ.*

- Bản đồ dạng lưới 82 bia, click để xem:
  - Năm khoa thi, triều đại, số người đỗ
  - Tên đầy đủ các vị Tiến sĩ (Trạng nguyên, Bảng nhãn, Thám hoa, Hoàng giáp, Đồng tiến sĩ)
  - Quê quán (bản đồ VN chấm đỏ)
  - Ảnh bia res cao + bản dịch văn bia (nếu có)
- **Filter nâng cao**:
  - Theo năm thi (slider 1442-1779)
  - Theo quê quán (province dropdown)
  - Theo họ (trong 1.304 vị có bao nhiêu họ Nguyễn, họ Lê…)
  - Theo dòng họ khoa bảng
- **Search**: "Có vị Tiến sĩ nào họ Nguyễn, quê Hải Dương, đỗ năm 1535 không?"
- Chia sẻ 1 vị Tiến sĩ cụ thể qua URL + social card

### 4.3. Bán vé online 🎫

- Chọn ngày, khung giờ (30 phút/slot), số lượng vé
- Các loại vé: Người lớn · HS/SV · 60+ · Trẻ dưới 15 · Nhóm · Family pack · Vé năm
- Upsell: audio guide + tour thuyết minh
- Thanh toán:
  - **VN**: VNPay, MoMo, ZaloPay, thẻ nội địa
  - **International**: Stripe (Visa/MC/Amex), Apple Pay, Google Pay
- QR code gửi qua email + Apple Wallet / Google Wallet
- Quét QR tại cửa, không cần in giấy
- Huỷ/đổi trong vòng 24h trước
- Đặt theo nhóm: sinh nhật, học đường, doanh nghiệp — có discount code

### 4.4. Bảo tàng ảo / Virtual tour 360° 🥽

- **8 điểm 360°**: Cổng VM, Đại Trung Môn, Khuê Văn Các, giếng Thiên Quang, vườn bia, Đại Thành Môn, điện Đại Thành, nhà Thái Học
- Matterport hoặc Pannellum embed
- Hotspot tương tác: click vào Khuê Văn Các → popup giải thích kiến trúc, link đến bài viết đầy đủ
- Mode "đi tour có HDV ảo" — audio tự động phát theo từng điểm
- Preview miễn phí 2 điểm · full bundle 5 điểm qua subscription hoặc sau khi mua vé

### 4.5. AR (Augmented Reality) trên điện thoại 📱

- Scan 1 bia Tiến sĩ → popup overlay:
  - Dịch nghĩa văn bia
  - Danh sách các vị được khắc tên
  - Năm thi, khoa thi
  - Đọc to (audio 8 ngôn ngữ)
- Tech: WebXR (không cần app), fallback QR code nếu WebXR không hỗ trợ
- Gamification: "Khám phá đủ 10 bia để nhận huy hiệu số"

### 4.6. Audio guide streaming 🎧

- Thay thế thiết bị thuê tại chỗ cho khách có smartphone
- 8 ngôn ngữ: VN, EN, FR, ES, KR, JA, CN, TH
- Download offline (PWA, ~50MB/ngôn ngữ)
- Giọng chuyên nghiệp, không AI-voice
- Free với vé đã mua (kèm QR code)

### 4.7. AI Search / Chatbot di sản 🤖

- "Kể cho tôi về Khuê Văn Các" · "Có tiến sĩ nào quê Nam Định không?" · "Giờ tôi vào thì đông không?"
- LLM + RAG trên chính content của site (bao giờ có thêm dữ liệu 82 bia)
- Gợi ý câu hỏi thông dụng
- Đa ngôn ngữ

### 4.8. Calendar sự kiện + đăng ký 📅

- Tháng xem kiểu Google Calendar
- Lọc theo: Lễ tế · Triển lãm · Workshop · Sự kiện cộng đồng
- Click sự kiện → mô tả + nút "Đăng ký" (form hoặc link vé)
- Add to calendar (Google/Apple/Outlook)
- Newsletter subscribe

### 4.9. Bản đồ tương tác 🗺

- MapBox GL hoặc Leaflet với vector tiles
- Zoom từ quận Đống Đa vào toàn cảnh VM → click từng công trình
- Click công trình → sidebar panel với ảnh + mô tả + link bài chi tiết
- "Trip planner": tôi có 60 phút, gợi ý 5 điểm phải xem
- Chia đường: từ vị trí tôi → cổng VM (Google Maps deep link)

### 4.10. Gamification giáo dục 🎮

- Sau khi HS tham gia chương trình → quiz 10 câu trên điện thoại
- Huy hiệu số theo cấp: "Nhà sử học trẻ", "Khám phá Khuê Văn Các"
- Leaderboard trường / lớp
- Giáo viên xem dashboard kết quả

### 4.11. Cửa hàng lưu niệm số 🛒

- Bản dập bia Tiến sĩ limited, sách, đồ thủ công
- Check-in tại shop → unlock voucher
- Gift set cho du khách nước ngoài
- Ship nội địa VN + quốc tế (DHL)

### 4.12. Newsletter + CRM 📧

- Subscribe theo chủ đề: Sự kiện · Giáo dục · Nghiên cứu
- Tự động nhắc sinh nhật (cho tiến sĩ nào đó cùng ngày sinh bạn!) — fun feature
- Segment: khách nội địa / quốc tế / trường học

---

## 5. Yêu cầu về Design & UX

### 5.1. Nguyên tắc thiết kế

| Nguyên tắc | Chi tiết |
|---|---|
| **Mobile-first** | >65% visitors du lịch là mobile. Design cho màn 375px trước, rồi scale lên |
| **Tốc độ** | LCP <2s, INP <200ms trên 4G. Ảnh AVIF/WebP, critical CSS inline, lazy load |
| **Tối giản có chiều sâu** | Trắng/kem làm nền, ít màu, typography mạnh. Không clip-art, không gradient chói |
| **Cinematic imagery** | Ảnh full-bleed, ít nhưng chất lượng cao. Video ambient khi network cho phép |
| **Chuyển động tinh tế** | Micro-interaction hover, scroll-reveal, parallax nhẹ. Không overdo |
| **Accessibility WCAG 2.2 AA** | Alt text mọi ảnh, keyboard nav, contrast ≥4.5, skip links, screen reader |
| **Đa ngôn ngữ** | Language switcher bên phải header, không giấu trong menu |
| **Tìm kiếm ưu tiên** | Search bar icon luôn hiện ở header, open với `/` hoặc Cmd+K |
| **Không popup xâm lấn** | Không pop-up đăng ký email sau 3s. Subtle banner dưới cùng |

### 5.2. Hệ thống thiết kế đề xuất

**Palette** (lấy cảm hứng kiến trúc VM, tinh chỉnh cho web):
- **Nền chính**: `#FBF8F1` (giấy gió nhạt) — thay cho trắng trần
- **Text**: `#1E1812` (nâu mực) — thay cho đen
- **Accent chính**: `#9B1B1B` (đỏ son sáng) — chỉ dùng cho CTA, link
- **Accent phụ**: `#C9A14A` (vàng kim sáng) — border, highlight
- **Xanh ngói**: `#34524A` (xanh rêu lợp) — dark mode base

**Typography**:
- **Display** (tiêu đề): `Playfair Display` (serif cổ điển, có đường nét thanh đậm rõ) HOẶC `Source Serif 4`
- **Body**: `Inter` (clean, mở, hỗ trợ tiếng Việt tốt) HOẶC `Be Vietnam Pro`
- **Tiêu đề chữ Hán**: `Noto Serif TC` cho văn bia, thư pháp
- Hierarchy rõ ràng: H1 48px/72px, H2 32px/48px, body 17px/28px, mobile scale 87%

**Layout grid**: 12-col, gutter 24px, max-width 1280px · container 1100px

**Components** (shadcn/ui + Tailwind):
- Button, Card, Dialog, Sheet, Tabs, Accordion — prebuilt đẹp
- Custom: TimelineScroll, StelaeFilter, VirtualTourEmbed, TicketPicker, LanguageSwitcher

**Iconography**: Lucide (line icons), kết hợp custom glyph cho các công trình kiến trúc

**Hình ảnh**:
- Chụp mới bằng máy FF + ống fix chất lượng cao
- Golden hour + blue hour cho ảnh kiến trúc ngoài trời
- Detail close-up: thư pháp, chi tiết chạm khắc, rêu phủ
- Ảnh con người: du khách tương tác, HS học tập, các lễ tế
- **Tránh**: ảnh rẻ tiền từ stock, ảnh AI-generated

---

## 6. Tech stack đề xuất

| Lớp | Công nghệ | Lý do chọn |
|---|---|---|
| Frontend | **Next.js 15 App Router** | SSR/SSG kết hợp, i18n built-in, tốt cho SEO, giỏi image optimization |
| UI | **Tailwind CSS v4** + **shadcn/ui** | Design system modern, dễ maintain, accessibility built-in |
| CMS | **Sanity** (headless) HOẶC **Payload CMS** | Staff cập nhật triển lãm, sự kiện, tin tức không cần dev. Block-based editor. |
| Auth | **Clerk** hoặc **Auth.js** | Cho admin + user mua vé |
| Payment | **Stripe** (quốc tế) + **VNPay / ZaloPay / MoMo** (nội địa) | Coverage toàn cầu |
| Database | **Postgres** (Supabase / Neon) | Booking, events, CRM |
| Search | **Meilisearch** hoặc **Typesense** | Nhanh, on-prem hoặc cloud, tốt với Tiếng Việt có dấu |
| Maps | **MapBox GL JS** | Đẹp, customizable style, hỗ trợ 3D buildings |
| Virtual tour | **Matterport** (pro) HOẶC **Pannellum** (open-source) | |
| Analytics | **Plausible** (privacy) + **Google Analytics 4** | |
| Images | **Cloudinary** hoặc **Imgix** | Auto format/resize/CDN, AVIF support |
| Hosting | **Vercel** (frontend) + **Supabase** (DB) | Deploy dễ, edge network, tốt cho VN |
| CDN | **Cloudflare** (trước Vercel) | Tăng tốc VN, chống DDoS |
| AI | **OpenAI API** + **RAG** qua LangChain | Chatbot di sản, search tự nhiên |
| Email | **Resend** + **React Email** | Transactional + marketing |
| i18n | **next-intl** | Type-safe, route-based locale |

---

## 7. Roadmap triển khai

### Phase 1 — MVP (Tháng 1–3): ~60% giá trị

- [x] Content migration từ site cũ (đã có 264 docx → 102 trang)
- [ ] Redesign UI hiện đại với design system mới
- [ ] Trang chủ + các section chính
- [ ] Timeline lịch sử interactive
- [ ] Mua vé online (VN + Stripe quốc tế)
- [ ] Bản đồ tương tác 10 công trình kiến trúc
- [ ] CMS cho staff (events, news)
- [ ] Multi-lang: VN + EN (nội dung tối thiểu đã có + bổ sung EN Kiến trúc)
- [ ] Mobile-first responsive
- [ ] Tìm kiếm cơ bản
- [ ] SEO + analytics

**Output**: Site sẵn sàng đón khách du lịch quốc tế, bán vé online

### Phase 2 — Rich features (Tháng 4–6)

- [ ] Database 82 bia + 1.304 Tiến sĩ — **cần đội research scan/số hoá bia**
- [ ] Virtual tour 360° — 8 điểm
- [ ] Audio guide streaming (VN + EN đầu tiên)
- [ ] Calendar sự kiện + đăng ký
- [ ] Bản dịch EN đầy đủ cho Kiến trúc, Tiến sĩ, Tham quan
- [ ] Thêm ngôn ngữ FR + CN (dựa trên audio guide có sẵn)

### Phase 3 — Bảo tàng số (Tháng 7–12)

- [ ] AR scan bia qua WebXR
- [ ] 3D models bia, tượng, hiện vật
- [ ] AI chatbot di sản
- [ ] Gamification giáo dục
- [ ] Cửa hàng lưu niệm online
- [ ] KR + JA + TH (đầy đủ 8 ngôn ngữ như audio guide)
- [ ] Mobile app (PWA hoặc native)

---

## 8. KPI đo đạc (sau 6 tháng launch)

| Chỉ số | Mục tiêu | Baseline site cũ |
|---|---|---|
| Visitors/tháng | 150.000+ | ~20.000 |
| Tỉ lệ khách quốc tế | >30% | <10% |
| Thời gian trung bình trên site | >3 phút | 1:20 |
| Bounce rate | <50% | 68% |
| Mobile share | >65% | 40% |
| Tỉ lệ mua vé online / truy cập | >5% | 0% (chưa có) |
| Lighthouse Performance | >90 | <50 |
| Lighthouse Accessibility | >95 | ~70 |
| LCP | <2s | 4.5s |
| Search impressions/tháng (Google) | 300.000+ | ~40.000 |

---

## 9. Ngân sách ước tính (tham khảo)

| Hạng mục | Phase 1 | Phase 2 | Phase 3 |
|---|---:|---:|---:|
| Design system + UX | ₫300M | ₫100M | ₫80M |
| Frontend development | ₫400M | ₫300M | ₫400M |
| Backend + CMS | ₫250M | ₫200M | ₫200M |
| Content (viết bổ sung, dịch) | ₫150M | ₫300M | ₫200M |
| Ảnh + video chụp mới | ₫150M | ₫100M | ₫100M |
| Virtual tour (8 điểm Matterport) | — | ₫200M | — |
| Database 82 bia (số hoá + OCR Hán Nôm) | — | ₫500M | — |
| 3D scan bia + tượng | — | — | ₫400M |
| Audio guide 8 ngôn ngữ | — | ₫300M | ₫200M |
| QA, testing, accessibility | ₫80M | ₫80M | ₫80M |
| Hạ tầng cloud (12 tháng) | ₫60M | ₫60M | ₫60M |
| **Tổng** | **₫1.39B** | **₫2.14B** | **₫1.72B** |

*Ngân sách tham khảo, phụ thuộc scope chi tiết + team size.*

---

## 10. Kết luận

### Điểm mạnh của data hiện có
1. ✅ **Lõi nội dung lịch sử & văn hoá mạnh** — 264 bài, 208 ảnh
2. ✅ **Giáo dục di sản** — hệ thống 192 tài liệu cho 4 cấp học, hiếm di tích nào có
3. ✅ **Chuyên môn cao** — bài viết của chính Trung tâm, có giá trị học thuật

### Điểm yếu cần giải quyết
1. ❌ **Thiếu "present"** — không có sự kiện, triển lãm đang/sắp diễn ra
2. ❌ **Không có database 82 bia** — đây là linh hồn di tích
3. ❌ **EN yếu, thiếu 4 ngôn ngữ khác** — audio guide đã có 8 mà web chỉ 2
4. ❌ **Không có chức năng giao dịch** — vé, đặt chỗ, shop

### Cơ hội
- Văn Miếu là **điểm du lịch top 5 Hà Nội** — traffic tự nhiên lớn nếu SEO tốt
- UNESCO brand — kéo khách quốc tế
- Data giáo dục → partnership với Sở GD Hà Nội, trường học toàn quốc
- Dữ liệu 82 bia, nếu số hoá đúng, thành **nguồn nghiên cứu học thuật toàn cầu**

### Khuyến nghị thứ tự ưu tiên
1. 🔴 **Tuần 1-2**: Khảo sát đối tượng du khách thực tế (survey + phỏng vấn 30 người)
2. 🔴 **Tuần 3-4**: Design system + high-fi prototype 3 màn chính
3. 🔴 **Tháng 2**: Build MVP (Phase 1 features)
4. 🟡 **Tháng 3-4**: Content bổ sung (EN Kiến trúc + Tiến sĩ, 7 bài CVA VN còn thiếu)
5. 🟡 **Tháng 5-6**: Database 82 bia (đội research chuyên về Hán Nôm)
6. 🟢 **Tháng 7-12**: Bảo tàng số (virtual tour, AR, 3D)

---

*Tài liệu này là foundation cho một site xứng tầm Di tích Quốc gia Đặc biệt đầu tiên của Việt Nam. Mọi quyết định thiết kế và công nghệ đều hướng đến mục tiêu: **tôn vinh 950+ năm đạo học & khiến mỗi du khách — trong hay ngoài nước — ra về với một điều gì đó đáng nhớ**.*
