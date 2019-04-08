from .celery import app as celery_app

# 这一步会确保当Django项目运行时这个app总是被import
__all__=('celery_app',)
