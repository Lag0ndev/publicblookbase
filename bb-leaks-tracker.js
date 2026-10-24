/* Blookbase Leaks page only (Tracker removed) */
(function () {
  'use strict';
  if (window.__bbLeaksOnly) return;
  window.__bbLeaksOnly = 1;

  var STYLE =
    '.pack-blook.bb-click{cursor:pointer}' +
    '.bb-ut-meta{font-size:13px;font-weight:700;opacity:.9;margin:0 0 8px}' +
    '.bb-ut-title{font-family:Titan One,sans-serif;font-weight:normal;font-size:20px;margin:0 0 8px;color:#fff;text-shadow:2px 2px 0 rgba(0,0,0,.15)}' +
    '.bb-ut-body{font-size:15px;font-weight:700;line-height:1.5;margin:0 0 10px}' +
    '.bb-ut-imgs{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px}' +
    '.bb-ut-img{background:rgba(0,0,0,.18);border-radius:8px;padding:8px 6px 6px;text-align:center;min-width:72px}' +
    '.bb-ut-img img{width:48px;height:48px;object-fit:contain;display:block;margin:0 auto 4px}' +
    '.bb-ut-img span{display:block;font-size:10px;font-weight:800;line-height:1.2;max-width:80px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}' +
    '.bb-ut-img.bb-click{cursor:pointer}' +
    '.bb-ut-badge{display:inline-block;font-size:11px;font-weight:900;text-transform:uppercase;background:rgba(0,0,0,.2);padding:3px 8px;border-radius:6px;margin-right:6px}';

  var LEAKS_HTML =
    '<div class="main-content" id="view-leaks" style="display:none;flex-direction:column;align-items:center;">' +
    '<h1 class="header-title">Leaks</h1>' +
    '<div class="leaks-wrap">' +
    '<div class="leaks-section"><h3>Unreleased / Secret Blooks</h3>' +
    '<p style="font-weight:700;opacity:.95;margin:0 0 10px;">Click a Blook for details (same style as Packs).</p>' +
    '<div class="pack-blooks-grid" id="bb-unreleased-grid"></div></div>' +
    '<div class="leaks-section"><h3>Uniques</h3><div class="pack-blooks-grid" id="bb-uniques-grid"></div></div>' +
    '<div class="leaks-section"><h3>Mysticals</h3><ul id="bb-mysticals-list"></ul></div>' +
    '<div class="leaks-section"><h3>Secret Pack \u2014 Color Pack</h3>' +
    '<p style="font-weight:700;opacity:.95;margin:0 0 10px;">Only when all Commons are taken in a live game.</p>' +
    '<div class="pack-blooks-grid" id="bb-color-grid"></div></div>' +
    '<div class="leaks-section"><h3>Gamemode status</h3><ul id="bb-gm-list"></ul></div>' +
    '</div></div>';

  var RARITY_GRADIENTS = {
    Common: 'radial-gradient(rgb(160,160,160) 40%, rgb(90,90,95))',
    Uncommon: 'radial-gradient(rgb(125,255,179) 40%, rgb(45,140,70))',
    Rare: 'radial-gradient(rgb(108,182,255) 40%, rgb(10,20,180))',
    Epic: 'radial-gradient(rgb(255,100,100) 40%, rgb(180,20,20))',
    Legendary: 'radial-gradient(rgb(255,179,71) 40%, rgb(200,100,20))',
    Chroma: 'radial-gradient(rgb(94,234,212) 40%, rgb(0,140,130))',
    Mystical: 'radial-gradient(rgb(232,121,249) 40%, rgb(120,30,160))',
    Unique: 'radial-gradient(rgb(45,212,191) 40%, rgb(0,120,110))'
  };

  var pathHandled = false;
  var sidebarInjected = false;

  function injectStyle() {
    if (document.getElementById('bb-lt-style')) return;
    var s = document.createElement('style');
    s.id = 'bb-lt-style';
    s.textContent = STYLE;
    document.head.appendChild(s);
  }

  function rarityTag(rarity) {
    if (typeof window.rarityTagHtml === 'function') {
      try { return window.rarityTagHtml(rarity); } catch (e) {}
    }
    return '<span class="bb-shop-tag">' + (rarity || '\u2014') + '</span>';
  }

  function openBlookModal(b) {
    var name = b.name || 'Unknown';
    var rarity = b.rarity || 'Unique';
    var packName = b.pack || (b.pack === null ? 'Secret / Unique' : '');
    var chance =
      b.chance != null && b.chance !== ''
        ? Number(b.chance) + '%'
        : b.notes
          ? 'Event / Exclusive'
          : 'Unreleased';
    var img =
      b.url ||
      (typeof window.getBlookImg === 'function' ? window.getBlookImg(name) : '') ||
      'https://ac.blooket.com/marketassets/blooks/' +
        name.toLowerCase().replace(/[^a-z0-9]/g, '') +
        '.svg';
    var bg = RARITY_GRADIENTS[rarity] || RARITY_GRADIENTS.Uncommon;
    var body = document.getElementById('blook-detail-body');
    var modal = document.getElementById('blook-detail-modal');
    if (body && modal) {
      body.innerHTML =
        '<div class="bb-shop-row"><div class="bb-shop-card" style="background:' + bg + ';">' +
        '<div class="bb-shop-shadow-letter">B</div><div class="bb-shop-img-wrap">' +
        '<img class="bb-shop-hero" src="' + img + '" alt="' + name + '" draggable="false" onerror="this.style.opacity=.3">' +
        '</div><div class="bb-shop-overlay"></div></div><div class="bb-shop-form"><div>' +
        '<h2 class="bb-shop-title">' + name + '</h2><div class="bb-shop-tags">' +
        rarityTag(rarity) +
        '<span class="bb-shop-tag">' + chance + '</span>' +
        (packName ? '<span class="bb-shop-tag">' + packName + '</span>' : '') +
        '</div>' +
        (b.notes ? '<p style="font-weight:700;margin:12px 0 0;opacity:.95;line-height:1.4;">' + b.notes + '</p>' : '') +
        '</div><button type="button" class="bb-shop-btn" onclick="closeBlookDetail()"><div class="bb-shop-btn-inner">Close</div></button></div></div>';
      modal.style.display = 'flex';
      return;
    }
    if (typeof window.openBlookDetail === 'function') {
      window.openBlookDetail(name, rarity, b.chance != null ? b.chance : null, packName);
    }
  }

  function cell(b) {
    var src = b.url || '';
    var img = src ? '<img src="' + src + '" alt="" loading="lazy" onerror="this.style.opacity=.3">' : '';
    var payload = encodeURIComponent(JSON.stringify(b));
    return (
      '<div class="pack-blook bb-click" data-bb="' + payload + '">' + img +
      '<div class="bn">' + (b.name || '') + '</div><div class="br">' + (b.rarity || '') +
      (b.pack ? ' \u00b7 ' + b.pack : '') + '</div></div>'
    );
  }

  function bindClicks(root) {
    if (!root) return;
    root.querySelectorAll('.bb-click').forEach(function (el) {
      el.onclick = function () {
        try {
          openBlookModal(JSON.parse(decodeURIComponent(el.getAttribute('data-bb'))));
        } catch (e) {}
      };
    });
  }

  window.renderLeaksPage = async function () {
    try {
      var special = await fetch('/data/special-blooks.json').then(function (r) { return r.json(); });
      var ug = document.getElementById('bb-unreleased-grid');
      var uq = document.getElementById('bb-uniques-grid');
      var ml = document.getElementById('bb-mysticals-list');
      if (ug) {
        ug.innerHTML = (special.unreleased || []).map(cell).join('');
        bindClicks(ug);
      }
      if (uq) {
        uq.innerHTML = (special.uniques || [])
          .map(function (u) {
            return cell({ name: u.name, url: u.url, rarity: 'Unique', notes: u.notes || '', pack: null });
          })
          .join('');
        bindClicks(uq);
      }
      if (ml) {
        ml.innerHTML = (special.mysticals || [])
          .map(function (m) {
            return '<li><span class="tag">mystical</span> <strong>' + m.name + '</strong> \u2014 ' + m.event + ' (' + m.copies + ' copies)</li>';
          })
          .join('');
      }
    } catch (e) {}
    try {
      var packs = await fetch('/data/packs.json').then(function (r) { return r.json(); });
      var color = (packs.packs || []).find(function (p) { return p.id === 'color'; });
      var cg = document.getElementById('bb-color-grid');
      if (cg && color) {
        cg.innerHTML = (color.blooks || [])
          .map(function (b) {
            return cell(Object.assign({}, b, { pack: 'Color Pack', notes: 'Secret pack \u2014 only when all normal Commons are taken' }));
          })
          .join('');
        bindClicks(cg);
      }
    } catch (e) {}
    try {
      var gm = await fetch('/data/gamemodes.json').then(function (r) { return r.json(); });
      var gl = document.getElementById('bb-gm-list');
      if (gl) {
        gl.innerHTML = (gm.gamemodes || [])
          .map(function (g) {
            var tag = g.status === 'Released' ? 'released' : 'upcoming';
            return '<li><span class="tag ' + tag + '">' + g.status + '</span> <strong>' + g.name + '</strong> \u2014 ' + (g.notes || '') + '</li>';
          })
          .join('');
      }
    } catch (e) {}
  };

  function setSidebarActive(view) {
    try { window.currentView = view; } catch (e) {}
    document.querySelectorAll('.sidebar-link').forEach(function (btn) {
      var v = btn.getAttribute('data-view');
      var on = v === view;
      btn.classList.toggle('active', on);
      if (on) btn.setAttribute('aria-current', 'page');
      else btn.removeAttribute('aria-current');
    });
  }

  function removeTrackerUI() {
    document.querySelectorAll('[data-view="tracker"]').forEach(function (btn) {
      var li = btn.closest('li');
      if (li) li.remove();
      else btn.remove();
    });
    var vt = document.getElementById('view-tracker');
    if (vt) {
      vt.style.display = 'none';
      vt.innerHTML = '';
    }
  }

  function injectSidebar() {
    removeTrackerUI();
    if (sidebarInjected || document.querySelector('[data-view="leaks"]')) {
      sidebarInjected = true;
      removeTrackerUI();
      return;
    }
    var list = document.querySelector('.sidebar-list');
    if (!list) return;
    var whats = list.querySelector('[data-view="whatsnew"]');
    var liParent = whats && whats.closest('li');
    if (!liParent) return;

    var leaksLi = document.createElement('li');
    leaksLi.innerHTML =
      '<button class="sidebar-link" data-view="leaks" type="button">' +
      '<span class="sidebar-listIcon"><i class="fas fa-user-secret"></i></span>' +
      '<span class="sidebar-text">Leaks</span></button>';
    leaksLi.querySelector('button').onclick = function (e) {
      e.preventDefault();
      e.stopPropagation();
      window.switchView('leaks');
    };
    liParent.after(leaksLi);

    list.querySelectorAll('.sidebar-link').forEach(function (btn) {
      var v = btn.getAttribute('data-view');
      var text = btn.querySelector('.sidebar-text');
      if (!text) return;
      if (v === 'market') text.textContent = 'Packs';
      if (v === 'packsim') text.textContent = 'Calculator';
    });
    sidebarInjected = true;
    removeTrackerUI();
  }

  function ensureViews() {
    if (!document.getElementById('view-leaks')) {
      document.body.insertAdjacentHTML('beforeend', LEAKS_HTML);
    }
    removeTrackerUI();
  }

  function patchSwitch() {
    if (typeof window.switchView !== 'function') return;
    if (window.switchView.__bbLeaksOnly) return;
    var orig = window.switchView;
    window.switchView = function (view, skipUrl) {
      injectStyle();
      ensureViews();
      injectSidebar();

      if (view === 'tracker') view = 'home';

      if (view === 'leaks') {
        document.querySelectorAll('.main-content').forEach(function (el) {
          el.style.display = 'none';
        });
        var target = document.getElementById('view-leaks');
        if (target) target.style.display = 'flex';
        setSidebarActive('leaks');
        window.renderLeaksPage();
        if (!skipUrl) {
          try { history.pushState(null, '', '/leaks'); } catch (e) {}
        }
        return;
      }

      return orig.call(this, view, skipUrl);
    };
    window.switchView.__bbLeaksOnly = 1;
  }

  function handlePath() {
    if (pathHandled) return;
    var seg = (location.pathname || '/').replace(/^\/|\/$/g, '').toLowerCase() || 'home';
    if (seg === 'tracker') {
      pathHandled = true;
      window.switchView('home', true);
      return;
    }
    if (seg === 'leaks') {
      pathHandled = true;
      window.switchView('leaks', true);
    }
  }

  function boot() {
    injectStyle();
    ensureViews();
    injectSidebar();
    patchSwitch();
    handlePath();
    window.addEventListener('popstate', function () {
      pathHandled = false;
      handlePath();
    });
    var t = 0;
    var iv = setInterval(function () {
      injectSidebar();
      patchSwitch();
      removeTrackerUI();
      if (++t > 30) clearInterval(iv);
    }, 200);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
