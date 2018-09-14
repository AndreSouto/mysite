from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Question, Choice
from django.utils import timezone
from django.http import Http404
from django.core.urlresolvers import reverse

# Create your views here.
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Choice
	template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    latest_question_list = Question.objects.order_by('-pub_date')[:10]
    return render(request, 'polls/vote.html', {'latest_question_list': latest_question_list})
