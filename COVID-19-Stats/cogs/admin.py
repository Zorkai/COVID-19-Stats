from discord.ext import commands
import textwrap
import traceback
from contextlib import redirect_stdout
import io
import re


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_result = None

    async def cog_check(self, ctx):
        return ctx.author.id in self.client.ADMINS

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    @commands.command()
    async def eval(self, ctx, *, body: str):
        "A command to run some code."
        if body.startswith('```py') and body.endswith('```'):
            body = body[5:-3]
        if body.startswith('```py') and body.endswith('```'):
            body = body[9:-3]
        if body.startswith('```') and body.endswith('```'):
            body = body[3:-3]

        env = {
            'bot': self.client,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(re.sub(r'(?s)(/Users/)(.*?)(/)', r"\1Censure\3", f'```py\n{e.__class__.__name__}: {e}\n```'))

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            text = f'**Error. :x: :**\n```py\n{value}{traceback.format_exc()}\n```'
        else:
            value = stdout.getvalue()
            try:
                text = "**The code has been successfully executed. ✅**"
            except:
                pass

            if ret is None:
                if value:
                    text = f'```py\n{value}\n```'
            else:
                self._last_result = ret
                text = f'```py\n{value}{ret}\n```'
        await ctx.send(re.sub(r'(?s)(/Users/)(.*?)(/)', r"\1Censure\3", text))


def setup(client):
    client.add_cog(Admin(client))
