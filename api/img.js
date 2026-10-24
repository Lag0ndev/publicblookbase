// Vercel serverless: redirect to allowed Blooket asset URLs
// /api/img?blook=clownfish  OR  /api/img?src=https://ac.blooket.com/...

const ALLOW = [
  'ac.blooket.com',
  'media.blooket.com',
  'www.blooket.com',
  'blooket.com',
];

function allowed(url) {
  try {
    const u = new URL(url);
    return ALLOW.some((h) => u.hostname === h || u.hostname.endsWith('.' + h));
  } catch {
    return false;
  }
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'public, max-age=86400');

  const q = req.query || {};
  let target = q.src || q.url || '';

  if (!target && q.blook) {
    const slug = String(q.blook)
      .toLowerCase()
      .replace(/[^a-z0-9]/g, '');
    target = `https://ac.blooket.com/marketassets/blooks/${slug}.svg`;
  }

  if (!target || !allowed(target)) {
    res.statusCode = 400;
    res.setHeader('Content-Type', 'application/json');
    return res.end(JSON.stringify({ error: 'Invalid or disallowed asset URL' }));
  }

  res.statusCode = 302;
  res.setHeader('Location', target);
  res.end();
};
