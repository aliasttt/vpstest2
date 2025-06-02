from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Room(models.Model):
    ROOM_TYPES = [
        ('deluxe', 'Deluxe Oda'),
        ('suite', 'Suite Oda'),
        ('executive', 'Executive Oda'),
    ]
    
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    capacity = models.IntegerField(default=2)
    size = models.IntegerField(help_text='Size in square meters', default=30)
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)
    amenities = models.JSONField(default=list)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_room_type_display()} - {self.name}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('confirmed', 'Onaylandı'),
        ('cancelled', 'İptal Edildi'),
        ('completed', 'Tamamlandı'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation for {self.guest_name} - {self.room}"

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Beklemede'),
        ('completed', 'Tamamlandı'),
        ('failed', 'Başarısız'),
        ('refunded', 'İade Edildi'),
    ]
    
    PAYMENT_METHODS = [
        ('credit_card', 'Kredi Kartı'),
        ('bank_transfer', 'Banka Transferi'),
    ]
    
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.reservation} - {self.amount}"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Yıldız'),
        (2, '2 Yıldız'),
        (3, '3 Yıldız'),
        (4, '4 Yıldız'),
        (5, '5 Yıldız'),
    ]
    
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reservation.guest_name} - {self.rating} stars"
