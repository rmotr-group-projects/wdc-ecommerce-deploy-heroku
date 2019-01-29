import base64
from freezegun import freeze_time

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from api.models import APIClient
from products.models import Product, Category


class ProductTestCase(TestCase):

    @freeze_time('2018-12-20T10:15:30+00:00')
    def setUp(self):
        self.user_1 = User.objects.create(username='test')
        self.user_1.set_password('test')
        self.user_1.save()

        self.admin = User.objects.create(username='admin', is_staff=True)
        self.admin.set_password('admin')
        self.admin.save()
        self.token_admin = Token.objects.create(user=self.admin)

        self.category_1 = Category.objects.create(name='Sport')
        self.category_2 = Category.objects.create(name='Clothes')

        self.product_1 = Product.objects.create(
            id=1,
            name='Nike Vapor',
            sku='44444444',
            category=self.category_1,
            description='Some product description',
            price=129.99)
        self.product_2 = Product.objects.create(
            id=2,
            name='Sweater',
            sku='88888888',
            category=self.category_2,
            description='Some product description',
            price=59.99)

    def test_list_not_authenticated(self):
        """Should return 401 when user is not authenticated"""
        response = self.client.get('/api/products/')
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected)

    def test_list_basic_auth(self):
        """Should return list of products when user is authenticated with Basic auth"""
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'test:test').decode("ascii")
        }
        expected = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.product_1.id,
                    'name': self.product_1.name,
                    'category': self.product_1.category.id,
                    'created': '2018-12-20T10:15:30Z',
                    'description': self.product_1.description,
                    'featured': self.product_1.featured,
                    'price': str(self.product_1.price),
                    'sku': self.product_1.sku
                },
                {
                    'id': self.product_2.id,
                    'name': self.product_2.name,
                    'category': self.product_2.category.id,
                    'created': '2018-12-20T10:15:30Z',
                    'description': self.product_2.description,
                    'featured': self.product_2.featured,
                    'price': str(self.product_2.price),
                    'sku': self.product_2.sku
                }
            ]
        }
        response = self.client.get('/api/products/', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_list_token_auth(self):
        """Should return list of products when user is authenticated with Token auth"""
        token = Token.objects.create(user=self.user_1)
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(token)
        }
        expected = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.product_1.id,
                    'name': self.product_1.name,
                    'category': self.product_1.category.id,
                    'created': '2018-12-20T10:15:30Z',
                    'description': self.product_1.description,
                    'featured': self.product_1.featured,
                    'price': str(self.product_1.price),
                    'sku': self.product_1.sku
                },
                {
                    'id': self.product_2.id,
                    'name': self.product_2.name,
                    'category': self.product_2.category.id,
                    'created': '2018-12-20T10:15:30Z',
                    'description': self.product_2.description,
                    'featured': self.product_2.featured,
                    'price': str(self.product_2.price),
                    'sku': self.product_2.sku
                }
            ]
        }
        response = self.client.get('/api/products/', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_list_api_client_auth(self):
        """Should return list of products when API client accesskey and secretkey are valid"""
        api_client = APIClient.objects.create(
            name='test', accesskey='a' * 32, secretkey='s' * 32)
        headers = {'secretkey': api_client.secretkey}
        expected = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.product_1.id,
                    'name': self.product_1.name,
                    'category': self.product_1.category.id,
                    'created': '2018-12-20T10:15:30Z',
                    'description': self.product_1.description,
                    'featured': self.product_1.featured,
                    'price': str(self.product_1.price),
                    'sku': self.product_1.sku
                },
                {
                    'id': self.product_2.id,
                    'name': self.product_2.name,
                    'category': self.product_2.category.id,
                    'created': '2018-12-20T10:15:30Z',
                    'description': self.product_2.description,
                    'featured': self.product_2.featured,
                    'price': str(self.product_2.price),
                    'sku': self.product_2.sku
                }
            ]
        }
        response = self.client.get(
            '/api/products/?accesskey={}'.format(api_client.accesskey), **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_list_api_client_auth_invalid_credentials(self):
        """Should return 401 when provided APIClient credentials are invalid"""
        api_client = APIClient.objects.create(
            name='test', accesskey='a' * 32, secretkey='s' * 32)

        headers = {'secretkey': 'INVALID-SECRETKEY'}
        response = self.client.get(
            '/api/products/?accesskey={}'.format('INVALID-ACCESSKEY'), **headers)

        expected = {'detail': 'Invalid APIClient credentials'}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected)

    @freeze_time('2018-12-20T10:15:30+00:00')
    def test_detail(self):
        """Should return the detail of given product when provided id is odd"""
        self.assertEqual(self.product_1.id, 1)

        token = Token.objects.create(user=self.user_1)
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(token)
        }
        response = self.client.get(
            '/api/products/{}/'.format(self.product_1.id), **headers)

        expected = {
            'id': self.product_1.id,
            'name': self.product_1.name,
            'sku': self.product_1.sku,
            'category': self.product_1.category.id,
            'description': self.product_1.description,
            'price': str(self.product_1.price),
            'created': '2018-12-20T10:15:30Z',
            'featured': self.product_1.featured
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json(), expected)

    def test_detail_odd_product_id_permission(self):
        """Should return 403 when trying to retrieve product data with NOT odd id"""
        self.assertEqual(self.product_2.id, 2)

        token = Token.objects.create(user=self.user_1)
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(token)
        }
        response = self.client.get(
            '/api/products/{}/'.format(self.product_2.id), **headers)

        expected = {'detail': 'You do not have permission to perform this action.'}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), expected)

    def test_detail_is_hacker_permission(self):
        """Should return 403 when authenticated user has 'hacker' in its name"""
        self.user_1.username = 'pythonhacker'
        self.user_1.save()

        token = Token.objects.create(user=self.user_1)
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(token)
        }
        response = self.client.get(
            '/api/products/{}/'.format(self.product_1.id), **headers)

        expected = {'detail': 'You do not have permission to perform this action.'}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), expected)

    @freeze_time('2018-12-20T10:15:30+00:00')
    def test_list(self):
        """Should return the list of all products paginated in pages of 3 products"""
        product_3 = Product.objects.create(
            name='Third product',
            sku='99999999',
            category=self.category_1,
            description='Displayed in FIRST page',
            price=129.99
        )
        Product.objects.create(
            name='Fourth product',
            sku='88888888',
            category=self.category_1,
            description='Displayed in SECOND page',
            price=129.99
        )
        expected = {
            'count': 4,
            'next': 'http://testserver/api/products/?page=2',
            'previous': None,
            'results': [
                {
                    'id': self.product_1.id,
                    'name': self.product_1.name,
                    'category': self.product_1.category.id,
                    'created': '2018-12-20T10:15:30Z',
                    'description': self.product_1.description,
                    'featured': self.product_1.featured,
                    'price': str(self.product_1.price),
                    'sku': self.product_1.sku
                },
                {
                    'id': self.product_2.id,
                    'name': self.product_2.name,
                    'category': self.product_2.category.id,
                    'created': '2018-12-20T10:15:30Z',
                    'description': self.product_2.description,
                    'featured': self.product_2.featured,
                    'price': str(self.product_2.price),
                    'sku': self.product_2.sku
                },
                {
                    'id': product_3.id,
                    'name': product_3.name,
                    'category': product_3.category.id,
                    'created': '2018-12-20T10:15:30Z',
                    'description': product_3.description,
                    'featured': product_3.featured,
                    'price': str(product_3.price),
                    'sku': product_3.sku
                }
            ]
        }
        token = Token.objects.create(user=self.user_1)
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(token)
        }
        response = self.client.get('/api/products/', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json(), expected)

    @freeze_time('2018-04-14T10:15:30+00:00')
    def test_create(self):
        """Should create a product when given data is valid and user is admin"""
        self.assertEqual(Product.objects.count(), 2)
        payload = {
            'name': 'New product',
            'category': self.category_1.id,
            'sku': '11111111',
            'description': 'New product description',
            'price': 39.99
        }

        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.token_admin)
        }
        response = self.client.post(
            '/api/products/', data=payload, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(Product.objects.count(), 3)

        product = Product.objects.get(name='New product')
        self.assertEqual(product.name, 'New product')
        self.assertEqual(product.category, self.category_1)
        self.assertEqual(product.sku, '11111111')
        self.assertEqual(product.description, 'New product description')
        self.assertEqual(float(product.price), 39.99)

    def test_create_not_admin(self):
        """Should return 403 when a non admin user tries to create a product"""
        self.assertEqual(Product.objects.count(), 2)
        payload = {
            'name': 'New product',
            'category': self.category_1.id,
            'sku': '11111111',
            'description': 'New product description',
            'price': 39.99
        }

        token = Token.objects.create(user=self.user_1)
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(token)
        }
        expected = {'detail': 'You do not have permission to perform this action.'}
        response = self.client.post(
            '/api/products/', data=payload,
            content_type='application/json', **headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), expected)
        self.assertEqual(Product.objects.count(), 2)

    @freeze_time('2018-04-14T10:15:30+00:00')
    def test_full_update(self):
        """Should full update a product when given data is valid and user is admin"""
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(self.product_1.name, 'Nike Vapor')
        self.assertEqual(self.product_1.sku, '44444444')
        self.assertEqual(self.product_1.category, self.category_1)
        self.assertEqual(self.product_1.description, 'Some product description')
        self.assertEqual(self.product_1.price, 129.99)
        self.assertEqual(self.product_1.featured, False)

        payload = {
            'name': 'Updated name',
            'category': self.category_2.id,
            'sku': '11111111',
            'description': 'New product description',
            'price': 39.99,
            'featured': True
        }

        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.token_admin)
        }
        response = self.client.put(
            '/api/products/{}/'.format(self.product_1.id),
            data=payload, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(Product.objects.count(), 2)

        product = Product.objects.get(id=self.product_1.id)
        self.assertEqual(product.name, 'Updated name')
        self.assertEqual(product.sku, '11111111')
        self.assertEqual(product.category, self.category_2)
        self.assertEqual(product.description, 'New product description')
        self.assertEqual(float(product.price), 39.99)
        self.assertEqual(product.featured, True)

    @freeze_time('2018-04-14T10:15:30+00:00')
    def test_partial_update(self):
        """Should partial update a product when given data is valid and user is admin"""
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(self.product_1.name, 'Nike Vapor')

        payload = {
            'name': 'Updated name',
        }

        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.token_admin)
        }
        response = self.client.patch(
            '/api/products/{}/'.format(self.product_1.id),
            data=payload, content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(Product.objects.count(), 2)

        product = Product.objects.get(id=self.product_1.id)
        self.assertEqual(product.name, 'Updated name')

    @freeze_time('2018-04-14T10:15:30+00:00')
    def test_delete(self):
        """Should delete a product when given product id is valid and user is admin"""
        self.assertEqual(Product.objects.count(), 2)

        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.token_admin)
        }
        response = self.client.delete(
            '/api/products/{}/'.format(self.product_1.id), **headers)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 1)
