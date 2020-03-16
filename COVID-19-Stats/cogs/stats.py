import aiohttp
import discord
from discord.ext import commands
from datetime import datetime


class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.stats_api_url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"
        self.countrys_api_url = "https://restcountries.eu/rest/v2/name/"
        self.flags_api_url = "https://www.countryflags.io/{}/flat/64.png"
        self.headers = {
            'x-rapidapi-host':
            "covid-19-coronavirus-statistics.p.rapidapi.com",
            'x-rapidapi-key': self.client.API_KEY
        }

    @commands.command()
    async def stats(self, ctx, *, country):
        "See COVID-19 Stats about a country."
        country = country.title()
        querystring = {"country": country}
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    self.stats_api_url, headers=self.headers,
                    params=querystring) as r:

                resp = await r.json()

                if resp["message"] == "Country not found. Returning all stats." \
                                      "Please use a country name found in the" \
                                    " data property.":
                    return await ctx.send("Country not found.")

                data = resp["data"]

                lastChecked = data["lastChecked"]
                timestamp = datetime.strptime(lastChecked,
                                              "%Y-%m-%dT%H:%M:%S.%fZ")

                e = discord.Embed(
                    title=f":bar_chart: {country} Stats :",
                    color=0xff0000,
                    timestamp=timestamp)

                dicts = data["covid19Stats"]
                confirmed = 0
                deaths = 0
                recovered = 0
                for x in dicts:
                    confirmed += x["confirmed"]
                    deaths += x["deaths"]
                    recovered += x["recovered"]

                e.add_field(
                    name=":mask: **Confirmed :**",
                    value=confirmed,
                    inline=True)
                e.add_field(
                    name=":skull: **Deaths :**",
                    value=deaths,
                    inline=True)
                e.add_field(
                    name=":dove: **Recovered :**",
                    value=recovered,
                    inline=True)
                e.set_footer(text="Last checked")

                async with cs.get(self.countrys_api_url + country) as r:
                    resp = await r.json()
                    countryCode = resp[0]["alpha2Code"]
                    e.set_thumbnail(url=self.flags_api_url.format(countryCode))

                await ctx.send(embed=e)


def setup(client):
    client.add_cog(Stats(client))
