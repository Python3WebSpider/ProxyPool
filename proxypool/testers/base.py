from proxypool.setting import TEST_DONT_SET_MAX_SCORE, PROXY_SCORE_INIT, PROXY_SCORE_MAX, PROXY_SCORE_MIN


class BaseTester(object):
    test_url = ""
    key = ""
    test_dont_set_max_score = TEST_DONT_SET_MAX_SCORE
    proxy_score_init = PROXY_SCORE_INIT
    proxy_score_max = PROXY_SCORE_MAX
    proxy_score_min = PROXY_SCORE_MIN

    def headers(self):
        return None

    def cookies(self):
        return None

    async def parse(self, html, url, proxy, expr='{"code":0'):
        return True if expr in html else False
