# Docker vs Virtual Machine

Docker container dan Virtual Machine (VM) keduanya menyediakan lingkungan terisolasi untuk aplikasi, tapi dengan arsitektur fundamental yang berbeda.

## Arsitektur

```
VIRTUAL MACHINE:                    DOCKER CONTAINER:

┌──────────┐ ┌──────────┐          ┌──────────┐ ┌──────────┐
│  App A   │ │  App B   │          │  App A   │ │  App B   │
├──────────┤ ├──────────┤          ├──────────┤ ├──────────┤
│  Bins/   │ │  Bins/   │          │  Bins/   │ │  Bins/   │
│  Libs    │ │  Libs    │          │  Libs    │ │  Libs    │
├──────────┤ ├──────────┤          └─────┬────┘ └─────┬────┘
│ Guest OS │ │ Guest OS │                │            │
├──────────┤ ├──────────┤          ┌─────▼────────────▼─────┐
│Hypervisor│ │Hypervisor│          │     Docker Engine      │
├──────────┴─┴──────────┤          ├─────────────────────────┤
│      HOST OS           │          │       HOST OS          │
├────────────────────────┤          ├─────────────────────────┤
│    INFRASTRUCTURE      │          │    INFRASTRUCTURE       │
└────────────────────────┘          └─────────────────────────┘
```

## Perbandingan

| Aspek | Virtual Machine | Docker Container |
|---|---|---|
| **Virtualisasi** | Hardware-level | OS-level (kernel sharing) |
| **OS** | Tiap VM punya OS sendiri | Sharing kernel host |
| **Boot time** | Menit | Detik |
| **Ukuran image** | GB | MB (biasanya) |
| **Densitas** | Puluhan per host | Ratusan per host |
| **Isolasi** | Full (hypervisor) | Proses + namespace (weaker) |
| **Portabilitas** | Terbatas (tergantung hypervisor) | Sangat portable (image standar) |
| **Overhead** | Berat (kernel utuh) | Ringan (hanya app + deps) |
| **Persistensi** | Disk image (persisten by default) | Ephemeral (butuh volume) |
| **Security** | Sangat terisolasi | Isolasi lebih lemah (sharing kernel) |

## Kapan Pakai VM?

- Butuh isolasi keamanan penuh (multi-tenant hosting)
- Aplikasi perlu kernel spesifik (Windows app di Linux host)
- Environment yang butuh full OS GUI
- Legacy app yang tidak bisa di-containerize

## Kapan Pakai Container?

- Microservices / cloud-native apps
- CI/CD pipelines
- Development & testing
- Deploy cepat & scaling dinamis
- Aplikasi yang butuh portabilitas tinggi

## Bisa Juga Hybrid

Pakai container **di dalam** VM — dapat isolasi VM + efisiensi container. Banyak cloud provider menjalankan container di VM (GKE node, ECS instance, AKS).

```
┌──────────────────────────────┐
│          VIRTUAL MACHINE     │
│  ┌──────────┐ ┌──────────┐   │
│  │Container │ │Container │   │
│  │  App A   │ │  App B   │   │
│  └──────────┘ └──────────┘   │
│  ┌────────────────────────┐  │
│  │    Docker Engine       │  │
│  ├────────────────────────┤  │
│  │      Guest OS          │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

## Sumber

- [Docker vs VM — Docker Docs](https://docs.docker.com/get-started/docker-overview/#the-underlying-technology)
