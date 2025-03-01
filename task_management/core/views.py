from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from .models import User, Project, Category, Priority, Task 
from .serializers import UserSerializer, ProjectSerializer, CategorySerializer, PrioritySerializer, TaskSerializer 
from rest_framework.filters import SearchFilter 
from django_filters.rest_framework import DjangoFilterBackend 
import logging 
from rest_framework.permissions import IsAuthenticated 
from .permissions import IsAdmin, IsManager, IsEmployee
from django.shortcuts import render 
from .forms import ContactForm 

def contact_view(request): 
    if request.method == "POST": 
        form = ContactForm(request.POST) 
        if form.is_valid(): 
            name = form.cleaned_data['name'] 
            email = form.cleaned_data['email'] 
            message = form.cleaned_data['message'] 
            # You can process the form data (e.g., save to DB, send an email) 
            return render(request, 'success.html', {'name': name}) 
    else: 
        form = ContactForm() 

    return render(request, 'contact.html', {'form': form}) 





class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsManager]

 

class CategoryViewSet(ModelViewSet): 
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer 

 

class PriorityViewSet(ModelViewSet): 
    queryset = Priority.objects.all() 
    serializer_class = PrioritySerializer 

 

logger = logging.getLogger(__name__) 
class TaskViewSet(ModelViewSet): 
    queryset = Task.objects.all() 
    serializer_class = TaskSerializer 
    permission_classes = [IsEmployee]
    filter_backends = [DjangoFilterBackend, SearchFilter] 
    filterset_fields = ['project', 'priority', 'category'] 
    search_fields = ['title', 'description'] 
    permission_classes = [IsAuthenticated] 
    def perform_create(self, serializer): 
        logger.info("Creating a new task") 
        serializer.save() 