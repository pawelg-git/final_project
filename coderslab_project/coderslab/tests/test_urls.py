from django.urls import resolve, reverse


class TestUrls:

    def test_order_detail_url(self):
        path = reverse('order-detail', kwargs={'order_id': 15})
        assert resolve(path).view_name == 'order-detail'

    def test_home_url(self):
        path = reverse('coderslab-home')
        assert resolve(path).view_name == 'coderslab-home'

    def test_pipe_configurator_url(self):
        path = reverse('coderslab-pipe_configurator')
        assert resolve(path).view_name == 'coderslab-pipe_configurator'

    def test_login_url(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'

    def test_logout_url(self):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'

    def test_register_url(self):
        path = reverse('register')
        assert resolve(path).view_name == 'register'

    def test_rorder_list_url(self):
        path = reverse('order-list')
        assert resolve(path).view_name == 'order-list'
