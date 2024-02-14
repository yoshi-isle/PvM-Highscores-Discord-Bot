from imgurpython import ImgurClient

from settings import get_environment_variable

class ImgurInterface():
    def __init__(self) -> None:
        client_id = get_environment_variable("CLIENT_ID")
        client_secret = get_environment_variable("CLIENT_SECRET")
        access_token = get_environment_variable("ACCESS_TOKEN")
        refresh_token = get_environment_variable("REFRESH_TOKEN")

        self.client = ImgurClient(client_id, client_secret, access_token, refresh_token)

    
    def send_image(self, url: str, config: dict):
        return self.client.upload_from_url(url=url, config=config, anon=False)

    async def send_image_async(self, loop, url, config):
        # None uses the default executor (ThreadPoolExecutor)
        return await loop.run_in_executor(None, self.send_image, url, config)
