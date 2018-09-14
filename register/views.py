from django.shortcuts import render
from django.views import generic
from .models import User

# Create your views here.
class LogInView(generic.DetailView):
    template_name = 'register/login.html'
    context_object_name = 'uname'

