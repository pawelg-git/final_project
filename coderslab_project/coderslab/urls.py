from django.urls import path
from . import views as coderslab_views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('', coderslab_views.HomeView.as_view(), name="coderslab-home"),
    path('pipe_confi/', coderslab_views.PipeConfiguratorView.as_view(), name="coderslab-pipe_configurator"),
    path('login/', auth_views.LoginView.as_view(template_name='coderslab/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='coderslab/logout.html'), name="logout"),
    path('register/', coderslab_views.RegisterView.as_view(), name="register"),
    path('list_orders/', coderslab_views.OrderListView.as_view(template_name="coderslab/order_list.html"), name="order-list"),
    path('list_orders/order_detail/<int:order_id>/', coderslab_views.OrderDetailView.as_view(), name="order-detail"),
]
