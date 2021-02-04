from django.urls import path
from .views import login, entrar, usuarios, usuario, novo, salvarNovo, edicao, salvar_edicao, delecao, salvar_delecao

urlpatterns = [
	path('login/', login),
	path('entrar/', entrar),
	path('', usuarios),
	path('usuario/<int:code>/', usuario),
	path('novo/', novo),
	path('salvarNovo/', salvarNovo),
	path('edicao/<int:id>/', edicao),
	path('salvar_edicao/', salvar_edicao),
	path('delecao/<int:id>/', delecao),
	path('salvar_delecao/', salvar_delecao)
]
