from django.urls import include, path
from rest_framework_nested import routers

from .views import ClientViewset, ContractViewset, EventViewset

client_router = routers.SimpleRouter()
client_router.register("clients", ClientViewset, basename="clients")
contract_router = routers.SimpleRouter()
contract_router.register("contracts", ContractViewset, basename="contracts")
event_router = routers.SimpleRouter()
event_router.register("events", EventViewset, basename="events")

urlpatterns = [
    path("", include(client_router.urls)),
    path("", include(contract_router.urls)),
    path("", include(event_router.urls)),
]
