from rest_framework import viewsets

from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    filterset_fields = ['category']
    search_fields = ['description']
    ordering_fields = ['amount', 'created_at', 'category']
    ordering = ['-created_at']

    def get_queryset(self):
        return self.request.user.expenses.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)