from django.shortcuts import render
from core.models import Journal, Category
from django.db.models import Q


def is_query_params_valid(params):
    return params != '' and params is not None


# Create your views here.
def bootstrap_filter_view(request):
    qs = Journal.objects.all()
    list_category = Category.objects.all()

    title_contains = request.GET.get('title_contains')
    id_exact = request.GET.get('id_exact')
    title_or_author = request.GET.get('title_or_author')
    view_count_min = request.GET.get('view_count_min')
    view_count_max = request.GET.get('view_count_max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    category = request.GET.get('category')
    reviewed = request.GET.get('reviewed')
    not_reviewed = request.GET.get('not_reviewed')

    if is_query_params_valid(title_contains):
        qs = qs.filter(title__icontains=title_contains)

    if is_query_params_valid(id_exact):
        qs = qs.filter(id=id_exact)

    if is_query_params_valid(title_or_author):
        qs = qs.filter(
            Q(title__icontains=title_or_author) |
            Q(author__name__icontains=title_or_author)
        ).distinct()

    # Views Check
    if is_query_params_valid(view_count_min):
        qs = qs.filter(views__gte=view_count_min)

    if is_query_params_valid(view_count_max):
        qs = qs.filter(views__lte=view_count_max)

    # Publish Date Check
    if is_query_params_valid(date_min):
        qs = qs.filter(publish_date__gte=date_min)

    if is_query_params_valid(date_max):
        qs = qs.filter(publish_date__lte=date_max)

    # Category
    if is_query_params_valid(category) and category != 'Choose...':
        qs = qs.filter(category__name=category)

    # Reviewed
    if reviewed == 'on':
        qs = qs.filter(reviewed=True)

    elif not_reviewed == 'on':
        qs = qs.filter(reviewed=False)

    context = {
        'query_set': qs,
        'list_category': list_category
    }

    return render(request, "bootstrap_form.html", context)
