
from django.shortcuts import render, redirect
from owner.models import Book
from django.views.generic import View,CreateView,ListView,DetailView
from django.urls import reverse_lazy
from customer.forms import UserRegistrationForm, LoginForm,PasswordResetForm,OrderForm,ReviewForm
from django.contrib.auth import authenticate, login,logout
from customer.models import Carts,Order,Reviews
from django import forms
from django.contrib.auth.models import User
from customer.decorators import sign_in_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Sum


# Create your views here.
@method_decorator(sign_in_required,name='dispatch')
class CustomerIndex(ListView):
    model = Book
    template_name = "custhome.html"
    context_object_name = "book"

    # def get(self, request, *args, **kwargs):
    #     qs = Book.objects.all()
    #     return render(request, "custhome.html", {'book': qs})

class SignUpView(CreateView):
    model=User
    form_class=UserRegistrationForm
    template_name="signup.html"
    success_url=reverse_lazy('signin')
    # def get(self, request, *args, **kwargs):
    #     form = UserRegistrationForm()
    #     return render(request, "signup.html", {'form': form})
    #
    # def post(self, request, *args, **kwargs):
    #     form = UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('signin')
    #     else:
    #         return render(request, 'signup.html', {'form': form})
    #

class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'signin.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                print('login success')
                login(request,user)
                return redirect('home')
            else:
                print('login failed')
                return render(request, 'signin.html', {'form': form})

@sign_in_required
def SignOut(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

@method_decorator(sign_in_required,name='dispatch')
class PasswordResetView(View):
    def get(self,request,*args,**kwargs):
        form=PasswordResetForm()
        return render(request,'password_reset.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get('oldpassword')
            newpassword=form.cleaned_data.get('newpassword')
            user=authenticate(request,username=request.user,password=oldpassword)
            if user:
                user.set_password(newpassword)
                user.save()
                return redirect('signin')
            else:
                return render(request, 'password_reset.html', {'form': form})
        else:
            return render(request, 'password_reset.html', {'form': form})

@sign_in_required
def AddToCart(request,*args,**kwargs):
    book=Book.objects.get(id=kwargs['id'])
    user=request.user
    cart=Carts(product=book,user=user)
    cart.save()
    messages.success(request,"Item Added to Cart")
    return redirect('home')

@method_decorator(sign_in_required,name='dispatch')
class ViewMyCart(ListView):
    model = Carts
    template_name = 'mycart.html'
    context_object_name = "carts"

    # def get_queryset(self):
    #     return Carts.objects.filter(user=self.request.user).exclude(status="cancelled").order_by('-date')
    def get(self,request,*args,**kwargs):
        carts=Carts.objects.filter(user=self.request.user).exclude(status="cancelled").order_by('-date')
        total=Carts.objects.filter(user=request.user).exclude(status="cancelled").aggregate(Sum("product__price"))
        gtotal=total.get("product__price__sum")
        context={
            "carts":carts,"total":gtotal
        }
        return render(request,"mycart.html",context)


def remove_from_cart(request,*args,**kwargs):
    cart=Carts.objects.get(id=kwargs['id'])
    cart.status="cancelled"
    cart.save()
    messages.error(request,"Your item has been removed from Cart")
    return redirect('viewmycart')

class OrderCreateView(CreateView):
    form_class = OrderForm
    template_name = 'ordercreate.html'
    model = Order

    def post(self,request,*args,**kwargs):
        cart_id=kwargs.get('c_id')
        product_id=kwargs.get('p_id')
        form=OrderForm(request.POST)
        if form.is_valid():
            order=form.save(commit=False)
            product=Book.objects.get(id=product_id)
            user=request.user
            order.product=product
            order.user=request.user
            order.save()
            cart=Carts.objects.get(id=cart_id)
            cart.status="orderplaced"
            cart.save()
            messages.success(request,"Your order has been placed")
        return redirect('home')

class OrdersListView(ListView):
    model = Order
    template_name = 'orderlist.html'
    context_object_name = 'orders'
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-date')

class CreateReview(CreateView):
    model = Reviews
    form_class = ReviewForm
    template_name = "post_review.html"

    def post(self, request, *args, **kwargs):
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.posted_by=self.request.user
            product=Book.objects.get(id=kwargs["id"])
            review.product=product
            review.save()
            messages.success(request,"Your review has been posted")
            return redirect('home')
        else:
            return render(request,self.template_name,{"form":form})

class BookDetailView(DetailView):
    model = Book
    template_name = "detailview.html"
    context_object_name = "book"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        book=self.get_object()
        reviews=book.reviews.all()
        context["reviews"]=reviews
        return context


