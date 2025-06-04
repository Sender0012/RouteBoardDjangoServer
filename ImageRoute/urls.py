from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views, api_views
from django.contrib.auth import views as auth_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# --- Swagger schema imports ---
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Image Route API",
      default_version='v1',
      description="API do zarządzania trasami i punktami na obrazach.",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('route/create/', views.create_route, name='create_route'),
    path('route/<int:route_id>/', views.route_detail, name='route_detail'),
    path('route/<int:route_id>/add_point/', views.add_point, name='add_point'),
    path('route/<int:route_id>/delete_point/<int:point_id>/', views.delete_point, name='delete_point'),

    #Boardgame
    # path('boards/', views.gameboard_list, name='gameboard_list'),
    # path('boards/new/', views.create_game_board, name='create_gameboard'),
    # path('board/<int:board_id>/', views.board_detail, name='board_detail'),
    # path('boards/<int:board_id>/edit/', views.edit_game_board, name='edit_gameboard'),

    path('gameboards/', views.gameboard_list, name='gameboard_list'),
    path('gameboards/new/', views.gameboard_create, name='gameboard_create'),
    path('gameboards/edit/<int:board_id>/', views.gameboard_update, name='gameboard_update'),
    path('gameboards/<int:pk>/delete/', views.gameboard_delete, name='gameboard_delete'),


    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Routes API
    path('api/routes/', api_views.RouteListCreateAPIView.as_view(), name='api_routes'),
    path('api/routes/<int:pk>/', api_views.RouteDetailAPIView.as_view(), name='api_route_detail'),

    # RoutePoints API
    path('api/routes/<int:route_id>/points/', api_views.RoutePointListCreateAPIView.as_view(),
        name='api_points'),
    path('api/routes/<int:route_id>/points/<int:point_id>/', api_views.RoutePointDeleteAPIView.as_view(),
        name='api_point_delete'),
    # Swagger docs
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)