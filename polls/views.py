from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice 
# Create your views here.
def index(request):
    questions = Question.objects.order_by('-pub_date')
    return render(request, 'index.html', { 'questions' : questions })

#get detail
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'detail.html', { 'question' : question })

#get specific question and return results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', { 'question' : question })

#vote function
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', { 'question' : question, 'error_message' : "You didn't select a choice" })
    else:
        selected_choice.vote += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))