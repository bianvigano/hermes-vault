# Regen Regions Plugin — Blok Regenerasi Otomatis

Plugin Minecraft (Spigot/Paper) untuk membuat region di mana blok yang hancur akan beregenerasi otomatis setelah waktu tertentu.

## Konsep

Regen Regions memungkinkan admin membuat area (region) di mana blok akan **beregenerasi kembali** setelah durasi yang bisa dikustomisasi. Cocok untuk:
- Event PvP/explosion tanpa merusak terrain permanen
- Ability/fight dengan efek destruktif
- Mini-game dengan damage lingkungan

## Fitur Utama

- Admin membuat region dengan `pos1` & `pos2`
- Blok hancur disimpan, diregen setelah waktu tertentu
- Waktu regen custom per region
- Region bisa enable/disable
- Aman untuk explosion & ability

## Struktur Plugin

```
RegenRegions/
 ├─ src/
 │  └─ me/example/regenregions/
 │      ├─ RegenRegions.java      # Main plugin
 │      ├─ Region.java            # Data region
 │      └─ RegionManager.java     # Logic + event handler
 └─ plugin.yml
```

## plugin.yml

```yml
name: RegenRegions
version: 1.0
main: me.example.regenregions.RegenRegions
api-version: 1.20
commands:
  regenregion:
    permission: regenregions.admin
```

## RegenRegions.java (Main)

```java
public class RegenRegions extends JavaPlugin {
    private static RegenRegions instance;
    private RegionManager regionManager;

    @Override
    public void onEnable() {
        instance = this;
        regionManager = new RegionManager(this);
        getServer().getPluginManager().registerEvents(regionManager, this);
    }

    public RegionManager getRegionManager() { return regionManager; }
    public static RegenRegions getInstance() { return instance; }
}
```

## Region.java (Data Model)

```java
public class Region {
    private final Location pos1, pos2;
    private final int regenTime;         // detik
    private boolean enabled = true;
    private final Map<Location, BlockData> brokenBlocks = new HashMap<>();

    public boolean isInside(Location loc) {
        return loc.getWorld().equals(pos1.getWorld())
            && loc.getX() >= Math.min(pos1.getX(), pos2.getX())
            && loc.getX() <= Math.max(pos1.getX(), pos2.getX())
            && loc.getY() >= Math.min(pos1.getY(), pos2.getY())
            && loc.getY() <= Math.max(pos1.getY(), pos2.getY())
            && loc.getZ() >= Math.min(pos1.getZ(), pos2.getZ())
            && loc.getZ() <= Math.max(pos1.getZ(), pos2.getZ());
    }

    public void saveBlock(Block block) {
        brokenBlocks.put(block.getLocation(), block.getBlockData());
    }
}
```

## RegionManager.java (Logic)

Handle event `BlockBreakEvent`, `BlockExplodeEvent`, `EntityExplodeEvent`. Simpan block data, schedule regen via `Bukkit.getScheduler().runTaskLater()`.

## Command

```
/regenregion create <nama> <waktu_detik>
/regenregion pos1
/regenregion pos2
/regenregion toggle <nama>
/regenregion list
/regenregion delete <nama>
```

## Best Practices 2024-2025

- Gunakan Paper API (lebih optimal dari Spigot)
- Simpan data region ke file YAML/JSON untuk persistensi antar restart
- Batasi maksimum blok per region untuk mencegah memory leak
- Gunakan `BlockData` bukan `Material` + data byte (modern API)
- Pertimbangkan `Bukkit.createExplosion()` dengan `breakBlocks=false` + regen manual untuk kontrol penuh

## Related

- [[tools/fawe-troubleshooting]] — FAWE issues
- [[server/server-properties]] — Konfigurasi server
- [[plugin/worldguard]] — Plugin protection
