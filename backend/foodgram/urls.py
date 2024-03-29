from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'api/docs/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path(
        'api/docs/openapi-schema.yml',
        TemplateView.as_view(
            template_name='openapi-schema.yml',
            content_type='application/x-yaml'
        ), name='openapi-schema'
    ),
]
