from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Person
from .serializers import PeopleSerializer

# Create your views here.
@api_view(["GET", "POST", "PUT", "PATCH"])
def index(request):
    courses = {
            "course_name": "Python",
            "learn": ["Django", "Tornado", "Python", "Flask", "FastAPI"],
            "course_provider": "Scaler"
        }
    if request.method == "GET":
        print(request.GET) #prints query dict
        print(request.GET.get("search"))
        print(request.GET.get("page"))
        print("You have hit get method")
    elif request.method == "POST":
        print(request.data) # prints request body data
        print("You have hit get method")
    elif request.method == "PUT":
        print("You have hit put method")
    elif request.method == "PATCH":
        print("You have hit patch method")
    return Response(courses)

@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def person(request):
    #check request method
    if request.method == "GET":
        objs = Person.objects.all()
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data)

    elif request.method=="POST":
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "PUT":
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "PATCH":
        data = request.data
        obj = Person.objects.get(id = data["id"])
        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "DELETE":
        data = request.data
        obj = Person.objects.get(id = data["id"])
        obj.delete()
        return Response({"message":"person deleted"})