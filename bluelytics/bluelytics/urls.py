from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('dolar_blue.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
