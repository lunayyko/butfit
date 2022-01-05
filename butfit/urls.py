from django.urls import path, re_path, include

# from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg       import openapi, generators

# class BothHttpAndHttpsSchemaGenerator(generators.OpenAPISchemaGenerator):
#     def get_schema(self, request=None, public=False):
#         schema = super().get_schema(request, public)
#         schema.schemes = ["http", "https"]
#         return schema

urlpatterns = [
    path('', include('butfitapp.urls')),
]

# schema_view = get_schema_view(
#     openapi.Info(
#         title            = "Butfit API",
#         default_version  = "v0",
#         description      = "Butfit API 문서",
#         license          = openapi.License(name="고유영"),
#     ),
#     public             = True,
#     # permission_classes = (permissions.AllowAny,),
#     generator_class    = BothHttpAndHttpsSchemaGenerator,
# )

# urlpatterns += [
#     re_path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
#     re_path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     re_path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]