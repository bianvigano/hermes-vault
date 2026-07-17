# Discord — Server & Permissions

Pengaturan server Discord: role default untuk member baru, mention control, Onboarding.

---

## Auto Role Join (Tanpa Bot)

### Onboarding — Default Role

1. Server Settings → Community → Enable Community
2. Server Settings → Onboarding / Server Guide
3. Scroll ke **Default Channels & Roles**
4. Tambahkan role untuk member baru
5. Publish

Setiap member baru join → langsung dapat role.

### Rules Screening (Semi-Otomatis)

1. Server Settings → Safety Setup / Membership Screening
2. Aktifkan rules
3. Role diberikan setelah user klik "I Agree"

⚠️ Role tidak langsung muncul sebelum user setuju rules.

## Batasi Mention

### Matikan @everyone & @here

1. Server Settings → Roles → pilih role (misalnya `@everyone`)
2. Matikan: **Mention @everyone, @here, and All Roles**

### Matikan Mention ke Role Tertentu

1. Server Settings → Roles → pilih role
2. Matikan: **Allow anyone to @mention this role**

### Per-Channel Restriction

1. Klik kanan channel → Edit Channel → Permissions
2. Pilih role → matikan mention permission

### Supaya Kamu Tidak Kena Tag

1. Klik kanan server → Notification Settings
2. Centang: Suppress @everyone and @here, Suppress All Role Mentions

## Customisation Questions vs Default Role

| Bagian | Fungsi |
|--------|--------|
| Customisation Questions | Role pilihan user (user milih sendiri) |
| Default Channels & Roles | ✅ Role otomatis saat join |
| Browse Channels | Daftar channel saja |

## Pitfall

- Customisation Questions = role OPSIONAL (user pilih), bukan otomatis
- Discord tidak punya auto-role berdasarkan region, umur akun, atau jawaban form — butuh bot
- Tanpa bot, tidak bisa auto role selain via Onboarding default
- Rules Screening tidak memberikan role sebelum user klik agree

## Related

- [[discord/bot/discordjs-bot]] — Bot auto role + welcome
- [[discord/webhook/webhook-basics]] — Webhook untuk notifikasi otomatis
