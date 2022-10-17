from main import AmazonAuth


def reload_access_token():
    """
    reload access token
    """
    amazon_api = AmazonAuth()
    amazon_api.run()
