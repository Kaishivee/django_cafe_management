from django import forms
from django.core.validators import MinValueValidator

from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'status', 'items']
        widgets = {
            'table_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'step': '1',
                'required': True,  # Поле обязательно для заполнения
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'items': forms.HiddenInput(),  # Скрытое поле для хранения списка блюд
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['items'].required = False  # Поле items не обязательно для заполнения вручную
        self.fields['table_number'].validators.append(MinValueValidator(1)) # Валидатор для table_number

    def clean_table_number(self):
        """
        Валидация номера стола.
        """
        table_number = self.cleaned_data.get('table_number')
        if table_number < 1:
            raise forms.ValidationError("Номер стола должен быть положительным числом, начиная с 1.")
        return table_number

    def clean(self):
        """
        Валидация формы. В заказе есть хотя бы одно блюдо.
        """
        cleaned_data = super().clean()
        items = cleaned_data.get('items', [])

        if not items:
            raise forms.ValidationError("Заказ должен содержать хотя бы одно блюдо.")

        # Дополнительная валидация каждого блюда
        for item in items:
            if not item.get('name') or not item.get('price') or not item.get('quantity'):
                raise forms.ValidationError("Все поля элемента заказа должны быть заполнены.")

        return cleaned_data