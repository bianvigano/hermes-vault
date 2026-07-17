# Discord.js — Bot Development

Referensi pengembangan bot Discord menggunakan Node.js + discord.js v14.

**Library**: discord.js v14
**Docs**: https://discord.js.org/
**Node.js**: v16.9+ (v18+ recommended)

---

## Setup Project

```bash
mkdir bot-discord && cd bot-discord
npm init -y
npm install discord.js dotenv
```

## Welcome Bot (guildMemberAdd)

```js
require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMembers
    ]
});

client.on('guildMemberAdd', member => {
    const channel = member.guild.channels.cache.find(
        ch => ch.name === 'welcome'
    );
    if (!channel) return;
    channel.send(`👋 Selamat datang ${member} di **${member.guild.name}**!`);
});

client.login(process.env.TOKEN);
```

**WAJIB**: aktifkan **Server Members Intent** di Discord Developer Portal → Bot.

## Prefix Command: `:userinfo`

```js
const PREFIX = ':';

client.on('messageCreate', async message => {
    if (message.author.bot) return;
    if (!message.content.startsWith(PREFIX)) return;

    const args = message.content.slice(PREFIX.length).trim().split(/ +/);
    const command = args.shift().toLowerCase();

    if (command === 'userinfo') {
        const target = message.mentions.users.first() || message.author;
        const member = await message.guild.members.fetch(target.id);

        const embed = new EmbedBuilder()
            .setColor('#00BFFF')
            .setThumbnail(target.displayAvatarURL({ dynamic: true, size: 1024 }))
            .addFields(
                { name: '🆔 ID', value: target.id, inline: true },
                { name: '🏷️ Tag', value: `#${target.discriminator}`, inline: true },
                { name: '📅 Akun Dibuat', value: `<t:${Math.floor(target.createdTimestamp / 1000)}:F>` },
                { name: '📥 Join Server', value: `<t:${Math.floor(member.joinedTimestamp / 1000)}:F>` },
                { name: '🎭 Roles', value: member.roles.cache.filter(r => r.id !== message.guild.id).map(r => r.toString()).join(', ') || 'Tidak ada' }
            )
            .setFooter({ text: `Diminta oleh ${message.author.username}` })
            .setTimestamp();

        message.reply({ embeds: [embed] });
    }
});
```

Butuh intent: Guilds, GuildMessages, MessageContent, GuildMembers.

## Slash Command: `/userinfo`

```js
const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('userinfo')
        .setDescription('Melihat informasi user')
        .addUserOption(option =>
            option.setName('user').setDescription('Pilih user').setRequired(false)
        ),
    async execute(interaction) {
        const user = interaction.options.getUser('user') || interaction.user;
        const member = await interaction.guild.members.fetch(user.id);
        const fetchedUser = await user.fetch();
        const bannerURL = fetchedUser.bannerURL({ size: 1024 });

        const embed = new EmbedBuilder()
            .setColor('#00FFFF')
            .setThumbnail(user.displayAvatarURL({ dynamic: true, size: 1024 }))
            .addFields(
                { name: '🆔 User ID', value: user.id, inline: true },
                { name: '🏷️ Tag', value: `#${user.discriminator}`, inline: true },
                { name: '📅 Akun Dibuat', value: `<t:${Math.floor(user.createdTimestamp / 1000)}:F>` },
                { name: '📥 Join Server', value: `<t:${Math.floor(member.joinedTimestamp / 1000)}:F>` },
                { name: '🎭 Roles', value: member.roles.cache.filter(role => role.id !== interaction.guild.id).map(role => role.toString()).join(', ') || 'Tidak ada' }
            );

        if (bannerURL) embed.setImage(bannerURL);
        await interaction.reply({ embeds: [embed] });
    }
};
```

## Streaming Audio ke Voice Channel

```js
const { joinVoiceChannel, createAudioPlayer, createAudioResource } = require('@discordjs/voice');

const connection = joinVoiceChannel({
    channelId: CHANNEL_ID,
    guildId: GUILD_ID,
    adapterCreator: guild.voiceAdapterCreator,
});

const player = createAudioPlayer();
const resource = createAudioResource('https://radio-stream-url');
player.play(resource);
connection.subscribe(player);
```

## Pitfall

- Bot **tidak bisa** share screen / video streaming — Discord tidak sediakan API
- `discriminator` dihapus di Discord username baru (pomelo) — jadi `#0`
- Self-bot untuk video streaming = melanggar ToS, risiko banned
- MessageContent intent WAJIB untuk prefix command (didaftarkan di Developer Portal)

## Related

- [[discord/webhook/webhook-basics]] — Webhook vs Bot
- [[discord/webhook/webhook-storage]] — Webhook sebagai storage file
- [[discord/bot/permissions]] — Setting permission mention
