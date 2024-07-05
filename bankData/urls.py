from django.urls import path
from . import views

urlpatterns = [
    path('viewaccounts/', views.viewaccounts, name='viewaccounts'),
    path('main/', views.main, name='main'),
    path('index_login/', views.index_login, name='index_login'),
    path('index_signup/', views.index_signup, name='index_signup'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('addaccounts/<int:user_id>/', views.addaccounts, name='addaccounts'),
    path('listaccounts/', views.listaccounts, name='listaccounts'),
    path('storedetails/', views.storedetails, name='storedetails'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('myWithdraw/', views.myWithdraw, name='myWithdraw'),
    path('deposit/', views.deposit, name='deposit'),
    path('myDeposit/', views.myDeposit, name='myDeposit'),
    path('delete/', views.delete, name='delete'),
    path('myDelete/', views.myDelete, name='myDelete'),
    path('update/', views.update, name='update'),
    path('myUpdate/', views.myUpdate, name='myUpdate'),
    path('signUp_cust/', views.signUp_cust, name='signUp_cust'),
    path('login_cust/', views.login_cust, name='login_cust'),
    path('userhome/', views.userhome, name='userhome'),

    path('viewprofile/', views.viewprofile, name='viewprofile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('update_editprofile/', views.update_editprofile, name='update_editprofile'),
    path('transaction/', views.transaction, name='transaction'),
    path('userDeposits/', views.Deposits, name='Deposits'),
    path('create_fd/', views.create_fd, name='create_fd'),
    path('show_fd/', views.show_fd, name='show_fd'),
    path('fd_details/', views.fd_details, name='fd_details'),
    path('logout/', views.logout, name='logout'),
    path('storedetails_cust_sign/', views.storedetails_cust_sign, name='storedetails_cust_sign'),
    path('login_success/', views.mylogin_cust, name='mylogin_cust')
]   