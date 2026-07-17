#!/usr/bin/env python3
"""
Vault Session Manager
- Buat folder/grup baru di vault/sessions/
- Pindah file ke folder yang sesuai
- Auto-link ke wiki kalau topik berkaitan
- Generate index.md per folder otomatis
"""

import os
import re
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

VAULT_SESSIONS = Path.home() / ".hermes/vault/sessions"
VAULT_WIKI = Path.home() / ".hermes/vault/wiki"
VAULT_ROOT = Path.home() / ".hermes/vault"

# Topic keywords → folder name mapping
TOPIC_KEYWORDS = {
    "minecraft": ["minecraft", "mc", "bukkit", "spigot", "paper", "folia", "plugin", "server", "spark", "luckperms", "hungergames"],
    "senyawa": ["senyawa", "nextjs", "next.js", "prisma", "tailwind", "react", "typescript", "javascript", "html", "css", "web"],
    "hermes": ["hermes", "vault", "skill", "cron", "memory", "session", "agent", "openrouter", "gateway"],
}

# Wiki file mapping → wiki link
WIKI_FILES = {
    "minecraft": "minecraft-servers.md",
    "senyawa": "senyawa-web-x.md",
    "hermes": "hermes-setup.md",
}


def scan_files():
    """Scan all .md files in vault/sessions/ (not in subfolders)."""
    files = []
    for f in VAULT_SESSIONS.rglob("*.md"):
        # Skip index.md and README.md
        if f.name in ("index.md", "README.md"):
            continue
        # Only process files that are directly in sessions/ root (not in subfolders)
        if f.parent == VAULT_SESSIONS:
            files.append(f)
    return files


def read_frontmatter(f):
    """Read YAML frontmatter from file."""
    content = f.read_text()
    lines = content.split("\n")
    meta = {"title": "", "date": "", "tags": [], "content": ""}
    
    in_fm = False
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                body_start = i + 1
                break
        if in_fm:
            if line.startswith("title:"):
                meta["title"] = line.replace("title:", "").strip()
            elif line.startswith("date:"):
                meta["date"] = line.replace("date:", "").strip()
            elif line.startswith("tags:"):
                tags_str = line.replace("tags:", "").strip()
                # Parse [tag1, tag2, ...]
                meta["tags"] = [t.strip().strip("[]'\"") for t in tags_str.split(",") if t.strip()]
    
    meta["content"] = "\n".join(lines[body_start:]).strip()
    return meta


def detect_topic(meta):
    """Detect which topic folder a file belongs to."""
    text = (meta["title"] + " " + " ".join(meta["tags"]) + " " + meta["content"][:200]).lower()
    
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[topic] = score
    
    if not scores:
        return "other"
    
    return max(scores, key=scores.get)


def generate_slug(title, tags):
    """Generate clean slug from title."""
    # Remove special chars
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
    # Take first 4 meaningful words
    words = [w for w in slug.split() if len(w) > 2][:4]
    slug = "-".join(words) if words else "session"
    # Clean up
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug


def create_folder(folder_name):
    """Create folder structure with README.md and index.md."""
    folder_path = VAULT_SESSIONS / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)
    
    # Create README.md if not exists
    readme_path = folder_path / "README.md"
    if not readme_path.exists():
        wiki_link = ""
        if folder_name in WIKI_FILES:
            wiki_file = WIKI_FILES[folder_name]
            wiki_link = f"\n\nLihat juga: [[{wiki_file.replace('.md', '')}]] di wiki/"
        
        readme_content = f"""# {folder_name.capitalize()}

Session terkait {folder_name}.{wiki_link}
"""
        readme_path.write_text(readme_content)
    
    return folder_path


def update_index(folder_path, folder_name):
    """Update or create index.md for a folder."""
    index_path = folder_path / "index.md"
    
    # Collect all .md files in folder (not subfolders, not index/readme)
    files = sorted([f for f in folder_path.glob("*.md") 
                    if f.name not in ("index.md", "README.md")])
    
    lines = [f"# {folder_name.capitalize()} — Daftar Session\n"]
    
    for f in files:
        meta = read_frontmatter(f)
        title = meta["title"] or f.stem
        slug = f.stem
        lines.append(f"- [[{slug}]] — {title}")
    
    # Add cross-folder links
    lines.append("\n## Cross-folder Links")
    for other_folder in sorted(VAULT_SESSIONS.iterdir()):
        if other_folder.is_dir() and other_folder.name != folder_name:
            other_index = other_folder / "index.md"
            if other_index.exists():
                lines.append(f"- [[{other_folder.name}/index]] — {other_folder.name.capitalize()} sessions")
    
    # Add wiki link
    if folder_name in WIKI_FILES:
        wiki_file = WIKI_FILES[folder_name]
        lines.append(f"\n## Wiki")
        lines.append(f"- [[wiki/{wiki_file.replace('.md', '')}]] — {folder_name.capitalize()} wiki page")
    
    index_path.write_text("\n".join(lines))


def add_wiki_link_to_file(file_path, folder_name):
    """Add wiki link to file's Related section."""
    content = file_path.read_text()
    
    if folder_name not in WIKI_FILES:
        return
    
    wiki_file = WIKI_FILES[folder_name]
    wiki_slug = wiki_file.replace(".md", "")
    wiki_link = f"[[wiki/{wiki_slug}]]"
    
    # Check if already has wiki link
    if wiki_link in content:
        return
    
    # Add to Related section or create one
    if "## Related" in content:
        content = content.replace("## Related", f"## Related\n- {wiki_link} — Wiki page untuk {folder_name}")
    else:
        content += f"\n\n## Related\n- {wiki_link} — Wiki page untuk {folder_name}"
    
    file_path.write_text(content)


def move_file_to_folder(file_path, folder_name):
    """Move file to appropriate folder with clean name."""
    meta = read_frontmatter(file_path)
    slug = generate_slug(meta["title"], meta["tags"])
    
    folder_path = create_folder(folder_name)
    new_path = folder_path / f"{slug}.md"
    
    # Handle duplicates
    counter = 2
    while new_path.exists():
        new_path = folder_path / f"{slug}-{counter}.md"
        counter += 1
    
    shutil.move(str(file_path), str(new_path))
    return new_path


def cmd_create_folder(folder_name):
    """Create a new folder/group."""
    folder_path = create_folder(folder_name)
    
    # Create initial index.md
    index_path = folder_path / "index.md"
    index_content = f"""# {folder_name.capitalize()} — Daftar Session

Belum ada session di folder ini.
"""
    index_path.write_text(index_content)
    
    print(f"✅ Folder created: {folder_path}")
    print(f"   README.md: {folder_path / 'README.md'}")
    print(f"   index.md: {index_path}")
    return folder_path


def cmd_organize():
    """Auto-organize all loose files in sessions/ root."""
    files = scan_files()
    
    if not files:
        print("ℹ️  No loose files to organize.")
        return
    
    print(f"📁 Found {len(files)} loose files. Organizing...\n")
    
    moved = []
    for f in files:
        meta = read_frontmatter(f)
        topic = detect_topic(meta)
        new_path = move_file_to_folder(f, topic)
        add_wiki_link_to_file(new_path, topic)
        moved.append((f.name, topic, new_path.name))
        print(f"  {f.name}")
        print(f"    → {topic}/{new_path.name}")
    
    # Update all index files
    print("\n📝 Updating index files...")
    for folder in sorted(VAULT_SESSIONS.iterdir()):
        if folder.is_dir() and not folder.name.startswith("."):
            update_index(folder, folder.name)
            print(f"  ✅ {folder.name}/index.md")
    
    # Update root index
    update_root_index()
    print(f"\n✅ Done! {len(moved)} files organized.")


def cmd_move(file_pattern, folder_name):
    """Move matching files to a folder."""
    files = list(VAULT_SESSIONS.rglob(f"*{file_pattern}*.md"))
    files = [f for f in files if f.name not in ("index.md", "README.md")]
    
    if not files:
        print(f"❌ No files matching '{file_pattern}'")
        return
    
    folder_path = create_folder(folder_name)
    
    for f in files:
        new_path = folder_path / f.name
        shutil.move(str(f), str(new_path))
        add_wiki_link_to_file(new_path, folder_name)
        print(f"  {f.name} → {folder_name}/")
    
    update_index(folder_path, folder_name)
    print(f"✅ Moved {len(files)} files to {folder_name}/")


def cmd_link_wiki(folder_name):
    """Add wiki links to all files in a folder."""
    folder_path = VAULT_SESSIONS / folder_name
    if not folder_path.exists():
        print(f"❌ Folder '{folder_name}' not found")
        return
    
    count = 0
    for f in folder_path.glob("*.md"):
        if f.name in ("index.md", "README.md"):
            continue
        add_wiki_link_to_file(f, folder_name)
        count += 1
    
    print(f"✅ Added wiki links to {count} files in {folder_name}/")


def update_root_index():
    """Update vault/index.md with folder listing."""
    index_path = VAULT_ROOT / "index.md"
    
    folders = sorted([d for d in VAULT_SESSIONS.iterdir() if d.is_dir() and not d.name.startswith(".")])
    
    lines = ["# Vault Sessions Index\n"]
    lines.append("Semua session dikelompokkan per topik.\n")
    lines.append("## Folders\n")
    
    for folder in folders:
        readme = folder / "README.md"
        index = folder / "index.md"
        desc = ""
        if readme.exists():
            desc = readme.read_text().split("\n")[0].replace("# ", "")
        lines.append(f"- [[{folder.name}/index]] — {desc}")
    
    lines.append(f"\n## Stats")
    lines.append(f"- Total folders: {len(folders)}")
    lines.append(f"- Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    index_path.write_text("\n".join(lines))


def cmd_status():
    """Show current vault/sessions status."""
    print("📊 Vault Sessions Status\n")
    
    folders = sorted([d for d in VAULT_SESSIONS.iterdir() if d.is_dir() and not d.name.startswith(".")])
    
    total_files = 0
    for folder in folders:
        files = [f for f in folder.rglob("*.md") if f.name not in ("index.md", "README.md")]
        total_files += len(files)
        print(f"  {folder.name}/ — {len(files)} files")
    
    # Loose files
    loose = scan_files()
    if loose:
        print(f"  [root] — {len(loose)} loose files (need organizing)")
    
    print(f"\nTotal: {total_files} files in {len(folders)} folders")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nCommands:")
        print("  status                    - Show vault status")
        print("  organize                  - Auto-organize loose files")
        print("  create <folder>           - Create new folder/group")
        print("  move <pattern> <folder>   - Move matching files to folder")
        print("  link <folder>             - Add wiki links to folder files")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        cmd_status()
    elif cmd == "organize":
        cmd_organize()
    elif cmd == "create" and len(sys.argv) >= 3:
        cmd_create_folder(sys.argv[2])
    elif cmd == "move" and len(sys.argv) >= 4:
        cmd_move(sys.argv[2], sys.argv[3])
    elif cmd == "link" and len(sys.argv) >= 3:
        cmd_link_wiki(sys.argv[2])
    else:
        print(f"❌ Unknown command: {cmd}")
        print("Run without args for usage.")


if __name__ == "__main__":
    main()
