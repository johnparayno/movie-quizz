# pua

A frontend-only PWA that displays one-liners. Swipe or tap thumbs up/down to vote and see the next item. Content from `content.json`; votes stored locally in the browser.

## Quick start

```bash
cd frontend
python -m http.server 3000
```

Open http://localhost:3000

## Deploy via FTP (GigaHost, etc.)

1. Upload everything inside the `frontend/` folder to your web root (e.g. `public_html/`).
2. Serve over HTTPS for full PWA support.
3. Works in subfolders too — upload to `public_html/pua/` if needed.

**Files to upload:**
- index.html
- app.js
- styles.css
- manifest.json
- content.json
- sw.js
- icons/icon.svg

## PWA

Install to home screen on iOS (Safari → Share → Add to Home Screen) or Android (Chrome → Install). Works offline after first load.
