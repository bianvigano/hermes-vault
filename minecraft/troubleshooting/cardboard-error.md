# Cardboard Error — Fix Version Mismatch di Modrinth

Error saat menginstal Cardboard via Modrinth/mc-image-helper dari itzg/minecraft-server:
```
[mc-image-helper] ERROR: Invalid parameter provided for 'modrinth' command:
No candidate versions of 'Cardboard' [1.21.11-7=alpha, 1.21.11-6=alpha] matched versionType=release
```

## Penyebab

Installer (`mc-image-helper`) minta **release build**, tapi Cardboard hanya punya **alpha build** untuk versi Minecraft yang ditargetkan. Modrinth mengkategorikan versi jadi 3 jenis:

| Type | Deskripsi | Stabilitas |
|------|-----------|------------|
| `release` | Build stabil, siap produksi | Tinggi |
| `beta` | Fitur baru, testing | Sedang |
| `alpha` | Development awal | Rendah |

Cardboard banyak versi hanya tersedia sebagai alpha karena project masih aktif dikembangkan.

## Tentang Cardboard

Cardboard adalah mod Fabric/Paper hybrid yang memungkinkan **plugin Bukkit/Spigot/Paper berjalan di server Fabric/Quilt**. Berguna kalau ingin pakai mod Fabric tapi tetap butuh plugin seperti EssentialsX, LuckPerms, dll.

Website: https://cardboardpowered.org/
Modrinth: https://modrinth.com/mod/cardboard

## Solusi

### Opsi 1: Izinkan Alpha Versions (di Docker itzg)

Di `docker-compose.yml`, tambahkan/modifikasi environment:
```yaml
MODRINTH_VERSION_TYPE: alpha
```

Atau kalau pakai `MODRINTH_PROJECTS`:
```yaml
MODRINTH_PROJECTS: |
  cardboard:alpha
```

### Opsi 2: Gunakan Versi Minecraft yang Punya Release Stable

Cek https://modrinth.com/mod/cardboard/versions — filter by release type. Gunakan versi Minecraft yang match.

### Opsi 3: Manual Download

Download JAR langsung dari Modrinth, taruh di `mods/` folder:
```
./data/mods/cardboard-xxx.jar
```

## Tips Penggunaan Cardboard

- Cardboard tidak selalu stabil — uji coba di server test dulu
- Tidak semua plugin Bukkit kompatibel (terutama yang menyentuh NMS)
- Alternatif lain:
  - **Banner**: plugin loader untuk Fabric (https://modrinth.com/mod/banner)
  - **Paper/Purpur**: kalau tidak butuh mod Fabric, lebih stabil
  - **Arclight**: Forge + Bukkit hybrid

## Verifikasi

Cek log server:
```bash
docker logs container-name | grep -i cardboard
```

Harus muncul seperti: "Cardboard loaded" atau "Cardboard initialized".

## Related

- [[modding/fabric-mods]] — Mod Fabric untuk server
- [[server/docker-compose-fabric]] — Setup Fabric via Docker Compose
- [[server/minecraft-docker]] — Setup server via Docker
- [[troubleshooting/minecraft-crash]] — Troubleshooting umum
