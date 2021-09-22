from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from volaa.views import logout_view
# generate schema view to see the schema
from rest_framework.schemas import get_schema_view
#for documentation
from rest_framework.documentation import include_docs_urls
# for auth token
from rest_framework.authtoken import views

# drf documentation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="VolaaAPI",
      default_version='v1',
      description="Volaa Backend",
      terms_of_service="https://www.volaa.app/policies/terms/",
      contact=openapi.Contact(email="fredricknjeri64@gmail.com"),
      license=openapi.License(name="Volaa License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('logout/', logout_view, name='logout'),
                  path('users/', include('users.urls')),
                  path('drivers/', include('drivers.urls')),
                  path('shops/', include('shops.urls')),
                  path('orders/', include('orders.urls')),
                  path('docs/', include_docs_urls(title='VolaaAPI')),
                  path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
                  # path('schema', get_schema_view(
                  #     title="Volaa",
                  #     description="API for Volaa ",
                  #     version="1.0.0"
                  # ), name='openapi-schema'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
