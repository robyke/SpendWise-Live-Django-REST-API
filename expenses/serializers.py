from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Expense
        fields = [
            'id',
            'amount',
            'description',
            'category',
            'created_at',
            'owner',
        ]