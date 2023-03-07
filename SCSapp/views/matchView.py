from SCSapp.models.Match import AbstractMatch
from django.shortcuts import render, get_object_or_404

def matchView(request, match_id):
    if request.method == 'GET':
        match = get_object_or_404(AbstractMatch, pk=match_id)
        match_data = match.getData()
        return render(request, 'match.html', match_data)
