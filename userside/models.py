from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

class userManager(BaseUserManager):
    def create_user(self,email,first_name,last_name, password=None):
        if not email:
            raise ValueError('Users must have an email adress.')
        if not first_name or not last_name:
            raise ValueError('Users must have an FullName adress.')
        if not password:
            raise ValueError('Users must have an password adress.')
        user = self.model(
            email= self.normalize_email(email),
            first_name = first_name,
            last_name= last_name,
            
        )
        user.set_password(password)
        user.save(using= self.db)
        return user
    
    def create_superuser(self,email,first_name,last_name, password):
        user = self.create_user(
            email= self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin= True
        user.is_staff= True
        user.is_superuser= True
        user.save(using= self.db)
        return user


class User(AbstractBaseUser):
    first_name= models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField( max_length=254, unique=True)
    profilePic = models.ImageField(upload_to="profiles/", null=True, default='default.jpg' )
    date_joined= models.DateTimeField(auto_now_add= True)
    last_login= models.DateTimeField(auto_now=True)
    is_admin= models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    
    USERNAME_FIELD= 'email'
    
    REQUIRED_FIELDS= ['first_name', 'last_name']
    objects= userManager()


    def __str__(self):
        return self.email
    def has_perm(self, perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True
    def has_change_permission(self,request, obj=None):
        return True
    def has_delete_permission(self,request, obj=None):
        return True
    
    


class BillingInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    company_name = models.CharField(max_length=255, null=True)
    street_address = models.CharField(max_length=255, null=True)
    apartment = models.CharField(max_length=255, null=True)
    town = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    postcode = models.CharField(max_length=255, null=True)
    email_address = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)

class About(models.Model):
    company= models.CharField(max_length=100)
    platforms= models.CharField(max_length=250)
    description= models.TextField()

    def __str__(self):
        return self.company
    
# class Catagory(models.Model):

#     catagory_name = models.CharField(max_length=100, blank=False, null=False)
#     image = models.ImageField(upload_to="catagories/", null=True, default='default.jpg' )

#     def __str__(self):
#         return self.catagory_name
class Catagory(models.Model):
    catagory_name= models.CharField(max_length=150,)
    image= models.ImageField(upload_to="catagories/", default= 'default.jpg')
    
    def __str__(self):
         return self.catagory_name
    
    
    
    

   


class Product(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    product_price = models.CharField(max_length=10, null=False, default="0")
    product_image_url = models.ImageField(upload_to="products/", null=True )
    catagory= models.ForeignKey(to=Catagory,on_delete=models.CASCADE, null=True)
    quantity = models.CharField(max_length=5, null=True, default="0")
    product_description = models.CharField(max_length=1000, null=True)
    data_sheet = models.CharField(max_length=1000, null=True)
    more_info = models.CharField(max_length=1000, null=True)
    
    def __str__(self):
        return self.product_name
    

class UserCart(models.Model):
    user= models.ForeignKey(to=User, on_delete=models.CASCADE)
    product= models.ForeignKey(to=Product, on_delete=models.CASCADE)
    items= models.CharField(max_length=10, default="1")
    
    def __str__(self):
        return f'{self.product.product_name} - {self.user.email}'
    
from django.db import models

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token