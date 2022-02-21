from django.urls import path 
from . import views 
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('users/', views.register_user, name="register_user"),
    path('notes/', views.getOrSaveNotes, name="notes"),
    path('notes/<str:pk>', views.getOrUpdateOrDeleteNote, name="note"),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
