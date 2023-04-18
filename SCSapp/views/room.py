from django.shortcuts import render

def roomView(request, match_id):
    return render(request, "room.html", {'match_id':match_id})