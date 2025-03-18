"""URLConf for al_wazeer.ui"""

from django.contrib.auth import views as auth
from django.urls import path

from al_wazeer.ui import views


# Create your URLConf here.
app_name = "al-wazeer"

auth_urls = [
    path("accounts/login/", auth.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", views.SignupView.as_view(), name="signup"),
    path("accounts/profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "accounts/<int:pk>/update/", views.UserUpdateView.as_view(), name="update-user"
    ),
    path(
        "accounts/<int:pk>/delete/", views.UserDeleteView.as_view(), name="delete-user"
    ),
    path(
        "accounts/password/change/",
        auth.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "accounts/password/change/done/",
        auth.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "accounts/password/reset/",
        auth.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "accounts/password/reset/done/",
        auth.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/password/reset/<uidb64>/<token>/",
        auth.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password/reset/complete/",
        auth.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

admin_urls = [
    path("assistants/", views.AssistantListView.as_view(), name="assistants"),
    path(
        "assistants/new/", views.AssistantCreateView.as_view(), name="create-assistant"
    ),
    path(
        "assistants/<int:pk>/",
        views.AssistantDetailView.as_view(),
        name="view-assistant",
    ),
    path(
        "assistants/<int:pk>/update/",
        views.AssistantUpdateView.as_view(),
        name="update-assistant",
    ),
    path(
        "assistants/<int:pk>/delete/",
        views.AssistantDeleteView.as_view(),
        name="delete-assistant",
    ),
]

user_urls = [
    path("chats/", views.ChatListView.as_view(), name="chats"),
    path("chats/new/", views.ChatCreateView.as_view(), name="create-chat"),
    path("chats/<int:pk>/", views.ChatDetailView.as_view(), name="view-chat"),
    path(
        "chats/<int:pk>/details/",
        views.ChatDetailView.as_view(template_name="ui/detail/chat_details.html"),
        name="view-chat-details",
    ),
    path("chats/<int:pk>/update/", views.ChatUpdateView.as_view(), name="update-chat"),
    path("chats/<int:pk>/delete/", views.ChatDeleteView.as_view(), name="delete-chat"),
    path(
        "chats/<int:id>/message/<int:pk>/update/",
        views.MessageUpdateView.as_view(),
        name="update-message",
    ),
    path(
        "chats/<int:id>/message/<int:pk>/delete/",
        views.MessageDeleteView.as_view(),
        name="delete-message",
    ),
]

urlpatterns = (
    [path("", views.IndexView.as_view(), name="index")]
    + auth_urls
    + admin_urls
    + user_urls
)
