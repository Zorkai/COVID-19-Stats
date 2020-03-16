import discord
from discord.ext import commands
from datetime import datetime


class HelpCommand(commands.HelpCommand):
    def __init__(self):
        commands.HelpCommand.__init__(
            self, verify_checks=True, command_attrs={"hidden": True})

    async def send_bot_help(self, mapping):
        bot = self.context.bot
        prefix = bot.PREFIX
        embed = discord.Embed(
            title="**List of commands :**",
            description=f"```fix\nMy current prefix is \"{prefix}\" but you" \
            " can mention me too, get more information on a command with" \
            f" \"{prefix}help <command>\".```",
            color=bot.EMBED_COLOR,
            timestamp=datetime.utcnow())
        for cog, cmds in mapping.items():
            cmds = await self.filter_commands(cmds)
            if not cog or not cmds:
                continue
            content = "\n".join(f"{prefix}{cmd}" if cmd.signature is ""
                                else f"{prefix}{cmd} {cmd.signature}"
                                for cmd in cmds)
            embed.add_field(
                name=f"**{cog.qualified_name}**", value=f"```md\n{content}```")
        embed.set_footer(text=bot.BOT_NAME, icon_url=bot.user.avatar_url)
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        bot = self.context.bot
        prefix = self.clean_prefix
        embed = discord.Embed(
            title=f"**{cog.qualified_name}**",
            color=bot.EMBED_COLOR,
            timestamp=datetime.utcnow())
        ls = await self.filter_commands(cog.get_commands(), sort=True)
        content = "\n".join(f"{prefix}{cmd}" if cmd.signature is "" else
                            f"{prefix}{cmd} {cmd.signature}" for cmd in ls)
        embed.add_field(name="Commands", value=f"```\n{content}```")
        embed.set_footer(text=bot.BOT_NAME, icon_url=bot.user.avatar_url)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        bot = self.context.bot
        prefix = self.clean_prefix
        embed = discord.Embed(
            title=f"**Infos about {command.name}**",
            color=bot.EMBED_COLOR,
            timestamp=datetime.utcnow())
        content = f"{prefix}{command}" if command.signature is "" else f"{prefix}{command} {command.signature}"
        embed.add_field(name="Usage", value=f"```\n{content}```", inline=False)
        if command.help is not None:
            embed.add_field(
                name="Description",
                value=f"```\n{command.help}```",
                inline=False)
        embed.set_footer(text=bot.BOT_NAME, icon_url=bot.user.avatar_url)
        await self.get_destination().send(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

def setup(bot):
    bot.add_cog(Help(bot))
