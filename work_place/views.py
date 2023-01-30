from django.shortcuts import render
from django.views import View

from client.views import auth_decoration


class WorkPlaceView(View):
    @auth_decoration
    def get(self, request):
        return render(request,"work_place/work_place.html")
