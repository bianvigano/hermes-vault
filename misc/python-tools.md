# Python — Tools & Scripts

Kumpulan script Python untuk tooling: duplicate image finder, backup, file utilities.

---

## Duplicate Image Finder (pHash + Multi-Process)

```bash
pip install pillow imagehash tqdm
```

### Simple Version (Single Process)

```python
from PIL import Image
import imagehash

img1 = Image.open("foto1.jpg")
img2 = Image.open("foto2.jpg")
hash1 = imagehash.phash(img1)
hash2 = imagehash.phash(img2)
jarak = hash1 - hash2

# jarak < 5 → hampir sama, < 10 → mirip, > 15 → beda
```

### Advanced: Multi-Process + SQLite Temp (Low RAM)

```python
from multiprocessing import Pool, cpu_count
import sqlite3, tempfile, os
from PIL import Image
import imagehash
from tqdm import tqdm

def process_image(path):
    try:
        with Image.open(path) as img:
            return (path, str(imagehash.phash(img)))
    except: return None

# CLI: python scan.py D:\Foto --threshold 8 --workers 6
```

Fitur:
- Threshold kemiripan (hash beda sedikit)
- Multi-process (CPU bound, bypass GIL)
- SQLite temp file (RAM minim)
- Progress bar + ETA + waktu total
- Skala jutaan file

## Backup Script

### Bash ke Python

Banyak script backup dari bash → Python: lebih readable, error handling lebih baik, library compression built-in (`shutil`, `tarfile`, `zipfile`).

```python
import shutil
import datetime

name = f"backup-{datetime.date.today()}.tar.gz"
shutil.make_archive(name.replace('.tar.gz', ''), 'gztar', '/source/folder')
```

## VS Code Cache Clean (Linux)

```bash
# Lokasi cache
~/.config/Code/Cache/
~/.config/Code/CachedData/
~/.config/Code/User/workspaceStorage/   # per-project, sering paling besar
~/.config/Code/User/Backups/            # auto-backup saat crash
/tmp                                     # temporary sistem

# Quick clean
rm -rf ~/.config/Code/Cache/*
rm -rf ~/.config/Code/CachedData/*
rm -rf ~/.config/Code/User/Backups/*
```

## Related

- [[misc/media-processing]] — ffmpeg, video, kompresi
- [[webdev/backend/nodejs-api]] — Node.js backend
