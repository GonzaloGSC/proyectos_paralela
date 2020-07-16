from rest_framework import routers
from .views import postulanteViewSet

router = routers.SimpleRouter()

router.register('postulante', postulanteViewSet)

urlpatterns = router.urls