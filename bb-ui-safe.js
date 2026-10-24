/* Blookbase UI fixes — safe, no MutationObserver */
(function () {
  'use strict';
  if (window.__bbUiFixes) return;
  window.__bbUiFixes = 1;

  function fixHomeBanner() {
    var banner = document.querySelector('.home-banner');
    if (!banner || banner.getAttribute('data-bb-fixed') === '1') return;
    var h2 = banner.querySelector('h2');
    var p = banner.querySelector('p');
    var label = banner.querySelector('.home-banner-label');
    var logo = banner.querySelector('.home-banner-logo');
    if (h2 && /coming/i.test(h2.textContent || '')) h2.textContent = 'Spooky Pack is LIVE!';
    if (label && label.textContent.indexOf('LIVE') === -1) label.textContent = 'Spooktober \u00b7 LIVE';
    if (p && /countdown is live|days until Spooktober/i.test(p.textContent || '')) {
      p.textContent =
        'Halloween is here \u2014 Spooky Pack is in the Market with 14 blooks. Open Countdown for event timers and Season updates.';
    }
    if (logo && logo.getAttribute('data-bb-src') !== '1') {
      logo.src = 'https://ac.blooket.com/marketassets/blooks/spookymoth.svg';
      logo.alt = 'Spooky Pack';
      logo.setAttribute('data-bb-src', '1');
    }
    banner.setAttribute('data-bb-fixed', '1');
  }

  function fixWhatsNewBlooks() {
    var view = document.getElementById('view-whatsnew');
    if (!view) return;
    view.querySelectorAll('.pack-blook').forEach(function (el) {
      if (el.getAttribute('data-bb-click')) return;
      var nameEl = el.querySelector('.bn');
      if (!nameEl) return;
      var name = (nameEl.textContent || '').trim();
      if (!name) return;
      var rarEl = el.querySelector('.br');
      var chEl = el.querySelector('.chance');
      var rarity = rarEl ? (rarEl.textContent || 'Uncommon').trim() : 'Uncommon';
      var chance = null;
      if (chEl) {
        var n = parseFloat(String(chEl.textContent || '').replace('%', ''));
        if (!isNaN(n)) chance = n;
      }
      el.setAttribute('data-bb-click', '1');
      el.style.cursor = 'pointer';
      el.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        if (typeof window.openBlookDetail === 'function') {
          window.openBlookDetail(name, rarity, chance, 'Spooky Pack');
        }
      });
    });
  }

  function run() {
    try {
      fixHomeBanner();
      fixWhatsNewBlooks();
    } catch (e) {}
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
  setTimeout(run, 600);
})();
