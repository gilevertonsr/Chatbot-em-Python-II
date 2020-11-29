from django.urls import path
from .views import perguntas, pergunta, novo, salvar_novo, edicao, salvar_edicao, delecao, salvar_delecao, chatbot, questao, api

urlpatterns = [
	path('<int:code_user>/', perguntas),
	path('pergunta/<int:id>/', pergunta),
	path('novo/<int:code_user>/', novo),
	path('salvarNovo/', salvar_novo),
	path('edicao/<int:id>/', edicao),
	path('salvarEdicao/', salvar_edicao),
	path('delecao/<int:id>/', delecao),
	path('salvarDelecao/', salvar_delecao),
	path('chatbot/<int:code_user>/', chatbot),
	path('questao/<int:code_user>/<int:code_before>/<str:question>/', questao),
	path('api/<int:code_user>/', api)
]
