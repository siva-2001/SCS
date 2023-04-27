from django.shortcuts import render

def roomView(request, match_id):
    return render(request, "room.html", {'match_id':match_id})

def translationView(request, match_id):
    return render(request, "translation.html", {'match_id':match_id})