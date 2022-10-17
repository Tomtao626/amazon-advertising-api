from api.ad.ad_api import ProClient


class Profiles(ProClient):

    def register(self, **params):
        """
        只能在沙盒环境使用 用于新建账户
        :param params:
        :return:
        """
        self.uri_path = "/v2/profiles/register"
        self.data = params
        self.method = "put"
        return self.execute()

    def get_profiles(self):
        """
        获取账号信息
        :return:
        """
        self.uri_path = "/v2/profiles?apiProgram=billing&profileTypeFilter=seller&validPaymentMethodFilter=true"
        self.method = "get"
        return self.execute()
