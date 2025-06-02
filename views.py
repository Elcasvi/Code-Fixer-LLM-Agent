from django.views import View
from django.http import JsonResponse
from .models import Product

class ProductDetailView(View):

    def get_object(self, pk):
        return Product.object.get(pk=pk)  # ❌ Error

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product.is_in_stock:
            return JsonResponse({'error': 'Out of stock'}, status=404)
        return JsonResponse({
            'name': product.name,
            'price': str(product.price),
            'stock': product.stock,
            'description': product.description
        })
