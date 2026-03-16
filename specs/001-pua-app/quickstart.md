# Quickstart: pua

**Branch**: `001-pua-app` | **Updated**: 2025-03-16

## Overview

pua is a **frontend-only PWA** — no backend required. All content is in `content.json`. Votes are stored locally in the browser (IndexedDB).

## Run locally

```bash
cd frontend
python -m http.server 3000
# Or: npx serve .
```

App: http://localhost:3000

## Deploy via FTP (e.g. GigaHost)

1. Upload the entire `frontend/` folder contents to your web root (e.g. `public_html/`).
2. Ensure these files are present:
   - `index.html`
   - `app.js`
   - `styles.css`
   - `manifest.json`
   - `content.json`
   - `sw.js`
   - `icons/icon.svg`
3. Serve over HTTPS for full PWA support (install to home screen, offline).

### Subfolder deployment

If you deploy to a subfolder (e.g. `example.com/pua/`), the app works as-is. The service worker and manifest use relative paths.

## Install as PWA (iOS / Android)

1. Open the app in Safari (iOS) or Chrome (Android).
2. **iOS**: Share → Add to Home Screen
3. **Android**: Menu → Install app / Add to Home Screen
4. Swipe right = thumbs up, swipe left = thumbs down. Works offline.

## Content

Edit `frontend/content.json` to add or change one-liners. Format:

```json
[
  { "id": 1, "text": "Nice shoes. Did you choose those yourself?" },
  { "id": 2, "text": "Nice jacket. My little cousin has one like that." }
]
```
