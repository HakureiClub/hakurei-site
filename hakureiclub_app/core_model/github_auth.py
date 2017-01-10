import aiohttp
from mu_sanic.config import loop

GITHUB_BASE = 'https://github.com/login/oauth/authorize'
CLIENT = ''
SECRET = ''
SCOPE = 'repo'
loop = loop


class authit:
    def getGitHubAuth():
        return GITHUB_BASE + '?client_id=' + \
                CLIENT + '&scope=user%20admin:org%20repo&allow_singup=false'

    async def getToken(code):
        payload = {"client_id": CLIENT, "client_secret": SECRET, "code": code}
        headers = {'Accept': 'application/json'}
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.post(
                    'https://github.com/login/oauth/access_token/',
                    data=payload,
                    headers=headers
                    ) as resp:
                return await resp.json()


class getuser:
    async def getusername(token):
        authheaders = {'Authorization': 'token '+token}
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(
                    'https://api.github.com/user',
                    headers=authheaders
                    ) as resp:
                return await resp.json()

    async def getorg(name, token):
        authheaders = {'Authorization': 'token '+token}
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(
                    'https://api.github.com/orgs/HakureiClub/\
                            memberships/%s' % name,
                    headers=authheaders
                    ) as resp:
                return resp.status
