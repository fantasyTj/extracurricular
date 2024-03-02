import os
import random
import asyncio
import logging
import requests
from pyppeteer import launch

try:
    import nest_asyncio
except:
    os.system('pip install nest_asyncio')
    import nest_asyncio

nest_asyncio.apply()

pyppeteer_level = logging.WARNING
logging.getLogger('pyppeteer').setLevel(pyppeteer_level)
logging.getLogger('websockets.protocol').setLevel(pyppeteer_level)
pyppeteer_logger = logging.getLogger('pyppeteer')
pyppeteer_logger.setLevel(logging.WARNING)


class AtomExecutor(object):
    name = '知乎'
    base_url = 'https://www.zhihu.com/'

    def init(self):
        self.loop = asyncio.get_event_loop()
        self.browser = ''
        self.x96_js = 'D=window.zhimuhuan_x96=function(e){return __g._encrypt(encodeURIComponent(e))};exports.ENCRYPT_VERSION=A'
        self.x81_js = '{"x-zst-81":window.zhimuhuan_x81=f.xZst81})'

    def process_item(self, keyword):
        self.init()
        self.oppen_pyppeteer()
        self.loop.run_until_complete(self.go_to(keyword))

    async def go_to(self, keyword):
        url = "https://www.zhihu.com/search?type=content&q={}".format(keyword)
        try:
            await self.page.goto(url, options={'timeout': 1000 * 20})
        except:
            pass
        await asyncio.sleep(5)
        dimensions = await self.page.evaluate(f'varq=document.documentElement.scrollTop={555500}')
        check_96 = await self.page.evaluate("window.zhimuhuan_x96('{}')".format('460858518271c07cca7e6d7b9620ef8e'))
        check_81 = await self.page.evaluate('window.zhimuhuan_x81')
        return True

    async def intercept_network_request(self, request):
        if 'static.zhihu.com/heifetz/main.app' in request.url and '.js' in request.url:
            response = requests.request("GET", request.url, headers=request.headers, timeout=20)
            html = response.text
            x96_code = 'D=function(e){return __g._encrypt(encodeURIComponent(e))};exports.ENCRYPT_VERSION=A'
            x81_code = '{"x-zst-81":f.xZst81})'
            app_js = html.replace(x96_code, self.x96_js).replace(x81_code, self.x81_js)
            resp = {"body": app_js, "headers": response.headers, "status": response.status_code}
            await request.respond(resp)
        elif request.resourceType in ['image', 'media', 'eventsource', 'websocket']:
            await request.abort()
        else:
            await request.continue_()

    def oppen_pyppeteer(self):
        try:
            asyncio.get_event_loop().run_until_complete(self.browser.close())
        except:
            pass
        asyncio.get_event_loop().run_until_complete(self.PyppeteerMain())
        self.loop.run_until_complete(self.page.setRequestInterception(True))
        self.page.on('request', lambda request: asyncio.create_task(self.intercept_network_request(request)))

    async def PyppeteerMain(self):
        self.browser = await launch({
            'headless': True,
            'userDataDir': 'pyppeteer_data_for_cjt',
            'args': [
                '--no-sandbox',
                '--start-maximized',
                '--disable-gpu',
                '--disable-blink-features=AutomationControlled',
                '--user-agent={}'.format(self.get_ua()),
            ],
            'dumpio': True
        })
        self.page = await self.browser.newPage()
        await self.page.setUserAgent(self.get_ua())
        await self.page.setViewport({"width": 1920, "height": 1080})

    @staticmethod
    def get_ua():
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
        ]
        return random.choice(user_agent_list)


if __name__ == "__main__":
    function = AtomExecutor()
    function.process_item('手机')