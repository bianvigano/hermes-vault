# Minecraft Commands — Heart, Attribute, Totem Effects

Kumpulan command Minecraft vanilla untuk atribut pemain, heart (max_health), dan trik meniru efek Totem.

---

## Tambah Heart (max_health)

### Permanen (attribute)
```
/attribute @p minecraft:generic.max_health base set 40
```

- Default: 20 (10 heart)
- `40` = 20 heart
- `60` = 30 heart

### Isi ulang setelah set (biar ga mati instan)
```
/effect give @p minecraft:instant_health 1 10
```

### Balikin normal
```
/attribute @p minecraft:generic.max_health base set 20
```

### Sementara (potion)
```
/effect give @p minecraft:health_boost 99999 4 true
```

- Level 4 = +10 heart
- Hilang kalau mati/efek habis

### Command Block otomatis (Repeat + Always Active)
```
/attribute @a minecraft:generic.max_health base set 40
```

---

## Custom Food dengan Efek (NBT)

```
/give @p minecraft:apple{
  Food:{
    Nutrition:4,
    Saturation:2.4,
    Effects:[
      {EffectId:10,Duration:200,Amplifier:1},
      {EffectId:22,Duration:200,Amplifier:0}
    ]
  }
} 1
```

Effect ID:
- `10` = Regeneration
- `22` = Absorption
- `5` = Strength
- `12` = Fire Resistance

---

## Trik Totem Effect (Vanilla, pakai Command Block)

Totem tidak bisa disalin langsung — effect Totem adalah hardcoded mechanic, BUKAN potion effect. Tapi bisa ditiru 99%:

### Deteksi HP kritis → beri regen
```
/execute as @a if entity @s[nbt={Health:1.0f}] run effect give @s minecraft:regeneration 5 3 true
/execute as @a if entity @s[nbt={Health:1.0f}] run effect give @s minecraft:absorption 5 1 true
/execute as @a if entity @s[nbt={Health:1.0f}] run effect give @s minecraft:fire_resistance 5 0 true
```

### Khusus pegang item tertentu
```
/execute as @a[nbt={SelectedItem:{id:"minecraft:diamond_sword"}}] if entity @s[nbt={Health:1.0f}] run effect give @s minecraft:regeneration 5 3 true
```

### Item sekali pakai (hilang setelah trigger)
```
/execute as @a if entity @s[nbt={Health:1.0f}] run clear @s minecraft:stick 1
```

---

## Particle Darah (Red Dust)
```
/particle minecraft:dust 1 0 0 1 ~ ~1 ~ 0 0 0 0.1 20
```

Tidak otomatis — harus dipanggil via command block atau datapack.

---

## Ringkasan

| Cara | Permanen | Vanilla |
|------|----------|---------|
| Attribute | ✅ | ✅ |
| Health Boost | ❌ | ✅ |
| Command Block | ✅ | ✅ |
| Food + Effect | ❌ | ✅ |
| Mod | ✅ | ❌ |

## Related

- [[minecraft/server/gamerules]] — Gamerule untuk gameplay
- [[minecraft/tools/scoreboard]] — Scoreboard + health display
- [[minecraft/plugin/denizen-scripting]] — Otomatisasi dengan Denizen
- [[minecraft/server/minecraft-docker]] — Docker server setup
