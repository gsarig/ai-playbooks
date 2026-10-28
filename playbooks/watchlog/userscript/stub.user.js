// ==UserScript==
// @name         imdb-capture
// @namespace    watchlog
// @version      0.1
// @description  Records your IMDB ratings and watchlist state into the Watchlog vault as you browse. All code lives in imdb-capture.js in this vault, loaded from disk below. Edit the @require path to where your vault lives.
// @match        https://www.imdb.com/*
// @run-at       document-idle
// @grant        none
// @require      file:///PATH/TO/watchlog/userscript/imdb-capture.js
// ==/UserScript==

// Intentionally empty. Tampermonkey runs imdb-capture.js from the @require line above, re-reading it from disk on every page load, so edits to imdb-capture.js need no change here. Review any edit to imdb-capture.js before the next IMDB page load: it runs inside your logged-in IMDB session.
