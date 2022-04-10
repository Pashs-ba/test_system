from threading import Thread

from django.shortcuts import redirect, render
from django.db.models import Count 

from core.decorators import admin_only
from core.models import VariantQuestion, VariantQuestionGenerator

from ..forms import QuestionGeneratorForm
from ..utils import generate_variants_question


@admin_only
def quest_generator_page(request):
    return render(request, 'question_generator/management.html', {'generators': VariantQuestionGenerator.objects.all().order_by('name')})


@admin_only
def generator_delete(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = VariantQuestionGenerator.objects.get(pk=int(i))
            a.delete()
        return redirect('question_generator_manage')
    else:
        return render(request, 'question_generator/delete.html', {'to_del': request.GET['to_del']})

        
@admin_only
def question_gen_create(request):
    if request.method == 'POST':
        model = QuestionGeneratorForm(request.POST, request.FILES)
        print(model.is_valid())
        if model.is_valid():
            model = model.save()
            Thread(target=generate_variants_question, args=[model.var_count, model.pk, model.generator]).start()
            return redirect('question_generator_manage')
    else:
        
        return render(request, 'question_generator/create.html', {'form': QuestionGeneratorForm()})  

@admin_only
def question_generator(request, pk):
    if request.method == 'POST':
        model = QuestionGeneratorForm(request.POST, request.FILES, instance=VariantQuestionGenerator.objects.get(pk=pk))
        if model.is_valid():
            count = VariantQuestionGenerator.objects.annotate(variant_count=Count('variantquestion')).get(pk=pk).variant_count
            model = model.save()
            if int(model.var_count) == 0:
                variants = VariantQuestionGenerator.objects.get(pk=pk).variantquestion_set.all().order_by('user')
                for i in variants:
                    i.delete()
            elif model.var_count > count:
                Thread(target=generate_variants_question, args=[model.var_count-count, model.pk, model.generator]).start()
            elif model.var_count < count:
                variants = VariantQuestionGenerator.objects.get(pk=pk).variantquestion_set.all().order_by('user')
                to_del = count-model.var_count
                for i in range(to_del):
                    variants[i].delete()
        return redirect('question_generator_manage')
    else:
        print(VariantQuestionGenerator.objects.annotate(variant_count=Count('variantquestion')).get(pk=pk).variant_count)
        return render(request, 'question_generator/update.html', {'form': QuestionGeneratorForm(instance=VariantQuestionGenerator.objects.get(pk=pk)), 
                                                                  'model': VariantQuestionGenerator.objects.get(pk=pk), 
                                                                  'variants': VariantQuestionGenerator.objects.get(pk=pk).variantquestion_set.all().order_by('-user')})


@admin_only
def delete_variant_question(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = VariantQuestion.objects.get(pk=int(i))
            a.generator.var_count -= 1
            a.generator.save()
            a.delete()
        return redirect('question_generator_manage')
    else:
        return render(request, 'question_generator/delete_variant.html', {'to_del': request.GET['to_del']})
