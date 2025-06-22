from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None):
        if not phone_number:
            raise ValueError('Foydalanuvchi raqami kerak')
        user = self.model(phone_number=phone_number, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password=None):
        user = self.create_user(phone_number, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    phone_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.price} so'm"

class Hall(models.Model):
    name = models.CharField(max_length=100) 
    is_vip = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({'VIP' if self.is_vip else 'Oddiy'})"
    
class Table(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    seats = models.PositiveIntegerField()
    is_reserved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Stol {self.number} ({self.hall.name})"
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Kutilmoqda"),
        ("approved", "Tasdiqlandi"),
        ("rejected", "Rad etildi")
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} uchun {self.date} {self.time} da {self.table.number}"

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Kutilmoqda"),
        ("approved", "Tasdiqlandi"),
        ("rejected", "Rad etildi")
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='OrderItem')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} buyurtmasi ({self.get_status_display()})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item.name} x{self.quantity}"
    
