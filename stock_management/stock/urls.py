from django.urls import path
from . import views
from .views import restock_stock

urlpatterns = [
    path('', views.home_view, name='home'),  # Home URL
    path('house/', views.house_view, name='house'),  # Home URL
    path('login/', views.login_view, name='login'),  # Combined user/admin login URL
    path('admin_login/', views.admin_login, name='admin_login'),  # Admin-specific login URL
    path('dashboard/', views.dashboard_view, name='dashboard'),  # User dashboard URL
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-profile/', views.admin_profile, name='admin_profile'),
    path('admin-edit-profile/', views.edit_profile, name='edit_profile'),
    path('admin-change-password/', views.change_password, name='change_password'),  
    path('manage_stocks/', views.manage_stocks, name='manage_stocks'),
    path('view_users/', views.view_users, name='view_users'),
    path('success/', views.success_page, name='success_page'),
    path('settings/', views.settings_view, name='settings'),
    path('add-stock/', views.add_stock, name='add_stock'),
    path('view_stock/', views.view_stock, name='view_stock'),
    path('restock-stock/',restock_stock, name='restock_stock'), 
    path('profile/', views.profile_view, name='profile'),  # Profile view for both users and admins
    path('signup/', views.signup, name='signup'),  # Signup page URL
    path('logout/', views.logout_view, name='logout'),  # Logout URL
    path('orders/', views.orders_view, name='orders'),
    path('contact/', views.contact_view, name='contact'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('export-stock-csv/', views.export_stock_csv, name='export_stock_csv'),
    path('export-user-csv/', views.export_user_csv, name='export_user_csv'),
    path('register-store/', views.register_store, name='register_store'),
    path('sell-stock/', views.sell_stock, name='sell_stock'),
    path('stores/', views.store_list, name='store_list'),
    path('buy-stocks/', views.buy_stocks, name='buy_stocks'),
    path('payment/', views.payment, name='payment'),  # Payment page URL
    path('payment-success/', views.payment_success, name='payment_success'),  # Success page URL
    path('fetch_stocks/', views.fetch_stocks, name='fetch_stocks'),
    


    # User management and stock management URLs
    path('fetch_users/', views.fetch_users, name='fetch_users'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
    path('edit-stock/<int:id>/', views.edit_stock, name='edit_stock'),
    path('delete-stock/<int:id>/', views.delete_stock, name='delete_stock'),
    path('fetch_store_requests/', views.fetch_store_requests, name='fetch_store_requests'),
    path('handle-request/<int:id>/', views.handle_request, name='handle_request'),
]