# Denizen Scripting — Dasar If, Waktu, dan Worldborder

Denizen adalah plugin scripting untuk Minecraft server (Spigot/Paper). Menggunakan YAML-based scripting language dengan tag system.

## Instalasi

1. Download Denizen dari SpigotMC atau GitHub
2. Taruh `.jar` di folder `plugins/`
3. Restart server
4. File script ditaruh di `plugins/Denizen/scripts/`

## Struktur Script Denizen

```yaml
nama_script:
  type: command
  name: namacommand
  script:
  - narrate "Halo!"
```

## If Statement

```yaml
example_command:
  type: command
  name: cekumur
  script:
  - if <player.flag[umur]> >= 18:
      - narrate "Kamu sudah dewasa."
    else:
      - narrate "Kamu masih di bawah umur."
```

If sederhana:
```yaml
test_if:
  type: task
  script:
  - if <player.health> < 10:
      - narrate "HP kamu rendah!"
```

## If Kompleks (Daily Reward)

```yaml
daily_reward:
  type: command
  name: daily
  script:
  - if <player.has_flag[daily_claimed]>:
      - narrate "<red>Kamu sudah mengambil reward hari ini!"
      - stop

  - if <player.world.name> == world_nether:
      - narrate "<red>Reward tidak bisa diambil di Nether!"
      - stop

  - if <player.inventory.contains[diamond]>:
      - give money quantity:500
      - narrate "<green>Kamu mendapatkan 500 coins!"
    else if <player.level> >= 30:
      - give money quantity:300
      - narrate "<yellow>Kamu mendapatkan 300 coins!"
    else:
      - give money quantity:100
      - narrate "<gray>Kamu mendapatkan 100 coins."

  - flag player daily_claimed duration:1d
  - narrate "<aqua>Reward harian berhasil diambil!"
```

## Mengatur Waktu Dunia

```denizen
# Set waktu ke siang
- time 6000 world:<player.world>
```

Nilai waktu:
- `0` = pagi (sunrise)
- `6000` = siang
- `12000` = malam
- `18000` = tengah malam

## Timer / Delay

```denizen
- narrate "Mulai"
- wait 10s
- narrate "10 detik sudah lewat"
```

## Loop

```denizen
- repeat 5:
    - narrate "Loop <[value]>"
    - wait 5s
```

## Worldborder

Format command:
```denizen
- execute as_server "worldborder set 500"
- execute as_server "worldborder set 100 60"     # mengecil ke 100 selama 60 detik
- execute as_server "worldborder center 0 0"
```

## Battle Royale Shrinking Border

```denizen
battle_royale_border:
  type: task
  script:
  - execute as_server "worldborder set 500"
  - narrate "&aGame dimulai! Border: 500" targets:<server.online_players>

  - wait 10m
  - execute as_server "worldborder set 300 120"
  - title "title:&eBorder mengecil!|subtitle:Menuju 300" targets:<server.online_players>

  - wait 10m
  - execute as_server "worldborder set 150 120"
  - title "title:&6Zona semakin kecil!|subtitle:Menuju 150" targets:<server.online_players>

  - wait 10m
  - execute as_server "worldborder set 50 120"
  - title "title:&cFase akhir!|subtitle:Menuju 50" targets:<server.online_players>

  - wait 5m
  - execute as_server "worldborder set 20 60"
  - title "title:&4FINAL BORDER!|subtitle:Fight!" targets:<server.online_players>
```

Jalankan dengan:
```denizen
- run battle_royale_border
```

## Denizen vs JavaScript

Logika Denizen daily reward di JS:
```javascript
function dailyReward(player) {
    if (player.flags.daily_claimed) {
        console.log("Kamu sudah mengambil reward hari ini!");
        return;
    }
    if (player.world === "world_nether") {
        console.log("Reward tidak bisa diambil di Nether!");
        return;
    }
    if (player.inventory.includes("diamond")) {
        player.money += 500;
    } else if (player.level >= 30) {
        player.money += 300;
    } else {
        player.money += 100;
    }
    player.flags.daily_claimed = true;
}
```

## Related

- [[gameplay/daylight-cycle]] — Set siang terus
- [[plugin/regen-regions]] — Plugin regenerasi blok
- [[plugin/scoreboard-custom]] — Custom scoreboard
- [[plugin/minimessage-format]] — Format MiniMessage
