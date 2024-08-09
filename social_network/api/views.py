from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import User, FriendRequest, Friend
from .serializers import SignupSerializer, LoginSerializer, UserSerializer, FriendRequestSerializer, FriendSerializer

from datetime import timedelta
from django.utils import timezone



class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @csrf_exempt
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=400)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"}, status=200)

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.all()
        query = self.request.query_params.get('q', None)
        if query:
            queryset = queryset.filter(
                Q(email__iexact=query) |
                Q(name__icontains=query)
            )
        return queryset


class FriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Custom rate limiting: Allow only 3 friend requests per minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        friend_requests_last_minute = FriendRequest.objects.filter(
            from_user=request.user,
            timestamp__gte=one_minute_ago
        ).count()

        if friend_requests_last_minute >= 3:
            return Response({"error": "Rate limit exceeded. Only 3 friend requests are allowed per minute."},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        to_user_id = request.data.get('to_user')
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response({"status": "Friend request sent"}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def list_friends(request):
    friends = Friend.objects.filter(current_user=request.user).first()
    serializer = FriendSerializer(friends)
    return Response(serializer.data)

@api_view(['GET'])
def list_pending_requests(request):
    print(request.user)
    requests = FriendRequest.objects.filter(to_user=request.user)
    serializer = FriendRequestSerializer(requests, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def accept_request(request, From_user_id):
    try:
        # Get the friend request where the 'from_user' matches the provided ID and 'to_user' is the current user
        friend_request = FriendRequest.objects.get(from_user_id=From_user_id, to_user=request.user)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)
    if friend_request.to_user == request.user:
        Friend.make_friend(friend_request.from_user, request.user)
        Friend.make_friend(request.user, friend_request.from_user)
        friend_request.delete()
        return Response({'status': 'friend request accepted'})
    return Response({'status': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def reject_request(request, From_user_id):
    try:
        # Get the friend request where the 'from_user' matches the provided ID and 'to_user' is the current user
        friend_request = FriendRequest.objects.get(from_user_id=From_user_id, to_user=request.user)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)
    if friend_request.to_user == request.user:
        friend_request.delete()
        return Response({'status': 'friend request rejected'})
    return Response({'status': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
