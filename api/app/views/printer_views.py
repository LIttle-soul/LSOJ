from app.models import Printer
from app.serializer.printer_serializer import PrinterSerializer
from rest_framework import generics


class PrinterList(generics.ListCreateAPIView):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class PrinterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer
