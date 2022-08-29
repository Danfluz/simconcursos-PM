import PySimpleGUI as sg
from principal import disciplina

sg.theme('GreenMono')
layout = [
    [sg.Text('', size=10), sg.Text('Gerador de Simulados',font=('arial 12 bold'),size=(20,2)), sg.Text('ver. 1.0',font='arial 8', size=(10,2))],
    [sg.Text(''), sg.Text('O PDF será gerado em:',font='arial 11',auto_size_text=True), sg.FolderBrowse('Pasta',size=10, key='pastadestino')],
    [sg.Text('',size=20), sg.Button('Gerar',size=10,key="gerar"), sg.Text('')]
]

janela = sg.Window('Gerador de simulados', layout, icon='database/simulado.ico', finalize=True)

while True:
    event, values = janela.read()

    if event == sg.WINDOW_CLOSED:
        break
    if event == "gerar":
        output = values['pastadestino'] + '/'
        if output == '/':
            disciplina.gerar_simulado(topdf=True, caminhopdf=None)
        else:
            disciplina.gerar_simulado(topdf=True, caminhopdf=output)
        sg.popup('Pronto!',icon='database/simulado.ico')

janela.close()