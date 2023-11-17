from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ingredient
from .serializers import IngredientSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import re

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"})
        return Response(serializer.errors, status=400)

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid Credentials"}, status=400)


class CheckIngredientsView(APIView):
    def post(self, request, format=None):
        # Get the ingredients string from the request
        ingredients_string = request.data.get('ingredients', '')
        
        # Split the string into ingredients
        ingredients_list = self.parse_ingredients(ingredients_string)
        
        results = []
        for ingredient_name in ingredients_list:
            try:
                # Perform a case-insensitive lookup in the database
                ingredient = Ingredient.objects.get(name__iexact=ingredient_name.lower())
                if ingredient.is_unhealthy:
                    # Only add to results if the ingredient is unhealthy
                    result = {
                        'ingredient': ingredient_name,
                        'is_unhealthy': ingredient.is_unhealthy,
                        'description': ingredient.description,
                        'country_banned_in': ingredient.country_banned_in,
                        'severity': ingredient.severity
                    }
                    results.append(result)
            except Ingredient.DoesNotExist:
                # Ingredient not found, use default values
                # Since we don't want to return ingredients with is_unhealthy = False,
                # we don't add this result to the results list
                pass

        # If no unhealthy ingredients are found, return a list with an empty JSON object
        if not results:
            results.append({})

        return Response(results)

    def parse_ingredients(self, ingredients_string):
        # Replace symbols, newlines, tabs, etc., with commas
        cleaned_string = re.sub(r'[\[\]{}()*\n\t]', ',', ingredients_string)

        # Split the string by commas and remove extra spaces
        ingredients = [ingredient.strip() for ingredient in cleaned_string.split(',') if ingredient.strip()]

        # Replace multiple whitespaces with a single space and remove trailing periods
        ingredients = [re.sub(r'\s+', ' ', ingredient).rstrip('.').strip() for ingredient in ingredients]

        return ingredients
