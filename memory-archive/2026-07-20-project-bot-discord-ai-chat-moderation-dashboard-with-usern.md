# Project bot-discord-ai-chat: moderation dashboard with username+password auth ad

- **Source:** memory
- **Archived:** 2026-07-20T11:51:21+07:00
- **Tags:** project,archive

---

Project bot-discord-ai-chat: moderation dashboard with username+password auth added. Files: bot_app/moderation_dashboard.py (dashboard module), bot_app/config.py (MOD_DASH_USERNAME/MOD_DASH_PASSWORD config), bot_app/faq_admin.py (HTTP routes /moderation, /moderation/login, /moderation/logout, /moderation/data), bot_app/ai_client.py (system prompt KEMAMPUAN MODERASI BOT section), bot_app/parsers.py (parse_moderation_dashboard_command), bot.py (handle_moderation_dashboard handler). Owner types '@Bot dashboard' -> URL printed to terminal only (not Discord reply). Set MOD_DASH_USERNAME + MOD_DASH_PASSWORD in .env.
