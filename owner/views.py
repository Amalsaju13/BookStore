from django.shortcuts import render, redirect
from owner.forms import BookForm,OrderEditForm
from django.urls import reverse_lazy
from django.views.generic import View,ListView,CreateView,DetailView,UpdateView,TemplateView
from owner.models import Book
from customer.models import Order
from django.core.mail import send_mail

# Create your views here.

class AddBook(CreateView):
    model = Book
    form_class = BookForm
    template_name = "addbook.html"
    success_url = reverse_lazy("allbooks")
    # def get(self, request):
    #     form = BookForm()
    #     return render(request, "addbook.html", {"form": form})
    #
    # def post(self, request):
    #     form = BookForm(request.POST, files=request.FILES)
    #     if form.is_valid():
    #         form.save()
            # print(form.cleaned_data.get("book_name"))
            # print(form.cleaned_data.get("author"))
            # print(form.cleaned_data.get("price"))
            # print(form.cleaned_data.get("copies"))
            #
            # qs=Book(
            #     book_name=form.cleaned_data.get("book_name"),
            #     author=form.cleaned_data.get("author"),
            #     price=form.cleaned_data.get("price"),
            #     copies=form.cleaned_data.get("copies")
            # )
            # qs.save()

        #     return redirect("allbooks")
        #     # return render(request,"addbook.html",{"msg":"book added"})
        # else:
        #     return render(request, "addbook.html", {"form": form})


class BookListView(ListView):
    model=Book
    template_name="booklist.html"
    context_object_name="book"
    # def get(self, request):
    #     qs = Book.objects.all()
    #     return render(request, 'booklist.html', {'book': qs})


class BookDetailView(DetailView):
    model=Book
    template_name="bookdetail.html"
    context_object_name="book"
    pk_url_kwarg="id"


    # def get(self, request, *args, **kwargs):
    #     qs = Book.objects.get(id=kwargs.get("id"))
    #     return render(request, 'bookdetail.html', {'book': qs})


class BookDeleteView(View):
    def get(self, request, *args, **kwargs):
        qs = Book.objects.get(id=kwargs.get("id"))
        qs.delete()
        return redirect('allbooks')


class ChangeBook(UpdateView):
    model = Book
    template_name = "changebook.html"
    form_class = BookForm
    success_url = reverse_lazy('allbooks')
    pk_url_kwarg = "id"
    # def get(self, request, *args, **kwargs):
    #     qs = Book.objects.get(id=kwargs.get("id"))
    #     form = BookForm(instance=qs)
    #     return render(request, 'changebook.html', {'form': form})
    #
    # def post(self, request, *args, **kwargs):
    #     qs = Book.objects.get(id=kwargs.get("id"))
    #     form = BookForm(request.POST, instance=qs,files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('allbooks')
    #
class DashBoardView(TemplateView):
    template_name = 'dashboard.html'
    def get(self, request, *args, **kwargs):
        neworders=Order.objects.filter(status='orderplaced')
        return render(request,self.template_name,{"neworders":neworders})

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orderdetail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'id'


class OrderChangeView(UpdateView):
    model = Order
    template_name = "orderchange.html"
    form_class = OrderEditForm
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        order=Order.objects.get(id=kwargs['id'])
        return render(request,self.template_name,{"order":order,"form":self.form_class})

    def post(self, request, *args, **kwargs):
        order=Order.objects.get(id=kwargs['id'])
        form=OrderEditForm(request.POST,instance=order)
        if form.is_valid():
            deliverydate=str(form.cleaned_data.get("expected_delivery_date"))
            form.save()
            send_mail(
                "Order Notification",
                "Your order will be delivered on"+deliverydate,
                "geoamal12@gmail.com",
                ["amalsaju13@outlook.com"],
                fail_silently=False,
            )
            return redirect('dashboard')