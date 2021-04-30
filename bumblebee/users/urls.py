from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .api.views.auth_views import (
    LogoutView,
    RegisterView,
    VerifyEmailView,
    LoginView,
    ResendEmailVerificationView,
    SendResetPasswordView,
    ConfirmResetPasswordView,
)

registers = [
    path("register/", RegisterView.as_view(), name="register-user"),
]

logins = [
    path("login", LoginView.as_view(), name="login"),
    path("login/refresh", TokenRefreshView.as_view(), name="login-token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

email_verifications = [
    path(
        "email_verification/send",
        ResendEmailVerificationView.as_view(),
        name="send-email-verification",
    ),
    path(
        "email_verification/confirm/<slug:uidb64>/<slug:token>",
        VerifyEmailView.as_view(),
        name="confirm-email-verification",
    ),
]

password_resets = [
    path(
        "reset_password/send",
        SendResetPasswordView.as_view(),
        name="send-password-reset",
    ),
    path(
        "reset_password/confirm",
        ConfirmResetPasswordView.as_view(),
        name="confirm-password-reset",
    ),
]

user_methods = [
    # path("update_user/{username or id}", as_view(), name="update-user"),
    # path("delete_user/{username or id}", as_view(), name="delete-user"),
    # path("deactivate_user/{username or id}", as_view(), name="deactivate-user"),
]

urlpatterns = registers + logins + email_verifications + password_resets + user_methods
