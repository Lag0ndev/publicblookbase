/* Force Lag0n watermark to never truncate */
(function () {
  'use strict';
  function fix() {
    document.querySelectorAll('.watermark').forEach(function (el) {
      el.textContent = 'Lag0n';
      el.style.setProperty('max-width', 'none', 'important');
      el.style.setProperty('overflow', 'visible', 'important');
      el.style.setProperty('text-overflow', 'clip', 'important');
      el.style.setProperty('white-space', 'nowrap', 'important');
      el.style.setProperty('width', 'auto', 'important');
      el.style.setProperty('min-width', 'max-content', 'important');
    });
    if (!document.getElementById('bb-wm-full-css')) {
      var s = document.createElement('style');
      s.id = 'bb-wm-full-css';
      s.textContent =
        '.watermark{max-width:none!important;overflow:visible!important;' +
        'text-overflow:clip!important;white-space:nowrap!important;' +
        'width:auto!important;min-width:max-content!important;}';
      document.head.appendChild(s);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fix);
  else fix();
  setTimeout(fix, 200);
  setTimeout(fix, 1000);
  setTimeout(fix, 3000);
})();
