from django.shortcuts import render, redirect
from django.views.generic import View
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages

class BaseView(View):
    views = {}
    views['category'] = Category.objects.filter(status='active')
class HomeView(BaseView):
    def get(self,request):
        self.views['sliders'] = Slider.objects.filter(status = 'active')
        self.views['ads'] = Ad.objects.all()
        self.views['brands'] = Brand.objects.filter(status = 'active')
        self.views['hots'] = Item.objects.filter(status = 'active', label='hot')
        self.views['new'] = Item.objects.filter(status = 'active', label='new')
        return render(request,'index.html',self.views)
class CategoryItemView(BaseView):
    def get(self,request,slug):
        category_id = Category.objects.get(slug=slug).id
        self.views['cat_items'] = Item.objects.filter(category=category_id)
        return render(request, 'category.html', self.views)

class ItemSearchView(BaseView):
    def get(self,request):
        search = request.GET.get('search',None)
        if search is None:
            return redirect('/')
        else:
            self.views['search_item'] = Item.objects.filter(title__icontains = search)
            return render(request, 'search.html',self.views)

        return render(request,'search.html')

class ItemDetailView(BaseView):
    def get(self, request, slug):
        self.views['items_details'] = Item.objects.filter(slug=slug)
        return render(request, 'product-list.html', self.views)

def signup(request):
    if request.method == "POST":
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,'This username is already taken')
                return redirect('home:signup')
            elif User.objects.filter(email = email).exists():
                messages.error(request,'This email is already taken')
                return redirect('home:signup')
            else:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    first_name = f_name,
                    last_name = l_name,
                )
                user.save()
                messages.success(request,'You are sucesfully registered.')
                return redirect('home:signup')
        else:
            messages.error(request, 'This password doesnt match')
            return redirect('home:signup')
    return render(request,'signup.html')
