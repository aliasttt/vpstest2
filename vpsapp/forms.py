from django import forms  
from django.utils.translation import gettext_lazy as _
from datetime import date
from .models import *


class Contactusform(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız'}),
        error_messages={'required': 'Lütfen adınızı giriniz.'}
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta adresiniz'}),
        error_messages={
            'required': 'Lütfen e-posta adresinizi giriniz.',
            'invalid': 'Lütfen geçerli bir e-posta adresi giriniz.'
        }
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon numaranız'}),
        error_messages={'required': 'Lütfen telefon numaranızı giriniz.'}
    )
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Konu'}),
        error_messages={'required': 'Lütfen bir konu giriniz.'}
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Mesajınız',
            'rows': 5
        }),
        error_messages={'required': 'Lütfen mesajınızı giriniz.'}
    )

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'guest_name', 'guest_email', 'guest_phone', 'check_in', 'check_out', 'adults', 'children', 'special_requests']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        adults = cleaned_data.get('adults')
        children = cleaned_data.get('children')

        if check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError(_('Çıkış tarihi giriş tarihinden sonra olmalıdır.'))
            
            if (check_out - check_in).days > 14:
                raise forms.ValidationError(_('Maksimum 14 günlük rezervasyon yapabilirsiniz.'))

        if adults and children:
            total_guests = adults + children
            if total_guests > 4:
                raise forms.ValidationError(_('Toplam misafir sayısı 4 kişiyi geçemez.'))

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.RadioSelect,
        }

    card_number = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'pattern': '[0-9\s]{13,19}',
            'maxlength': '19'
        })
    )
    expiry_date = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/YY',
            'pattern': '(0[1-9]|1[0-2])\/([0-9]{2})',
            'maxlength': '5'
        })
    )
    cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CVV',
            'pattern': '[0-9]{3,4}',
            'maxlength': '4'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        if payment_method == 'credit_card':
            card_number = cleaned_data.get('card_number')
            expiry_date = cleaned_data.get('expiry_date')
            cvv = cleaned_data.get('cvv')

            if not all([card_number, expiry_date, cvv]):
                raise forms.ValidationError(_('Kredi kartı bilgileri eksik.'))
            
            # Validate card number using Luhn algorithm
            if not self._is_valid_card_number(card_number.replace(' ', '')):
                raise forms.ValidationError(_('Geçersiz kart numarası.'))
            
            # Validate expiry date
            if not self._is_valid_expiry_date(expiry_date):
                raise forms.ValidationError(_('Geçersiz son kullanma tarihi.'))

    def _is_valid_card_number(self, card_number):
        digits = [int(d) for d in card_number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(divmod(d * 2, 10))
        return checksum % 10 == 0

    def _is_valid_expiry_date(self, expiry_date):
        try:
            month, year = expiry_date.split('/')
            month = int(month)
            year = int(year)
            return 1 <= month <= 12 and year >= 23
        except:
            return False

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect,
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment.strip()) < 10:
            raise forms.ValidationError(_('Yorumunuz en az 10 karakter olmalıdır.'))
        return comment


