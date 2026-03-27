from django.urls import path
from .views import cadastro, listagem_faturas, notificar_fatura

urlpatterns = [
    path('', cadastro, name='cadastro'),
    path('faturas/', listagem_faturas, name='listagem_faturas'),
    path('faturas/notificar/<int:fatura_id>/', notificar_fatura, name='notificar_fatura'),
]
