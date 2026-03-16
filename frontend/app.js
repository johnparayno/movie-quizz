/**
 * pua - Frontend-only PWA
 * Quiz app: categorize pickup lines. Content from movie_quizz.json.
 * Votes stored locally (IndexedDB); no backend.
 */

const SESSION_COOKIE_NAME = 'pua_session';
const SESSION_COOKIE_MAX_AGE = 365 * 24 * 60 * 60; // 1 year
const OFFLINE_DB_NAME = 'pua_offline';
const OFFLINE_STORE = 'votes';

/**
 * Get or create session ID. Uses first-party cookie for persistence.
 */
function getOrCreateSessionId() {
  const match = document.cookie.match(new RegExp(`${SESSION_COOKIE_NAME}=([^;]+)`));
  if (match) return match[1];
  const id = crypto.randomUUID();
  document.cookie = `${SESSION_COOKIE_NAME}=${id}; path=/; max-age=${SESSION_COOKIE_MAX_AGE}; SameSite=Lax`;
  return id;
}

const ANSWER_OPTIONS = ['Neg', 'Opener', 'Compliment'];

/**
 * Normalize content item to app shape.
 */
function normalizeItem(item) {
  return {
    id: item.id,
    text: item.text,
    correct: item.correct || 'Neg',
    content_type: item.content_type || 'neg',
    created_at: item.created_at || '',
  };
}

/**
 * Shuffle array (Fisher-Yates).
 */
function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/**
 * Get 3 answer options for a quiz item (correct + 2 wrong), shuffled.
 */
function getAnswerOptions(correct) {
  const wrong = ANSWER_OPTIONS.filter((o) => o !== correct);
  const twoWrong = shuffle(wrong).slice(0, 2);
  return shuffle([correct, ...twoWrong]);
}

/**
 * Load content from movie_quizz.json.
 */
async function loadContent() {
  const res = await fetch('movie_quizz.json', { cache: 'no-store' });
  if (!res.ok) throw new Error('Content unavailable');
  const items = await res.json();
  return Array.isArray(items) ? items : [];
}

/**
 * Pick random item from array, excluding excludeId.
 */
function pickRandom(items, excludeId) {
  const filtered = excludeId != null ? items.filter((i) => i.id !== excludeId) : [...items];
  if (filtered.length === 0) return null;
  return normalizeItem(filtered[Math.floor(Math.random() * filtered.length)]);
}

/**
 * Store vote locally (IndexedDB). No server.
 */
async function storeVote(contentItemId, voteType) {
  if (!indexedDB) return Promise.resolve({ offline: true });
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(OFFLINE_DB_NAME, 1);
    req.onerror = () => reject(req.error);
    req.onsuccess = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(OFFLINE_STORE)) {
        db.close();
        return resolve({ offline: true });
      }
      const tx = db.transaction(OFFLINE_STORE, 'readwrite');
      const store = tx.objectStore(OFFLINE_STORE);
      store.add({
        content_item_id: contentItemId,
        vote_type: voteType,
        session_id: getOrCreateSessionId(),
        created_at: new Date().toISOString(),
      });
      tx.oncomplete = () => resolve({ offline: true });
      tx.onerror = () => reject(tx.error);
    };
    req.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains(OFFLINE_STORE)) {
        db.createObjectStore(OFFLINE_STORE, { keyPath: 'id', autoIncrement: true });
      }
    };
  });
}

/**
 * Get deterministic background variant index from content item id (skin tones type 1–5).
 */
function getBackgroundVariantIndex(id) {
  const variants = 5;
  return (id - 1) % variants;
}

const SKIN_TONE_COLORS = ['#FFE5D9', '#F5D0C5', '#EBC4AF', '#D4A574', '#C68642'];

function setThemeColor(variantIndex) {
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta && SKIN_TONE_COLORS[variantIndex]) {
    meta.setAttribute('content', SKIN_TONE_COLORS[variantIndex]);
  }
}

/**
 * Confetti burst animation (thumbs up feedback).
 */
function runConfetti(canvas, durationMs = 1200) {
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const colors = ['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43'];
  const particleCount = 60;
  const particles = [];

  const resize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };
  resize();

  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;

  for (let i = 0; i < particleCount; i++) {
    const angle = (Math.PI * 2 * i) / particleCount + Math.random() * 0.5;
    const speed = 4 + Math.random() * 8;
    particles.push({
      x: centerX,
      y: centerY,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed - 2,
      color: colors[Math.floor(Math.random() * colors.length)],
      size: 4 + Math.random() * 6,
      rotation: Math.random() * 360,
      rotationSpeed: (Math.random() - 0.5) * 20,
    });
  }

  const start = performance.now();
  const onResize = () => { resize(); };
  window.addEventListener('resize', onResize);

  function tick(now) {
    const elapsed = now - start;
    if (elapsed > durationMs) {
      window.removeEventListener('resize', onResize);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      return;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach((p) => {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.15;
      p.vx *= 0.99;
      p.vy *= 0.99;
      p.rotation += p.rotationSpeed;

      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate((p.rotation * Math.PI) / 180);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = Math.max(0, 1 - elapsed / durationMs);
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
      ctx.restore();
    });
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// Register service worker for PWA
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js').then((reg) => {
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible') reg.update();
    });
  }).catch(() => {});
}

document.addEventListener('DOMContentLoaded', () => {
  const main = document.querySelector('main');
  const contentEl = document.getElementById('content-text');
  const contentBlock = document.getElementById('content-block');
  const answer1 = document.getElementById('answer-1');
  const answer2 = document.getElementById('answer-2');
  const answer3 = document.getElementById('answer-3');
  const loadingState = document.getElementById('loading-state');
  const errorState = document.getElementById('error-state');
  const emptyState = document.getElementById('empty-state');
  const retryFetchBtn = document.getElementById('retry-fetch');
  const voteErrorOverlay = document.getElementById('vote-error-overlay');
  const retryVoteBtn = document.getElementById('retry-vote');
  const voteFeedbackOverlay = document.getElementById('vote-feedback-overlay');
  const confettiCanvas = document.getElementById('confetti-canvas');
  const boohFeedback = document.getElementById('booh-feedback');
  const wrongFeedback = document.getElementById('wrong-feedback');
  const scoreDisplay = document.getElementById('score-display');

  let lastShownId = null;
  let isTransitioning = false;
  let pendingAnswer = null;
  let allContent = [];
  let score = 0;
  let currentItem = null;

  function showState(which) {
    loadingState?.classList.toggle('hidden', which !== 'loading');
    errorState?.classList.toggle('hidden', which !== 'error');
    emptyState?.classList.toggle('hidden', which !== 'empty');
    contentBlock?.classList.toggle('hidden', which !== 'content');
    voteErrorOverlay?.classList.toggle('hidden', which !== 'vote-error');
    if (which !== 'content') setThemeColor(0);
  }

  function updateScoreDisplay() {
    if (scoreDisplay) scoreDisplay.textContent = `SCORE: ${score}`;
  }

  function setContent(item) {
    if (!item) return;
    currentItem = item;
    lastShownId = item.id;
    contentEl.textContent = item.text;
    contentEl.setAttribute('data-content-id', item.id);
    const variant = getBackgroundVariantIndex(item.id);
    main.classList.remove('bg-variant-0', 'bg-variant-1', 'bg-variant-2', 'bg-variant-3', 'bg-variant-4');
    main.classList.add(`bg-variant-${variant}`);
    setThemeColor(variant);
    const options = getAnswerOptions(item.correct);
    if (answer1) { answer1.textContent = options[0]; answer1.disabled = false; }
    if (answer2) { answer2.textContent = options[1]; answer2.disabled = false; }
    if (answer3) { answer3.textContent = options[2]; answer3.disabled = false; }
    showState('content');
  }

  function showTransition(callback) {
    if (isTransitioning) return;
    isTransitioning = true;
    main.classList.add('transition-out');
    setTimeout(() => {
      callback();
      main.classList.remove('transition-out');
      main.classList.add('transition-in');
      requestAnimationFrame(() => {
        requestAnimationFrame(() => main.classList.remove('transition-in'));
      });
      setTimeout(() => { isTransitioning = false; }, 400);
    }, 300);
  }

  function showAnswerFeedback(correct) {
    if (!voteFeedbackOverlay) return;
    voteFeedbackOverlay.classList.remove('hidden');
    boohFeedback?.classList.add('hidden');
    wrongFeedback?.classList.add('hidden');
    const ctx = confettiCanvas?.getContext('2d');
    if (ctx) ctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
    if (correct) {
      runConfetti(confettiCanvas, 1200);
      setTimeout(() => voteFeedbackOverlay?.classList.add('hidden'), 1200);
    } else {
      wrongFeedback?.classList.remove('hidden');
      setTimeout(() => {
        voteFeedbackOverlay?.classList.add('hidden');
        wrongFeedback?.classList.add('hidden');
      }, 800);
    }
  }

  async function loadNext(wasCorrect = null) {
    if (wasCorrect === true) {
      showAnswerFeedback(true);
    } else if (wasCorrect === false) {
      showAnswerFeedback(false);
    } else {
      showState('loading');
    }
    try {
      if (allContent.length === 0) {
        allContent = await loadContent();
      }
      const item = pickRandom(allContent, lastShownId);
      if (item) {
        showTransition(() => setContent(item));
      } else {
        showState('empty');
      }
    } catch (err) {
      console.error('Load failed:', err);
      showState('error');
    }
  }

  function handleAnswer(selectedAnswer) {
    if (!currentItem || isTransitioning) return;
    const correct = selectedAnswer === currentItem.correct;
    if (answer1) answer1.disabled = true;
    if (answer2) answer2.disabled = true;
    if (answer3) answer3.disabled = true;
    if (correct) {
      score += 1;
      updateScoreDisplay();
    } else {
      score = 0;
      updateScoreDisplay();
    }
    pendingAnswer = { id: currentItem.id, correct };
    storeVote(currentItem.id, correct ? 'up' : 'down').catch(() => {});
    loadNext(correct);
  }

  answer1?.addEventListener('click', () => handleAnswer(answer1.textContent));
  answer2?.addEventListener('click', () => handleAnswer(answer2.textContent));
  answer3?.addEventListener('click', () => handleAnswer(answer3.textContent));
  retryFetchBtn?.addEventListener('click', () => loadNext());

  // Info overlay
  const infoBtn = document.getElementById('info-btn');
  const infoOverlay = document.getElementById('info-overlay');
  const infoClose = document.getElementById('info-close');
  function openInfoOverlay() {
    infoOverlay?.classList.remove('hidden');
    infoBtn?.setAttribute('aria-expanded', 'true');
  }
  function closeInfoOverlay() {
    infoOverlay?.classList.add('hidden');
    infoBtn?.setAttribute('aria-expanded', 'false');
  }
  infoBtn?.addEventListener('click', openInfoOverlay);
  infoClose?.addEventListener('click', closeInfoOverlay);
  infoOverlay?.addEventListener('click', (e) => {
    if (e.target === infoOverlay) closeInfoOverlay();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && infoOverlay && !infoOverlay.classList.contains('hidden')) {
      closeInfoOverlay();
    }
  });

  // Keyboard: 1, 2, 3 for answer buttons
  document.addEventListener('keydown', (e) => {
    if (document.activeElement?.tagName === 'INPUT' || document.activeElement?.tagName === 'TEXTAREA') return;
    if (e.key === '1' && answer1 && !answer1.disabled) {
      e.preventDefault();
      handleAnswer(answer1.textContent);
    } else if (e.key === '2' && answer2 && !answer2.disabled) {
      e.preventDefault();
      handleAnswer(answer2.textContent);
    } else if (e.key === '3' && answer3 && !answer3.disabled) {
      e.preventDefault();
      handleAnswer(answer3.textContent);
    }
  });

  // Initial load
  (async () => {
    showState('loading');
    try {
      allContent = await loadContent();
      const item = pickRandom(allContent, null);
      if (item) setContent(item);
      else showState('empty');
    } catch (err) {
      console.error('Initial load failed:', err);
      showState('error');
    }
  })();
});
