from django.shortcuts import render
from core.models import Journal
from django.db.models import Q


# Create your views here.
def bootstrap_filter_view(request):
    qs = Journal.objects.all()

    title_contains = request.GET.get('title_contains')
    id_exact = request.GET.get('id_exact')
    title_or_author = request.GET.get('title_or_author')

    if title_contains != '' and title_contains is not None:
        qs = qs.filter(title__icontains=title_contains)

    if id_exact != '' and id_exact is not None:
        qs = qs.filter(id=id_exact)

    if title_or_author != '' and title_or_author is not None:
        qs = qs.filter(
            Q(title__icontains=title_or_author) |
            Q(author__name__icontains=title_or_author)
        ).distinct()

    context = {
        'query_set': qs
    }

    return render(request, "bootstrap_form.html", context)
