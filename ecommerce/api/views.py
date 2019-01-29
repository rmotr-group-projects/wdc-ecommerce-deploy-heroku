from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from products.models import Product
from api.serializers import ProductSerializer
from api.permissions import IsOddProductID, IsNotHacker


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        permissions = [IsAuthenticated(), IsNotHacker()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions += [IsAdminUser()]
        elif self.action == 'retrieve':
            permissions += [IsOddProductID()]
        return permissions
