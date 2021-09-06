from app.models import CodeLanguage
from app.serializer.language_serializer import CodeLanguageSerializer
from rest_framework import generics


class CodeLanguageList(generics.ListCreateAPIView):
    queryset = CodeLanguage.objects.all()
    serializer_class = CodeLanguageSerializer


class CodeLanguageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CodeLanguage.objects.all()
    serializer_class = CodeLanguageSerializer
