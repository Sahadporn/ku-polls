"""View for django poll application."""
import logging
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s] %(levelname)-2s %(message)s'
        },
        'file': {
            'format': '[%(asctime)s] %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

logging.basicConfig(format=format)
logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Return: user ip address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def detail(request, question_id):
    """Return HttpResponse object direct to detail page.

    Args:
        request: HttpRequest
        question_id: specific question id

    Returns:
        if question cannot vote return redirect to index page
        else return HttpResponse object to detail page
    """
    question = get_object_or_404(Question, pk=question_id)
    if (not question.can_vote()):
        messages.error(request, f"The '{question}' poll is already ended.")
        return HttpResponseRedirect(reverse('polls:index'))

    vote = Vote.objects.filter(question_id=question.id, user=request.user)
    if not vote.exists():
        vote = Vote.objects.create(user=request.user, voted=False, question_id=question.id)
        return render(request, 'polls/detail.html', {'question': question})
    else:
        vote = vote[:1].get()
        question.vote = vote
    return render(request, 'polls/detail.html', {'question': question})


class IndexView(generic.ListView):
    """Display the index view with question sorted from most recent to oldest."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class ResultsView(generic.DetailView):
    """Display the result view of a specific question."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Return HttpResponse object to results page for specific question.

    Args:
        request: HttpRequest
        question_id: specific question id

    Returns:
        if the choice have not been made direct to detail page with message
        else redirect to results page for specific question
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        messages.error(request, f'{"You didn not make a choice"}')
        return render(request, 'polls/detail.html', {
            'question': question, })
    else:
        vote = Vote.get_or_new(question.id, request.user)
        if vote.selected_choice_id != 0:
            prev_choice = question.choice_set.get(pk=vote.selected_choice_id)
            if selected_choice.id == prev_choice.id:
                return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
            prev_choice.decrease_vote()

        selected_choice.increase_vote()
        vote.save_choice(selected_choice.id)

        logger.info("IP: %s Username: %s Poll id: %d vote success", get_client_ip(request),
                    request.user.username, question_id)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
