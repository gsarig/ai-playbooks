/*
 * imdb-sync: records your IMDB rating and watchlist state for the titles you see, as JSON files in the Watchlog vault's `_data/imdb/` folder. scripts/process_queues.py (cron, every 15 minutes) applies them to the notes.  Loaded by userscript/stub.user.js through Tampermonkey's @require and re-read from disk on every page load.
 *
 * It only reads what the page already shows and writes files; it makes no requests and never clicks. It reports a state only when it is sure of it: you are logged in, and the page has finished loading your rating and watchlist state. A title missing from a list page is never read as "removed": only a row or title page that shows the state counts.
 *
 * What it keeps: the folder handle in imdb.com's IndexedDB (database `imdb-sync`, store `handles`). Nothing else is stored in the browser.
 *
 * Page markers, as seen on imdb.com in October 2026: the header's `imdbHeader-userMenuFlyoutLabel` (your name, absent when logged out); on a title page `hero-rating-bar__user-rating__score` ("9/10") or `hero-rating-bar__user-rating__unrated` ("Rate"), and `tm-box-wl-text` ("In Watchlist" / "Add to Watchlist"); on list rows the `poster-watchlist-ribbon-remove` / `-add` ribbon, `aria-label="Your rating: N"` or `"Rate <title>"`, and on the ratings page the text "Rated on Oct 23, 2026".
 */
(function () {
  'use strict';

  if (window.top !== window.self) return;

  const FOLDER = 'imdb';
  const LOAD_WAIT_MS = 20000; // a page that has not shown your state by then records nothing
  const POLL_MS = 500;
  const SETTLE_MS = 1500; // quiet time after DOM changes before re-reading

  // ===================================================================================
  // Helpers
  // ===================================================================================

  const pad = (n, w = 2) => String(n).padStart(w, '0');
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const localDay = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  // File names sort in the order things were seen; the processor relies on that.
  const fileStamp = (d) => `${localDay(d)}T${pad(d.getHours())}-${pad(d.getMinutes())}-${pad(d.getSeconds())}-${pad(d.getMilliseconds(), 3)}`;
  function localIso(d) {
    const off = -d.getTimezoneOffset();
    const a = Math.abs(off);
    return `${localDay(d)}T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}${off >= 0 ? '+' : '-'}${pad(Math.floor(a / 60))}:${pad(a % 60)}`;
  }
  const errText = (e) => (e && e.message ? e.message : String(e));
  const byTestId = (id, root = document) => root.querySelector(`[data-testid="${id}"]`);
  const MONTHS = { Jan: 1, Feb: 2, Mar: 3, Apr: 4, May: 5, Jun: 6, Jul: 7, Aug: 8, Sep: 9, Oct: 10, Nov: 11, Dec: 12 };

  // ===================================================================================
  // Corner label: shown only when the folder needs a click or a write failed
  // ===================================================================================

  const ui = (() => {
    let box = null, text, buttons;
    function ensure() {
      if (box && box.isConnected) return;
      box = document.createElement('div');
      box.style.cssText = 'position:fixed;right:12px;bottom:12px;z-index:2147483647;max-width:380px;padding:8px 10px;border-radius:6px;font:12px/1.4 system-ui,sans-serif;color:#fff;background:#24292f;box-shadow:0 2px 8px rgba(0,0,0,.3);white-space:pre-wrap';
      text = document.createElement('div');
      buttons = document.createElement('div');
      box.append(text, buttons);
      (document.body || document.documentElement).appendChild(box);
    }
    return {
      show(msg, isError = false) {
        ensure();
        text.textContent = msg;
        box.style.background = isError ? '#8b1a1a' : '#24292f';
        buttons.replaceChildren();
      },
      clear() {
        if (box) box.remove();
        box = null;
      },
      // Resolves with fn's result once a click succeeds. fn runs inside the click, because picking a folder and granting permission need a user gesture.
      ask(msg, label, fn) {
        this.show(msg);
        return new Promise((resolve) => {
          const b = document.createElement('button');
          b.textContent = label;
          b.style.cssText = 'margin:6px 0 0;padding:3px 8px;font:inherit;cursor:pointer';
          b.addEventListener('click', async () => {
            try {
              resolve(await fn());
            } catch (e) {
              text.textContent = `${msg}\n${errText(e)}`;
              box.style.background = '#8b1a1a';
            }
          });
          buttons.appendChild(b);
        });
      },
    };
  })();

  // ===================================================================================
  // Folder handle and writer
  // ===================================================================================

  function openDb() {
    return new Promise((resolve, reject) => {
      const r = indexedDB.open('imdb-sync', 1);
      r.onupgradeneeded = () => r.result.createObjectStore('handles');
      r.onsuccess = () => resolve(r.result);
      r.onerror = () => reject(r.error);
    });
  }
  async function dbGet(key) {
    const db = await openDb();
    return new Promise((resolve, reject) => {
      const q = db.transaction('handles').objectStore('handles').get(key);
      q.onsuccess = () => resolve(q.result);
      q.onerror = () => reject(q.error);
    });
  }
  async function dbPut(key, value) {
    const db = await openDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('handles', 'readwrite');
      tx.objectStore('handles').put(value, key);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
  }

  // `granted`: carry on. `prompt` (normal after an Edge restart until "Allow on every visit" is chosen) or `denied`: one click on "Allow". No handle yet: "Pick folder", which must be watchlog/_data/imdb.
  async function getFolder() {
    const stored = await dbGet(FOLDER);
    if (stored) {
      if ((await stored.queryPermission({ mode: 'readwrite' })) === 'granted') return stored;
      return ui.ask('IMDB sync needs permission for the folder watchlog/_data/imdb.', 'Allow', async () => {
        const s = await stored.requestPermission({ mode: 'readwrite' });
        if (s !== 'granted') throw new Error(`permission ${s}; click again and allow`);
        return stored;
      });
    }
    return ui.ask('IMDB sync: pick the folder watchlog/_data/imdb.', 'Pick folder', async () => {
      const h = await window.showDirectoryPicker({ mode: 'readwrite', id: 'imdb-sync' });
      if (h.name !== FOLDER) throw new Error(`picked a folder named "${h.name}"; pick watchlog/_data/imdb`);
      await dbPut(FOLDER, h);
      return h;
    });
  }

  // Never overwrites: the name must not exist yet. Then create, write, close, and read back.
  async function writeNew(dir, name, text) {
    try {
      await dir.getFileHandle(name);
      throw new Error(`${name} already exists`);
    } catch (e) {
      if (!e || e.name !== 'NotFoundError') throw e;
    }
    const fh = await dir.getFileHandle(name, { create: true });
    const w = await fh.createWritable();
    await w.write(text);
    await w.close();
    const back = await (await fh.getFile()).text();
    if (back !== text) throw new Error(`${name}: read-back did not match what was written`);
  }

  // One write at a time, so two observations never race for the folder prompt or a file name.
  let chain = Promise.resolve();
  function emit(source, items) {
    if (!items.length) return;
    const now = new Date(); // when seen, not when the folder prompt was finally clicked
    chain = chain.then(async () => {
      try {
        const dir = await getFolder();
        ui.clear();
        const body = JSON.stringify({ version: 1, source, seen_at: localIso(now), items });
        await writeNew(dir, `${fileStamp(now)}_${source}.json`, body);
      } catch (e) {
        ui.show(`IMDB sync: could not save (${errText(e)}).`, true);
      }
    });
  }

  // ===================================================================================
  // Reading the page
  // ===================================================================================

  function loggedIn() {
    const el = byTestId('imdbHeader-userMenuFlyoutLabel');
    return !!el && el.textContent.trim() !== '';
  }

  // The hero bar renders twice (two layouts); querySelector takes the first. Labels like "Your rating: 7" elsewhere on a title page belong to recommended titles, so only the hero test ids are read.
  function readTitle(imdbId) {
    const score = byTestId('hero-rating-bar__user-rating__score');
    const unrated = byTestId('hero-rating-bar__user-rating__unrated');
    if (!!score === !!unrated) return null; // not loaded yet, or mid-update
    let rating = null;
    if (score) {
      const m = score.textContent.match(/^\s*(\d{1,2})\s*\/\s*10/);
      if (!m || +m[1] < 1 || +m[1] > 10) return null;
      rating = +m[1];
    }
    const wl = byTestId('tm-box-wl-text');
    const t = wl ? wl.textContent.trim() : '';
    const inWatchlist = t === 'In Watchlist' ? true : t === 'Add to Watchlist' ? false : null;
    if (inWatchlist === null) return null;
    return { imdb_id: imdbId, rating, in_watchlist: inWatchlist };
  }

  // A row is reported only when both its watchlist ribbon and its rating state are on screen.
  function readRows(source) {
    const root = document.querySelector('main') || document;
    const rows = new Set();
    for (const a of root.querySelectorAll('a[href*="/title/tt"]')) {
      const li = a.closest('li');
      if (li) rows.add(li);
    }
    const out = [];
    for (const li of rows) {
      const m = (li.querySelector('a[href*="/title/tt"]').getAttribute('href') || '').match(/\/title\/(tt\d+)/);
      if (!m) continue;
      const inWatchlist = byTestId('poster-watchlist-ribbon-remove', li) ? true
        : byTestId('poster-watchlist-ribbon-add', li) ? false : null;
      if (inWatchlist === null) continue;
      let rating, unrated = false;
      for (const el of li.querySelectorAll('[aria-label]')) {
        const label = el.getAttribute('aria-label');
        const r = label.match(/^Your rating: (\d{1,2})$/);
        if (r) rating = +r[1];
        else if (/^Rate /.test(label)) unrated = true;
      }
      if (rating === undefined && !unrated) continue;
      if (rating !== undefined && (rating < 1 || rating > 10)) continue;
      const item = { imdb_id: m[1], rating: rating === undefined ? null : rating, in_watchlist: inWatchlist };
      if (source === 'ratings') {
        const d = li.innerText.match(/Rated on ([A-Z][a-z]{2}) (\d{1,2}), (\d{4})/);
        if (d && MONTHS[d[1]]) item.rated_on = `${d[3]}-${pad(MONTHS[d[1]])}-${pad(+d[2])}`;
      }
      out.push(item);
    }
    return out;
  }

  const keyOf = (i) => `${i.rating}|${i.in_watchlist}`;

  // ===================================================================================
  // Page watchers. `generation` stops a watcher once a client-side navigation leaves its page.
  // ===================================================================================

  let generation = 0;

  async function waitFor(gen, fn) {
    const until = Date.now() + LOAD_WAIT_MS;
    while (Date.now() < until) {
      if (gen !== generation) return null;
      const v = loggedIn() ? fn() : null;
      if (v) return v;
      await sleep(POLL_MS);
    }
    return null;
  }

  // Calls fn after the DOM has been quiet for SETTLE_MS, for as long as this page is current.
  function onSettled(gen, fn) {
    let timer = null;
    const obs = new MutationObserver(() => {
      if (gen !== generation) { obs.disconnect(); return; }
      clearTimeout(timer);
      timer = setTimeout(() => { if (gen === generation && loggedIn()) fn(); }, SETTLE_MS);
    });
    obs.observe(document.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['aria-label', 'data-testid'] });
  }

  async function watchTitle(gen, imdbId) {
    const first = await waitFor(gen, () => readTitle(imdbId));
    if (!first) return;
    let last = keyOf(first);
    emit('title', [first]);
    // Rating or un-watchlisting on the page itself shows up here.
    onSettled(gen, () => {
      const now = readTitle(imdbId);
      if (now && keyOf(now) !== last) {
        last = keyOf(now);
        emit('title', [now]);
      }
    });
  }

  async function watchList(gen, source) {
    const first = await waitFor(gen, () => { const r = readRows(source); return r.length ? r : null; });
    if (!first) return;
    const seen = new Map(first.map((i) => [i.imdb_id, keyOf(i)]));
    emit(source, first);
    // Rows added by scrolling, and ribbon changes such as a removal click.
    onSettled(gen, () => {
      const changed = readRows(source).filter((i) => seen.get(i.imdb_id) !== keyOf(i));
      for (const i of changed) seen.set(i.imdb_id, keyOf(i));
      emit(source, changed);
    });
  }

  function route() {
    const gen = ++generation;
    const path = location.pathname;
    const title = path.match(/^\/title\/(tt\d+)\/?$/);
    if (title) return watchTitle(gen, title[1]);
    const list = path.match(/^\/user\/[^/]+\/(watchlist|ratings)\/?$/);
    if (list) return watchList(gen, list[1]);
  }

  let lastPath = null;
  function check() {
    try {
      if (location.pathname === lastPath) return;
      lastPath = location.pathname;
      route();
    } catch (e) { /* never break the page */ }
  }
  for (const fn of ['pushState', 'replaceState']) {
    const orig = history[fn];
    history[fn] = function () {
      const r = orig.apply(this, arguments);
      setTimeout(check, 0);
      return r;
    };
  }
  window.addEventListener('popstate', check);
  check();
})();
