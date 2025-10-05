from datetime import datetime, timedelta
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, Project, Objective, DailyCheckIn, Tip, Hobby
from .serializers import (
    UserSerializer, UserProfileSerializer, ProjectSerializer,
    ObjectiveSerializer, DailyCheckInSerializer, TipSerializer,
    HobbySerializer, OnboardingSerializer
)
from .llm_service import generate_daily_plan, generate_hobby_suggestion, generate_workout_plan


@api_view(['POST'])
@permission_classes([AllowAny])
def onboarding_view(request):
    serializer = OnboardingSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    from django.contrib.auth import authenticate
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    try:
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'Profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    try:
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'Profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def daily_plan_view(request):
    try:
        user = request.user
        profile = user.profile
        
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        existing_objectives = Objective.objects.filter(user=user, date=today)
        if existing_objectives.exists():
            serializer = ObjectiveSerializer(existing_objectives, many=True)
            return Response({
                'objectives': serializer.data,
                'message': 'Retrieved existing objectives for today'
            })
        
        objectives_list = generate_daily_plan(user, profile, yesterday)
        
        created_objectives = []
        for obj_description in objectives_list:
            objective = Objective.objects.create(
                user=user,
                description=obj_description,
                date=today
            )
            created_objectives.append(objective)
        
        serializer = ObjectiveSerializer(created_objectives, many=True)
        return Response({
            'objectives': serializer.data,
            'message': 'Daily plan generated successfully'
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def objectives_list_view(request):
    date_str = request.query_params.get('date')
    
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        date_obj = timezone.now().date()
    
    objectives = Objective.objects.filter(user=request.user, date=date_obj)
    serializer = ObjectiveSerializer(objectives, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def objective_update_view(request, pk):
    try:
        objective = Objective.objects.get(pk=pk, user=request.user)
    except Objective.DoesNotExist:
        return Response(
            {'error': 'Objective not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    is_completed = request.data.get('is_completed')
    if is_completed is not None:
        objective.is_completed = is_completed
        if is_completed:
            objective.completed_at = timezone.now()
        else:
            objective.completed_at = None
        objective.save()
    
    serializer = ObjectiveSerializer(objective)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def daily_checkin_view(request):
    serializer = DailyCheckInSerializer(data=request.data)
    if serializer.is_valid():
        date = serializer.validated_data.get('date', timezone.now().date())
        
        checkin, created = DailyCheckIn.objects.update_or_create(
            user=request.user,
            date=date,
            defaults={
                'mood': serializer.validated_data['mood'],
                'notes': serializer.validated_data.get('notes', '')
            }
        )
        
        serializer = DailyCheckInSerializer(checkin)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def random_tip_view(request):
    tip = Tip.objects.order_by('?').first()
    
    if tip:
        serializer = TipSerializer(tip)
        return Response(serializer.data)
    else:
        return Response(
            {'message': 'No tips available'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hobby_suggestion_view(request):
    try:
        user = request.user
        profile = user.profile
        
        suggestion = generate_hobby_suggestion(user, profile)
        
        return Response(suggestion)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def workout_plan_view(request):
    try:
        user = request.user
        profile = user.profile
        
        workout = generate_workout_plan(user, profile)
        
        return Response(workout)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class HobbyListCreateView(generics.ListCreateAPIView):
    serializer_class = HobbySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Hobby.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HobbyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HobbySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Hobby.objects.filter(user=self.request.user)
