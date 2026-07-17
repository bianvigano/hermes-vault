# Health System — Menambah Heart/HP di Minecraft

Cara menambah heart (nyawa) di Minecraft vanilla menggunakan command `/attribute` dan efek potion.

## Vanilla Minecraft — Heart Tambahan

Minecraft vanilla tidak punya "darah" (blood effect). Yang tersedia: partikel damage abu-abu/merah kecoklatan, animasi mob kedip merah. Untuk efek darah realistik butuh mod seperti **Blood Particles Mod** atau **Realistic Blood Mod**.

## Menambah Maksimum Heart (Permanen)

```
/attribute @p minecraft:generic.max_health base set 40
```

| Nilai | Heart | Notes |
|-------|-------|-------|
| 20 | 10 ❤️ | Default |
| 40 | 20 ❤️ | 2x |
| 60 | 30 ❤️ | 3x |
| 100 | 50 ❤️ | 5x |

Setelah command, isi HP:
```
/effect give @p minecraft:instant_health 1 10
```

## Balik Normal

```
/attribute @p minecraft:generic.max_health base set 20
```

## Heart Sementara (Health Boost)

```
/effect give @p minecraft:health_boost 99999 4 true
```

- Level 4 = +10 heart
- Hilang saat mati atau efek habis
- `true` = sembunyikan partikel

## Target Selectors

| Selector | Target |
|----------|--------|
| `@p` | Player terdekat |
| `@a` | Semua player |
| `@s` | Diri sendiri (command block/entity) |
| `@r` | Player random |

## Via Command Block

Untuk permanent di server via command block:
1. `/give @p command_block`
2. Isi dengan command di atas
3. Set ke **Repeat** + **Always Active** (untuk auto apply)

## Plugin Approach (Java)

```java
Player player = ...;
player.getAttribute(Attribute.GENERIC_MAX_HEALTH).setBaseValue(40.0);
player.setHealth(40.0);
```

## Mod Darah (Blood)

Mod populer untuk efek darah realistik:
- **Blood Particles Mod** (Forge/Fabric)
- **Realistic Blood Mod**
- **Combat Effects Mod**

Cocok untuk server PvP atau RPG.

## Related

- [[gameplay/hunger-settings]] — Konfigurasi lapar
- [[gameplay/daylight-cycle]] — Waktu siang terus
- [[gameplay/denizen-basics]] — Scripting Denizen
- [[server/server-properties]] — difficulty & gamemode
