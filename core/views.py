from django.shortcuts import render


# Create your views here.
def bootstrap_filter_view(request):
    return render(request, "bootstrap_form.html")
