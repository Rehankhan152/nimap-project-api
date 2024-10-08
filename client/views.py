from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone 
from .models import Client, Project
from .serializers import ClientSerializer,ProjectListSerializer, ClientUpdateSerializer,ProjectCreateSerializer, ClientDetailSerializer, ProjectDetailSerializer

# List all clients
class ClientListView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Retrieve, and delete a client
class ClientDetailView(generics.RetrieveDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated]

# Update a client
class ClientUpdateView(generics.UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())
        

# Create a new project for a client
class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        client = get_object_or_404(Client, id=kwargs['client_id'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save(client=client, created_by=request.user)
        output_serializer = ProjectDetailSerializer(project)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


# List all projects assigned to the logged-in user

class UserProjectListView(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)