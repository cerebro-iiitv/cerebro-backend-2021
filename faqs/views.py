from rest_framework.viewsets import ModelViewSet

from faqs.models import Faq
from faqs.serializers import FaqSerializer


class FaqViewSet(ModelViewSet):
    serializer_class = FaqSerializer
    queryset = Faq.objects.all()
    http_method_names = ["get"]
