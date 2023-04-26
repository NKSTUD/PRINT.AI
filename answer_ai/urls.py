"""answer_ai URL Configuration
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from my_ai.views import index

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', index, name='home'),
                  path('printai/', include('my_ai.urls')),
                  path('accounts/', include('accounts.urls')),
                  path('memberships/', include('memberships.urls')),
                  path('tinymce/', include('tinymce.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
