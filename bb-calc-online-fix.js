/**
 * Blookbase fixes v3:
 * - Online presence (MQTT failover)
 * - Calculator: lock Autumn/Blizzard, better results (rate %, tokens, avg)
 * - /calculator route
 * - Remove Leaks nav/page
 * - Sidebar-safe online count + Lag0n watermark
 * - Live videos = Blooket only (no brainrot search)
 */
(function () {
  'use strict';
  if (window.__bbFixV3) return;
  window.__bbFixV3 = 1;

  var LOCKED_PACKS = {
    Autumn: 'Not out yet — Autumn Pack is not currently in the Market.',
    Blizzard: 'Not out yet — Blizzard Pack is not currently in the Market.'
  };

  /* ========== CSS: overlays + locked packs + calc ========== */
  function injectStyles() {
    if (document.getElementById('bb-fix-v3-css')) return;
    var s = document.createElement('style');
    s.id = 'bb-fix-v3-css';
    s.textContent = [
      /* Keep online + watermark on screen with any sidebar layout */
      '.online-counter{',
      '  position:fixed!important;z-index:80!important;pointer-events:none!important;',
      '  left:auto!important;right:14px!important;bottom:14px!important;',
      '  max-width:calc(100vw - 28px);',
      '}',
      'body.sb-right .online-counter,body.sb-right-side .online-counter{',
      '  right:auto!important;left:14px!important;',
      '}',
      'body.sb-always:not(.sb-right) .online-counter{',
      '  left:auto!important;right:14px!important;',
      '}',
      '@media(min-width:901px){',
      '  body.sb-always:not(.sb-right) .online-counter{ right:14px!important; left:auto!important; }',
      '  body.sb-always.sb-right .online-counter{ left:14px!important; right:auto!important; }',
      '}',
      '.watermark{',
      '  position:fixed!important;z-index:40!important;pointer-events:none!important;',
      '  right:12px!important;bottom:48px!important;left:auto!important;',
      '  max-width:min(40vw,220px);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;',
      '}',
      'body.sb-right .watermark{',
      '  right:auto!important;left:12px!important;',
      '}',
      '@media(max-width:600px){',
      '  .online-counter{ font-size:12px!important; bottom:10px!important; right:10px!important; }',
      '  .watermark{ bottom:40px!important; font-size:28px!important; opacity:0.2!important; }',
      '}',

      /* Locked pack cards */
      '.calc-pack-card.is-locked{',
      '  opacity:0.55;filter:grayscale(0.35);cursor:not-allowed!important;position:relative;',
      '}',
      '.calc-pack-card.is-locked::after{',
      '  content:"🔒 Soon";position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);',
      '  background:rgba(0,0,0,0.72);color:#fff;font-weight:900;font-size:12px;',
      '  padding:6px 10px;border-radius:10px;letter-spacing:0.3px;white-space:nowrap;z-index:2;',
      '}',
      '.calc-pack-card.is-locked img,.calc-pack-card.is-locked .calc-pack-img-wrap{ pointer-events:none; }',

      /* Calculator results */
      '#view-packsim .calc-results{ margin-top:8px; }',
      '#view-packsim .calc-summary{',
      '  display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));',
      '  gap:10px;margin-bottom:16px;',
      '}',
      '#view-packsim .calc-stat{',
      '  background:rgba(0,0,0,0.28);border-radius:14px;padding:16px 12px;text-align:center;',
      '  border:3px solid rgba(255,255,255,0.18);box-shadow:3px 3px rgba(0,0,0,0.15);',
      '}',
      '#view-packsim .calc-stat b{',
      '  display:block;font-family:"Titan One",cursive;font-size:26px;font-weight:normal;',
      '  line-height:1.1;margin-bottom:4px;color:#fff!important;',
      '}',
      '#view-packsim .calc-stat span{',
      '  font-size:11px;font-weight:800;letter-spacing:0.5px;text-transform:uppercase;',
      '  opacity:0.9;color:#fff!important;',
      '}',
      '#view-packsim .calc-section-label{',
      '  font-family:"Titan One",cursive;font-size:18px;margin:16px 0 10px;',
      '  text-align:center;font-weight:normal;color:#fff!important;',
      '}',
      '#view-packsim .calc-avg-table-wrap{',
      '  overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:14px;',
      '  border-radius:14px;border:3px solid rgba(255,255,255,0.16);background:rgba(0,0,0,0.22);',
      '}',
      '#view-packsim .calc-avg-table{ width:100%;border-collapse:collapse;min-width:340px; }',
      '#view-packsim .calc-avg-table th,#view-packsim .calc-avg-table td{',
      '  padding:10px 12px;text-align:left;border-bottom:1px solid rgba(255,255,255,0.1);',
      '  font-size:13px;font-weight:700;color:#fff!important;',
      '}',
      '#view-packsim .calc-avg-table th{',
      '  background:rgba(0,0,0,0.25);font-size:11px;text-transform:uppercase;letter-spacing:0.4px;',
      '}',
      '#view-packsim .calc-avg-table tr:last-child td{ border-bottom:none; }',
      '#view-packsim .calc-avg-table .num{ text-align:right;font-variant-numeric:tabular-nums;font-weight:900; }',
      '#view-packsim .calc-avg-table .blook-cell{ display:flex;align-items:center;gap:8px; }',
      '#view-packsim .calc-avg-table .blook-cell img{ width:32px;height:32px;object-fit:contain;flex-shrink:0; }',
      '#view-packsim .calc-note{',
      '  margin-top:12px;font-size:12px;font-weight:700;opacity:0.85;text-align:center;',
      '  line-height:1.45;padding:10px 12px;background:rgba(0,0,0,0.18);border-radius:10px;color:#fff!important;',
      '}',
      '#view-packsim .calc-locked-msg{',
      '  text-align:center;padding:28px 16px;background:rgba(0,0,0,0.25);border-radius:16px;',
      '  border:3px solid rgba(255,255,255,0.15);color:#fff;font-weight:800;',
      '}',
      '#view-packsim .calc-locked-msg b{ font-family:"Titan One",cursive;font-weight:normal;font-size:22px;display:block;margin-bottom:8px; }'
    ].join('\n');
    document.head.appendChild(s);
  }

  /* ========== ONLINE COUNTER ========== */
  function fixOnlineCounter() {
    if (window.__bbOnlineV3) return;
    window.__bbOnlineV3 = 1;
    var TOPIC_PREFIX = 'blookbase/v3/online/';
    var BROKERS = [
      'wss://broker.emqx.io:8084/mqtt',
      'wss://test.mosquitto.org:8081/mqtt',
      'wss://broker.hivemq.com:8884/mqtt'
    ];
    var STALE_MS = 45000;
    var HEARTBEAT_MS = 15000;
    var sessionId;
    try {
      sessionId = sessionStorage.getItem('blookbase_sid');
      if (!sessionId) {
        sessionId = 's' + Math.random().toString(36).slice(2) + Date.now().toString(36);
        sessionStorage.setItem('blookbase_sid', sessionId);
      }
    } catch (e) {
      sessionId = 's' + Math.random().toString(36).slice(2) + Date.now().toString(36);
    }
    var onlineMap = new Map();
    var countEl = document.getElementById('online-count');
    var client = null;
    var brokerIndex = 0;
    var heartbeatTimer = null;
    var connecting = false;

    function myName() {
      try {
        if (typeof getDisplayName === 'function') {
          var n = getDisplayName();
          return n == null ? '' : String(n).slice(0, 24);
        }
      } catch (e) {}
      return '';
    }
    function renderCount() {
      var now = Date.now();
      onlineMap.forEach(function (info, id) {
        var t = info && typeof info === 'object' ? info.t : Number(info);
        if (!t || now - t > STALE_MS) onlineMap.delete(id);
      });
      onlineMap.set(sessionId, { t: now, name: myName() });
      if (countEl) countEl.textContent = String(onlineMap.size);
      if (typeof renderAdminVisitors === 'function') {
        try { renderAdminVisitors(onlineMap); } catch (e) {}
      }
    }
    function onPresenceMessage(topic, payload) {
      if (!topic || topic.indexOf(TOPIC_PREFIX) !== 0) return;
      var id = topic.slice(TOPIC_PREFIX.length);
      if (!id || id === sessionId) return;
      var text = payload ? payload.toString() : '';
      if (!text) onlineMap.delete(id);
      else {
        var t = Date.now(), name = '', parts = text.split('|');
        if (parts.length >= 2) {
          t = Number(parts[0]) || Date.now();
          name = parts.slice(1).join('|').slice(0, 24);
        } else t = Number(text) || Date.now();
        if (Date.now() - t > STALE_MS) onlineMap.delete(id);
        else onlineMap.set(id, { t: t, name: name });
      }
      renderCount();
    }
    function myTopic() { return TOPIC_PREFIX + sessionId; }
    function publishHere() {
      if (!client || !client.connected) return;
      var name = myName();
      try {
        client.publish(myTopic(), String(Date.now()) + '|' + name, { qos: 0, retain: true });
      } catch (e) {}
      onlineMap.set(sessionId, { t: Date.now(), name: name });
      renderCount();
    }
    window.__bbPublishPresence = publishHere;

    function tryNextBroker() {
      if (heartbeatTimer) { clearInterval(heartbeatTimer); heartbeatTimer = null; }
      if (client) {
        try { client.removeAllListeners(); client.end(true); } catch (e) {}
        client = null;
      }
      brokerIndex += 1;
      if (brokerIndex < BROKERS.length) setTimeout(connectBroker, 600);
      else renderCount();
    }
    function connectBroker() {
      if (typeof mqtt === 'undefined' || brokerIndex >= BROKERS.length) {
        renderCount();
        return;
      }
      if (connecting) return;
      connecting = true;
      try {
        client = mqtt.connect(BROKERS[brokerIndex], {
          clientId: 'bb_' + sessionId.slice(0, 16) + '_' + Math.random().toString(36).slice(2, 6),
          clean: true,
          reconnectPeriod: 0,
          connectTimeout: 10000,
          will: { topic: myTopic(), payload: '', retain: true, qos: 0 }
        });
        client.on('connect', function () {
          connecting = false;
          try { client.subscribe(TOPIC_PREFIX + '#', { qos: 0 }); } catch (e) {}
          publishHere();
          if (heartbeatTimer) clearInterval(heartbeatTimer);
          heartbeatTimer = setInterval(publishHere, HEARTBEAT_MS);
          setInterval(renderCount, 10000);
        });
        client.on('message', function (t, p) { onPresenceMessage(t, p); });
        client.on('error', function () { connecting = false; tryNextBroker(); });
        client.on('close', function () {
          if (heartbeatTimer) { connecting = false; tryNextBroker(); }
        });
      } catch (e) {
        connecting = false;
        tryNextBroker();
      }
    }
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) publishHere();
    });
    window.addEventListener('beforeunload', function () {
      try {
        if (client && client.connected) client.publish(myTopic(), '', { qos: 0, retain: true });
      } catch (e) {}
    });
    renderCount();
    setTimeout(connectBroker, 400);
  }

  /* ========== REMOVE LEAKS ========== */
  function removeLeaks() {
    document.querySelectorAll('[data-view="leaks"]').forEach(function (btn) {
      var li = btn.closest('li');
      if (li) li.remove();
      else btn.remove();
    });
    var view = document.getElementById('view-leaks');
    if (view) view.remove();
    // Home card linking to leaks
    document.querySelectorAll('[onclick*="leaks"], a[href*="leaks"]').forEach(function (el) {
      if (el.closest('#sidebar')) return;
      var card = el.closest('.home-card');
      if (card && /leak/i.test(card.textContent || '')) card.style.display = 'none';
    });
  }

  /* ========== /calculator route ========== */
  function fixCalculatorRoute() {
    var path = (location.pathname || '').replace(/\/+$/, '') || '/';
    if (path === '/calculator' || path === '/packsim') {
      if (typeof switchView === 'function') {
        try { switchView('packsim', true); } catch (e) {
          try { switchView('packsim'); } catch (e2) {}
        }
      }
    }
    // Make calculator nav set /calculator
    document.querySelectorAll('[data-view="packsim"]').forEach(function (btn) {
      if (btn.__bbCalcRoute) return;
      btn.__bbCalcRoute = 1;
      btn.addEventListener('click', function () {
        try {
          history.pushState({ view: 'packsim' }, '', '/calculator');
        } catch (e) {}
      }, true);
    });
    document.querySelectorAll('[onclick*="packsim"]').forEach(function (btn) {
      if (btn.__bbCalcRoute2) return;
      btn.__bbCalcRoute2 = 1;
      btn.addEventListener('click', function () {
        try {
          history.pushState({ view: 'packsim' }, '', '/calculator');
        } catch (e) {}
      }, true);
    });
  }

  /* ========== LOCK PACKS IN CALCULATOR ========== */
  function isLockedPack(name) {
    if (!name) return false;
    var n = String(name).replace(/\s*Pack$/i, '').trim();
    return Object.prototype.hasOwnProperty.call(LOCKED_PACKS, n) || Object.prototype.hasOwnProperty.call(LOCKED_PACKS, name);
  }
  function lockMsg(name) {
    var n = String(name).replace(/\s*Pack$/i, '').trim();
    return LOCKED_PACKS[n] || LOCKED_PACKS[name] || 'This pack is not available yet.';
  }

  function patchSelectCalcPack() {
    if (typeof window.selectCalcPack !== 'function') return;
    if (window.selectCalcPack.__bbLocked) return;
    var orig = window.selectCalcPack;
    window.selectCalcPack = function (name, quiet) {
      if (isLockedPack(name)) {
        var detail = document.getElementById('calc-detail');
        var pick = document.getElementById('calc-pick-section');
        var results = document.getElementById('calc-results');
        if (pick) pick.style.display = 'none';
        if (detail) {
          detail.style.display = 'block';
          var packEl = document.getElementById('calc-detail-pack');
          var meta = document.getElementById('calc-selected-meta');
          var blookGrid = document.getElementById('calc-blook-grid');
          var pack = (marketPacks || []).find(function (p) { return p && p.name === name; });
          if (packEl && pack) {
            packEl.innerHTML = '<img src="' + (pack.icon || '') + '" alt="">';
          }
          if (meta) {
            meta.innerHTML = '<b>' + name + ' Pack</b><span style="opacity:0.95">🔒 Not released</span>';
          }
          if (blookGrid) blookGrid.innerHTML = '';
        }
        if (results) {
          results.innerHTML =
            '<div class="calc-locked-msg"><b>🔒 Coming soon</b>' +
            lockMsg(name) +
            '<div style="margin-top:14px"><button type="button" class="calc-change-pack" onclick="showCalcPackPicker()">' +
            '<i class="fas fa-th"></i> Pick another pack</button></div></div>';
        }
        if (typeof calcSelectedPack !== 'undefined') calcSelectedPack = name;
        var hidden = document.getElementById('calc-pack');
        if (hidden) hidden.value = name;
        return;
      }
      return orig.apply(this, arguments);
    };
    window.selectCalcPack.__bbLocked = 1;
  }

  function markLockedPackCards() {
    var grid = document.getElementById('calc-pack-grid');
    if (!grid) return;
    grid.querySelectorAll('.calc-pack-card').forEach(function (card) {
      var title = card.getAttribute('title') || card.getAttribute('onclick') || '';
      var name = card.getAttribute('title');
      if (!name && card.getAttribute('onclick')) {
        var m = String(card.getAttribute('onclick')).match(/selectCalcPack\('([^']+)'\)/);
        if (m) name = m[1];
      }
      if (isLockedPack(name)) {
        card.classList.add('is-locked');
        card.setAttribute('aria-disabled', 'true');
        card.onclick = function (e) {
          e.preventDefault();
          e.stopPropagation();
          selectCalcPack(name);
        };
      }
    });
  }

  /* ========== CALCULATOR RESULTS UI ========== */
  function fmtExp(n) {
    if (n >= 100) return n.toFixed(0);
    if (n >= 10) return n.toFixed(1);
    if (n >= 1) return n.toFixed(2);
    if (n >= 0.01) return n.toFixed(3);
    return n.toFixed(4);
  }

  window.runPackCalculator = function () {
    injectStyles();
    var name =
      (typeof calcSelectedPack !== 'undefined' && calcSelectedPack) ||
      ((document.getElementById('calc-pack') || {}).value) ||
      '';
    var out = document.getElementById('calc-results');
    if (!out) return;

    if (isLockedPack(name)) {
      out.innerHTML =
        '<div class="calc-locked-msg"><b>🔒 Coming soon</b>' + lockMsg(name) + '</div>';
      return;
    }

    var tokensIn = Math.max(0, Math.floor(Number((document.getElementById('calc-tokens') || {}).value) || 0));
    var resell = !!(document.getElementById('calc-resell') || {}).checked;
    var pack = (marketPacks || []).find(function (p) { return p && p.name === name; });
    if (!pack) {
      out.innerHTML = '<p class="calc-empty">Pick a pack first.</p>';
      return;
    }
    var price = Number(pack.price);
    var pool = (pack.blooks || []).filter(function (b) {
      return b && b.chance != null && Number(b.chance) > 0;
    });
    if (!pool.length || !(price > 0)) {
      out.innerHTML = '<p class="calc-empty">This pack has no drop rates.</p>';
      return;
    }

    var baseOpens = Math.floor(tokensIn / price);
    var expected = {};
    pool.forEach(function (b) {
      expected[b.name] = baseOpens * (Number(b.chance) / 100);
    });

    var totalPulled = {};
    var kept = {};
    var tokens = tokensIn;
    var packsOpened = 0;
    var tokensFromSales = 0;
    var tokensSpentOnPacks = 0;
    var maxRounds = 500000;

    function addBlook(b) {
      if (!totalPulled[b.name]) totalPulled[b.name] = { blook: b, count: 0 };
      totalPulled[b.name].count++;
      if (!kept[b.name]) kept[b.name] = { blook: b, count: 0 };
      kept[b.name].count++;
    }

    if (!resell) {
      packsOpened = baseOpens;
      tokensSpentOnPacks = baseOpens * price;
      tokens = tokensIn - tokensSpentOnPacks;
      for (var i = 0; i < baseOpens; i++) addBlook(calcRollBlook(pool));
    } else {
      var rounds = 0;
      while (tokens >= price && rounds < maxRounds) {
        rounds++;
        tokens -= price;
        tokensSpentOnPacks += price;
        packsOpened++;
        addBlook(calcRollBlook(pool));
        var sold = 0;
        Object.keys(kept).forEach(function (n) {
          var row = kept[n];
          if (row.count > 1) {
            var extra = row.count - 1;
            sold += extra * calcSellPrice(row.blook);
            row.count = 1;
          }
        });
        tokens += sold;
        tokensFromSales += sold;
      }
    }

    var expectedForDisplay = {};
    pool.forEach(function (b) {
      expectedForDisplay[b.name] = packsOpened * (Number(b.chance) / 100);
    });

    var rows = pool
      .map(function (b) {
        var got = totalPulled[b.name] ? totalPulled[b.name].count : 0;
        var exp = expectedForDisplay[b.name] || 0;
        return { b: b, got: got, exp: exp, pct: Number(b.chance) };
      })
      .filter(function (r) { return r.exp >= 0.005 || r.got > 0; })
      .sort(function (a, b) { return b.pct - a.pct || b.exp - a.exp; });

    // tokens spent on this calculation
    var coinsLabel = tokensSpentOnPacks.toLocaleString();

    var summaryHtml =
      '<div class="calc-summary">' +
      '<div class="calc-stat"><b>' + packsOpened.toLocaleString() + '</b><span>Packs opened</span></div>' +
      '<div class="calc-stat"><b>' + coinsLabel + '</b><span>Tokens spent</span></div>' +
      (resell
        ? '<div class="calc-stat"><b>' + tokensFromSales.toLocaleString() + '</b><span>From selling</span></div>'
        : '') +
      '<div class="calc-stat"><b>' + tokens.toLocaleString() + '</b><span>Tokens left</span></div>' +
      '</div>';

    // Table: Blook | Drop % | Avg you get | This run
    var tableRows = rows
      .map(function (r) {
        var img = typeof getBlookImg === 'function' ? getBlookImg(r.b.name) : '';
        return (
          '<tr>' +
          '<td><div class="blook-cell"><img src="' +
          img +
          '" alt=""><span>' +
          r.b.name +
          '</span></div></td>' +
          '<td class="num">' +
          r.pct +
          '%</td>' +
          '<td class="num">' +
          fmtExp(r.exp) +
          '</td>' +
          '<td class="num">' +
          r.got.toLocaleString() +
          '</td>' +
          '</tr>'
        );
      })
      .join('');

    var tableHtml =
      '<div class="calc-section-label">With ' +
      coinsLabel +
      ' tokens spent — drop % & average you get</div>' +
      '<div class="calc-avg-table-wrap"><table class="calc-avg-table">' +
      '<thead><tr>' +
      '<th>Blook</th>' +
      '<th class="num">Drop %</th>' +
      '<th class="num">Avg you get</th>' +
      '<th class="num">This run</th>' +
      '</tr></thead><tbody>' +
      tableRows +
      '</tbody></table></div>';

    var note =
      '<p class="calc-note">' +
      (resell
        ? 'Resell on: duplicates sold (keep 1), tokens reused. <b>Avg you get</b> = packs opened × drop %. <b>This run</b> is one random simulation.'
        : 'With <b>' +
          coinsLabel +
          ' tokens</b> you open <b>' +
          packsOpened.toLocaleString() +
          '</b> packs at ' +
          price +
          ' each. <b>Avg you get</b> = packs × drop %. <b>This run</b> is one random simulation.') +
      '</p>';

    out.innerHTML = summaryHtml + tableHtml + note;
    try {
      out.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (e) {}
  };

  /* ========== LIVE VIDEOS = BLOOKET ONLY ========== */
  function fixLiveVideos() {
    // Fix YouTube live search CTA so it doesn't show unrelated / brainrot streams
    document.querySelectorAll('a[href*="youtube.com/results"]').forEach(function (a) {
      var href = a.getAttribute('href') || '';
      if (/search_query=Blooket/i.test(href) || /sp=EgJAAQ/i.test(href)) {
        a.setAttribute(
          'href',
          'https://www.youtube.com/results?search_query=Blooket+live+games&sp=EgJAAQ%253D%253D'
        );
      }
    });

    // Patch isLiveVideo / renderVideos to require Blooket in title or known channels
    if (typeof window.renderVideos !== 'function') return;
    if (window.renderVideos.__bbLiveFix) return;

    var BLOOKET_LIVE_OK = /blooket|unblooked|waymore|lag0n|fastyjay|blooket\s*ace|purple\s*panda|neonate|monkey\s*master/i;

    var orig = window.renderVideos;
    window.renderVideos = function () {
      // Temporarily filter videoData for live tab
      if (typeof currentVideoFilter === 'string' && currentVideoFilter === 'live' && Array.isArray(videoData)) {
        var backup = videoData.slice();
        videoData = videoData.filter(function (v) {
          var t = String(v.title || '');
          var c = String(v.channel || '');
          var isLive =
            v.cat === 'live' ||
            v.isLive === true ||
            v.views === 'LIVE' ||
            /\bLIVE\b/i.test(t) ||
            /\b(hosting\s+blooket|games\s+live)\b/i.test(t);
          if (!isLive) return true; // non-live kept for other filters inside orig
          return BLOOKET_LIVE_OK.test(t + ' ' + c);
        });
        try {
          return orig.apply(this, arguments);
        } finally {
          videoData = backup;
        }
      }
      return orig.apply(this, arguments);
    };
    window.renderVideos.__bbLiveFix = 1;

    // Update CTA text if present
    document.querySelectorAll('#videos-grid a, .video-live-cta, .videos-live-banner').forEach(function (el) {
      if (/brainrot/i.test(el.textContent || '')) {
        el.textContent = (el.textContent || '').replace(/brainrot/gi, 'Blooket');
      }
    });
  }

  /* ========== UPDATES PAGE TOUCH ========== */
  function enhanceUpdatesHint() {
    // Soft banner if updates view exists
    var view = document.getElementById('view-updates');
    if (!view || view.querySelector('.bb-updates-note')) return;
    var note = document.createElement('p');
    note.className = 'bb-updates-note';
    note.style.cssText =
      'text-align:center;font-weight:800;opacity:0.9;margin:0 0 14px;color:#fff;';
    note.textContent =
      'Official Blooket product updates · Newest first · Fan-made tracker (not affiliated with Blooket)';
    var title = view.querySelector('.header-title');
    if (title && title.nextSibling) title.parentNode.insertBefore(note, title.nextSibling);
    else if (title) title.after(note);
  }

  /* ========== BOOT ========== */
  function boot() {
    injectStyles();
    removeLeaks();
    fixCalculatorRoute();
    patchSelectCalcPack();
    markLockedPackCards();
    fixLiveVideos();
    enhanceUpdatesHint();
    fixOnlineCounter();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
  setTimeout(boot, 400);
  setTimeout(function () {
    markLockedPackCards();
    fixLiveVideos();
    removeLeaks();
  }, 1500);

  // Re-mark locked cards when opening calculator
  document.addEventListener('click', function () {
    setTimeout(markLockedPackCards, 200);
  });
})();
