from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.validators import MinValueValidator
from datetime import date, timedelta
def validate_driver_age(value):
    if value < 18 or value > 70:
        raise ValidationError('Возраст водителя должен быть от 18 до 70 лет.')

class VehicleType(models.Model):
    PICKUP = 'Pickup'
    TRUCK = 'Truck'
    VAN = 'Van'
    VEHICLE_TYPE_CHOICES = [
        (PICKUP, 'Pickup'),
        (TRUCK, 'Truck'),
        (VAN, 'Van'),
    ]

    name = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.name

class BodyType(models.Model):
    CLOSED = 'Closed'
    OPEN = 'Open'
    REFRIGERATED = 'Refrigerated'
    BODY_TYPE_CHOICES = [
        (CLOSED, 'Closed'),
        (OPEN, 'Open'),
        (REFRIGERATED, 'Refrigerated'),
    ]

    name = models.CharField(max_length=15, choices=BODY_TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400,default='Описание по умолчанию')
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='companyprofile',
                                 null=True, blank=True)
    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)]  # Проверка, что стоимость не меньше 0
    )
    description = models.TextField()
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Driver(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(validators=[validate_driver_age])
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='drivers')

    def __str__(self):
        return self.name

class CargoType(models.Model):
    FRAGILE = 'Fragile'
    PERISHABLE = 'Perishable'
    CARGO_TYPE_CHOICES = [
        (FRAGILE, 'Fragile'),
        (PERISHABLE, 'Perishable'),
    ]

    name = models.CharField(max_length=15, choices=CARGO_TYPE_CHOICES, unique=True)
    suitable_body_types = models.ManyToManyField(BodyType, related_name='suitable_cargos')

    def __str__(self):
        return self.name

class Order(models.Model):
    COST_STATUS_CHOICES = [
        (True, 'Completed'),
        (False, 'Not completed')
    ]

    driver = models.ForeignKey('ClientProfile', on_delete=models.CASCADE, related_name='orders_driver',null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='orders')
    text = models.CharField(max_length=50,default="",blank=True,null=True)
    status = models.BooleanField(choices=COST_STATUS_CHOICES, default=False)
    client = models.ForeignKey('ClientProfile', on_delete=models.CASCADE, related_name='orders_client', null=True, blank=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=200,default="default", null=True)
    def __str__(self):
        return f"Order {self.id} by {self.company.name}"

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='coupons')

    def is_active(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        return self.code

class ClientProfile(models.Model):
    CLIENT = 'client'
    DRIVER = 'driver'
    COMPANY_OWNER = 'company_owner'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (DRIVER, 'Driver'),
        (COMPANY_OWNER, 'Company Owner'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order, related_name='clients', blank=True)
    services = models.ManyToManyField(Service, related_name='services', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENT)
    age = models.PositiveIntegerField(default=18)
    vehicle = models.OneToOneField('Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    birthday = models.DateField(default=date(2000, 1, 1))

    def clean(self):
        if self.birthday:
            today = date.today()
            age = (today - self.birthday).days // 365
            if age < 18:
                raise ValidationError(('Пользователь должен быть старше 18 лет'))

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    body_type = models.ForeignKey(BodyType, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vehicles')
    driver = models.ForeignKey(ClientProfile, related_name='vehicles', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.vehicle_type.name} - {self.body_type.name})"

class Article(models.Model):
    title = models.CharField(max_length=200)
    short_text = models.CharField(max_length=255)
    full_text = models.TextField()
    image = models.ImageField(upload_to='images/',default='images/default.jpg')
    def __str__(self):
        return self.title
class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    company = models.OneToOneField('Company', on_delete=models.CASCADE, related_name='vacancy')

    def __str__(self):
        return self.title
class Employee(models.Model):
    phone_regex = RegexValidator(regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
                                 message="Номер телефона должен быть в формате: +375 (29) XXX-XX-XX")
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='employees_photos/',default='images/default.jpg')
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(validators=[phone_regex], max_length=19, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.full_name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews',default=None)

    def __str__(self):
        return f"Отзыв от {self.user.username} с рейтингом {self.rating}"

class Term(models.Model):
    term = models.CharField(max_length=200, unique=True, verbose_name="Термин")
    definition = models.TextField(verbose_name="Определение")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.term

class FAQ(models.Model):
    question = models.CharField(max_length=200, unique=True, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.question