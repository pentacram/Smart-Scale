from django.apps import AppConfig


class ScaleSetConfig(AppConfig):
    name = 'scale_set'
    def ready(self):
        import scale_set.signals
        # import scale_set.serials