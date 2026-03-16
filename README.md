# quiz

A frontend-only PWA movie quote quiz. Read the quote and tap the correct answer. Content from `content.json`; votes stored locally in the browser.

## Quick start

```bash
cd frontend
python -m http.server 3000
```

Open http://localhost:3000

## Deploy via FTP (GigaHost, etc.)

1. Upload everything inside the `frontend/` folder to your web root (e.g. `public_html/`).
2. Serve over HTTPS for full PWA support.
3. Works in subfolders too — upload to `public_html/quiz/` if needed.

**Files to upload:**
- index.html
- app.js
- styles.css
- manifest.json
- movie_quizz_500_updated.json
- sw.js
- icons/icon.svg

## PWA

Install to home screen on iOS (Safari → Share → Add to Home Screen) or Android (Chrome → Install). Works offline after first load.
