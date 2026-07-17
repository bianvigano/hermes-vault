# MinecraftTitleGenerator project (June 26, 2026): Located at /home/the-meh/Docume

- **Source:** memory
- **Archived:** 2026-06-29T03:07:09+07:00
- **Tags:** minecraft,nodejs,rendering,project

---

MinecraftTitleGenerator project (June 26, 2026): Located at /home/the-meh/Documents/MinecraftTitleGenerator/. Uses skia-canvas + gl + node-three for rendering Minecraft title textures. Scripts in scripts/ subfolder with own package.json. Requires: Node 20.x (not 18 — import assertions; not 22 — gl binary mismatch), xvfb-run (Intel Ivy Bridge GPU too slow for real X server, causes XIO timeout). Build command: source ~/.nvm/nvm.sh && nvm use 20.19.6 && xvfb-run node compile.js. Output: 1195 PNGs in fonts/, shapes/ folders.
