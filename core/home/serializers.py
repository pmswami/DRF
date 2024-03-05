from rest_framework import serializers
from .models import Person

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        # fields = ["name", "age"]
        fields = "__all__" #include all fields
        # fields = ["name"]  #include specific fields
        # exclude = ["name"] #used to exclude some of the fields