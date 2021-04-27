from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api.views.auth_views import RegisterView, ActivateView, LoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register-user"),
    path("login", LoginView.as_view(), name="login"),
    path("login/refresh", TokenRefreshView.as_view(), name="login-token-refresh"),
    # path("logout/", as_view(), name="logout"),
    # path(
    #     "user/<str:username>/email_verification/send",
    #     Activate.as_view(),
    #     name="send-email-verification",
    # ),
    path(
        "user/<str:username>/email_verification/confirm/<slug:uidb64>/<slug:token>",
        ActivateView.as_view(),
        name="confirm-email-verification",
    ),
    # path("reset_password/send", as_view(), name="send-password-reset"),
    # path("reset_password//", as_view(), name="confirm-password-reset"),
    # path("update_user/{username or id}", as_view(), name="update_user"),
    # path("delete_user/{username or id}", as_view(), name="delete_user"),
    # path("deactivate_user/{username or id}", as_view(), name="deactivate_user"),
]
