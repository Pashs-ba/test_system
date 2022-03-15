from core.models import VariantQuestionGenerator, VariantQuestion, QuestionAns


def get_variant(request, question):
    if VariantQuestion.objects.filter(generator=VariantQuestionGenerator.objects.get(question=question).pk, user=request.user.pk):
        return VariantQuestion.objects.filter(generator=VariantQuestionGenerator.objects.get(question=question).pk, user=request.user.pk)[0]
    elif VariantQuestion.objects.filter(generator = VariantQuestionGenerator.objects.get(question=question).pk).order_by('user')[0].user == None:
        variant = VariantQuestion.objects.filter(generator = VariantQuestionGenerator.objects.get(question=question).pk).order_by('user')[0]
        variant.user = request.user
        return variant
    else:
        return 0
def variant(request, user, question):
    variant = get_variant(request, question)
    print(variant.ans)
    if variant.ans['type'] == 0:
        QuestionAns(user=user,
                        question=question,
                            ).save()