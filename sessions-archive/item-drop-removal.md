---
title: cara untuk meberuh waktu drop item di lantai supaya cepet hilang
date: 2026-06-02
session_id: session_20260602_224505_fc2413
messages: 46
tags: [minecraft, world, entity, level, statictext]
---

## Summary
User shared Spark profiler link (https://spark.lucko.me/iZL61OZ7rI) and asked how to reduce item drop despawn time on the ground.

## Key Points
- Spark profiler link analysis for item entity performance
- Goal: reduce item despawn time (default 5 minutes → faster)
- Covered: world, entity, level, statictext, lambda, block
- Paper/Spigot configuration for `merge-radius` and `despawn-rates`
- Model switched from deepseek-v4-flash to owl-alpha

## Result
ProvidedPaper config changes to speed up item despawn (despawn-rates, merge-radius).

## Related
- [[folia-performance]] — server performance
- [[folia-lag]] — server lag
- [[spark-debug-0530]] — spark profiler analysis
- [[spark-profiler-0602]] — spark profiler data
