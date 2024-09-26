from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from .models import About


def contact_send(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Mesajınız başarılı bir şekilde gönderildi.")
        return redirect("index")
    context = {
        "form": form
    }
    return render(request, "contact.html", context)


def about_view(request):
    about = About.objects.first()
    context = {
        "about": about
    }
    return render(request, "about.html", context)



# Create your views here.
