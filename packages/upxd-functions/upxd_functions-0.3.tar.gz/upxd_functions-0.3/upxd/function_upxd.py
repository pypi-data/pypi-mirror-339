from random import choice
from time import sleep, time
from os import system
import google.generativeai as genai
#---- PRINT STYLE ------

def print_style(string, time=0.1, colors=['green', 'yellow', 'red', 'cian', 'purple']):

    ansci_colors = {'green':'\033[32m', 'yellow':'\033[33m', 'red':'\033[31m','cian':'\033[36m', 'purple':'\033[35m'}
#-------------
    color_keys = [key for key in colors]
#-------------
    for caracter in range(0, len(string)+1):
        choice_color = choice(color_keys)
        sleep(time)
        print(f"\r{ansci_colors[choice_color]}{string[0:caracter]}{ansci_colors[choice_color]}", end='')

#---------------------- FILTRAGEM DE CARACTERES ---------

def  filter(string, character_filtering=[], word_filtering=[]):
    new_string = ''
    string_filter_one = string
    for indice in word_filtering:
        string_filter_one = string_filter_one.replace(indice, '')
#-----------------
    for caractere in string_filter_one:
        if caractere not in character_filtering:
            new_string = new_string + caractere    
    
    return new_string

#---------- LIMPAR TERMINAL -----

def clear_terminal(comand='cls'):
    clears = ['cls', 'clear']
    if comand not in clears:
        pass
    else:
        system(comand)

#---------- WRITE FILE -----

def write_file(caminho, modo, encode, texto='', read=False):
        if read == True:
            with open(caminho, mode=modo, encoding=encode) as arquivo:
                return arquivo.read()
        else:
             with open(caminho, mode=modo, encoding=encode) as arquivo:
                 arquivo.write(f"{texto}")


def help_upgrade_IA(code='', simplificado=False):
    """Help troubleshooting bugs and checking features with the Gemini API"""
    forma =  'Retorne mensagens mais completas, detalhadas e com exemplos, não ultrapasse 70 caracteres por linha,' if simplificado == False else  "Retorne mensagens de forma clara e simplicficada, não ultrapasse 40 caracteres por linha,"
    genai.configure(api_key="AIzaSyDJfca9KZaUxRFaW-hVxe2HRqQbrAmttSE")
    Gnai = genai.GenerativeModel("gemini-2.0-flash")
    chat = Gnai.start_chat(history=[])
    instrução = f"Responda apenas perguntas relacionadas a erros e código python, erros relacionados ao sistema, sobre códigos e bibliotecas python, e informe possiveis mitigações para os erros.{forma}  as demais perguntas ignore e retorne 'none'"
    chat.history.append({'role': 'user', 'parts': [instrução]})    
    retorno = chat.send_message(f"{code}")
    return retorno.text