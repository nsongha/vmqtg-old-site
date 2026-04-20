# Văn Miếu – Quốc Tử Giám (Old Site)

Static website MVP sinh tự động từ dữ liệu nguồn (.docx + ảnh) của di tích Văn Miếu – Quốc Tử Giám.

## Tech stack

- **Static HTML / CSS thuần** — không framework, không runtime, không database.
- **Build script: Python 3 + `textutil` (macOS)** — convert .docx → text → HTML.
- **Image pipeline: `sips` (macOS)** — resize max 1600px + nén JPEG quality 82.
- **Hosting: Vercel** — chỉ serve static files, không build trên server.

> **Lưu ý:** Build script chỉ chạy được trên **macOS** (vì dùng `textutil` & `sips`).
> Vercel chỉ deploy thư mục `site/` đã build sẵn — không chạy lại Python.

## Cấu trúc

```
.
├── site/                      ← OUTPUT — deploy thư mục này
│   ├── index.html
│   ├── di-tich/               (Trang 1: lịch sử, bia, tượng, danh nhân)
│   ├── tham-quan/             (Trang 2: vé, nội quy, dịch vụ)
│   ├── hoat-dong/             (Trang 3: trưng bày)
│   ├── giao-duc-di-san/       (Trang 4: chương trình theo cấp học)
│   ├── ve-chung-toi/          (Trang 5)
│   ├── assets/{css,js,images}
│   └── build.py               ← script build (không deploy)
├── Trang 1 Trang di tich/     ← DỮ LIỆU NGUỒN (.docx + ảnh)
├── Trang 2 Thăm quan/
├── Trang 3 các hoạt động/
├── trang 4 Trang Giáo dục di sản/
├── Trang 5 Về chúng tôi/
├── vercel.json                ← config Vercel
├── .vercelignore              ← loại trừ data nguồn khỏi deploy
└── .gitignore
```

## Build local

```bash
cd site
python3 build.py
```

Build mất ~30s. Output ra `site/{di-tich,tham-quan,...}` + `site/assets/images/`.
Mỗi lần chạy sẽ xoá output cũ và rebuild từ đầu.

## Preview local

```bash
cd site
python3 -m http.server 8000
# → http://localhost:8000
```

## Deploy

### Khuyến nghị: **GitHub Pages** (free, auto-deploy khi push)

**Setup 1 lần**:

1. Tạo repo public trên GitHub (ví dụ tên `vmqtg-old-site`).
2. Vào **Settings → Pages → Build and deployment → Source**: chọn **"GitHub Actions"**.
3. Push code lên branch `main`:
   ```bash
   cd "/Users/songha/Documents/Projects/Website VMQTG - olddata"
   git init
   git add .
   git commit -m "initial"
   git branch -M main
   git remote add origin https://github.com/<user>/vmqtg-old-site.git
   git push -u origin main
   ```
4. Actions tự chạy build (macOS runner) và deploy. Xem tab **Actions** để theo dõi.
5. Khi xong: site có tại `https://<user>.github.io/vmqtg-old-site/`.

**Lần sau**: mỗi lần `git push` → Actions tự rebuild + deploy.

**Lưu ý**:
- Workflow `.github/workflows/deploy.yml` đã tự set `BASE_PATH=/<repo-name>`, không cần cấu hình gì thêm.
- Nếu dùng repo tên `<user>.github.io` (1 repo/account), site ở gốc domain → xoá dòng `BASE_PATH: ...` trong workflow.
- Public repo → Actions miễn phí không giới hạn; private repo: macOS runner tốn 10× minutes (200 phút free/tháng).

### Alt 1: **Cloudflare Pages** (simple, free, 500MB)

1. `vercel.json` không dùng được; tạo file `site/_headers`:
   ```
   /assets/*
     Cache-Control: public, max-age=31536000, immutable
   ```
2. Connect repo trên https://pages.cloudflare.com → **Build command**: để trống. **Output**: `site`.
3. (Tuỳ chọn) Build trên Cloudflare không khả thi vì `textutil` macOS-only → phải commit sẵn `site/` output.

### Alt 2: **Vercel**

Đã có sẵn `vercel.json`:
```bash
npm i -g vercel
vercel --prod
```
Site ~66MB — vừa giới hạn 100MB Vercel Hobby.

### Alt 3: **Tunnel từ máy bạn** (test nhanh, không cần upload)

Cloudflare Quick Tunnel (không cần tài khoản):
```bash
brew install cloudflared
cd site && python3 -m http.server 8000 &
cloudflared tunnel --url http://localhost:8000
# → https://xxx-xxx.trycloudflare.com
```
URL sống đến khi tắt process. Phù hợp demo tạm thời.

## BASE_PATH

Build script hỗ trợ env var `BASE_PATH` để deploy dưới subpath (GitHub project repo):

```bash
BASE_PATH=/vmqtg-old-site python3 build.py
```

Không set → deploy ở root domain (Vercel, Netlify, Cloudflare, hoặc repo `<user>.github.io`).

## Size deploy

- Site build: **~66MB** (81 trang HTML + 131 ảnh đã nén)
- Nguồn: ~700MB (bị `.vercelignore` loại trừ khi push Vercel; với GitHub Pages, dữ liệu nguồn cũng lên repo nhưng không ảnh hưởng deploy size)

## Số liệu

- 81 trang HTML (5 section + index + ~70 article)
- 131 ảnh đã nén (từ ~200 ảnh gốc, có file gộp do dedup)
- Song ngữ Việt / Anh ở những bài có sẵn cả hai bản (collapse `<details>`)

## Hạn chế đã biết

- Một số bài (đặc biệt nhánh Chu Văn An trong "Tế tửu – Tư nghiệp") chỉ có ảnh trong source, không có .docx → không sinh được trang.
- Tiếng Anh chỉ có ở ~1/3 số bài.
- Trang chủ + thông tin liên hệ ở footer là hardcoded (lấy từ doc Trung tâm + nội quy tham quan).
- Không có search, không có map, không có version EN cho UI chrome (nav/footer luôn tiếng Việt).

Các phần này sẽ làm ở phiên bản site mới.
