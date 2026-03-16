#!/bin/bash
# Run local demo matching live URL: http://localhost:3000/movie-quiz/frontend/
# Same path structure as https://parayno.dk/movie-quiz/frontend/

cd "$(dirname "$0")/.."
echo "Serving at http://localhost:3000/movie-quiz/frontend/"
echo "Press Ctrl+C to stop"
python3 -m http.server 3000
