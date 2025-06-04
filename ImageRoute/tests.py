from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Route, RoutePoint, BackgroundImage
from .forms import RouteForm, RoutePointForm

User = get_user_model()

class ViewTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create a background image (optional, can be set for route creation if needed)
        self.background_image = BackgroundImage.objects.create(image='test_image.jpg')
        # Create a route for the test user
        self.route = Route.objects.create(user=self.user, background=self.background_image)

    def test_register_view(self):
        # Ensure no user exists yet
        self.assertFalse(User.objects.filter(username='newuser').exists())

        # GET request to the register page
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Zarejestruj')  # Adjust to match your template

        # POST valid registration data
        data = {
            'username': 'newuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # POST invalid data (e.g., passwords don't match)
        data_invalid = {
            'username': 'invaliduser',
            'password1': 'pass1',
            'password2': 'pass2',
        }
        response = self.client.post(reverse('register'), data_invalid)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='password')

        # GET request to the dashboard page
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Moje trasy')  # Assuming 'Routes' is in the template

        # Check if the route created for the user is shown in the dashboard
        # print()

    def test_dashboard_view_unauthenticated(self):
        self.client.logout()
        # GET request to the dashboard page without being logged in
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("dashboard")}')  # Should redirect to login page


    # -------- Tests for create_route view --------

    def test_create_route_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('create_route'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("create_route")}')

    def test_create_route_view_get_logged_in(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('create_route'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_create_route_view_post_valid_data(self):
        self.client.login(username='testuser', password='password')
        data = {
            'name': 'My New Route',
            'description': 'Test route',
            'background': self.background_image.id,
        }
        response = self.client.post(reverse('create_route'), data)
        self.assertEqual(Route.objects.filter(name='My New Route').count(), 1)
        new_route = Route.objects.get(name='My New Route')
        self.assertRedirects(response, reverse('route_detail', args=[new_route.id]))
        self.assertEqual(new_route.user, self.user)

    def test_create_route_view_post_invalid_data(self):
        self.client.login(username='testuser', password='password')
        data = {
            'name': '',  # Name is required
            'background': self.background_image.id,
        }
        response = self.client.post(reverse('create_route'), data)
        self.assertEqual(response.status_code, 200)

    # -------- Tests for add_point and delete_point --------

    def test_add_point_view_post_valid_data(self):
        # User must be logged in
        self.client.login(username='testuser', password='password')

        # POST valid x/y coordinates
        data = {'x': 100, 'y': 200}
        response = self.client.post(reverse('add_point', args=[self.route.id]), data)

        # One point should be created with correct coords
        self.assertEqual(RoutePoint.objects.count(), 1)
        point = RoutePoint.objects.first()
        self.assertEqual(point.x, 100)
        self.assertEqual(point.y, 200)

        # Redirect back to route detail
        self.assertRedirects(response, reverse('route_detail', args=[self.route.id]))

    def test_add_point_view_get(self):
        self.client.login(username='testuser', password='password')

        # GET should render the form
        response = self.client.get(reverse('add_point', args=[self.route.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="x"')
        self.assertContains(response, 'name="y"')

    def test_delete_point_view_post(self):
        self.client.login(username='testuser', password='password')

        # Create a point to delete
        point = RoutePoint.objects.create(route=self.route, x=10, y=20, order=1)

        # POST to delete
        response = self.client.post(reverse('delete_point', args=[self.route.id, point.id]))
        self.assertRedirects(response, reverse('route_detail', args=[self.route.id]))
        self.assertFalse(RoutePoint.objects.filter(id=point.id).exists())

    def test_delete_point_view_get_confirmation(self):
        self.client.login(username='testuser', password='password')

        # Create a point to confirm deletion
        point = RoutePoint.objects.create(route=self.route, x=10, y=20, order=1)

        # GET should render confirmation template
        response = self.client.get(reverse('delete_point', args=[self.route.id, point.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Czy na pewno')