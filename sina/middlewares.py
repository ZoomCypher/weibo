# encoding: utf-8
import random
from sina.user_agents import agents


class UserAgentMiddleware(object):
    """
    change User-agents
    """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """
    change cookie    
    """
    # def __init__(self):
        # self.cookie_pool = []
        
    def process_request(self, request, spider):
        # cookie = random.choice(self.cookie_pool)
        cookie = {'_T_WM':'9d2a0b73673813d614859bdad1a2f30b', 'SUB': '_2A253EfdeDeRhGeBK6lIW8i3JzziIHXVU_ZkWrDV6PUJbkdBeLVDWkW1NR-CqYYSLb4InvaD0FlHev6rXOfbMZQLs', 'SUHB': '08J7wh-7Mzgvxb', 'SCF': 'AtI_mo1dzV0t3FEBU1oce69xEOZhmRkd-DvaQHz8aPS8Bm0eoBy93Fbff_a3L8y9FGecbvikzCsFm08HAx0tx90.', 'SSOLoginState': '1511360271'}

        request.cookies = cookie

    def process_response(self, request, response, spider):
        if response.status in [300, 301, 302, 303]:
            try:
                redirect_url = response.headers["location"]
                if "login.weibo" in redirect_url or "login.sina" in redirect_url:
                    logger.warning("One Cookie need to be updating...")
                    self.process_request(request, spider)
                elif "weibo.cn/security" in redirect_url:  # killed
                    logger.warning("One Account is locked! Remove it!")
                    self.process_request(request, spider)
                elif "weibo.cn/pub" in redirect_url:
                    logger.warning(
                        "Redirect to 'http://weibo.cn/pub'!( Account:%s )" % request.meta["accountText"].split("--")[0])
                reason = response_status_message(response.status)
                return self._retry(request, reason, spider) or response
            except Exception:
                raise IgnoreRequest
        elif response.status in [403, 414]:
            logger.error("%s! Stopping..." % response.status)
            os.system("pause")
        else:
            return response