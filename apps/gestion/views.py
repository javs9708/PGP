from django.shortcuts import render

def gestionMenu(request):
    return render(request, 'gestion/Gestion.html')
