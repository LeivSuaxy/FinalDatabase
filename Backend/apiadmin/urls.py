from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
  # <--Products CRUD URLS-->
  path('products/', views.get_all_products, name='get_all_products'),
  path('insert_product/', views.insert_product_in_database, name='insert_product'),
  path('update_product/', views.update_product_in_database, name='update_product'),
  path('delete_product/', views.delete_product_in_database, name='delete_product'),
  # <--Employees CRUD URLS-->
  path('employees/', views.get_all_employees, name='get_all_employees'),
  path('insert_employee/', views.insert_employee_to_database, name='insert_employee'),
  path('update_employee/', views.update_employee_in_database, name='update_employee'),
  path('delete_employee/', views.delete_employee_in_database, name='delete_employee'),
  # <--Inventories CRUD URLS-->
  path('inventories/', views.get_all_inventories, name='get_all_inventories'),
  path('insert_inventory/', views.insert_inventory_in_database, name='insert_inventory'),
  path('delete_inventory/', views.delete_inventory_from_database, name='delete_inventory'),
  # <-- Reports CRUD URLS-->
  path('sales_reports/', views.get_all_sales_reports, name='get_all_sales_reports'),
  path('inventory_reports/', views.get_all_inventory_reports, name='get_all_inventory_reports'),
  path('generate_inventories_reports/', views.generate_inventories_reports, name='generate_inventories_reports'),
  path('generate_sales_reports/', views.generate_sales_reports, name='generate_sales_reports'),
  path('get_all_purchase_orders/', views.get_all_purchase_orders, name='get_all_purchase_orders'),
  path('delete_purchases_orders/', views.delete_purchase_orders, name='delete_purchase_orders'),
  # <--Warehouses CRUD URLS-->
  path('warehouses/', views.get_all_warehouses, name='get_all_warehouses'),
  path('insert_warehouse/', views.insert_warehouse, name='insert_warehouse'),
  path('delete_warehouse/', views.delete_warehouse, name='delete_warehouse'),
  # <--Messenger CRUD URLS-->
  path('messengers/', views.get_all_messengers, name='get_all_messengers'),
  path('insert_messenger/', views.insert_messenger, name='insert_messenger'),
  path('update_messenger/', views.update_messenger, name='update_messenger'),
  path('delete_messenger/', views.delete_messenger, name='delete_messenger'),
  # <--COMPLEMENTARY URLS-->
  path('reports_repeated/', views.verify_reports_repeated, name='reports_repeated'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
