from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Отдельно прописал url, чтобы указать формат письма HTML,
    # иначе отправит как txt, поэтому в прошлый раз
    # так странно ссылка выглядела
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy("auth_password_reset_done"),
            html_email_template_name="registration/password_reset_email.html",
        ),
        name="auth_password_reset",
    ),
    path("", include("registration.backends.default.urls")),
]
