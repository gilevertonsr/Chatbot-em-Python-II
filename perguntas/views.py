from django.shortcuts import render
from .models import Pergunta
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from unidecode import unidecode
from capturas.models import Captura
from usuarios.models import Usuario

codeUser = 0


def perguntas(request, code_user):
    titulo = 'Cadastro de Perguntas e Respostas'
    pergunta = Pergunta.objects.filter(code_user=code_user)
    usuario = Usuario.objects.filter(code=code_user)
    if len(usuario) > 0:
        global codeUser
        codeUser = code_user
        return render(request, 'perguntas.html', {'titulo': titulo, 'perguntas': pergunta, 'code_user': code_user})
    else:
        return render(request, 'redirecionar.html', {'code_user': 0})


def pergunta(request, id):
    titulo = 'Cadastro de Perguntas e Respostas'
    pergunta = Pergunta.objects.get(id=id)
    global codeUser
    usuario = Usuario.objects.filter(code=codeUser)
    if len(usuario) > 0:
        return render(request, 'perguntas.html', {'titulo': titulo, 'perguntas': [pergunta], 'code_user': codeUser})
    else:
        return render(request, 'redirecionar.html', {'code_user': 0})


def novo(request, code_user):
    titulo = 'Inserção de Perguntas e Respostas'
    todas = Pergunta.objects.filter(code_user=code_user)
    usuario = Usuario.objects.filter(code=code_user)
    if len(usuario) > 0:
        return render(request, 'novoPerguntas.html', {'titulo': titulo, 'code_user': code_user, 'todas': todas})
    else:
        return render(request, 'redirecionar.html', {'code_user': 0})


def get_code():
    from datetime import datetime
    dataHora = datetime.now()
    code = str(dataHora.year)
    code += str(dataHora.month)
    code += str(dataHora.day)
    code += str(dataHora.hour)
    code += str(dataHora.minute)
    code += str(dataHora.second)
    code = str(int(round(int(code) / 2, 0)))
    return code


@csrf_protect
def salvar_novo(request):
    code = get_code()
    code_user = request.POST.get("code_user")
    active = 1
    code_relation = request.POST.get("code_relation")
    question = request.POST.get("question")
    answer = request.POST.get("answer")

    p = Pergunta(
        code=code,
        code_user=code_user,
        active=active,
        code_relation=code_relation,
        question=question,
        answer=answer
    )
    p.save()
    return render(request, 'redirecionar.html', {'code_user': code_user})


def edicao(request, id):
    titulo = 'Edição de Perguntas e Respostas'
    global codeUser
    todas = Pergunta.objects.filter(code_user=codeUser)
    pergunta = Pergunta.objects.get(id=id)
    usuario = Usuario.objects.filter(code=codeUser)
    if len(usuario) > 0:
        return render(request, 'edicaoPerguntas.html',
                      {'titulo': titulo, 'perguntas': pergunta, 'todas': todas, 'code_user': codeUser})
    else:
        return render(request, 'redirecionar.html', {'code_user': 0})


@csrf_protect
def salvar_edicao(request):
    id = int(request.POST.get("id"))
    code_user = request.POST.get("code_user")
    code_relation = request.POST.get("code_relation")
    question = request.POST.get("question")
    answer = request.POST.get("answer")

    Pergunta.objects.filter(id=id).update(
        code_user=code_user,
        code_relation=code_relation,
        question=question,
        answer=answer
    )

    return render(request, 'redirecionar.html', {'code_user': code_user})


def delecao(request, id):
    titulo = 'Deleção de Perguntas e Respostas'
    global codeUser
    todas = Pergunta.objects.filter(code_user=codeUser)
    pergunta = Pergunta.objects.get(id=id)
    usuario = Usuario.objects.filter(code=codeUser)
    if len(usuario) > 0:
        return render(request, 'delecaoPerguntas.html',
                      {'titulo': titulo, 'perguntas': pergunta, 'todas': todas, 'code_user': codeUser})
    else:
        return render(request, 'redirecionar.html', {'code_user': 0})


@csrf_protect
def salvar_delecao(request):
    id = int(request.POST.get("id"))
    code_user = request.POST.get("code_user")
    Pergunta.objects.filter(id=id).delete()

    return render(request, 'redirecionar.html', {'code_user': code_user})


def chatbot(request, code_user):
    titulo = 'Chatbot'
    usuario = Usuario.objects.filter(code=code_user)
    if len(usuario) > 0:
        return render(request, 'chatbot.html', {'titulo': titulo, 'code_user': code_user})
    else:
        return render(request, 'redirecionar.html', {'code_user': 0})

# nlp - processamento de linguagem natural

def questao(request, code_user, code_before, question):
    question = question.replace('%20', ' ')
    qTemp = question.lower()
    if code_before > 0:
        consulta = Pergunta.objects.filter(code_user=code_user, code_relation=code_before, active=1)
        if len(consulta) <= 0:
            consulta = Pergunta.objects.filter(code_user=code_user, active=1)
    else:
        consulta = Pergunta.objects.filter(code_user=code_user, active=1)

    
    # capturas de informação

    # idade

    idade = 0
    import re
    if 'anos' in qTemp:
        valor = qTemp[qTemp.index('anos') - 8:qTemp.index('anos')]
        valor = re.sub('[^0-9]', '', qTemp)
        idade = valor

    else:
        tokens = qTemp.split(' ')
        for token in tokens:
            parts = re.sub('[^0-9]', '', token)
            if 1 <= len(parts) <= 3:
                idade = int(parts)


    # sexo


    sexo = ''
    _qTemp = qTemp.replace(',', '').replace('.', '').replace(';', '').replace('!', '')
    if ' m ' in _qTemp or 'masculino' in _qTemp:
        sexo = 'M'
    elif ' f ' in _qTemp or 'feminino' in _qTemp:
        sexo = 'F'


    # nome


    nome = ''


    # periodo

    periodo = ''
    if 'periodo' in qTemp:
        valor = qTemp[qTemp.index('periodo') - 5:qTemp.index('periodo')]
        valor = re.sub('[^0-9]', '', valor)

        if valor.isnumeric():
            periodo = int(valor)
            if periodo > 12:
                periodo = ''
            else:
                periodo = int(valor)

        else:
            valor = qTemp[qTemp.index('periodo'):qTemp.index('periodo') + 10]
            valor = re.sub('[^0-9]', '', valor)
            periodo = valor
            if periodo > 12:
                periodo =  ''
            else:
                periodo = int(valor)

    else:
        if 'semestre' in qTemp:
            valor = qTemp[qTemp.index('semestre') - 5:qTemp.index('semestre')]
            valor = re.sub('[^0-9]', '', valor)

            if valor.isnumeric():
                periodo = valor
                if periodo > 12:
                    periodo = ''
                else:
                    periodo = int(valor)
            else:
                valor = qTemp[qTemp.index('semestre'):qTemp.index('semestre') + 15]
                valor = re.sub('[^0-9]', '', valor)
                periodo = int(valor)
                if periodo > 12:
                    periodo =  ''
                else:
                    periodo = int(valor)

    # matricula
    import re
    matricula = ''
    if 'matricula' in qTemp:
        valor = qTemp[qTemp.index('matricula'):qTemp.index('matricula') + 10]
        matricula = valor
    elif 'fc' in qTemp:
        valor = qTemp[qTemp.index('fc'):qTemp.index('fc') + 10]
        matricula = valor
    else:
        tokens = qTemp.split(' ')
        for token in tokens:
            parts = re.sub('[^A-Za-z0-9]', '', token)
            if 'fc' in parts:
                matricula = parts

    # curso

    curso = ''
    cursos = ['administracao', 'agronomia', 'arquitetura e urbanismo', 'ciencias contabeis', 'direito',
              'engenharia ambiental', 'engenharia civil', 'engenharia eletrica', 'engenharia de producao',
              'engenharia de software', 'medicina veterinaria', 'zootecnia']

    qTemp = qTemp.replace(',', '').replace('.', '').replace(';', '').replace('!', '')
    _qTemp = qTemp.lower()
    for x in cursos:
        if x == _qTemp:
            curso = x
            break
        else:
            curso = ''

    # buscar informações
    lista = list()
    if len(nome) > 0 or len(sexo) > 0 or len(curso) > 0 or len(periodo) > 0 or len(matricula) > 0:
        code = get_code()
        global codeUser
        code_user = codeUser
        active = 1

        captura = Captura(
            code=code,
            code_user=code_user,
            active=active,
            name=nome,
            age=idade,
            sex=sexo.upper(),
            curso=curso,
            periodo=periodo,
            matricula=matricula
        )
        captura.save()
        lista.append({
            'code_current': 0,
            'code_user': code_user,
            'code_before': code_before,
            'question': question,
            'input': question,
            'output': 'Certo!'
        })

    else:

        # controle de abreviações
        qTemp = qTemp.replace('vc', 'voce')
        qTemp = qTemp.replace('vcs', 'voces')
        qTemp = qTemp.replace('eh', 'e')
        qTemp = qTemp.replace('tb', 'tambem')
        qTemp = qTemp.replace('tbm', 'tambem')
        qTemp = qTemp.replace('oq', 'o que')
        qTemp = qTemp.replace('td', 'tudo')
        qTemp = qTemp.replace('pq', 'por que')
        qTemp = qTemp.replace('rs', 'risos')

        # cria uma lista com query da consulta

        for x in consulta:
            lista.append({
                'code_current': x.code,
                'code_user': x.code_user,
                'code_before': code_before,
                'question': x.question,
                'input': question,
                'output': x.answer
            })

        # remove acentuação e espaços
        questao_recebida = unidecode(question)
        questao_recebida.replace('?', '')
        questao_recebida = questao_recebida.strip()
        # coloca em minúsculas
        questao_recebida = questao_recebida.lower()
        temp1 = questao_recebida.split(' ')
        temp2 = list()
        for x in temp1:
            temp2.append(x)

        questao_recebida = ' '.join(temp2)
        # percorre a lista de registros econtrados
        iguais = 0
        code = ''
        for x in lista:
            # remove acentuação e espaços
            questao_encontrada = unidecode(x['question'])
            questao_encontrada = questao_encontrada.replace('?', '')
            questao_encontrada = questao_encontrada.strip()
            # coloca em minúsculas
            questao_encontrada = questao_encontrada.lower()
            temp1 = questao_encontrada.split(' ')
            temp2 = list()
            for y in temp1:
                temp2.append(y)

            questao_encontrada = ' '.join(temp2)
            # cria uma lista para a questão recebida e uma para a questão encontrada
            qrList = questao_recebida.split(' ')
            qeList = questao_encontrada.split(' ')
            # conta as palavras recebidas que coincidem com as palavras de cada questão encontrada
            qtd = 0
            for y in qrList:
                if y in qeList:
                    qtd += 1

            if qtd >= iguais and qtd > 0:
                iguais = qtd
                code = x['code_current']

        if iguais == 0:
            lista = list()
            lista.append({
                'code_current': 0,
                'code_user': code_user,
                'code_before': code_before,
                'question': question,
                'input': question,
                'output': 'Desculpe, poderia tentar uma forma diferente?'
            })


        # deixa na lista somente a resposta correspondente

        else:
            if iguais > 0:
                correspondente = list()
                for x in lista:
                    if code == x['code_current']:
                        correspondente.append(x)
                        break
                lista = correspondente

    return JsonResponse(lista, safe=False)

# buscar informações
def api(request, code_user):
    titulo = 'API de Integração'
    usuario = Usuario.objects.filter(code=code_user)
    if len(usuario) > 0:
        return render(request, 'api.html', {'titulo': titulo, 'code_user': code_user})
    else:
        return render(request, 'redirecionar.html', {'code_user': 0})
