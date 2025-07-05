from django.urls import path, include
from rest_framework_nested import routers
from .views import CategoryViewSet, ProviderViewSet, RateProviderView, CommentViewSet

# El router principal ahora manejará tanto categorías como proveedores
router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'providers', ProviderViewSet, basename='provider')

# El router anidado para comentarios sigue igual
comments_router = routers.NestedSimpleRouter(router, r'providers', lookup='provider')
comments_router.register(r'comments', CommentViewSet, basename='provider-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
    path('providers/<int:pk>/rate/', RateProviderView.as_view(), name='rate-provider'),
]