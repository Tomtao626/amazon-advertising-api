from api import ad
from api.ad import conf
from api.ad.ad_api import Client
from api.ad.conf import profile_id_dict
from config.__init__ import read_conf
from crawl.bid_crawl import BidCrawl


def get_auth_api():
    """
    get_auth_api
    :return:
    """
    client_auth_conf = read_conf(conf_type='amazon_client_auth')
    auth_api = ad.Auth(client_id=client_auth_conf['ClientId'],
                       client_secret=client_auth_conf['ClientSecret'],
                       redirect_uri=client_auth_conf['RedirectUri'],
                       region=client_auth_conf['region'])
    return auth_api


class AmazonAuth(object):
    """
    amazon auth
    """

    def __init__(self):
        self.login_url = get_auth_api().get_grant_url()
        self.my_url = "https://www.amazon.com"
        self.region = "NA"

    def click_login(self):
        """
        点击链接 跳转到登录页面
        :return:
        """
        print(self.login_url)
        # self.driver.get(self.login_url)
        # # # 显式等待
        # self.driver.implicitly_wait(10)
        # selector = self.driver.find_element_by_id("ap_email")
        # selector.send_keys(self.username)
        # selector = self.driver.find_element_by_id("ap_password")
        # selector.send_keys(self.password)
        # selector = self.driver.find_element_by_id("signInSubmit")
        # selector.click()

    @staticmethod
    def get_auth_token_code():
        """
        获取授权token
        :return: access_token
        """
        # https: // www.baidu.com /?code = ANqaZKfzmkOGPWWzrWqY & scope = profile
        # access_token, refresh_token = get_auth_api().get_refresh_token(code="ANNOSXROwtBwhCtAVpah")
        refresh_token = ""
        access_token = get_auth_api().get_new_access_token(refresh_token=conf.REFRESH_TOKEN)
        print(access_token)
        print("-*-" * 30)
        # print(refresh_token)
        return access_token
        # pass

    def get_profile(self):
        """
        获取账号信息
        :return: response
        """
        # access_token = conf.ACCESS_TOKEN
        profile_api = ad.Profiles(  # access_token=conf.ACCESS_TOKEN,
            access_token=self.get_auth_token_code(),
            region=read_conf(conf_type='amazon_client_auth')['region'],
            client_id=read_conf(conf_type='amazon_client_auth')['ClientId'])
        profile_api.get_profiles()
        print("--end--" * 20)
        # print(response)

    def get_client_info(self):
        client_info = {'access_token': self.get_auth_token_code(),
                       'profile_id': profile_id_dict[self.region],
                       'region': read_conf(conf_type='amazon_client_auth')['region'],
                       'client_id': read_conf(conf_type='amazon_client_auth')['ClientId']}
        return client_info

    def get_campaigns(self):
        """
        get_campaigns
        :return:response
        """
        report_api = ad.sp_products.Campaigns(**self.get_client_info())
        params = {}
        report_api.get_campaigns(params=params)

    def get_reports(self):
        """
        about report
        :return:response
        """
        report_api = ad.sp_products.Reports(**self.get_client_info())
        params = {
            # "stateFilter": "enabled",
            # "campaignType": "sponsoredProducts",
            # "segment": "query",
            "reportDate": "20210801",
            "metrics": "campaignName,campaignId,impressions,clicks,cost,attributedConversions14d,attributedSales14d"
        }
        resp = report_api.request_report(record_type='campaigns', params=params)
        if resp["reportId"] and resp["status"] == "SUCCESS":
            download_resp = report_api.get_report(report_id=resp["reportId"])
            print("--0--" * 30)
            print(download_resp)

    def get_adgroups(self):
        """
        adgroups
        :return:
        """
        adgroup_api = ad.sp_products.AdGroup(**self.get_client_info())
        params = {}
        adgroup_api.get_ad_group(params=params)

    def update_keywords(self):
        """
        update keyword bid
        :return:
        """
        keyword_apis = ad.sp_products.Keywords(**self.get_client_info())
        # params = [
        #               {
        #                 "campaignId": xxxxxxxxxxxxx,
        #                 "adGroupId": xxxxxxxxxxxxx,
        #                 "state": "enabled",
        #                 "keywordText": "RM4mini Test",
        #                 "nativeLanguageKeyword": "",
        #                 "nativeLanguageLocale": "zh_CN",
        #                 "matchType": "exact",
        #                 "bid": 0.05
        #               }
        #             ]
        update_params = [
            {
                "keywordId": "xxxxxxxxxxxxx",
                "state": "enabled",
                "bid": 1.2
            }
        ]
        # keyword_apis.update_keywords(params=update_params)

    def run(self):
        """
        运行主函数
        :return:
        """
        # self.wait_input()
        self.click_login()
        self.get_profile()
        self.get_campaigns()
        self.get_reports()
        self.get_adgroups()
        # self.update_keywords()


if __name__ == "__main__":
    # amz = AmazonAuth()
    # amz.run()
    bid_api = BidCrawl()
    bid_api.start_crawl()
