from django.apps import AppConfig


class AssetsConfig(AppConfig):
    name = 'asset'

    def ready(self):
    	import asset.signals

