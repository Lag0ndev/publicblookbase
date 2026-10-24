/* Blookbase Leaks + Tracker + route aliases */
(function () {
  'use strict';

  const STYLE = `
  .pack-blook.bb-click{cursor:pointer}
  .bb-ut-meta{font-size:13px;font-weight:700;opacity:.9;margin:0 0 8px}
  .bb-ut-title{font-family:'Titan One',sans-serif;font-weight:normal;font-size:20px;margin:0 0 8px;color:#fff;text-shadow:2px 2px 0 rgba(0,0,0,.15)}
  .bb-ut-body{font-size:15px;font-weight:700;line-height:1.5;margin:0 0 10px}
  .bb-ut-imgs{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px}
  .bb-ut-img{background:rgba(0,0,0,.18);border-radius:8px;padding:8px 6px 6px;text-align:center;min-width:72px}
  .bb-ut-img img{width:48px;height:48px;object-fit:contain;display:block;margin:0 auto 4px}
  .bb-ut-img span{display:block;font-size:10px;font-weight:800;line-height:1.2;max-width:80px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .bb-ut-badge{display:inline-block;font-size:11px;font-weight:900;text-transform:uppercase;background:rgba(0,0,0,.2);padding:3px 8px;border-radius:6px;margin-right:6px}
  `;

  let pathHandled = false;
  let sidebarInjected = false;
  let bbCurrent = null;

  function injectStyle() {
    if (document.getElementById('bb-lt-style')) return;
    const s = document.createElement('style');
    s.id = 'bb-lt-style';
    s.textContent = STYLE;
    document.head.appendChild(s);
  }

  // PART0 truncated intentionally - will fix
  console.log('bb_o0 partial - needs full restore');
