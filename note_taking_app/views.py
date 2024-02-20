from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, request
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from note_taking_app.serializers import UserSerializer, NoteSerializer, HistorySerializer
from note_taking_app.models import Note, History


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'Token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class Create(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        print(request.user)
        Note.objects.create(user=request.user, content=request.data["content"])
        return Response({'message': "successfully created"})


class NoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, note_id):
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

        if note.user != request.user and not note.shared_users.filter(id=request.user.id).exists():
            return Response({'error': 'You do not have permission to view this note'}, status=status.HTTP_403_FORBIDDEN)

        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, note_id):
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff and request.user != note.user and not note.shared_users.filter(
                id=request.user.id).exists():
            return Response({'error': 'You do not have permission to update this note'},
                            status=status.HTTP_403_FORBIDDEN)

        updated_content = request.data.get('content', '')

        History.objects.create(user=request.user, note=note, content=updated_content, modified_at=timezone.now())

        note.content += '\n' + "good" + updated_content
        note.save()
        print(note)

        return Response({'message': 'Note updated successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_note(request):
    try:
        note_id = request.data.get('note_id')
        user_ids = request.data.get('users', [])
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

    if note.user != request.user:
        return Response({'error': 'You do not have permission to share this note'}, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.filter(id__in=user_ids.split(","))
    note.shared_users.add(*users)
    note.save()

    return Response({'message': 'Note shared successfully'}, status=status.HTTP_200_OK)


class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, note_id):
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

        if note.user != request.user and not note.shared_users.filter(id=request.user.id).exists():
            return Response({'error': 'You do not have permission to view the version history of this note'},
                            status=status.HTTP_403_FORBIDDEN)

        # Retrieve all NoteHistory objects associated with the note
        version_history = History.objects.filter(note=note)
        print(version_history)

        # Serialize the version history data
        serializer = HistorySerializer(version_history, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
