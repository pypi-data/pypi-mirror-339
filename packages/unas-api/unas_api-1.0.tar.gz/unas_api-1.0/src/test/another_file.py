from ..unas_api.unas import UnasAPIBase, Product

unas_client = UnasAPIBase("aa")

print(unas_client.get_unas_feed_url())
