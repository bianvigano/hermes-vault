# Denizen — Minecraft Scripting Engine

Denizen adalah plugin scripting powerful untuk Minecraft. Bisa bikin quest, NPC interaktif, command custom, animasi, sistem RPG, dan banyak lagi — tanpa perlu coding Java.

**Website**: https://denizenscript.com/
**Docs**: https://guide.denizenscript.com/

---

## Command Dasar

### Set Waktu (Time)
```yaml
- time 0 world:<player.world>      # 0 = pagi
- time 6000 world:<player.world>   # 6000 = siang
- time 12000 world:<player.world>  # 12000 = malam
- time 18000 world:<player.world>  # 18000 = tengah malam
```

### Wait / Delay
```yaml
- wait 10s    # 10 detik
- wait 5m     # 5 menit
- wait 1h     # 1 jam
```

### Execute Command Server
```yaml
- execute as_server "worldborder set 500"
```

### Title
```yaml
- title "title:&aPERMAINAN DIMULAI|subtitle:Semoga beruntung!|stay:60"
```

### Sound
```yaml
- playsound ENTITY_WITHER_SPAWN targets:<server.online_players>
```

### Actionbar (animasi)
```yaml
- actionbar "<green>Welcome!" targets:<player>
```

---

## Conditional Logic (if/else if/else)

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
```

## Loop + Animasi

### Rainbow Text (Moving Gradient)
```yaml
rainbow_moving:
  type: task
  script:
  - define text "WELCOME SERVER"
  - define colors li@red|gold|yellow|green|aqua|blue|light_purple
  - define shift 0
  - while true:
      - define output ""
      - foreach <def[text].to_list>:
          - define index <[loop_index].add[<def[shift]>].mod[<def[colors].size>]>
          - define color <def[colors].get[<def[index].add[1]>]>
          - define output "<def[output]><&[<def[color]>]><def[value]>"
      - actionbar "<def[output]>" targets:<player>
      - define shift <def[shift].add[1]>
      - wait 2t
```

### RGB Smooth Gradient Command
```yaml
rgbtext_command:
  type: command
  name: rgbtext
  description: RGB gradient animated text
  usage: /rgbtext <text>
  script:
  - define text "<context.args.join[ ]>"
  - run rgbtext_task def:<player>|<def[text]>
```

## Battle Royale (WorldBorder Timeline)

Denizen tidak punya `timeline:` seperti plugin YAML lain. Pakai `wait` + `execute as_server`:

```yaml
battle_royale_border:
  type: task
  script:
  # Start
  - execute as_server "worldborder set 500"
  - narrate "&aGame dimulai! Border: 500" targets:<server.online_players>
  
  # 10 menit
  - wait 10m
  - execute as_server "worldborder set 300 120"
  - title "title:&eBorder mengecil!|subtitle:Menuju 300" targets:<server.online_players>
  
  # 20 menit
  - wait 10m
  - execute as_server "worldborder set 150 120"
  - title "title:&6Zona semakin kecil!|subtitle:Menuju 150" targets:<server.online_players>
  
  # Final
  - wait 10m
  - execute as_server "worldborder set 50 120"
  - title "title:&4Fase akhir!|subtitle:Menuju 50" targets:<server.online_players>
```

## Variabel Umum

| Tag | Keterangan |
|-----|-----------|
| `<player.world.name>` | Nama world |
| `<player.flag[nama]>` | Flag pemain |
| `<player.health>` | HP saat ini |
| `<player.level>` | XP level |
| `<player.inventory.contains[item]>` | Cek item |
| `<server.online_players>` | Semua player online |

## Pitfall

- Tidak ada `timeline:` built-in — pakai `wait` + `execute as_server`
- `worldborder` harus via `execute as_server`, bukan dipanggil langsung
- Flag harus di-set dulu sebelum dicek
- Warna format: `&a` (bukan `<green>`), kecuali di narrate/actionbar
- Animasi terlalu banyak bisa bikin server lag

## Related

- [[minecraft/tools/chunky]] — Pre-generate chunk sebelum event
- [[minecraft/server/gamerules]] — Gamerule untuk game mode
- [[minecraft/server/minecraft-docker]] — Docker server setup
- [[minecraft/plugin/luckperms]] — Permission integration
