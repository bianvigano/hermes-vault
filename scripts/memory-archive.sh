#!/usr/bin/env bash
# memory-archive.sh
# Archive memory/user-profile entries to Vault. Search & retrieve.
#
# Usage:
#   memory-archive.sh flush <source> <content> [tags]
#   memory-archive.sh list
#   memory-archive.sh search <query>
#   memory-archive.sh get <filename>
#   memory-archive.sh status
#   memory-archive.sh delete <filename>

set -euo pipefail

VAULT_DIR="$HOME/.hermes/vault/memory-archive"
INDEX_FILE="$VAULT_DIR/INDEX.md"
DATE=$(TZ='Asia/Jakarta' date +"%Y-%m-%d")
DATETIME=$(TZ='Asia/Jakarta' date +"%Y-%m-%dT%H:%M:%S+07:00")

mkdir -p "$VAULT_DIR"

# ── helpers ──────────────────────────────────────────────────────────

slugify() {
    echo "$1" | head -c 60 \
        | tr '[:upper:]' '[:lower:]' \
        | sed 's/[^a-z0-9 ]/-/g' \
        | sed 's/  */-/g' \
        | sed 's/--*/-/g' \
        | sed 's/^-//;s/-$//'
}

index_add() {
    local date="$1" source="$2" summary="$3" tags="$4" file="$5"
    local tmp
    tmp=$(mktemp)
    local inserted=0
    while IFS= read -r line; do
        echo "$line" >> "$tmp"
        if [[ "$line" == *"---"* ]] && [[ "$line" == "|"* ]] && (( inserted == 0 )); then
            echo "| $date | $source | $summary | $tags | $file |" >> "$tmp"
            inserted=1
        fi
    done < "$INDEX_FILE"
    mv "$tmp" "$INDEX_FILE"
}

index_remove() {
    local file="$1"
    local tmp
    tmp=$(mktemp)
    while IFS= read -r line; do
        [[ "$line" == *"$file"* ]] && continue
        echo "$line" >> "$tmp"
    done < "$INDEX_FILE"
    mv "$tmp" "$INDEX_FILE"
}

# ── commands ─────────────────────────────────────────────────────────

cmd_flush() {
    local source="${1:?Usage: flush <source> <content> [tags]}"
    local content="${2:?Usage: flush <source> <content> [tags]}"
    local tags="${3:-general}"

    local slug
    slug=$(slugify "$content")
    local filename="${DATE}-${slug}.md"
    local filepath="$VAULT_DIR/$filename"

    # Avoid duplicates — append counter if file exists
    local counter=1
    while [[ -f "$filepath" ]]; do
        filename="${DATE}-${slug}-${counter}.md"
        filepath="$VAULT_DIR/$filename"
        (( counter++ ))
    done

    # Write entry
    cat > "$filepath" << ENTRY
# $(echo "$content" | head -c 80)

- **Source:** $source
- **Archived:** $DATETIME
- **Tags:** $tags

---

$content
ENTRY

    # Update index
    local summary
    summary=$(echo "$content" | head -c 40)
    index_add "$DATE" "$source" "$summary" "$tags" "$filename"

    echo "Archived → $filename"
}

cmd_list() {
    echo "=== Memory Archive ==="
    echo ""
    cat "$INDEX_FILE"
    echo ""
    echo "---"
    local count
    count=$(find "$VAULT_DIR" -maxdepth 1 -name '*.md' ! -name 'INDEX.md' | wc -l)
    local size
    size=$(du -sh "$VAULT_DIR" | awk '{print $1}')
    echo "Entries: $count  |  Size: $size"
}

cmd_search() {
    local query="${1:?Usage: search <query>}"
    echo "Search: \"$query\""
    echo ""
    local found=0
    for f in "$VAULT_DIR"/*.md; do
        [[ "$f" == "$INDEX_FILE" ]] && continue
        [[ -f "$f" ]] || continue
        if grep -qi "$query" "$f"; then
            found=1
            echo "=== $(basename "$f") ==="
            grep -n -i --color=never "$query" "$f" | head -5
            echo ""
        fi
    done
    (( found == 0 )) && echo "(no matches)"
}

cmd_get() {
    local input="${1:?Usage: get <filename>}"
    local filepath
    # Accept basename or full path
    if [[ "$input" == /* ]]; then
        filepath="$input"
    else
        filepath="$VAULT_DIR/$input"
    fi
    if [[ -f "$filepath" ]]; then
        cat "$filepath"
    else
        echo "Not found: $input"
        echo ""
        echo "Available:"
        find "$VAULT_DIR" -maxdepth 1 -name '*.md' ! -name 'INDEX.md' -printf '  %f\n' | sort
        exit 1
    fi
}

cmd_delete() {
    local input="${1:?Usage: delete <filename>}"
    local filepath
    if [[ "$input" == /* ]]; then
        filepath="$input"
    else
        filepath="$VAULT_DIR/$input"
    fi
    if [[ -f "$filepath" ]]; then
        rm "$filepath"
        index_remove "$(basename "$filepath")"
        echo "Deleted: $(basename "$filepath")"
    else
        echo "Not found: $input"
        exit 1
    fi
}

cmd_status() {
    local count
    count=$(find "$VAULT_DIR" -maxdepth 1 -name '*.md' ! -name 'INDEX.md' | wc -l)
    local size
    size=$(du -sh "$VAULT_DIR" | awk '{print $1}')
    echo "=== Memory Archive ==="
    echo "Entries:   $count"
    echo "Size:      $size"
    echo "Location:  $VAULT_DIR"
    echo ""
    if (( count > 0 )); then
        echo "By source:"
        grep -h '^\- \*\*Source:' "$VAULT_DIR"/*.md 2>/dev/null \
            | sed 's/.*Source:\*\* *//' | sort | uniq -c | sort -rn \
            | awk '{printf "  %s  (%s)\n", $2, $1}'
        echo ""
        echo "Latest:"
        find "$VAULT_DIR" -maxdepth 1 -name '*.md' ! -name 'INDEX.md' -printf '  %T+  %f\n' \
            | sort -r | head -5
    fi
}

# ── main ─────────────────────────────────────────────────────────────

case "${1:-}" in
    flush)  shift; cmd_flush  "$@" ;;
    list)   cmd_list ;;
    search) shift; cmd_search "$@" ;;
    get)    shift; cmd_get    "$@" ;;
    delete) shift; cmd_delete "$@" ;;
    status) cmd_status ;;
    *)
        echo "Usage: $0 {flush|list|search|get|delete|status}"
        exit 1
        ;;
esac
