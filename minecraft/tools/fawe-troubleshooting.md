# FAWE Troubleshooting — FastAsyncWorldEdit Error

Masalah dan solusi untuk error FastAsyncWorldEdit (FAWE) pada server Minecraft Paper/Purpur/Spigot.

## Error Umum

```
FAWE error saat PlayerInteractEvent
```

Penyebab: plugin bentrok atau versi FAWE tidak cocok.

## Penyebab Utama

1. **Versi FAWE tidak match dengan versi server**
   - Server 1.20+ tapi FAWE versi lama
   - Paper/Purpur terbaru, FAWE belum support penuh

2. **Bentrok dengan plugin lain**
   - Plugin protection: **WorldGuard**, **GriefPrevention**, **Lands**, **Residence**
   - Plugin item/ability custom
   - Plugin yang listen `PlayerInteractEvent`

3. **Bug FAWE**
   - Build tertentu FAWE v2.x punya known issues
   - Cek GitHub issues: https://github.com/IntellectualSites/FastAsyncWorldEdit

4. **Config FAWE rusak/kadaluarsa**
   - Config dari versi lama dipakai di versi baru

## Langkah Troubleshooting

### 1. Update FAWE

Download versi terbaru yang match dengan versi server:
```
Cek: /version
Download FAWE dari Modrinth atau GitHub
```

### 2. Tes Bentrok Plugin (Isolasi)

```bash
# Stop server
# Rename folder plugins
mv plugins plugins_backup
# Masukin FAWE doang
cp FAWE.jar plugins/
# Start server
```

- Error hilang → bentrok plugin (cek satu per satu)
- Error tetap → masalah FAWE sendiri

### 3. Reset Config FAWE

```bash
# Stop server
rm -rf plugins/FastAsyncWorldEdit/
# Start ulang (generate config baru)
```

### 4. Cek Dependensi

FAWE butuh WorldEdit API. Pastikan:
- WorldEdit terinstal (atau FAWE standalone build)
- Tidak ada WorldEdit dan FAWE bersamaan (konflik)

## Alternatif FAWE

- **WorldEdit** (vanilla, lebih lambat tapi stabil)
- **Axiom** (editor berbasis client-mod, performa tinggi)
- **VoxelSniper** (untuk terrain editing)

## Catatan

- FAWE jauh lebih cepat dari WorldEdit biasa untuk operasi besar (//set, //paste area besar)
- Kalau error cuma spam tapi tidak crash, bisa diabaikan sementara — tapi tidak disarankan jangka panjang
- Selalu backup world sebelum operasi FAWE besar

## Related

- [[troubleshooting/minecraft-crash]] — Troubleshooting umum
- [[tools/chunky]] — Pre-generate chunk
- [[server/server-properties]] — Konfigurasi server
