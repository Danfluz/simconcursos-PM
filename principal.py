import pdfplumber
from q_database import dados
from random import randint
from docx import Document
from docx.oxml.ns import qn
import datetime
import docx2pdf

class Disciplina():

    questoes = dados
    portugues = 'database/perguntas_portugues.pdf'
    raciocinio = 'database/perguntas_raciocinio.pdf'
    administrativo = 'database/perguntas_administrativo.pdf'
    constitucional = 'database/perguntas_constitucional.pdf'
    penal = 'database/perguntas_penal.pdf'
    processual_penal = 'database/perguntas_processual_penal.pdf'
    militar_penal = 'database/perguntas_militar_penal.pdf'

    def __init__(self, nome=None):
        self.nome = nome
        self.caminho = f'database/perguntas_{nome}.pdf'
        self.gabarito = self.gabarito()


    def dicio_pdf(self, caminhopdf):
        contadorquestao = 1
        dicio_questoes = {}
        questao_atual = ''

        with pdfplumber.open(caminhopdf) as pdf:
            base1 = pdf.pages

            for page in base1:
                arquivo = page.extract_text()
                for letra in arquivo:
                    if letra == '♥':
                        if questao_atual == '':
                            continue
                        dicio_questoes[f'{"questão" + str(contadorquestao)}'] = questao_atual
                        contadorquestao += 1
                        questao_atual = ''
                    else:
                        questao_atual += letra
                dicio_questoes[f'{"questão" + str(contadorquestao)}'] = questao_atual

        return dicio_questoes


    def gabarito(self):
        if self.nome == None:
            return 'Erro. Para a função gabarito, o nome da disciplina precisa ser definido.'
        materia = self.caminho.replace('perguntas', 'gabarito')
        materia = materia.replace('pdf', 'txt')
        respostas = open(materia)
        gabaritado = {}
        for perg in respostas.readlines():
            gabaritado[perg[:-2]] = perg[-2]
        respostas.close()

        return gabaritado

    def sortear(self, nome=None):
        if nome == None:
            nome = self.nome
        if nome == 'portugues':
            numeromax = 70
            qtd_questoes = 10
        elif nome == 'raciocinio':
            numeromax = 70
            qtd_questoes = 10
        elif nome == 'administrativo':
            numeromax = 120
            qtd_questoes = 10
        elif nome == 'constitucional':
            numeromax = 120
            qtd_questoes = 15
        elif nome == 'penal':
            numeromax = 120
            qtd_questoes = 15
        elif nome == 'processual_penal':
            numeromax = 90
            qtd_questoes = 17
        elif nome == 'militar_penal':
            numeromax = 10
            qtd_questoes = 3
        else:
            return 'Erro. O nome definido para a função sortear é inválido.'

        lista_questoes = []

        while len(lista_questoes) < qtd_questoes:
            aleatorio = randint(1,numeromax)

            questaotemp = self.questoes[nome][f'questão{aleatorio}']
            if not questaotemp[1].isdigit():
                questaotemp = '0'+questaotemp
            if questaotemp in lista_questoes:
                continue
            else:
                lista_questoes.append(questaotemp)

        lista_questoes.sort(key=lambda s: int(s[:2]))
        return lista_questoes

    def gerar_simulado(self, printsim=False, topdf=False, caminhopdf=None):

        simulado = [self.sortear('portugues'),
                    self.sortear('raciocinio'),
                    self.sortear('administrativo'),
                    self.sortear('constitucional'),
                    self.sortear('penal'),
                    self.sortear('processual_penal'),
                    self.sortear('militar_penal')
                    ]

        if printsim == True and topdf == False:

            for materia in simulado:
                if materia == simulado[0]:
                    print('')
                    print('=== PORTUGUÊS ===')
                    print('')
                elif materia == simulado[1]:
                    print('')
                    print('=== RACIOCÍNIO LÓGICO ===')
                    print('')
                elif materia == simulado[2]:
                    print('')
                    print('=== DIREITO ADMINISTRATIVO ===')
                    print('')
                elif materia == simulado[3]:
                    print('')
                    print('=== DIREITO CONSTITUCIONAL ===')
                    print('')
                elif materia == simulado[3]:
                    print('')
                    print('=== DIREITO PENAL ===')
                    print('')
                elif materia == simulado[5]:
                    print('')
                    print('=== DIREITO PROCESSUAL PENAL ===')
                    print('')
                elif materia == simulado[6]:
                    print('')
                    print('=== DIREITO PENAL MILITAR E PROCESSUAL PENAL MILITAR ===')
                    print('')
                for questao in materia:
                    print(questao)
        if printsim == False and topdf == True:
            simsimulado = []
            simsimulado.append(f'SIMULADO DE CONCURSO - POL MILITAR - GERADO EM {datetime.datetime.now().strftime("%d/%m/%Y, às %H:%M:%S")}\n\n')
            for materia in simulado:
                if materia == simulado[0]:
                    simsimulado.append('\n======== PORTUGUÊS ========\n')
                elif materia == simulado[1]:
                    simsimulado.append('\n====== RACIOCÍNIO LÓGICO ======\n')
                elif materia == simulado[2]:
                    simsimulado.append('\n===== DIREITO ADMINISTRATIVO =====\n')
                elif materia == simulado[3]:
                    simsimulado.append('\n===== DIREITO CONSTITUCIONAL =====\n')
                elif materia == simulado[4]:
                    simsimulado.append('\n======== DIREITO PENAL ========\n')
                elif materia == simulado[5]:
                    simsimulado.append('\n==== DIREITO PROCESSUAL PENAL ====\n')
                elif materia == simulado[6]:
                    simsimulado.append('\n=== DIREITO PENAL MILITAR E PROCESSUAL PENAL MILITAR ===\n')
                for questao in materia:
                    simsimulado.append('\n'+questao+'\n')

            # texto = open('database\simulado.txt', 'w', encoding='UTF-8')
            # texto.write(''.join(simsimulado))
            # texto.close()

            documento = Document()
            section = documento.sections[0]
            sectPr = section._sectPr
            cols = sectPr.xpath('./w:cols')[0]
            cols.set(qn('w:num'), '2')
            documento.add_paragraph(''.join(simsimulado))
            documento.save('database/simsimulado.docx')
            if caminhopdf == None:
                caminhopdf = 'simulado.pdf'
            else:
                caminhopdf = caminhopdf + 'simulado.pdf'
            docx2pdf.convert('database/simsimulado.docx', caminhopdf)

            simsimulado = 'Pronto.'
            return simsimulado
        else:
            return simulado


disciplina = Disciplina()

