# Hunger Settings — Konfigurasi Sistem Lapar di Minecraft

Cara mengatur dan troubleshooting sistem hunger/lapar di Minecraft server (Java & Bedrock).

## Prasyarat: Difficulty ≠ Peaceful

Di Peaceful, pemain **tidak akan lapar sama sekali**. Harus easy/normal/hard:

```
/difficulty easy
/difficulty normal
/difficulty hard
```

Atau di `server.properties`:
```properties
difficulty=normal
```

Lalu restart server.

## Gamerule Terkait

```
/gamerule naturalRegeneration true
```

Jika `false`, pemain tetap lapar tapi **tidak bisa regen darah alami**. Tidak ada gamerule khusus untuk mematikan hunger.

## Plugin yang Mempengaruhi Hunger

### EssentialsX

Config `config.yml`:
```yaml
disable-hunger-loss: false
```

Command toggle:
```
/essentials toggle hunger
```

### WorldGuard

Cek flag region:
```
/rg flag __global__ hunger deny   # Matikan hunger global
/rg flag __global__ hunger allow  # Nyalakan hunger global
```

Hunger flag `deny` = hunger tidak berkurang di region tersebut.

### Plugin RPG/Survival Lainnya

Plugin seperti **Tough As Nails**, **Diet**, **Scaling Health** bisa memodifikasi hunger. Cek file di `config/` folder.

## Testing Hunger

1. Masuk **Survival mode**
2. Sprint + lompat selama ~1 menit
3. Food bar harus berkurang

## Mempercepat Hunger (Opsional)

Vanilla tidak bisa mengatur kecepatan lapar. Alternatif:

### Command Repeat
```
/effect give @a hunger 5 1 true
```
Efek `hunger` menambah laju pengurangan food bar.

### Plugin Custom
Bisa buat plugin yang memodifikasi `FoodLevelChangeEvent` di Bukkit API.

### Denizen Script
```yaml
on player sprints:
    - adjust <player> food -1
```

## Troubleshooting

### Hunger tidak berkurang

1. Cek difficulty (`/difficulty`) — bukan peaceful?
2. Cek EssentialsX: `disable-hunger-loss: false`
3. Cek WorldGuard: `/rg info` di lokasi player
4. Cek plugin lain: `/plugins` lalu cek config masing-masing
5. Cek gamerule: pastikan tidak ada plugin yang memodifikasi

## Related

- [[server/server-properties]] — Konfigurasi server.properties
- [[gameplay/health-system]] — Sistem darah/HP di Minecraft
- [[gameplay/denizen-basics]] — Scripting dengan Denizen
- [[plugin/scoreboard-custom]] — Custom scoreboard
