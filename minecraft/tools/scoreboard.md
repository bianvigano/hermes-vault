# Scoreboard — Membuat dan Menyembunyikan Angka di Sidebar

Panduan membuat scoreboard sidebar di Bukkit/Spigot/Paper/Purpur, termasuk cara menyembunyikan angka merah di sebelah kanan.

## Apa Itu Scoreboard?

Scoreboard adalah fitur Minecraft untuk menampilkan informasi di sidebar, di atas kepala player (nametag), atau di tab list. Di plugin Bukkit/Spigot, biasanya dibuat dengan `ScoreboardManager` dan `Objective`.

## Membuat Scoreboard Dasar

```java
ScoreboardManager manager = Bukkit.getScoreboardManager();
Scoreboard board = manager.getNewScoreboard();

Objective obj = board.registerNewObjective("event", "dummy",
        ChatColor.translateAlternateColorCodes('&', "&a&lOne Chunk Event"));
obj.setDisplaySlot(DisplaySlot.SIDEBAR);

// Tambah baris
obj.getScore("&ePlayer: &fSteve").setScore(1);
obj.getScore("&eScore: &f100").setScore(2);

player.setScoreboard(board);
```

## Masalah Angka Merah di Kanan

Secara default, sidebar scoreboard selalu menampilkan angka di sebelah kanan setiap baris. Ini adalah **hardcoded behavior** dari Minecraft — API Bukkit/Spigot tidak punya method resmi untuk menyembunyikannya.

## Cara Menyembunyikan Angka

### Metode 1: Semua Score = 0 (Simplest)

```java
obj.getScore(line).setScore(0);
```

Kalau semua score bernilai 0, Minecraft biasanya tidak menampilkan angka. Tapi hasilnya tidak 100% konsisten di semua versi.

### Metode 2: Team + Dummy Entry (Recommended)

Gunakan entry invisible sebagai placeholder, lalu letakkan teks di prefix/suffix team:

```java
int score = lines.size();

for (int i = 0; i < lines.size(); i++) {
    String line = lines.get(i);

    // Entry invisible unik
    String entry = ChatColor.values()[i].toString();

    Team team = board.registerNewTeam("line_" + i);
    team.addEntry(entry);

    if (line.length() <= 16) {
        team.setPrefix(line);
    } else {
        team.setPrefix(line.substring(0, 16));
        team.setSuffix(line.substring(16, Math.min(line.length(), 32)));
    }

    obj.getScore(entry).setScore(score--);
}
```

**Cara kerja**:
- Entry scoreboard adalah string invisible (kode warna)
- Teks asli diletakkan di `team.setPrefix()` dan `team.setSuffix()`
- Angka score tetap ada secara teknis, tapi tidak terlihat karena entry-nya invisible

### Metode 3: Config Toggle

Tambahkan di `config.yml`:

```yaml
scoreboard:
  enable: true
  enable-nametag-color: true
  hide-numbers: true
  title: "&a&lOne Chunk Event"
  show-players-limit: 5
  lines:
    - " "
    - "%auto_teams%"
```

Lalu di kode Java:

```java
boolean hideNumbers = getConfig().getBoolean("scoreboard.hide-numbers", true);

if (hideNumbers) {
    // Gunakan metode Team + invisible entry
} else {
    // Tampilkan angka normal
}
```

## Full Method Contoh

```java
public void setupScoreboard(Player player) {
    if (!getConfig().getBoolean("scoreboard.enable", true)) return;

    ScoreboardManager manager = Bukkit.getScoreboardManager();
    if (manager == null) return;

    Scoreboard board = manager.getNewScoreboard();

    // Setup nametag color
    if (getConfig().getBoolean("scoreboard.enable-nametag-color", true)) {
        for (String teamKey : teams.keySet()) {
            Team team = board.registerNewTeam(teamKey);
            String colorCode = getConfig().getString("teams." + teamKey + ".color", "&f");
            ChatColor chatColor = ChatColor.WHITE;

            if (colorCode.length() >= 2) {
                ChatColor cc = ChatColor.getByChar(colorCode.charAt(1));
                if (cc != null) chatColor = cc;
            }

            team.setColor(chatColor);

            for (UUID id : teams.get(teamKey)) {
                Player p = Bukkit.getPlayer(id);
                if (p != null) team.addEntry(p.getName());
            }
        }
    }

    // Create objective
    String title = ChatColor.translateAlternateColorCodes('&',
            getConfig().getString("scoreboard.title", "&a&lOne Chunk Event"));

    Objective obj = board.registerNewObjective("event", "dummy", title);
    obj.setDisplaySlot(DisplaySlot.SIDEBAR);

    boolean hideNumbers = getConfig().getBoolean("scoreboard.hide-numbers", true);

    // Build lines
    List<String> lines = new ArrayList<>();
    List<String> configLines = getConfig().getStringList("scoreboard.lines");

    if (configLines.isEmpty()) {
        configLines = Arrays.asList(" ", "%auto_teams%");
    }

    int limit = getConfig().getInt("scoreboard.show-players-limit", 5);

    for (String line : configLines) {
        if (line.equalsIgnoreCase("%auto_teams%")) {
            for (String teamKey : teams.keySet()) {
                String displayName = getConfig().getString(
                        "teams." + teamKey + ".display-name", teamKey);
                String color = getConfig().getString(
                        "teams." + teamKey + ".color", "&f");

                lines.add(ChatColor.translateAlternateColorCodes('&',
                        displayName + " Remaining: " + teams.get(teamKey).size()));

                if (teams.get(teamKey).size() <= limit) {
                    for (UUID uuid : teams.get(teamKey)) {
                        Player p = Bukkit.getPlayer(uuid);
                        if (p != null) {
                            lines.add(ChatColor.translateAlternateColorCodes('&',
                                    color + " " + p.getName()));
                        }
                    }
                }
                lines.add(" ");
            }
            continue;
        }

        // Placeholder replace
        String formatted = line;
        for (String teamKey : teams.keySet()) {
            formatted = formatted
                    .replace("%" + teamKey + "_count%",
                            String.valueOf(teams.get(teamKey).size()))
                    .replace("%" + teamKey + "_name%",
                            ChatColor.translateAlternateColorCodes('&',
                                    getConfig().getString(
                                            "teams." + teamKey + ".display-name",
                                            teamKey)));
        }

        lines.add(ChatColor.translateAlternateColorCodes('&', formatted));
    }

    // Apply lines
    int score = lines.size();
    Set<String> used = new HashSet<>();

    for (int i = 0; i < lines.size(); i++) {
        String line = lines.get(i);

        // Prevent duplicate line crash
        while (used.contains(line)) {
            line += ChatColor.RESET;
        }
        used.add(line);

        if (hideNumbers) {
            String entry = ChatColor.values()[i].toString();

            Team lineTeam = board.registerNewTeam("line_" + i);
            lineTeam.addEntry(entry);

            if (line.length() <= 16) {
                lineTeam.setPrefix(line);
            } else {
                lineTeam.setPrefix(line.substring(0, 16));
                lineTeam.setSuffix(line.substring(16, Math.min(line.length(), 32)));
            }

            obj.getScore(entry).setScore(score--);
        } else {
            obj.getScore(line).setScore(score--);
        }
    }

    player.setScoreboard(board);
}
```

## Batasan Penting

| Versi | Bisa Hilang Total? | Catatan |
|-------|-------------------|---------|
| 1.8 - 1.12 | ❌ Tidak | Angka selalu muncul |
| 1.13 - 1.19 | ⚠️ Hampir tidak terlihat | Team trick berfungsi baik |
| 1.20+ | ✅ Lebih baik | Beberapa metode baru tersedia |
| 1.20.3+ | ✅ Native support | Bisa hide numbers via packet |

Untuk hasil 100% tanpa angka di semua versi, diperlukan packet manipulation (NMS/ProtocolLib).

## Best Practices 2024-2025

- **Jangan update scoreboard tiap tick** — bikin flicker dan lag. Update hanya saat data berubah.
- **Gunakan scheduler** untuk update periodik (misal setiap 1-2 detik), bukan setiap tick.
- **Anti-flicker**: Jangan recreate scoreboard setiap update. Update score yang sudah ada.
- **Limit lines**: Sidebar hanya menampilkan maksimal 15 baris. Lebih dari itu akan terpotong.
- **Unique entries**: Setiap baris harus memiliki entry unik. Kalau ada duplikat, scoreboard akan crash.
- **Async tidak aman**: Semua operasi scoreboard harus di main thread Bukkit.

## Troubleshooting

### Scoreboard tidak muncul

- Pastikan `obj.setDisplaySlot(DisplaySlot.SIDEBAR)` sudah dijalankan
- Pastikan player sudah di-set scoreboard: `player.setScoreboard(board)`
- Cek apakah plugin lain meng-override scoreboard player

### Angka masih muncul setelah hide-numbers

- Pastikan semua score diset ke 0 atau pakai metode Team
- Cek versi Minecraft — 1.8 beda behavior
- Kalau pakai metode setScore(0), beberapa client masih menampilkan angka kecil

### Duplicate line crash

- Setiap baris harus unik. Tambahkan `ChatColor.RESET` atau kode warna unik untuk membuat beda.

### Flicker / Berkedip

- Jangan recreate scoreboard setiap update
- Update nilai score yang sudah ada dengan `obj.getScore(entry).setScore(newScore)`

## Related

- [[minecraft/server/purpur-config]] — Konfigurasi Purpur server
- [[minecraft/server/server-properties]] — Konfigurasi server.properties
- [[minecraft/tools/chunky]] — Pre-generate chunk (performa server)
- [[minecraft/server/minecraft-docker]] — Setup server via Docker
