# Prayer-Bot

![image of prayer-bot image](https://media.discordapp.net/attachments/694994771638222861/848993179759542302/IMG_20210531_213504.jpg?width=444&height=445)

Prayer bot is a bot that allows you to store prayers to different entities. The bot is built using discord.py and has the following commands.

## Commands
- addentity \<name>
  - Creates an entity and you can also attach an image that will then be associated with that entity
- updatename \<old_name> \<new_name>
  - Changes an entitys name
- updateimage \<name>
  - Allows you to add or update an image for an entity
- addprayer \<name> \<prayer>
  - Stores a prayer dedicated to an entity
- prayers \<name>
  - Shows stored prayers for that entity and gives the prayers id along with them
- entities
  - Shows all entities you have added
- removeprayer \<name> \<id>
  - Removes a prayer from an entity and the rest of the prayer IDs might change
- removeentity \<name>
  - Removes an entity
- changeprefix \<new_prefix>
  - Changes the prefix in a server. The default prefix/dm prefix is !!

## **WARNING**
If an entity has name that involves two words you must encapsulate the name in quotation marks ex. \"prayer bot\" or you can add a underscore to represent a space ex. prayer_bot

## Adding Bot
To add to your server just invite using this [link](https://discord.com/api/oauth2/authorize?client_id=754848887323361350&permissions=265280&scope=bot)
