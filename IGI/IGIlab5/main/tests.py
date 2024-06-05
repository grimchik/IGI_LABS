from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import (
    VehicleType, BodyType, Company, Service, Driver, CargoType,
    Order, Coupon, ClientProfile, Vehicle, Article, Vacancy,
    Employee, Review, Term, FAQ
)
from django.core.exceptions import ValidationError

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.company = Company.objects.create(name='Test Company', owner=self.user)
        self.vehicle_type = VehicleType.objects.create(name='Pickup')
        self.body_type = BodyType.objects.create(name='Closed')
        self.vehicle = Vehicle.objects.create(name='Test Vehicle', vehicle_type=self.vehicle_type, body_type=self.body_type, company=self.company)
        self.client_profile = ClientProfile.objects.create(user=self.user, role=ClientProfile.CLIENT, vehicle=self.vehicle, company=self.company)
        self.driver = Driver.objects.create(name='Test Driver', age=30, company=self.company)
        self.service = Service.objects.create(name='Test Service', cost=100.00, description='Service description', company=self.company)
        self.coupon = Coupon.objects.create(code='DISCOUNT10', discount=10.00, start_date=timezone.now().date(), end_date=timezone.now().date() + timezone.timedelta(days=10), company=self.company)
        self.article = Article.objects.create(title='Test Article', short_text='Short text', full_text='Full text')
        self.vacancy = Vacancy.objects.create(title='Test Vacancy', description='Job description', company=self.company)
        self.employee = Employee.objects.create(full_name='John Doe', position='Manager', email='john.doe@example.com', phone='+375 (29) 123-45-67', description='Employee description', company=self.company)
        self.review = Review.objects.create(user=self.user, rating=5, text='Great service!', article=self.article)
        self.term = Term.objects.create(term='Test Term', definition='Term definition')
        self.faq = FAQ.objects.create(question='Test Question', answer='Test Answer')

    def test_vehicle_type_str(self):
        self.assertEqual(str(self.vehicle_type), 'Pickup')

    def test_body_type_str(self):
        self.assertEqual(str(self.body_type), 'Closed')

    def test_company_str(self):
        self.assertEqual(str(self.company), 'Test Company')

    def test_service_str(self):
        self.assertEqual(str(self.service), 'Test Service')

    def test_driver_str(self):
        self.assertEqual(str(self.driver), 'Test Driver')

    def test_cargo_type_str(self):
        cargo_type = CargoType.objects.create(name='Fragile')
        cargo_type.suitable_body_types.add(self.body_type)
        self.assertEqual(str(cargo_type), 'Fragile')

    def test_order_str(self):
        order = Order.objects.create(driver=self.client_profile, cost=200.00, company=self.company, status=True)
        self.assertEqual(str(order), f"Order {order.id} by Test Company")

    def test_coupon_str(self):
        self.assertEqual(str(self.coupon), 'DISCOUNT10')

    def test_coupon_is_active(self):
        self.assertTrue(self.coupon.is_active())

    def test_client_profile_str(self):
        self.assertEqual(str(self.client_profile), 'testuser - Client')

    def test_vehicle_str(self):
        self.assertEqual(str(self.vehicle), 'Test Vehicle (Pickup - Closed)')

    def test_article_str(self):
        self.assertEqual(str(self.article), 'Test Article')

    def test_vacancy_str(self):
        self.assertEqual(str(self.vacancy), 'Test Vacancy')

    def test_employee_str(self):
        self.assertEqual(str(self.employee), 'John Doe')

    def test_review_str(self):
        self.assertEqual(str(self.review), 'Отзыв от testuser с рейтингом 5')

    def test_term_str(self):
        self.assertEqual(str(self.term), 'Test Term')

    def test_faq_str(self):
        self.assertEqual(str(self.faq), 'Test Question')

    def test_validate_driver_age(self):
        with self.assertRaises(ValidationError):
            Driver.objects.create(name='Young Driver', age=16, company=self.company)
        with self.assertRaises(ValidationError):
            Driver.objects.create(name='Old Driver', age=71, company=self.company)
