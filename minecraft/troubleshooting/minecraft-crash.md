# Troubleshooting Crash Minecraft — Panduan Umum

Panduan troubleshooting crash Minecraft Java Edition, mencakup error umum seperti OpenAL, registry mismatch, koneksi, dan crash 1.8.9.

## Crash OpenAL (libopenal.so)

Error:
```
SIGFPE (0x8) at pc=0x00007f303858db4d
Problematic frame: C  [libopenal.so+0x9fb4d]
```

Penyebab: Bug/incompatibilitas OpenAL dengan driver audio Linux.

Solusi:
```bash
sudo apt update
sudo apt install --reinstall libopenal1
sudo apt install libopenal-soft
```

Jalankan dengan preload:
```bash
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libopenal.so.1 multimc
```

Atau matikan suara sementara lewat JVM args:
```
-Dorg.lwjgl.openal.libname=none
```

## Registry Mismatch / Mod Tidak Sama

Error:
```
Received 2 registry entries not known by this client
Namespace: oneblockchunk
```

Penyebab: Client dan server punya mod berbeda.

Solusi:
1. Samakan mod client & server (versi identik)
2. Pastikan loader sama (Fabric/Forge/NeoForge)
3. Pastikan versi Minecraft sama
4. Pakai modpack server jika tersedia
5. Restart game setelah ubah mod

## Invalid Public Key (Secure Chat)

Error:
```
multiplayer.disconnect.invalid_public_key
```

Penyebab: Waktu PC tidak sinkron atau server tidak mendukung secure profile.

Solusi client:
- Sync jam PC dengan internet
- Relog akun Microsoft
- Hapus `~/.minecraft/caches`

Solusi server (`server.properties`):
```properties
enforce-secure-profile=false
```

Restart server.

## Unable to Connect

Penyebab umum:
- Ping tinggi / koneksi unstable
- Server overload (RAM/CPU penuh)
- Versi/mod tidak cocok
- Port diblokir firewall
- Timeout / anti-cheat kick

Solusi:
1. Cek log server
2. Cek firewall: `sudo ufw allow 25565/tcp`
3. Pastikan versi & mod cocok
4. Monitor resource server

## Crash 1.8.9 (Prism Launcher / Forge)

Error umum: kombinasi Java 17 + Forge 1.8.9 + Intel i915.

Solusi:
- Minecraft 1.8.9 membutuhkan Java 8, bukan Java 17
- Di Prism Launcher: Edit Instance → Settings → Java → pilih Java 8
- Update driver Mesa / Intel
- Coba nonaktifkan mod satu per satu

## Langkah Umum Troubleshooting

1. Baca crash log terakhir di folder `.minecraft/crash-reports/`
2. Cari baris `Caused by:` atau `Problematic frame`
3. Google error message tersebut
4. Coba hapus mod/resource pack terakhir yang ditambahkan
5. Update Java, driver GPU, dan mod
6. Jalankan dengan instance vanilla untuk isolasi

## Related

- [[troubleshooting/connection-throttled]] — Pesan Purpur/Spigot
- [[server/server-properties]] — Konfigurasi server
- [[modding/fabric-mods]] — Mod Fabric
- [[modding/forge-mods]] — Mod Forge
- [[tools/spark-profiler]] — Profiling TPS
