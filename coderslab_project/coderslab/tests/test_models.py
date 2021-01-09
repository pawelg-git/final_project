from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestModels:

    def test_pipe_order_wall_thk(self):
        product = mixer.blend('coderslab.PipeOrder', wall_thk=3.2)
        assert product.wall_thk_mm == "3.2 mm"

    def test_pipe_order_size_sch(self):
        product = mixer.blend('coderslab.PipeOrder', size=101.6)
        assert product.size_sch == "DN100"
