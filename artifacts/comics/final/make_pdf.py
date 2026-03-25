#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

base = Path('/Users/hidream/.openclaw/workspace/projects/opc/artifacts/comics/final')
img_dir = base / 'images'
out = base / 'opc-architecture-comic.pdf'
paths = sorted(img_dir.glob('*.jpg'))
images = []
for p in paths:
    img = Image.open(p).convert('RGB')
    images.append(img)
if not images:
    raise SystemExit('No images found')
first, rest = images[0], images[1:]
first.save(out, save_all=True, append_images=rest)
print(out)
