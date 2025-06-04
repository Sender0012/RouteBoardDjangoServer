from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BackgroundImage, Route, RoutePoint

User = get_user_model()

def get_access_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class RouteAPITestCase(APITestCase):
    def setUp(self):
        # create two users and backgrounds
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.bg1 = BackgroundImage.objects.create(name='bg1', image='bg1.jpg')
        # create one route for user1
        self.route1 = Route.objects.create(name='Route1', user=self.user1, background=self.bg1)
        self.client = APIClient()

    def authenticate(self, user):
        token = get_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list_routes_authenticated(self):
        self.authenticate(self.user1)
        url = reverse('api_routes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # only one route for user1
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Route1')

    def test_list_routes_unauthenticated(self):
        url = reverse('api_routes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_route_valid(self):
        self.authenticate(self.user1)
        url = reverse('api_routes')
        data = {'name': 'NewRoute', 'background': self.bg1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Route.objects.filter(name='NewRoute', user=self.user1).exists())

    def test_create_route_invalid(self):
        self.authenticate(self.user1)
        url = reverse('api_routes')
        data = {'name': '', 'background': self.bg1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())

    def test_retrieve_route_owned(self):
        self.authenticate(self.user1)
        url = reverse('api_route_detail', args=[self.route1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], self.route1.name)

    def test_retrieve_route_not_owned(self):
        self.authenticate(self.user2)
        url = reverse('api_route_detail', args=[self.route1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_route_owned(self):
        self.authenticate(self.user1)
        url = reverse('api_route_detail', args=[self.route1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Route.objects.filter(id=self.route1.id).exists())

    def test_delete_route_not_owned(self):
        self.authenticate(self.user2)
        url = reverse('api_route_detail', args=[self.route1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class RoutePointAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.bg1 = BackgroundImage.objects.create(name='bg1', image='bg1.jpg')
        self.route1 = Route.objects.create(name='R1', user=self.user1, background=self.bg1)
        self.client = APIClient()

    def authenticate(self, user):
        token = get_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list_points_empty(self):
        self.authenticate(self.user1)
        url = reverse('api_points', args=[self.route1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    # def test_add_point_valid(self):
    #     self.authenticate(self.user1)
    #     url = reverse('api_points', args=[self.route1.id])
    #     data = {'x': 10, 'y': 20}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(RoutePoint.objects.count(), 1)
    #     pt = RoutePoint.objects.first()
    #     self.assertEqual(pt.x, 10)
    #     self.assertEqual(pt.y, 20)

    def test_add_point_valid(self):
        self.authenticate(self.user1)
        url = reverse('api_points', args=[self.route1.id])
        data = {'x': 10, 'y': 20}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pt = RoutePoint.objects.first()
        expected = {
            'id': pt.id,
            'x': pt.x,
            'y': pt.y,
            'order': pt.order,
            'route': self.route1.id,
        }
        import json
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected))
        self.assertEqual(RoutePoint.objects.count(), 1)


    def test_add_point_invalid(self):
        self.authenticate(self.user1)
        url = reverse('api_points', args=[self.route1.id])
        data = {'x': 'bad', 'y': 20}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('x', response.json())

    def test_delete_point_owned(self):
        self.authenticate(self.user1)
        pt = RoutePoint.objects.create(route=self.route1, x=1, y=2, order=1)
        url = reverse('api_point_delete', args=[self.route1.id, pt.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RoutePoint.objects.filter(id=pt.id).exists())

    def test_delete_point_not_owned(self):
        pt = RoutePoint.objects.create(route=self.route1, x=1, y=2, order=1)
        self.authenticate(self.user2)
        url = reverse('api_point_delete', args=[self.route1.id, pt.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
