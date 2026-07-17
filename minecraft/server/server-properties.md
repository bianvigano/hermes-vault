# Server Properties — Konfigurasi Dasar Minecraft Server

File `server.properties` adalah file konfigurasi utama semua Minecraft server (Vanilla, Bukkit, Spigot, Paper, Purpur, Fabric, Forge, NeoForge). Mengontrol semua pengaturan dasar dunia dan gameplay.

## Lokasi File

```
/server.properties
```

File dibuat otomatis saat server pertama kali dijalankan. Edit saat server mati, lalu restart.

## Pengaturan Esensial

### Difficulty & Gamemode

```properties
difficulty=normal        # peaceful / easy / normal / hard
gamemode=survival        # survival / creative / adventure / spectator
hardcore=false           # true: pemain jadi spectator saat mati
force-gamemode=false     # true: paksa gamemode setiap login
```

### World & Seed

```properties
level-seed=              # Kosongkan untuk seed random
level-name=world         # Nama folder world
max-world-size=29999984  # Batas radius world (blok), default 30 juta
```

`max-world-size` adalah radius (bukan diameter). Nilai default 29999984 = world ~60 juta blok diameter. Kecilkan untuk server survival kecil (misal 5000 = 10K×10K blok). Tidak memotong world yang sudah ada — perlu world baru untuk efek penuh.

### Spawn Settings

```properties
spawn-protection=0       # Radius proteksi spawn (0 = tidak ada)
spawn-radius=0           # Radius penyebaran spawn (0 = tepat di titik)
```

`spawn-protection` bukan lokasi spawn, tapi radius blok di sekitar spawn yang hanya bisa diedit OP. Lokasi spawn diatur dengan command `/setworldspawn`.

### Network & Performance

```properties
view-distance=10          # Jarak pandang server-side (chunk), beban CPU
simulation-distance=10    # Jarak simulasi entitas
max-players=20            # Maksimum pemain
online-mode=true          # false = cracked server (tidak disarankan)
allow-flight=false        # true = izinkan terbang tanpa creative
```

### PvP & Player

```properties
pvp=true                  # true: pemain bisa saling bunuh
player-idle-timeout=0     # Menit sebelum kick idle (0 = tidak ada)
enable-command-block=false # true: izinkan command block
```

## Gamerules Penting

Diset via command, bukan `server.properties`:

```
/gamerule doDaylightCycle false   # Hentikan siklus siang-malam
/gamerule spawnRadius 0           # Spawn tepat di titik (no spread)
/gamerule naturalRegeneration true # Regenerasi darah alami
/gamerule keepInventory true      # Simpan inventory saat mati
```

## Format UI (React/Vue/JS)

Untuk dashboard server panel, representasi JavaScript:

```js
const fields = {
    "allow-flight": { type: "select", label: "Allow flight", options: ["true", "false"], tip: "Allow flight on the server." },
    "difficulty": { type: "select", label: "Difficulty", options: ["peaceful", "easy", "normal", "hard"], tip: "Sets the difficulty for the server." },
    "enable-command-block": { type: "select", label: "Enable command blocks", options: ["true", "false"], tip: "Allow access to command blocks." },
    "force-gamemode": { type: "select", label: "Force game mode", options: ["true", "false"], tip: "Forces everyone into the game mode every time they log on." },
    "gamemode": { type: "select", label: "Game mode", options: ["survival", "creative", "adventure", "spectator"], tip: "Sets the default game mode on the server." },
    "hardcore": { type: "select", label: "Hardcore mode", options: ["true", "false"], tip: "Enables hardcore mode." },
    "player-idle-timeout": { type: "number", label: "Player idle timeout", tip: "Minutes before idle kick. 0 = never." },
    "pvp": { type: "select", label: "PvP", options: ["true", "false"], tip: "Toggles PvP." },
    "view-distance": { type: "number", label: "View distance", tip: "Server-side viewing distance.", tipMore: "Higher values increase CPU and RAM usage." }
};
```

## Catatan Penting

- Order baris di `server.properties` tidak penting
- Edit saat server OFF, lalu restart
- Bed respawn behavior adalah vanilla default: player tidur di bed → spawn pindah ke bed (khusus player itu). Bed hancur → balik world spawn. Tidak ada setting `server.properties` untuk ini.
- Plugin bisa override banyak setting di atas

## Related

- [[server/spawn-commands]] — Command set spawn dunia & player
- [[gameplay/daylight-cycle]] — Cara set siang terus
- [[gameplay/hunger-settings]] — Konfigurasi lapar/hunger
- [[troubleshooting/connection-throttled]] — Ganti pesan Purpur/Spigot
- [[server/minecraft-docker]] — Setup server via Docker
- [[server/docker-compose-8gb]] — Docker Compose untuk 8GB RAM
- [[wiki/minecraft-servers]] — Info server aktif
