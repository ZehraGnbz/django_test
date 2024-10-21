from rest_framework.routers import DefaultRouter
from .views import PartViewSet, PersonnelViewSet, AircraftViewSet
from django.contrib import admin
from django.urls import path, include  # Make sure 'include' is imported


router = DefaultRouter()
router.register(r'parts', PartViewSet)
router.register(r'personnel', PersonnelViewSet)
router.register(r'aircrafts', AircraftViewSet)

urlpatterns = router.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('aircraft.urls')),  # Include aircraft app's API URLs
]