from rest_framework import serializers
from .models import Person

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        # fields = ["name", "age"]
        fields = "__all__" #include all fields
        # fields = ["name"]  #include specific fields
        # exclude = ["name"] #used to exclude some of the fields

    #validate single input
    # def validate_age(self, data):
    #     if(data["age"]<18):
    #         raise serializers.ValidationError("Age should be greater than 18")
    #     return data

    #validate all inputs
    def validate(self,data):
        special_characters = "!@#$%^&*()_-=+<>?/"
        if any(c in special_characters for c in data["name"]):
            raise serializers.ValidationError("Name cannot contain special characters.")
        if(data["age"]<18):
            raise serializers.ValidationError("Age should be greater than 18")
        return data