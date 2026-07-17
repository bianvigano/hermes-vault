# Custom Seed — Mengatur Seed Kustom di Minecraft Server

Cara memasukkan seed kustom, menghapus world lama, dan memahami pengaturan terkait seed di `server.properties`.

## Apa Itu Seed?

Seed adalah nilai yang digunakan Minecraft untuk menghasilkan dunia (world generation). Seed yang sama → dunia yang sama persis. Seed kosong → Minecraft memilih seed acak.

## Cara Memasukkan Seed

### Langkah-langkah

1. **Matikan server** terlebih dahulu
2. Buka file `server.properties`
3. Cari baris `level-seed=`
4. Isi seed yang diinginkan, contoh:
   ```properties
   level-seed=123456789
   ```
5. **Simpan file**
6. Nyalakan server kembali

### Catatan Penting

- **Seed hanya berlaku saat world PERTAMA KALI dibuat**. Kalau folder `world/` sudah ada, seed di `server.properties` akan diabaikan.
- Untuk mengganti seed di world yang sudah ada → harus **hapus folder world lama**, lalu start ulang server.

## Mengganti Seed di World yang Sudah Ada

1. **Stop server**
2. Hapus folder world (`world/`, `world_nether/`, `world_the_end/`)
3. Edit `level-seed` di `server.properties`
4. Start server → world baru dengan seed kustom akan dibuat

## Pengaturan Terkait di server.properties

### `level-seed`

```properties
level-seed=         # Kosong = random
level-seed=abc123   # Bisa string juga
level-seed=-12345   # Bisa angka negatif
```

Seed bisa berupa string apapun. Minecraft akan mengkonversinya ke nilai numerik internal.

### `max-world-size`

```properties
max-world-size=29999984
```

Batas **radius** maksimum world dari titik pusat (0,0). Nilai dalam blok.

- `29999984` = default maksimal Minecraft (~60 juta blok diameter)
- `5000` = world 10.000 × 10.000 blok — cocok untuk SMP kecil
- Ini **tidak memotong world yang sudah ada** — perlu world baru
- World border bisa diatur juga via command: `/worldborder set 10000`

### `level-type`

```properties
level-type=minecraft:normal    # Default world
level-type=minecraft:flat      # Superflat
level-type=minecraft:large_biomes  # Bioma besar
level-type=minecraft:amplified    # Amplified (ekstrim)
```

### `generator-settings`

```properties
generator-settings=    # Kosong = default
```

Digunakan untuk preset custom (terutama superflat). Contoh superflat dengan village:
```properties
generator-settings={"layers":[{"block":"bedrock","height":1},{"block":"dirt","height":2},{"block":"grass_block","height":1}],"structures":{"structures":{"village":{}}}}
```

### `difficulty`

```properties
difficulty=peaceful   # Damai — tidak ada mob jahat, darah tidak berkurang
difficulty=easy       # Mudah — mob lemah, kelaparan tidak membunuh
difficulty=normal     # Normal — standar
difficulty=hard       # Sulit — mob kuat, zombie bisa dobrak pintu
```

Bisa diubah saat server berjalan dengan command: `/difficulty hard`

## Rekomendasi Ukuran World

| Tipe Server | `max-world-size` | WorldBorder | Keterangan |
|-------------|------------------|-------------|------------|
| Survival kecil | 5000 | 10000 | 10K×10K blok |
| SMP 10-20 orang | 10000 | 20000 | Cukup luas |
| Server RPG/Eksplorasi | 25000 | 50000 | Banyak bioma |

## Best Practices 2024-2025

- Seed terkenal bisa dicari di [r/minecraftseeds](https://reddit.com/r/minecraftseeds) atau situs seed viewer
- Untuk server survival, kombinasikan seed + WorldBorder + Chunky pre-generate
- `level-type` tidak bisa diubah setelah world dibuat (kecuali hapus world)
- Backup world sebelum menghapus — gunakan: `tar -czf world_backup.tar.gz world/`
- Beberapa host menyediakan seed manager di panel kontrol

## Troubleshooting

**Seed tidak berubah setelah restart?**
→ Folder `world/` masih ada. Hapus folder world, baru seed baru akan dipakai.

**World border tidak sesuai?**
→ `max-world-size` di `server.properties` hanya membatasi radius. WorldBorder (`/worldborder`) bisa diatur terpisah. Gunakan `/worldborder set <ukuran>` untuk batas dinamis.

## Related

- [[minecraft/server/server-properties]] — Konfigurasi lengkap server.properties
- [[minecraft/tools/chunky]] — Pre-generate chunk dengan seed kustom
- [[minecraft/server/minecraft-docker]] — Setup server via Docker
- [[minecraft/gameplay/daylight-cycle]] — Set siang terus
