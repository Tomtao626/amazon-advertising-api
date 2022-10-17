

from ..ad_api import Client


class ProductAds(Client):

    def get_product_ads_by_id(self, ad_id):
        self.method = "get"
        self.uri_path = "/v2/sp/productAds/{}".format(ad_id)
        return self.execute()

    def delete_product_ads_by_id(self, ad_id):
        self.method = "delete"
        self.uri_path = "/v2/sp/productAds/{}".format(ad_id)
        return self.execute()

    def get_product_ads(self, params):
        self.method = "get"
        self.uri_path = "/v2/sp/productAds"
        self.data = params
        return self.execute()

    def create_product_ads(self, params):
        self.method = "post"
        self.uri_path = "/v2/sp/productAds"
        self.data = params
        return self.execute()

    def update_product_ads(self, params):
        self.method = "put"
        self.uri_path = "/v2/sp/productAds"
        self.data = params
        return self.execute()

    def get_product_ads_extended_by_id(self, ad_id):
        self.method = "get"
        self.uri_path = "/v2/sp/productAds/extended/{}".format(ad_id)
        return self.execute()

    def get_product_ads_extended(self, params):
        self.method = "get"
        self.uri_path = "/v2/sp/productAds/extended"
        self.data = params
        return self.execute()



