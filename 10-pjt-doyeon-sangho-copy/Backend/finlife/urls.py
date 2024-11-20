from django.urls import path
from . import views

urlpatterns = [
    # 예금 관련 URL
    path('save-deposit-products/', views.save_deposit_products, name='save_deposit_products'),
    path('deposit-products/', views.deposit_products, name='deposit_products'),
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options, name='deposit_product_options'),
    path('deposit-products/top-rate/', views.top_rate, name='top_rate'),

    # 적금 관련 URL
    path('save-savings-products/', views.save_savings_products, name='save_savings_products'),
    path('savings-products/', views.savings_products, name='savings_products'),
    path('savings-product-options/<str:fin_prdt_cd>/', views.savings_product_options, name='savings_product_options'),
    path('savings-products/top-rate/', views.top_rate_savings_products, name='top_rate_savings_products'),
    
     path('api/deposit-products/<str:fin_prdt_cd>/', views.deposit_product_detail, name='deposit_product_detail'),
]
