from django_filters import rest_framework as filters


class ContractFilter(filters.FilterSet):
    date_created = filters.CharFilter(
        field_name="date_created", lookup_expr="icontains"
    )
    amount = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    client_last_name = filters.CharFilter(
        field_name="client__last_name", lookup_expr="iexact"
    )
    client_email = filters.CharFilter(
        field_name="client__email", lookup_expr="icontains"
    )


class ClientFilter(filters.FilterSet):
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")


class EventFilter(filters.FilterSet):
    date = filters.CharFilter(field_name="date", lookup_expr="icontains")
    client_last_name = filters.CharFilter(
        field_name="contract__client__last_name", lookup_expr="icontains"
    )
    client_email = filters.CharFilter(
        field_name="contract__client__email", lookup_expr="iexact"
    )
