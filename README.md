# fetidbot
This is a telegram bot that represents a personality of my little kitten - Vanya. She stinks, but only metaphorically. That's why fetidbot.

Basically, it just sends random photos of my kitten Vanya from my Imgur album to make one's day better :)

This bot uses pyTelegramBotAPI for telegram connection. It is deployed on heroku platform and uses heroku's PostgreSQL database to track sent photos and notify me, when somebody has already seen all available photos, so I can easily send photo to a bot and it will be automatically uploaded to a server and all such users will be notified.