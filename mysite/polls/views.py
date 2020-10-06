from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     # context = { 'latest_question_list': latest_question_list, }
#     # return HttpResponse(template.render(context, request))
#     context = {'latest_question_list': latest_question_list, }
#     return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk = question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})
    question = get_object_or_404(Question, pk=question_id)
    if (not question.can_vote()):
        messages.error(request, f"The '{question}' poll is already ended.")
        return HttpResponseRedirect(reverse('polls:index'))
    return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, 'polls/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be published in the future).
        """
        # published_polls = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        # return published_polls.filter(end_date__gt=timezone.now()).order_by('-pub_date')
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        # return published_polls

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'

#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # if (question.is_poll_end()):
    #     messages.error(request, f"This poll is already ended.")
    #     return HttpResponseRedirect(reverse('polls:index'))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        messages.error(request, f'{"You didn't make a choice"}')
        return render(request, 'polls/detail.html', {'question': question, })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class resetView(generic.ListView):
    template_name = 'polls/reset.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

def reset(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    q.reset_votes()
    messages.info(request, f"Reset votes for poll {q.question_text}")
    return HttpResponseRedirect(reverse('polls:reset_index'))
    # return render(request, reverse('polls:reset_index'))
