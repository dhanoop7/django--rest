from django.urls import path
from .import views
from .views import user_Login, BookView

urlpatterns = [
    path('register/', views.register_User, name='register'),
    path('login/', user_Login.as_view(), name='login'),
    path('verifyotp/', views.VerifyOtp, name='verifyotp'),
    path('books/', BookView.as_view(), name='books'),
]
