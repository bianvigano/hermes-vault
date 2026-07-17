#!/usr/bin/env python3
"""
vault_cache.py — Cache manager untuk vault yang di-host di GitHub Pages.
Baca file vault dari GitHub Pages, cache di local dengan TTL.
Multi-token GitHub untuk fallback kalau rate limit.

Usage:
  python vault_cache.py get <path>  # e.g. sessions/hermes/kode-sekarang.md
  python vault_cache.py clear
  python vault_cache.py status
"""

import argparse
import base64
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ─── Config ───────────────────────────────────────────────────────────────────

VAULT_CACHE_DIR = Path.home() / ".hermes" / "vault-cache"
META_PATH = VAULT_CACHE_DIR / ".meta.json"
CONFIG_PATH = Path.home() / ".hermes" / "config.yaml"

# GitHub Pages base URL
GITHUB_USER = "bianvigano"
GITHUB_REPO = "hermes-vault"
PAGES_BASE = f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}"

# GitHub API base (untuk private repo / fallback)
GITHUB_API_BASE = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}"

# Default TTL: 24 jam (dalam detik)
DEFAULT_TTL = 24 * 3600

# Max retry
MAX_RETRIES = 3


def load_config():
    """Baca config Hermes untuk github tokens."""
    tokens = []
    repo = f"{GITHUB_USER}/{GITHUB_REPO}"
    
    # Coba baca config.yaml
    if CONFIG_PATH.exists():
        try:
            import yaml
            with open(CONFIG_PATH) as f:
                cfg = yaml.safe_load(f) or {}
            gh_cfg = cfg.get("github", {})
            tokens = gh_cfg.get("tokens", gh_cfg.get("token", []))
            if isinstance(tokens, str):
                tokens = [tokens]
            repo = gh_cfg.get("vault_repo", repo)
        except Exception:
            pass
    
    # Fallback ke env vars
    if not tokens:
        env_tokens = os.environ.get("GITHUB_TOKENS", "")
        if env_tokens:
            tokens = [t.strip() for t in env_tokens.split(",") if t.strip()]
        elif os.environ.get("GITHUB_TOKEN"):
            tokens = [os.environ["GITHUB_TOKEN"]]
    
    return {"tokens": tokens, "repo": repo}


def load_meta():
    """Baca metadata cache."""
    if META_PATH.exists():
        try:
            with open(META_PATH) as f:
                return json.load(f)
        except:
            pass
    return {}


def save_meta(meta):
    """Simpan metadata cache."""
    VAULT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(META_PATH, "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def cache_path(vault_path):
    """Local cache path untuk file vault."""
    return VAULT_CACHE_DIR / vault_path.replace("/", "_")


def is_cache_valid(meta, vault_path, ttl=DEFAULT_TTL):
    """Cek apakah cache masih valid."""
    entry = meta.get(vault_path)
    if not entry:
        return False
    
    last_access = entry.get("last_access", 0)
    now = time.time()
    
    # Extend TTL kalau masih diakses dalam 1 hari terakhir
    if now - last_access < ttl:
        return True
    
    return False


def fetch_from_pages(vault_path):
    """Fetch file dari GitHub Pages."""
    url = f"{PAGES_BASE}/{vault_path}"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text


def fetch_from_api(vault_path, token):
    """Fetch file dari GitHub API (untuk private repo)."""
    url = f"{GITHUB_API_BASE}/contents/{vault_path}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content


def fetch_file(vault_path, config):
    """Fetch file dari GitHub Pages atau API dengan retry + token rotation."""
    tokens = config.get("tokens", [])
    last_error = None
    
    # Coba GitHub Pages dulu (no auth, no rate limit)
    for attempt in range(MAX_RETRIES):
        try:
            return fetch_from_pages(vault_path)
        except Exception as e:
            last_error = e
            time.sleep(0.5 * (attempt + 1))
    
    # Fallback ke GitHub API dengan token rotation
    if tokens:
        for token in tokens:
            try:
                return fetch_from_api(vault_path, token)
            except Exception as e:
                last_error = e
                continue
    
    raise Exception(f"Failed to fetch {vault_path}: {last_error}")


def get(vault_path, ttl=DEFAULT_TTL, force_refresh=False):
    """Ambil file vault. Cek cache dulu, kalau tidak ada/fetch dari GitHub."""
    meta = load_meta()
    local_file = cache_path(vault_path)
    
    # Cek cache
    if not force_refresh and local_file.exists() and is_cache_valid(meta, vault_path, ttl):
        content = local_file.read_text(encoding="utf-8")
        # Update last access
        meta[vault_path] = meta.get(vault_path, {})
        meta[vault_path]["last_access"] = time.time()
        save_meta(meta)
        return content
    
    # Fetch dari GitHub
    config = load_config()
    content = fetch_file(vault_path, config)
    
    # Simpan cache
    VAULT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    local_file.write_text(content, encoding="utf-8")
    
    # Update meta
    meta[vault_path] = {
        "last_access": time.time(),
        "cached_at": time.time(),
    }
    save_meta(meta)
    
    return content


def clear_cache():
    """Hapus semua cache."""
    if VAULT_CACHE_DIR.exists():
        for f in VAULT_CACHE_DIR.iterdir():
            if f.is_file():
                f.unlink()
    save_meta({})
    print("Cache cleared.")


def status():
    """Tampilkan status cache."""
    meta = load_meta()
    print(f"Cache dir: {VAULT_CACHE_DIR}")
    print(f"Cached files: {len(meta)}")
    
    now = time.time()
    valid = 0
    expired = 0
    for path, entry in meta.items():
        last = entry.get("last_access", 0)
        if now - last < DEFAULT_TTL:
            valid += 1
        else:
            expired += 1
    
    print(f"  Valid: {valid}")
    print(f"  Expired: {expired}")


def main():
    parser = argparse.ArgumentParser(description="Vault cache manager")
    parser.add_argument("command", choices=["get", "clear", "status"])
    parser.add_argument("path", nargs="?", help="Vault file path, e.g. sessions/hermes/file.md")
    parser.add_argument("--force", action="store_true", help="Force refresh from GitHub")
    
    args = parser.parse_args()
    
    if args.command == "get":
        if not args.path:
            print("Error: path required")
            return
        content = get(args.path, force_refresh=args.force)
        print(content)
    elif args.command == "clear":
        clear_cache()
    elif args.command == "status":
        status()


if __name__ == "__main__":
    main()
