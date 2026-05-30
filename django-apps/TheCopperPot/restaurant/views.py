from django.shortcuts import render, redirect
from django.core.mail import send_mail

# Create your views here.
# ! The URL routing function views
def landing(request):
    return render(request, 'landing.html')

def about(request):
    return render(request, 'about.html')


#* Contact wiring
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(
            f'Message from {name}',
            message,
            email,
            ['copperpot144@gmail.com'],
        )
        return redirect('contacts')
    return render(request, 'contacts.html')



def menu(request):
    return render(request, 'menu.html')

