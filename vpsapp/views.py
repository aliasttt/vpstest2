from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import *
from .forms import *

def home(request):
    return render(request, 'home.html')

def contact_us(request):
    if request.method == 'POST':
        form = Contactusform(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']

            email_subject = f"Yeni Mesaj: {name}"
            email_message = f"""
            İsim: {name}
            E-posta: {email}
            Telefon: {phone}
            Konu: {subject}
            
            Mesaj:
            {text}
            """
            from_email = 'aliasadi3853@gmail.com'
            recipient_list = ['aliasadi3853@gmail.com']

            try:
                send_mail(
                    email_subject,
                    email_message,
                    from_email,
                    recipient_list,
                    fail_silently=False,
                )
                messages.success(request, 'Mesajınız başarıyla gönderildi.')
                return redirect('contact')
            except Exception as e:
                messages.error(request, 'Mesaj gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.')
                print(f"E-posta gönderme hatası: {e}")
    else:
        form = Contactusform()

    return render(request, 'contact/contact.html', {'form': form})

def about_us(request):
    return render(request, 'about/about.html')

def rooms(request):
    return render(request, 'rooms/rooms.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return redirect('payment', reservation_id=reservation.id)
    else:
        form = ReservationForm()
    return render(request, 'reservation/reservation.html', {'form': form})

def payment(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.reservation = reservation
            payment.save()
            messages.success(request, 'Ödeme başarıyla tamamlandı.')
            return redirect('home')
    else:
        form = PaymentForm()
    return render(request, 'payment/payment.html', {'form': form, 'reservation': reservation})

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Değerlendirmeniz için teşekkür ederiz.')
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'review/review.html', {'form': form})
