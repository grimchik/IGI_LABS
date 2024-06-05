from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .forms import OrderEditForm,CustomVehicleForm,ServiceForm,ReviewForm,CityForm,VacancyForm,VehicleForm, SignUpForm , OrderForm, CompanyForm, EmployeeForm,CouponForm
from .models import Term,FAQ,Vehicle, ClientProfile,Driver,Service, Vacancy , Coupon, Article,Company, Employee,Vacancy, Review, Order, Coupon
from .utils import get_weather
from django.db.models import Avg
from django.utils import timezone
import calendar
import pytz
from datetime import datetime
import requests
from django.db.models import Q
import logging
from django.db.models import Sum

logger = logging.getLogger(__name__)


def get_crypto_market_data(api_key, symbol):
    url = f"https://rest.coinapi.io/v1/exchangerate/{symbol}/USD"
    headers = {'X-CoinAPI-Key': api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        logger.info(f"Успешно получены данные для символа {symbol}")
        return data
    else:
        logger.error(f"Не удалось получить данные для символа {symbol}. Код статуса: {response.status_code}")
        return None
def add_driver_to_company(request):
    if request.method == 'POST':
        selected_driver_username = request.POST.get('driver')
        try:
            selected_driver = ClientProfile.objects.get(user__username=selected_driver_username)
            current_user_company = request.user.clientprofile.company
            if selected_driver.company:
                logger.warning(f"Попытка добавления водителя {selected_driver_username} в компанию, когда он уже привязан к другой компании.")
                return redirect('company_list')
            selected_driver.company = current_user_company
            selected_driver.save()
            logger.info(f"Водитель {selected_driver_username} успешно добавлен в компанию {current_user_company.name}.")
            return redirect('company_list')
        except ClientProfile.DoesNotExist:
            logger.error(f"Водитель с именем пользователя {selected_driver_username} не найден.")
            return redirect('company_list')
    else:
        return redirect('company_list')

def add_driver(request):
    drivers_without_company = ClientProfile.objects.filter(role='driver', company=None)
    return render(request, 'main/add_driver.html',{'drivers': drivers_without_company})


def view_statistic(request):
    company = request.user.clientprofile.company
    clients = ClientProfile.objects.filter(company=company)
    avg_age = clients.aggregate(avg_age=Avg('age'))['avg_age']
    company_stats = []
    orders = Order.objects.filter(company=company)
    total_cost = orders.aggregate(total_cost=Sum('cost'))['total_cost']
    total_cost = float(total_cost)
    forecast = [total_cost * factor for factor in [2, 2.5, 3, 3.5, 4, 4.5]]
    company_stats.append({
        'company': company.name,
        'average_age': avg_age,
        'total_cost': total_cost,
        'forecast': forecast
        })

    context = {
        'company_stats': company_stats
    }
    return render(request, 'main/statistics.html', context)

def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    company = request.user.clientprofile.company
    drivers = ClientProfile.objects.filter(role='driver', company=company)
    driver_choices = [(driver.id, driver.user.username) for driver in drivers]
    discount = order.coupon.discount if (order.coupon and order.coupon.is_active) else 0

    if request.method == 'POST':
        form = OrderEditForm(request.POST, instance=order, driver_choices=driver_choices)
        if form.is_valid():
            order = form.save(commit=False)

            if discount:
                order.cost -= order.cost * (discount /100)
            order.save()
            logger.info(f"Заказ {order.id} успешно отредактирован.")
            return redirect('view_orders')
        else:
            logger.error(f"Форма редактирования заказа {order.id} невалидна: {form.errors}")
    else:
        form = OrderEditForm(instance=order, driver_choices=driver_choices)

    context = {
        'form': form,
        'discount': discount,
    }
    return render(request, 'main/edit_order.html', context)


def add_service_client(request):
    client_profile = ClientProfile.objects.get(user=request.user)
    all_services = Service.objects.all()
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        client_profile.services.add(service)
        return redirect('make_service_client')
    context = {
        'all_services': all_services
    }
    return render(request, 'main/add_service_client.html', context)
def client_services(request):
    client_profile = ClientProfile.objects.get(user=request.user)
    client_services = client_profile.services.all()
    total_spent = client_services.aggregate(total_spent=Sum('cost'))['total_spent']
    context = {
        'client_services': client_services,
        'total_spent': total_spent if total_spent else 0
    }
    return render(request, 'main/client_services.html', context)

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('view_orders')
    return render(request, 'main/delete_order.html', {'order': order})
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.company = request.user.clientprofile.company
            service.save()
            return redirect('view_services')
    else:
        form = ServiceForm()
    return render(request, 'main/add_service.html', {'form': form})

def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('view_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'main/edit_service.html', {'form': form})

def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        return redirect('view_services')
    return render(request, 'main/delete_service.html', {'service': service})
def view_drivers(request):
    company = request.user.clientprofile.company
    drivers = ClientProfile.objects.filter(role='driver',company=company)
    return render(request, 'main/drivers.html', {'drivers': drivers})

def view_services(request):
    company = request.user.clientprofile.company
    services = Service.objects.filter(company=company)
    return render(request, 'main/services.html', {'services': services})

def view_orders(request):
    company = request.user.clientprofile.company
    orders = Order.objects.filter(company=company)
    return render(request, 'main/orders.html', {'orders': orders})

def crypto_page(request):
    api_key = "B3AE47E4-255C-402A-AF18-19AE673787EC"
    symbol = "BTC"
    crypto_data = get_crypto_market_data(api_key, symbol)
    return render(request, 'main/crypto_page.html', {'crypto_data': crypto_data})
def weather_page(request):
    city = ''
    if 'city' in request.GET:
        city = request.GET['city']
    weather_data = get_weather(city)
    if weather_data is not None:
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
    else:
        weather_description = "Невозможно получить данные о погоде"
        temperature = "Н/Д"
        humidity = "Н/Д"
    return render(request, 'main/weather_page.html', {'weather_description': weather_description, 'temperature': temperature, 'humidity': humidity})

def add_vacancy(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = request.user.clientprofile.company
            vacancy.save()
            return redirect('view_vacancies')
    else:
        form = VacancyForm()
    return render(request, 'main/add_vacancy.html', {'form': form})

def edit_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    if request.method == 'POST':
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            return redirect('view_vacancies')
    else:
        form = VacancyForm(instance=vacancy)
    return render(request, 'main/edit_vacancy.html', {'form': form})

def delete_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    if request.method == 'POST':
        vacancy.delete()
        return redirect('view_vacancies')
    return render(request, 'main/delete_vacancy.html', {'vacancy': vacancy})
def view_vacancies(request):
        company = request.user.clientprofile.company
        vacancies = Vacancy.objects.filter(company=company)
        return render(request, 'main/view_vacancies.html', {'vacancies': vacancies, 'company': company})


def add_vehicle(request):
    driver_choices = []
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        company = request.user.clientprofile.company
        company_drivers_without_vehicle = ClientProfile.objects.filter(role='driver', company=company, vehicle=None)
        driver_choices = [(driver.id, driver.user.username) for driver in company_drivers_without_vehicle]
        if 'driver' in request.POST and request.POST['driver']:
            chosen_driver_id = int(request.POST['driver'])
            if company_drivers_without_vehicle.filter(id=chosen_driver_id).exists():
                if form.is_valid():
                    vehicle = form.save(commit=False)
                    vehicle.company = company
                    vehicle.driver = ClientProfile.objects.get(id=chosen_driver_id)
                    vehicle.save()
                    return redirect('view_vehicles')
            else:
                form.add_error('driver', 'Выбранный водитель недоступен для назначения на автомобиль.')
        else:
            if form.is_valid():
                vehicle = form.save(commit=False)
                vehicle.company = company
                vehicle.save()
                return redirect('view_vehicles')

    return render(request, 'main/create_vehicle.html', {'form': form, 'driver_choices': driver_choices})


def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

    company_drivers_without_vehicle = ClientProfile.objects.filter(role='driver',company=vehicle.company, vehicle=None)
    driver_choices = [(driver.id, driver.user.username) for driver in company_drivers_without_vehicle]

    if request.method == 'POST':
        form = CustomVehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            driver = vehicle.driver
            if driver:
                driver.vehicle = vehicle
                driver.save()
            return redirect('view_vehicles')
    else:
        form = CustomVehicleForm(instance=vehicle, driver_choices=driver_choices)
    return render(request, 'main/edit_vehicle.html', {'form': form})

def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('view_vehicles')
    return render(request, 'main/delete_vehicle.html', {'vehicle': vehicle})
def view_vehicles(request):
    company = request.user.clientprofile.company
    vehicles = Vehicle.objects.filter(company=company)
    return render(request, 'main/view_vehicles.html', {'vehicles': vehicles, 'company': company})
def view_coupons(request):
    coupons = Coupon.objects.all()
    return render(request, 'main/coupons.html', {'coupons': coupons})

def create_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            coupon = form.save(commit=False)
            coupon.company = request.user.clientprofile.company
            coupon.save()
            return redirect('view_coupons')
    else:
        form = CouponForm()
    return render(request, 'main/create_coupon.html', {'form': form})

def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('view_coupons')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'main/edit_coupon.html', {'form': form})

def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    if request.method == 'POST':
        coupon.delete()
        return redirect('view_coupons')
    return render(request, 'main/delete_coupon.html', {'coupon': coupon})
def vacancy_list(request, company_id):
    company = Company.objects.get(id=company_id)
    vacancies = Employee.objects.filter(company=company)
    return render(request, 'main/vacancy_list.html', {'company': company, 'vacancies': vacancies})

def company_contacts(request, company_id):
    company = Company.objects.get(id=company_id)
    employees = Employee.objects.filter(company=company)
    return render(request, 'main/contacts.html', {'company': company, 'employees': employees})

def privacy_policy(request):
    return render(request, 'main/privacy-policy.html')
def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    reviews = Review.objects.filter(article=article)
    return render(request, 'main/article_detail.html', {'article': article, 'reviews': reviews})
def get_timezone_by_ip(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        if data['status'] == 'success':
            return data['timezone']
        else:
            return None
    except Exception as e:
        print(f"Error fetching timezone: {e}")
        return None
def news_list(request):
    articles = Article.objects.all()
    return render(request, 'main/news_list.html', {'articles': articles})


def home(request):
    latest_article = Article.objects.order_by('-id').first()
    now_utc = timezone.now()
    user_ip = request.META.get('REMOTE_ADDR')
    user_timezone_str = get_timezone_by_ip(user_ip)
    if user_timezone_str:
        user_timezone = pytz.timezone(user_timezone_str)
    else:
        user_timezone = pytz.timezone('Europe/Minsk')

    now_user = now_utc.astimezone(user_timezone)
    cal = calendar.TextCalendar(calendar.SUNDAY)
    cal_text = cal.formatmonth(now_user.year, now_user.month)
    context = {
        'latest_article': latest_article,
        'now_utc': now_utc,
        'now_user': now_user,
        'cal_text': cal_text,
    }
    return render(request, 'main/home.html', context)
def make_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, company=request.user.clientprofile.company)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = False
            order.client = request.user.clientprofile
            order.cost = 0
            order.driver = None
            order.cargo_type = None
            order.coupon = None
            order.save()
            return redirect('order_list')
    else:
        form = OrderForm(company=request.user.clientprofile.company)
    return render(request, 'main/make_order.html', {'form': form})
def mark_order_completed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = True
        order.save()
        return redirect('order_list_driver')
def order_list_driver(request):
    client = request.user.clientprofile
    orders = Order.objects.filter(driver=client)
    return render(request, 'main/order_list_driver.html', {'orders': orders})
def order_list_client(request):
    orders = Order.objects.filter(client=request.user.clientprofile)
    total_cost = sum(order.cost for order in orders if order.status)
    return render(request, 'main/order_list_client.html', {'orders': orders, 'total_cost': total_cost})
def order_list(request):
    client = request.user.clientprofile
    orders = Order.objects.filter(client=client)
    return render(request, 'main/order_list.html', {'orders': orders})

def edit_company_info(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('edit_company_info', company_id=company.id)
    else:
        form = CompanyForm(instance=company)
    return render(request, 'main/edit_company_info.html', {'form': form})

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():

            employee = form.save(commit=False)
            employee.company = request.user.clientprofile.company
            employee.save()

            return redirect('view_employees')
    else:
        form = EmployeeForm()
    return render(request, 'main/add_employee.html', {'form': form})
def view_employees(request):
    company = request.user.clientprofile.company
    employees = Employee.objects.filter(company=company)
    return render(request, 'main/view_employees.html', {'employees': employees,'company': company})
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('view_employees')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'main/edit_employee.html', {'form': form, 'employee': employee})
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('view_employees')
    return render(request, 'main/delete_employee_confirm.html', {'employee': employee})
@login_required
def manage_company(request):
    try:
        company = Company.objects.get(owner=request.user)
        if request.method == 'POST':
            form = CompanyForm(request.POST, instance=company)
            if form.is_valid():
                form.save()
                return redirect('edit_company_info', company_id=company.id)
        else:
            form = CompanyForm(instance=company)
        return render(request, 'main/edit_company_info.html', {'form': form, 'company': company})
    except Company.DoesNotExist:
        if request.method == 'POST':
            form = CompanyForm(request.POST)
            if form.is_valid():
                company = form.save(commit=False)
                company.owner = request.user
                company.save()
                request.user.clientprofile.company = company
                request.user.clientprofile.save()

                return redirect('edit_company_info', company_id=company.id)
        else:
            form = CompanyForm()
        return render(request, 'main/create_company.html', {'form': form})
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            birthday = form.cleaned_data.get('birthday')
            login(request)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'main/vehicle_list.html', {'vehicles': vehicles})

def company_list(request):
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')
    search_query = request.GET.get('q', '')
    if search_query:
        companies = Company.objects.filter(name__icontains=search_query)
    else:
        companies = Company.objects.all()
    if order == 'asc':
        companies = companies.order_by(sort_by)
    else:
        companies = companies.order_by('-' + sort_by)
    return render(request, 'main/company_list.html', {'companies': companies, 'sort_by': sort_by, 'order': order, 'search_query': search_query})
def driver_list(request):
    sort_by = request.GET.get('sort', 'age')
    order = request.GET.get('order', 'asc')
    drivers = ClientProfile.objects.filter(role='driver')
    if order == 'asc':
        drivers = ClientProfile.objects.filter(role='driver').order_by(sort_by)
    else:
        drivers = ClientProfile.objects.filter(role='driver').order_by('-' + sort_by)
    return render(request, 'main/driver_list.html', {'drivers': drivers ,'sort_by': sort_by, 'order': order})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'main/review_list.html', {'reviews': reviews})

@login_required
def add_review(request, article_id):
    article = Article.objects.get(pk=article_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.article = article
            review.save()
            return redirect('news_list')
    else:
        form = ReviewForm()

    return render(request, 'main/add_review.html', {'article': article, 'form': form})


def coupon_list(request):

    filter_by = request.GET.get('filter', 'all')
    sort_by = request.GET.get('sort', 'discount')

    coupons = Coupon.objects.all()

    if filter_by == 'active':
        coupons = [coupon for coupon in coupons if coupon.is_active()]
    elif filter_by == 'inactive':
        coupons = [coupon for coupon in coupons if not coupon.is_active()]


    if sort_by == 'discount':
        coupons = sorted(coupons, key=lambda x: x.discount)
    elif sort_by == 'discount_desc':
        coupons = sorted(coupons, key=lambda x: x.discount, reverse=True)

    return render(request, 'main/coupon_list.html', {'coupons': coupons})
def term_list(request):
    terms = Term.objects.all().order_by('-date_added')
    return render(request, 'main/term_list.html', {'terms': terms})

def faq_list(request):
    faqs = FAQ.objects.all().order_by('-date_added')
    return render(request, 'main/faq_list.html', {'faqs': faqs})