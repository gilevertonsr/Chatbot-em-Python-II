qTemp = 'fc20131013'

idade = 0
import re

if 'anos' in qTemp:
    print(qTemp)
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


nome = ' '

# periodo

periodo = ' '
if 'periodo' in qTemp:
    valor = qTemp[qTemp.index('periodo') - 5:qTemp.index('periodo')]
    valor = re.sub('[^0-9]', '', valor)

    if valor.isnumeric():
        periodo = int(valor)
    else:
        valor = qTemp[qTemp.index('periodo'):qTemp.index('periodo') + 10]
        valor = re.sub('[^0-9]', '', valor)
        periodo = int(valor)

elif 'semestre' in qTemp:
    valor = qTemp[qTemp.index('semestre') - 5:qTemp.index('semestre')]
    valor = re.sub('[^0-9]', '', valor)

    if valor.isnumeric():
        periodo = valor
    else:
        valor = qTemp[qTemp.index('semestre'):qTemp.index('semestre') + 15]
        valor = re.sub('[^0-9]', '', valor)
        periodo = int(valor)

else:
    tokens = qTemp.split(' ')
    for token in tokens:
        parts = re.sub('[^0-9]', '', token)
        if 1 <= len(parts) <= 2:
            periodo = parts

# matricula
import re
matricula = ''
if 'matricula' and 'fc' in qTemp:
    valor = qTemp[qTemp.index('fc'):qTemp.index('fc') + 10]
    matricula = valor
    print(matricula)
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

_qTemp = qTemp.replace(',', '').replace('.', '').replace(';', '').replace('!', '')
_qTemp = qTemp.lower()
for x in cursos:
    if x == _qTemp:
        curso = x
    else:
        curso = ''


