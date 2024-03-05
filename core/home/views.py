from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(["GET", "POST", "PUT", "PATCH"])
def index(request):
    courses = {
            "course_name": "Python",
            "learn": ["Django", "Tornado", "Python", "Flask", "FastAPI"],
            "course_provider": "Scaler"
        }
    if request.method == "GET":
        print("You have hit get method")
    elif request.method == "POST":
        print("You have hit get method")
    elif request.method == "PUT":
        print("You have hit put method")
    elif request.method == "PATCH":
        print("You have hit patch method")
    return Response(courses)