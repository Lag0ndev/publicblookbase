#!/usr/bin/env python3
from pathlib import Path

p = Path('index.html')
t = p.read_text(encoding='utf-8')

# mqtt must not block HTML parse
t = t.replace(
    '<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>',
    '<script src="https://unpkg.com/mqtt/dist/mqtt.min.js" defer></script>',
)
t = t.replace(
    "<script src='https://unpkg.com/mqtt/dist/mqtt.min.js'></script>",
    "<script src='https://unpkg.com/mqtt/dist/mqtt.min.js' defer></script>",
)

# Guard if mqtt CDN fails
if "typeof mqtt === 'undefined'" not in t:
    t = t.replace(
        'client = mqtt.connect(url, {',
        "if (typeof mqtt === 'undefined' || !mqtt.connect) { renderCount(); return; }\n                    client = mqtt.connect(url, {",
    )

failsafe = '''
    <script>
    /* Failsafe: never leave the page blank */
    (function(){
      function show(){
        try{
          document.body && document.body.classList.remove('ps-opening','no-scroll','bb-page-editing');
          var home=document.getElementById('view-home');
          var any=document.querySelector('.main-content[style*="display: flex"], .main-content[style*="display:flex"]');
          if(home && !any){
            document.querySelectorAll('.main-content').forEach(function(el){ el.style.display='none'; });
            home.style.display='flex';
          }
        }catch(e){}
      }
      if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', show);
      else show();
      setTimeout(show, 400);
      setTimeout(show, 1500);
      setTimeout(show, 4000);
    })();
    </script>
'''
if 'Failsafe: never leave' not in t:
    t = t.replace('<body>', '<body>' + failsafe, 1)

p.write_text(t, encoding='utf-8')
print('index patched', p.stat().st_size)

Path('vercel.json').write_text('''{
  "rewrites": [
    { "source": "/((?!api/|.*\\..*).*)", "destination": "/index.html" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-cache, no-store, must-revalidate" },
        { "key": "X-Blookbase-Deploy", "value": "2026-10-02-load-fix" }
      ]
    }
  ]
}
''')
print('vercel.json written')
print('OK')
