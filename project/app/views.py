from django.shortcuts import render
from .analysis import generate_graphs

def dashboard(request):
    insights = generate_graphs()

    return render(request, 'dashboard.html', {
        "insights": insights
    })