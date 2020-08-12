from rest_framework import routers
from .views import  autores

# router = routers.SimpleRouter()

# router.register('postulante', postulanteViewSet)
router.register('autores', autores)

# urlpatterns = router.urls