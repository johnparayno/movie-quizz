# quiz

A frontend-only PWA movie quote quiz. Read the quote and tap the correct answer. Content from `content.json`; votes stored locally in the browser.

## Demo

**[Live demo](https://parayno.dk/movie-quiz/frontend/)**

## Quick start

**Option A — Match live demo URL** (recommended):

```bash
./run-demo.sh
```

Then open **http://localhost:3000/movie-quiz/frontend/**

**Option B — Simple local serve:**

```bash
cd frontend
python3 -m http.server 3000
```

Open http://localhost:3000

> Use **http://** not file:// — opening index.html directly will break loading.

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
