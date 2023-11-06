from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login/')
def recipes(request):
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get("recipe_name")
        recipe_description = data.get("recipe_description")
        recipe_image = request.FILES.get('recipe_image')

        Recipe.objects.create(
            recipe_name = recipe_name,
            recipe_description = recipe_description,
            recipe_image = recipe_image
        )

        return redirect("/recipes/")
    query_set = Recipe.objects.all()

    if request.GET.get('search'):
        query_set = query_set.filter(recipe_name__icontains = request.GET.get('search'))
        # print(request.GET.get('search'))

    return render(request, "vege/recipes.html", context={'recipes':query_set})

@login_required(login_url="/login/")
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id = id)
    queryset.delete()
    return redirect('/recipes/')

@login_required(login_url='/login/')
def update_recipe(request, id):
    queryset = Recipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST
        recipe_name = data.get("recipe_name")
        recipe_description = data.get("recipe_description")
        recipe_image = request.FILES.get('recipe_image')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if recipe_image:
            queryset.recipe_image = recipe_image
        
        queryset.save()

        return redirect('/recipes/')

    return render(request, "vege/update_recipe.html", context={'recipes': queryset})

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        user = authenticate(username= username, password = password)

        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/recipes/')
                
    return render(request, "accounts/login.html")

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.error(request, "Username Already exist")
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        
        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully")

    return render(request, "accounts/register.html")