/* Blooks page removed — intentional no-op so old caches cannot re-inject it */
(function () {
  'use strict';
  if (window.__bbBlooks) return;
  window.__bbBlooks = 1;
  try {
    var btn = document.querySelector('.sidebar-link[data-view="blooks"]');
    if (btn) {
      var li = btn.closest('li');
      if (li) li.remove();
      else btn.remove();
    }
    var view = document.getElementById('view-blooks');
    if (view) view.remove();
  } catch (e) {}
})();
