from django.shortcuts import render, redirect, get_object_or_404
from .models import DataItem, Statistic
from faker import Faker
from django.http import JsonResponse
from django.db.models import Sum
fake = Faker()

def main(request):
    qs = Statistic.objects.all()
    if request.method == 'POST':
        new_stat = request.POST.get('new-statistic')
        obj, _ = Statistic.objects.get_or_create(name=new_stat)
        return redirect('stats:dashboard', obj.slug)
    return render(request, 'stats/main.html', {'qs': qs})


def dashboard(request,slug):
    obj = get_object_or_404(Statistic, slug=slug)
    return render(request, 'stats/dashboard.html', {
        'name': obj.name,
        'slug': obj.slug,
        'data': obj.data,
        'user': request.user.username if request.user.username else fake.name()
    })

def chart_data(request,slug):
    obj = get_object_or_404(Statistic,slug=slug)
    qs = obj.data.values('owner').annotate(Sum('value'))
    chart_data = [x['value__sum'] for x in qs]
    chart_labels = [x['owner'] for x in qs]
    return JsonResponse({
        "chart_date":chart_data,
        "chard_labels":chart_labels
    })