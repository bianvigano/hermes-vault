# Minecraft Server Optimization

## Software
- Use Paper or Purpur (Don't use Bukkit/Spigot)
- Java 21+

## server.properties
- sync-chunk-writes=false (CRITICAL)
- simulation-distance=4
- view-distance=7
- network-compression-threshold=256

## bukkit.yml
- spawn-limits: monsters=20, animals=5, water-animals=2, water-ambient=2, ambient=1
- ticks-per: monster-spawns=10, sisanya=400

## spigot.yml
- mob-spawn-range=3
- entity-activation-range: animals=16, monsters=24, misc=8, water=8
- hopper-transfer=8, hopper-check=8
- merge-radius: item=3.5, exp=4.0
- nerf-spawner-mobs=true
- tick-inactive-villagers=false

## paper-world-defaults.yml
- redstone-implementation=ALTERNATE_CURRENT
- optimize-explosions=true
- per-player-mob-spawns=true
- prevent-moving-into-unloaded-chunks=true
- armor-stands.tick=false
- max-entity-collisions=2
- delay-chunk-unloads-by=10s

## purpur.yml
- use-alternate-keepalive=true
- entities-can-use-portals=false

## JVM
- Aikar's flags (use flags.sh)
- SSD mandatory, focus single-core CPU

## What to Avoid
- /reload command
- Mob stacker plugins
- Item remover plugins
- Plugin enable/disable at runtime
- Command-function datapacks
- Shared hosting

## Server minecraft-serverx
- Location: USER_HOME/Desktop/minecraft-serverx/
- Software: Purpur 1.21.11
- Issues found:
  - sync-chunk-writes=true (should be false)
  - simulation-distance=10 (should be 4)
  - view-distance=12 (should be 7)
  - spawn-limits too high (monsters 70→20)
  - mob-spawn-range=8 (should be 3)
  - redstone-implementation=VANILLA (should be ALTERNATE_CURRENT)
  - optimize-explosions=false (should be true)
  - Detected PlugManX (dangerous)
- Scripts available:
  - analyze_server.py: minecraft-optimization-guide/scripts/
  - fix_server.py: minecraft-optimization-guide/scripts/
- Spark Analyzer
  - Script: spark-profiler-analyzer/scripts/check_spark_selenium.py
  - Reference: spark-profiler-analyzer/references/spark-solutions.md
  - Features: --wait SEC, --json output, parse TPS/MSPT/CPU/mem/plugins/entities/chunks

Date: 2026-07-16T20:45:00+07:00
Tags: minecraft, optimization, server, configuration, configuration-management
Archived from MEMORY.md Entry 2