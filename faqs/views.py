from django.db.models.base import Model
from rest_framework.viewsets import ModelViewSet
from .models import Faq
from .serializers import FaqSerializer

class FaqViewSet(ModelViewSet):
    serializer_class = FaqSerializer
    queryset = Faq.objects.all()
