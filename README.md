# VideoCompress
A Telegram Video Compressor Bot By [@AbirHasan2005](https://t.me/linux_repo). **This bot works for all!** No need to define each user IDs to use bot. Also works in Group.

### Special Features:
- Bot's Live Status on Channel
- Force Sub to Channel
- Database:
	- Can Broadcast messages
	- Can Ban-Unban Manually
	- Can see numbers users in DB
- Bot will compress as HEVC
        - Video Quality will not lose much in this mode

* If you need more help to Deploy Feel Free to ask in [Support Group](https://t.me/linux_repo).

### Demo Bot:
<a href="https://t.me/VidCom_Robot"><img src="https://img.shields.io/badge/Demo-Telegram%20Bot-blue.svg?logo=telegram"></a>

### Demo Logs Channel:
<a href="https://t.me/VideoCompressLogs"><img src="https://img.shields.io/badge/Demo-Bot%20Logs%20Channel-blue.svg?logo=telegram"></a>

## Easy Deploy:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

#### Video Tutorial:
[![YouTube](https://img.shields.io/badge/YouTube-Video%20Tutorial-red?logo=youtube)](https://youtu.be/gMRsSqaUkio)

### Support Group:
<a href="https://t.me/linux_repo"><img src="https://img.shields.io/badge/Telegram-Join%20Telegram%20Group-blue.svg?logo=telegram"></a>

## Required Configs:
* `SESSION_NAME` - Any name of session. Better keep default.
* `TG_BOT_TOKEN` - Get this from [@BotFather](https://t.me/BotFather)
* `LOG_CHANNEL` - Put Your Bot's Logs Channel's Username. For Help ask in [Support Group](https://t.me/linux_repo).
* `BOT_USERNAME` - Your Bot's Username which you send to [@BotFather](https://t.me/BotFather) while creating Bot. ***(Without `@` Before Username!!)***
* `APP_ID` - Get this from my.telegram.org
* `API_HASH` - Get this from my.telegram.org
* `DATABASE_URL` - Your MongoDB Database URL.
* `AUTH_USERS` - Put your ID & other Sudo Users IDs. Separate with **Space**. Just for using [Admin Commands](https://github.com/AbirHasan2005/VideoCompress/tree/HEVC#admin-commands).

## Optional Configs:
* `UPDATES_CHANNEL` - Put your Channel Username which you want to do Force Sub. But bot should be Admin in that channel. If got any error or not understand anything than ask in [Support Group](https://t.me/linux_repo).
* `COMMAND_EXEC` - `/exec` Command Handler.
* `COMMAND_STATUS` - `/status` Command Handler.
* `COMMAND_CANCEL` - `/cancel` Command Handler.
* `COMMAND_COMPRESS` - `/compress` Command Handler.
* `COMMAND_START` - `/start` Command Handler.
* `COMMAND_HELP` - `/help` Command Handler

### Public Commands:
```
start - Start Bot
compress - Compress Video
help - How to Use Bot
```

### Admin Commands:
```
cancel - Cancel Last Process
status - Total User Number in Database
broadcast - Reply to Message to Broadcast
ban_user - Ban A User with time & reason
unban_user - Unban a User
banned_users - Show Banned Users
exec - EXEC 🙄
```

## Follow on:
<p align="left">
<a href="https://github.com/AbirHasan2005"><img src="https://img.shields.io/badge/GitHub-Follow%20on%20GitHub-inactive.svg?logo=github"></a>
</p>
<p align="left">
<a href="https://twitter.com/AbirHasan2005"><img src="https://img.shields.io/badge/Twitter-Follow%20on%20Twitter-informational.svg?logo=twitter"></a>
</p>
<p align="left">
<a href="https://facebook.com/AbirHasan2005"><img src="https://img.shields.io/badge/Facebook-Follow%20on%20Facebook-blue.svg?logo=facebook"></a>
</p>
<p align="left">
<a href="https://instagram.com/AbirHasan2005"><img src="https://img.shields.io/badge/Instagram-Follow%20on%20Instagram-important.svg?logo=instagram"></a>
</p>

### Credits:
* [Jijinr](https://github.com/Jijinr)
* [SpEcHide](https://github.com/spechide)
* [AbirHasan2005](https://github.com/AbirHasan2005)
