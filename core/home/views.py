from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework import authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action

from .models import Person
from .serializers import PeopleSerializer, LoginSerializer, RegisterSerializer

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({"status": False,"message": serializer.errors},status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=serializer.data["username"], password=serializer.data["password"])
        if not user:
            return Response({
                "status": False,
                "message": "invalid credentials or user not found"
            }, status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "status":True,
            "message": "user login",
            "token":str(token)
            },
            status=status.HTTP_200_OK
        )

class RegisterAPI(APIView):

    def post(self, request):
        data= request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({"status": False,"message": serializer.errors},status.HTTP_400_BAD_REQUEST)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"status":True, "message": "user created"}, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_200_OK, serializer.data)

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


@api_view(["POST"])
def login(request):
    data= request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({"message": "success"})
    return Response(serializer.errors)


class PersonAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            objs = Person.objects.all()
            page = request.GET.get("page", 1)
            page_size = 3
            paginator = Paginator(objs, page_size)
            serializer = PeopleSerializer(paginator.page(page), many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"status":False, "message": "invalid page"}, status.HTTP_404_NOT_FOUND)

        # serializer = PeopleSerializer(objs, many=True)


        # return Response({"message": "this is a get method"})

    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        # return Response({"message": "this is a post method"})

    def put(self, request):
        data = request.data
        obj = Person.objects.get(id = data["id"])
        serializer = PeopleSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        # return Response({"message": "this is a put method"})

    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data["id"])
        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        # return Response({"message": "this is a patch method"})

    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id = data["id"])
        obj.delete()
        return Response({"message":"person deleted"})
        # return Response({"message": "this is a delete method"})


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()
    http_method_names = ["get"] #restricts request methods. This allows only get method

    def list(self, request):
        search = request.GET.get("search")
        print(search)
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
        serializer = PeopleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response({"status": 200})


    # detail=False to ignore details in API
    # @action(detail=False, methods=["post"])
    # def send_mail_to_person(self, request):
    #     return Response({
    #         "status": True,
    #         "message": "email sent successfully"
    #     })


    # #to get details from API
    # @action(detail=True, methods=["POST"])
    # def send_mail_to_person(self, request, pk):
    #     print(pk)
    #     return Response({
    #         "status": True,
    #         "message": "email sent successfully"
    #     })


    @action(detail=True, methods=["GET"])
    def send_mail_to_person(self, request, pk):
        print(pk)
        return Response({
            "status": True,
            "message": "email sent successfully"
        })