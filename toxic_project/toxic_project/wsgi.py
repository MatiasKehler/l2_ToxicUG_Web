import os
from django.core.wsgi import get_wsgi_application

# Apuntamos a la configuración del proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toxic_project.settings')

application = get_wsgi_application()