# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.views import generic

from django.http import Http404

from django.shortcuts import get_object_or_404, render

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'votings/index.html'
    context_object_name = 'question_text'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'votings/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'votings/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'votings/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.vote += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('votings:results', args=(question.id,)))
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'votings/results.html', {'question': question})
