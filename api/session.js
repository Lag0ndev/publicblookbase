/**
 * Vercel serverless: serves client auth JS + loads Leaks/Tracker + UI fixes.
 * Browser calls /api/session.js as a script tag from index.html.
 */
module.exports = function handler(req, res) {
  const body = `/**
 * Blookbase admin auth (client).
 * window.__bbVerify(code) -> Promise<boolean>
 */
(function () {
  'use strict';
  var _H = '9c9e8256b1db825408039919a66305d6824c98641c47f296c2b4394d8756e3ac';
  function toHex(buf) {
    var a = new Uint8Array(buf);
    var s = '';
    for (var i = 0; i < a.length; i++) {
      var h = a[i].toString(16);
      s += h.length === 1 ? '0' + h : h;
    }
    return s;
  }
  function sha256hex(str) {
    if (!(window.crypto && window.crypto.subtle && window.TextEncoder)) {
      return Promise.reject(new Error('Web Crypto unavailable'));
    }
    return window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(str)).then(toHex);
  }
  function verify(code) {
    if (typeof code !== 'string') return Promise.resolve(false);
    var trimmed = code.trim();
    if (!trimmed) return Promise.resolve(false);
    return sha256hex(trimmed).then(function (hex) { return hex === _H; }).catch(function () { return false; });
  }
  window.__bbVerify = verify;
  try { Object.freeze(window.__bbVerify); } catch (e) {}

  function loadScript(src, attr) {
    try {
      if (document.querySelector('script[src="' + src + '"]')) return;
      var s = document.createElement('script');
      s.src = src;
      s.defer = true;
      if (attr) s.setAttribute(attr, '1');
      document.head.appendChild(s);
    } catch (e) {}
  }

  // Leaks + Tracker sidebar pages
  loadScript('/bb-leaks-tracker.js', 'data-bb-leaks');
  // Home LIVE banner + What's New clickable blooks
  loadScript('/bb-ui-fixes.js', 'data-bb-ui');
})();
`;
  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=60');
  res.end(body);
};
