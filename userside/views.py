from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics,permissions


from .serializers import *
from .models import *


class GetUserByEmail(APIView):
    
    print(User.objects.first())
    def get(self, request, email, format=None):
        
        try:
            
            user = User.objects.get(email=email)
          
            serializer = UserSerializer(user)
            print(serializer.data)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
class CreateCatagoryGeneric(generics.CreateAPIView):
    queryset = Catagory.objects.all()
    serializer_class= CatagorySeializer
    

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer
class CategoryCreateView(APIView):
    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
 
class CategoryListView(generics.ListAPIView):
    queryset = Catagory.objects.all()
    serializer_class = CategorySerializer
        
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

class CreateCartView(generics.ListCreateAPIView):
    queryset = UserCart.objects.all()
    serializer_class = UserCartSerializer
    print('adf')
    def perform_create(self, serializer):
        print(self.request.data.get('user'))
        user_email = self.request.data.get('user')
        product_id = self.request.data.get('product')
        print(user_email)
        try:
            user = User.objects.get(id=int(user_email))
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'Invalid product ID'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(user=user, product=product)  # Pass the product object here
        return Response({'Response': "Product added to cart" })

        
        

class ViewCartView(generics.ListAPIView):
    serializer_class = cartProdSerializer

    def get_queryset(self):
        email = self.kwargs['email']
        try:
            user = User.objects.get(email=email)
            cart_items = UserCart.objects.filter(user=user)
            a=set()
            products = []
            for cart_item in cart_items:
                
                if cart_item.product.pk in a:
                    continue
                else:
                    product = Product.objects.get(pk=cart_item.product.pk)
                    a.add(cart_item.product.pk)
                
                product_data = {
                    'name': product.product_name,
                    'price': product.product_price,
                    'image': f'{product.product_image_url}'
                }
                products.append(product_data)
            
            return products
        except User.DoesNotExist:
            return []

    def list(self, request, *args, **kwargs):
        email = self.kwargs['email']
        products = self.get_queryset()

        if not products:
            return Response({"detail": "No products found in the cart."}, status=status.HTTP_404_NOT_FOUND)
        print(products)
        return Response({"data": products})
    
class GetProduct(generics.ListAPIView):
    serializer_class= ProductSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Product.objects.filter(id=pk)



class DeleteCartView(generics.DestroyAPIView):
    queryset = UserCart.objects.all()
    serializer_class = UserCartSerializer



class CreateAbout(generics.CreateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

class GetAbout(generics.ListAPIView):
    serializer_class = AboutSerializer
    def get_queryset(self):   
        return About.objects.filter(pk= 1)
    

class UpdateAboutView(generics.UpdateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    lookup_field = 'pk'


