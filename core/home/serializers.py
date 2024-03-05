from rest_framework import serializers
from .models import Person, Color

class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model= Color
        fields = ["color_name"]

class PeopleSerializer(serializers.ModelSerializer):

    # color = ColorSerializer(many = True)
    color = ColorSerializer()

    color_info = serializers.SerializerMethodField() #this method is implemented down below by name get_color_info()

    class Meta:
        model = Person
        # fields = ["name", "age"]
        fields = "__all__" #include all fields
        # fields = ["name"]  #include specific fields
        # exclude = ["name"] #used to exclude some of the fields

        #depth is used to add related fields depth
        # depth = 1

    #add SerializerMethodFields
    def get_color_info(self, obj):
        color_obj = Color.objects.get(id= obj.color.id)
        return {"color_name":color_obj.color_name, "hex_code": "#000"}
        # return "India"

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