from django.urls import path 
from . import views

urlpatterns = [
    path('signup', views.SignupView.as_view(),name='signup'),
    path('createCatagory/', views.CreateCatagoryGeneric.as_view(),name='addProduct'),
    path('createProduct/', views.ProductCreateView.as_view(),name='addCatagory'),
    path('catagories/', views.CategoryListView.as_view()),
    path('products/', views.ProductListView.as_view()),
    path('addCart/',views.CreateCartView.as_view()),
    path('viewCart/<str:email>', views.ViewCartView.as_view()),
    path("getProduct/<int:pk>", views.GetProduct().as_view()),
    path('deleteCart/',views.DeleteCartView.as_view()),
    path('about/',views.CreateAbout.as_view()),
    path('getAbout/',views.GetAbout.as_view()),
    path('updateAbout/<int:pk>', views.UpdateAboutView.as_view()),
    path("",views.SignUp.as_view()),
    path('getUserId/<str:email>', views.GetUserByEmail.as_view(), name='get-user-by-email'),
    
    
]

