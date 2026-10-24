/* Blookbase Secret — DISABLED / fully removed */
(function(){
'use strict';
if (window.__bbS) return;
window.__bbS = 1;
// No-op: secret page fully removed. Redirect any leftover /secret hits.
window.__bbRenderSecret = function(){};
function seg(){
  return decodeURIComponent((location.pathname.replace(/\/+$/,'')||'/').split('/').filter(Boolean)[0]||'').toLowerCase();
}
function boot(){
  var s = seg();
  if (s === 'secret' || s === 'secret!!!' || s.indexOf('secret') === 0) {
    if (typeof switchView === 'function') switchView('home', true);
    try { history.replaceState(null, '', '/'); } catch(e){}
  }
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
else boot();
})();
