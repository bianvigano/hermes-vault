# Server Types — Plugin vs Mod vs Hybrid

Panduan memilih tipe server Minecraft: plugin saja, mod saja, atau hybrid (plugin + mod).

## Plugin Only (Stabil & Populer)

### Paper / Spigot / Bukkit / Purpur

- **Bisa**: Plugin (EssentialsX, LuckPerms, WorldEdit, WorldGuard)
- **Tidak bisa**: Mod Forge/Fabric
- **Cocok**: Survival, SMP, minigame, roleplay

**Rekomendasi**: PaperMC — fork Spigot, lebih cepat & stabil.
Download: https://papermc.io

## Mod Only

### Forge
- Mod besar & kompleks
- Cocok: modpack berat, Create, Pixelmon

### Fabric
- Ringan & cepat
- Cocok: vanilla+, performance mods (Lithium, Sodium)

## Hybrid (Plugin + Mod)

| Server | Basis | Stabilitas |
|--------|-------|------------|
| Mohist | Forge + Spigot | Sedang |
| Arclight | Forge + Bukkit | Sedang-Tinggi |
| Cardboard | Fabric + Bukkit API | Rendah (masih alpha) |
| Magma | Forge + Bukkit | Rendah |
| SpongeForge | Forge + Sponge plugins | Tinggi (plugin beda) |

### Cardboard

Fabric mod + Bukkit plugin. Versi yang didukung:
- 1.16.4 – 1.16.5
- 1.17.1
- 1.18.x
- 1.19.2 – 1.19.4
- 1.20.x
- 1.21.x

**Tidak ada Cardboard untuk 1.8.8** — Fabric sendiri baru muncul 1.14+.

Status: masih alpha. Tidak semua plugin Bukkit kompatibel.

### Mohist / Arclight

Rekomendasi untuk hybrid Forge + Bukkit. Mohist 1.12.2 paling stabil untuk versi lama.

## Versi Lama (1.8.8)

Untuk 1.8.8:
- Plugin: **Spigot/Paper 1.8.8** ← paling stabil
- Mod: **Forge 1.8.8**
- Hybrid: **Tidak ada yang stabil**

Opsi proxy (paling aman untuk mod + plugin di 1.8.8):
```
BungeeCord/Velocity
  ├── Server 1: Spigot 1.8.8 (plugin — lobby, auth)
  └── Server 2: Forge 1.8.8 (modpack)
```

## Rekomendasi Cepat

| Kebutuhan | Pilih |
|-----------|-------|
| Plugin saja | **Paper** |
| Mod saja | **Forge / Fabric** |
| Plugin + Mod | **Mohist / Arclight** (modern), **SpongeForge** (1.8.9) |
| Mod + Plugin terpisah | **Proxy (Bungee/Velocity)** |

## Related

- [[server/minecraft-docker]] — Setup via Docker
- [[troubleshooting/cardboard-error]] — Fix Cardboard version
- [[modding/fabric-mods]] — Mod Fabric
- [[server/velocity-proxy]] — Setup Velocity proxy
