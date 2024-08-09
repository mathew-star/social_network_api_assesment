from django.urls import path
from .views import SignupView, LoginView, logout_view, UserSearchView, FriendRequestView, accept_request, reject_request, list_friends, list_pending_requests

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/search/', UserSearchView.as_view(), name='user-search'),
    path('friends/request/', FriendRequestView.as_view(), name='friend-request'),
    path('friends/accept/<int:From_user_id>/', accept_request, name='accept-request'),
    path('friends/reject/<int:From_user_id>/', reject_request, name='reject-request'),
    path('friends/', list_friends, name='friend-list'),
    path('friends/pending/', list_pending_requests, name='pending-requests'),
]
