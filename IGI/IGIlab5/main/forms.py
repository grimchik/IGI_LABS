from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Service,Vacancy,Review, ClientProfile, Order,Company,Employee, Coupon,Vehicle,VehicleType,BodyType
from datetime import date
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'cost', 'description']
class CityForm(forms.Form):
    city = forms.CharField(label='Город')
class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'description']

class CustomVehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        driver_choices = kwargs.pop('driver_choices', None)
        super(CustomVehicleForm, self).__init__(*args, **kwargs)
        if driver_choices:
            self.fields['driver'].choices = driver_choices

    class Meta:
        model = Vehicle
        fields = ['name', 'vehicle_type', 'body_type', 'driver']
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'vehicle_type', 'body_type', 'driver']
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_discount(self):
            discount = self.cleaned_data['discount']
            if not (0 < discount <= 100):
                raise forms.ValidationError('Скидка должна быть в диапазоне от 0.01 до 100.00')
            return discount
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'email', 'phone', 'description', 'photo']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['company', 'coupon', 'description']

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        print("Company:", company)
        super(OrderForm, self).__init__(*args, **kwargs)
        if company:
            coupons = Coupon.objects.filter(company=company)
            print("Coupons:", coupons)
            self.fields['coupon'].queryset = coupons
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description']
class SignUpForm(UserCreationForm):
    CLIENT = 'client'
    DRIVER = 'driver'
    COMPANY_OWNER = 'company_owner'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (DRIVER, 'Driver'),
        (COMPANY_OWNER, 'Company Owner'),
    ]

    birthday = forms.DateField(
        help_text="Пользователь должен быть старше 18",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role', 'birthday')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            birthday = self.cleaned_data['birthday']
            age = (date.today() - birthday).days // 365
            ClientProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                age=age,
                birthday=birthday
            )
        return user

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        age = (date.today() - birthday).days // 365
        print(birthday.month,date.today().month)
        print(date.today().day,birthday.day)
        if age < 18:
            raise forms.ValidationError('Пользователь должен быть старше 18')
        if age == 18:
            eighteen = birthday.replace(year=birthday.year + 18)
            if eighteen > date.today():
                raise forms.ValidationError('Пользователь должен быть старше 18')
        return birthday
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 4}),
        }


class OrderEditForm(forms.ModelForm):
    driver = forms.ModelChoiceField(queryset=ClientProfile.objects.none())

    class Meta:
        model = Order
        fields = ['driver', 'cost']

    def __init__(self, *args, **kwargs):
        driver_choices = kwargs.pop('driver_choices', [])
        super(OrderEditForm, self).__init__(*args, **kwargs)
        self.fields['driver'].queryset = ClientProfile.objects.filter(id__in=[id for id, _ in driver_choices])