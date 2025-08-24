DJANGO_CACHE_APP_LABEL = "django_cache"


class CacheRouter:
    """Route cache queries to a separate "cache" database."""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == DJANGO_CACHE_APP_LABEL:
            return "cache"

        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == DJANGO_CACHE_APP_LABEL:
            return "cache"

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == DJANGO_CACHE_APP_LABEL:
            return db == "cache"

        return None
