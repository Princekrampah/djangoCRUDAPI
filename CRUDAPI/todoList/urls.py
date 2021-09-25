from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserCreate, TodosListCreateView, TodosRetrieveUpdateDestroyAPIView


urlpatterns = [
    path("registration/", UserCreate.as_view()),
    path('', TodosListCreateView.as_view()),
    path('todos/<int:pk>/', TodosRetrieveUpdateDestroyAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]