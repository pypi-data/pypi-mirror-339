from django.apps import AppConfig


class MozillaDjangoOidcDbConfig(AppConfig):
    name = "mozilla_django_oidc_db"
    default_auto_field = "django.db.models.AutoField"

    def ready(self) -> None:
        from . import checks  # noqa
        from . import signals  # noqa
