from django.shortcuts import render, redirect
from core.models import Competitions, Contests
from core.utils import competition_status, upload_file, get_extension, get_next_name
from django.conf import settings
from django.contrib import messages
import os


def competition_page(request, pk):
    competition = Competitions.objects.get(pk=pk)
    context = {
        'competition': competition
    }
    context.update({'status': competition_status(competition)})
    return render(request, 'competition.html', context=context)


def load_ans(request, pk):
    competition = Competitions.objects.get(pk=pk)
    if request.method == 'POST':
        task = request.POST['task']
        lang = request.POST['lang']
        code = request.POST.get('code', None)
        if not os.path.exists(f'{request.user.pk}\\'):
            os.mkdir(f'{request.user.pk}\\')
        name = get_next_name(f'{request.user.pk}\\')
        ext = get_extension(lang)
        if code == '\n' or code == '':
            upload_file(request.FILES['file'], f'{request.user.pk}\\', name+ext)
        else:
            with open(f'{request.user.pk}\\'+name+ext, 'w') as f:
                f.write(code)
        messages.info(request, 'Решение отправленно на проверку')
        return redirect('competition_page', competition.pk)
    else:
        context = {
            'competition': competition,
            'langs': settings.ACCEPTABLE_LANGUAGES
        }
        if request.GET.get('contest', ''):
            contest = Contests.objects.get(pk=request.GET.get('contest', ''))
            context.update({
                'contest': contest
            })
        return render(request, 'load_ans.html', context)