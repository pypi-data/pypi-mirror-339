from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connections

from isapilib.api.models import SepaBranch
from isapilib.core.exceptions import SepaException


def add_conn(user, branch: SepaBranch):
    try:
        user_model_path = getattr(settings, 'AUTH_USER_MODEL', 'isapilib.UserAPI')
        branch_model_path = getattr(settings, 'BRANCH_MODEL', 'isapilib.SepaBranch')
        permission_model_path = getattr(settings, 'PERMISSION_MODEL', 'isapilib.SepaBranchUsers')

        user_model = apps.get_model(user_model_path, require_ready=False)
        branch_model = apps.get_model(branch_model_path, require_ready=False)
        permission_model = apps.get_model(permission_model_path, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError as e:
        if settings.AUTH_USER_MODEL in str(e):
            raise ImproperlyConfigured(
                f"AUTH_USER_MODEL refers to model '{settings.AUTH_USER_MODEL}' that has not been installed"
            )
        elif settings.BRANCH_MODEL in str(e):
            raise ImproperlyConfigured(
                f"BRANCH_MODEL refers to model '{settings.BRANCH_MODEL}' that has not been installed"
            )
        elif settings.PERMISSION_MODEL in str(e):
            raise ImproperlyConfigured(
                f"PERMISSION_MODEL refers to model '{settings.PERMISSION_MODEL}' that has not been installed"
            )
        else:
            raise e

    try:
        permission_model.objects.get(iduser=user, idbranch=branch)
        conn = f'external-{branch.id}'
        if conn not in connections.databases:
            connections.databases[conn] = create_conn(branch)
        return conn
    except user_model.DoesNotExist:
        raise SepaException('The user does not exist')
    except branch_model.DoesNotExist:
        raise SepaException('The agency does not exist', user)
    except permission_model.DoesNotExist:
        raise SepaException('You do not have permissions on the agency', user, branch)


def get_version(version=6000):
    version = version or 6000

    if 5000 > version >= 4000:
        return '4000'

    return '6000'


def create_conn(_branch):
    return {
        'ENGINE': 'mssql',
        'NAME': _branch.conf_db if _branch.conf_db else '',
        'USER': _branch.conf_user if _branch.conf_user else '',
        'PASSWORD': _branch.conf_pass if _branch.conf_pass else '',
        'HOST': _branch.conf_ip_ext if _branch.conf_ip_ext else '',
        'PORT': _branch.conf_port if _branch.conf_port else '',
        'INTELISIS_VERSION': get_version(_branch.version),
        'TIME_ZONE': None,
        'CONN_HEALTH_CHECKS': None,
        'CONN_MAX_AGE': None,
        'ATOMIC_REQUESTS': None,
        'AUTOCOMMIT': True,
        'OPTIONS': settings.DATABASES['default'].get('OPTIONS')
    }
