from django.db import models, router
from django.conf import settings

from isapilib.external.utilities import execute_query
from isapilib.api.models import UserAPI # Dont delete


class DynamicManager(models.Manager):
    _alias = None

    def using(self, alias):
        self._alias = alias
        return super().using(alias)

    def get_queryset(self):
        queryset = super().get_queryset()

        if isinstance(queryset.model._meta.db_table, dict):
            version = settings.DATABASES[self._alias]['INTELISIS_VERSION']
            db_table_options = queryset.model._meta.db_table

            try:
                queryset.model._meta.db_table = db_table_options[version]
            except KeyError:
                raise Exception(f'El modelo {queryset.model} no tiene una tabla para la versión {version}')

        return queryset


class BaseModel(models.Model):
    objects = DynamicManager()

    def _add_field(self, name):
        new_field = models.TextField(db_column=name)
        new_field.contribute_to_class(self, name)

    def get(self, name):
        if name not in [field.attname for field in self._meta.get_fields()]:
            self._add_field(name)

        return getattr(self, name)

    def set(self, name, value):
        if name not in [field.attname for field in self._meta.get_fields()]:
            self._add_field(name)

        setattr(self, name, value)

    def get_triggers(self, disabled=0, using=None):
        using = using or router.db_for_write(None)
        tb_name = self._meta.db_table
        query = 'SELECT name FROM sys.triggers WHERE parent_id = OBJECT_ID(%s) AND is_disabled = %s'
        response = execute_query(query, [tb_name, disabled], using=using)
        return response[0] if 0 < len(response) else []

    def enable_trigger(self, name, using=None):
        using = using or router.db_for_write(None)
        try:
            tb_name = self._meta.db_table
            execute_query(f'ENABLE TRIGGER [{name}] ON [{tb_name}]', using=using)
        except Exception:
            pass

    def disable_trigger(self, name, using=None):
        using = using or router.db_for_write(None)
        try:
            tb_name = self._meta.db_table
            execute_query(f'DISABLE TRIGGER [{name}] ON [{tb_name}]', using=using)
        except Exception:
            pass

    def save(self, *args, **kwargs):
        check_triggers = kwargs.pop('triggers', False)
        using = kwargs.get('using', router.db_for_write(None))
        triggers = None
        if not check_triggers:
            triggers = self.get_triggers(using=using)
            for tgr in triggers:
                self.disable_trigger(tgr[0], using=using)

        try:
            return super().save(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            if not check_triggers:
                for tgr in triggers:
                    self.enable_trigger(tgr[0], using=using)

    class Meta:
        abstract = True
