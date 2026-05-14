# VMQTG V5

Website Văn Miếu – Quốc Tử Giám phiên bản V5, theo sitemap **09.05.2026**.

Style: wireframe đơn sắc (đen / trắng / xám), typography unicode tiếng Việt
không gạch chân, ảnh grayscale, không animation phức tạp ở UI tĩnh.

## Cấu trúc

```
vmqtg-v5/
├── build.py                ← script Python sinh toàn bộ site
├── translations.py         ← bảng dịch VI / EN / FR
├── FEATURES.md             ← mô tả 2 tính năng JS (search + đổi ngôn ngữ)
├── index.html              ← trang chủ (sinh tự động)
├── tham-quan/              ← A. Tham quan
├── ve-di-tich/             ← B. Về di tích (mega menu, 6 nhóm, ~31 item)
├── trung-bay-trien-lam/    ← C. Trưng bày, triển lãm
├── cac-hoat-dong/          ← D. Các hoạt động
├── dich-vu/                ← E. Dịch vụ
└── assets/
    ├── css/style.css       ← sinh tự động
    ├── js/data.js          ← sinh tự động (i18n + search index)
    ├── js/app.js           ← sinh tự động (logic)
    └── images/             ← copy từ old-site
```

Tổng cộng **64 trang** HTML được sinh tự động từ `SITEMAP` trong `build.py`.

## Build

```bash
cd vmqtg-v5
python3 build.py
```

Script sẽ:
1. Xoá thư mục output cũ
2. Ghi `assets/css/style.css`
3. Ghi `assets/js/data.js` + `assets/js/app.js`
4. Copy ảnh từ `../site/assets/images/`
5. Render `index.html` + 63 trang con (section hub / group hub / item page)

## Sitemap

| ID | Mục | Type | Số trang |
|----|-----|------|----------|
| A  | Tham quan                | single   | 1 |
| B  | Về di tích               | mega     | 1 + 6 nhóm + 31 item = 38 |
| C  | Trưng bày, triển lãm     | dropdown | 1 + 3 + 3 = 7 |
| D  | Các hoạt động            | dropdown | 1 + 7 + 2 = 10 |
| E  | Dịch vụ                  | dropdown | 1 + 6 = 7 |

## Tính năng

- **Navigation hover** — mega-menu cho B, simple dropdown cho C/D/E (CSS-only, không JS).
- **Search autocomplete** — gõ tìm tên mục, không dấu, đa ngôn ngữ. → xem [FEATURES.md](FEATURES.md#1-tìm-kiếm-autocomplete)
- **Đổi ngôn ngữ VI/EN/FR live** — không reload, có hiệu ứng smart-move. → xem [FEATURES.md](FEATURES.md#2-đổi-ngôn-ngữ-vi--en--fr)
- **Breadcrumb** đa cấp, có dịch ngôn ngữ.
- **Sidebar điều hướng** trong từng nhóm (item page có sidebar list items, group page có sidebar list groups).
- **Mobile responsive** — search box thu nhỏ, mega menu wrap ở `max-width 900px`.

## Tài liệu

- [FEATURES.md](FEATURES.md) — chi tiết kỹ thuật 2 tính năng JS (search + i18n)

## Lưu ý vận hành

- `assets/js/data.js` là **build artifact**, không sửa thủ công.
- Thêm trang mới: chỉ cần sửa `SITEMAP` trong `build.py`, dịch label trong
  `translations.py`, rồi `python3 build.py`.
- Thêm nội dung dài (article body): thêm vào dict `CONTENT` trong `build.py`
  (bản VI) và `translations.py` `CONTENT` (bản EN/FR).
