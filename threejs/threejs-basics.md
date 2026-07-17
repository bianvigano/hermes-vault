# Three.js — 3D Graphics Library

Library JavaScript untuk 3D graphics di browser. WebGL-based, powerful untuk game, visualisasi, product configurator, AR/VR.

**Website**: https://threejs.org/
**Docs**: https://threejs.org/docs/
**npm**: `three`

---

## Instalasi

```bash
npm install three
```

## Kamera Perspektif (PerspectiveCamera)

```js
const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 2000);
```

| Parameter | Nama | Fungsi |
|-----------|------|--------|
| `75` | FOV (Field of View) | Sudut pandang, semakin besar = makin lebar |
| `1` | Aspect Ratio | Lebar:tinggi, biasanya `window.innerWidth / window.innerHeight` |
| `0.1` | Near Plane | Jarak minimum objek terlihat |
| `2000` | Far Plane | Jarak maksimum objek terlihat |

Visualisasi frustum:
```
        /---------\
       /           \
      /   TERLIHAT   \
     |                |
      \              /
       \------------/
```

## GLTFLoader — Import Model 3D

```js
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

const loader = new GLTFLoader();
loader.load(
  "/model.glb",
  (gltf) => scene.add(gltf.scene),
  (progress) => console.log((progress.loaded / progress.total) * 100 + "% loaded"),
  (error) => console.error(error)
);
```

**WAJIB** pakai `.js` di akhir path import:
- ✅ `"three/examples/jsm/loaders/GLTFLoader.js"`
- ❌ `"three/examples/jsm/loaders/GLTFLoader"`

Bundler yang support: Vite ✅, Webpack ✅, Parcel ✅, Next.js ✅.

## LineSegments — Kumpulan Garis Terpisah

```js
const geometry = new THREE.BufferGeometry();
const vertices = new Float32Array([
  0, 0, 0,   1, 0, 0,   // garis 1
  1, 0, 0,   1, 1, 0,   // garis 2
  1, 1, 0,   0, 1, 0    // garis 3
]);
geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));

const material = new THREE.LineBasicMaterial({ color: 0x00ff00 });
const lineSegments = new THREE.LineSegments(geometry, material);
scene.add(lineSegments);
```

**Bedanya dengan Line:**

| | Line | LineSegments |
|---|------|-------------|
| Koneksi | Semua titik bersambung | Dua titik = satu garis independen |
| Jumlah titik | Bebas | HARUS genap |
| Use case | Path, kurva | Wireframe, grid, sumbu |

## Canvas 2D — Team Builder / UI Game

```html
<canvas id="game"></canvas>
```

```js
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');

// Draw pixel-style box
ctx.fillStyle = '#8B8B8B';
ctx.fillRect(x, y, w, h);
ctx.strokeStyle = '#FFFFFF';
ctx.strokeRect(x, y, w, h);

// Minecraft-style bevel effect
ctx.fillStyle = '#C6C6C6';
ctx.fillRect(x, y, w, 2);  // top highlight
ctx.fillStyle = '#555555';
ctx.fillRect(x, y + h - 2, w, 2);  // bottom shadow
```

Canvas bisa dipakai untuk UI kustom: team builder, drag & drop, save/load JSON, Minecraft-style UI.

## Common Pitfall

- `PerspectiveCamera` aspect ratio `1` = square; di production pakai `window.innerWidth / window.innerHeight`
- `linewidth` di `LineBasicMaterial` tidak berfungsi di kebanyakan browser (limit WebGL)
- GLTFLoader **harus** pakai `.js` di path import
- Canvas `drawImage` butuh image yang sudah loaded — pakai `img.onload`
- Muat terlalu banyak model GLB → memory leak, pakai `gltf.scene.traverse` untuk dispose

## Related

- [[threejs/canvas-ui]] — Canvas 2D untuk UI game / tool builder
- [[webdev/frontend/index]] — Frontend web dev
