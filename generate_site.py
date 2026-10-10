from PIL import Image, ImageDraw, ImageFont
import json
import os

os.makedirs('/home/ubuntu/a7x-singalong', exist_ok=True)

# 1. Generate Icons (512x512 and 192x192)
for size in [512, 192]:
    img = Image.new('RGB', (size, size), color='#09090b')
    draw = ImageDraw.Draw(img)
    
    pad = int(size * 0.08)
    draw.rounded_rectangle([pad, pad, size - pad, size - pad], radius=int(size * 0.22), fill='#18181b', outline='#27272a', width=max(2, int(size * 0.02)))
    
    # Inner badge
    c_pad = int(size * 0.2)
    draw.ellipse([c_pad, c_pad, size - c_pad, size - c_pad], fill='#121215', outline='#3f3f46', width=max(1, int(size * 0.015)))
    
    # Stylized A7X monogram
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(size * 0.22))
    except Exception:
        font = ImageFont.load_default()
        
    text = "A7X"
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((size - w) / 2, (size - h) / 2 - int(size * 0.04)), text, fill='#ffffff', font=font)
    
    # Sub text "2026"
    try:
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(size * 0.1))
        sub_text = "2026"
        sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
        sw = sub_bbox[2] - sub_bbox[0]
        draw.text(((size - sw) / 2, (size - h) / 2 + int(size * 0.22)), sub_text, fill='#a1a1aa', font=sub_font)
    except Exception:
        pass

    img.save(f'/home/ubuntu/a7x-singalong/icon-{size}.png')

print("Icons generated.")

# 2. Generate manifest.json
manifest = {
    "name": "A7X Asia Tour 2026",
    "short_name": "A7X 2026",
    "description": "Avenged Sevenfold Asia Tour 2026 Setlist & Lyrics",
    "start_url": "./index.html",
    "display": "standalone",
    "background_color": "#09090b",
    "theme_color": "#09090b",
    "orientation": "portrait-primary",
    "icons": [
        {
            "src": "./icon-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any maskable"
        },
        {
            "src": "./icon-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any maskable"
        }
    ]
}
with open('/home/ubuntu/a7x-singalong/manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2)

# 3. Generate sw.js
sw_code = """const CACHE_NAME = 'a7x-2026-v2';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
    )).then(() => clients.claim())
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(res => res || fetch(e.request))
  );
});
"""
with open('/home/ubuntu/a7x-singalong/sw.js', 'w') as f:
    f.write(sw_code)

print("Manifest and SW generated.")
