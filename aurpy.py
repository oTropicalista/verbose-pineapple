#!/usr/bin/python
#------------------------------------------------------------------+
# Name: aurpy.py                                                   |
# Autor: oTropicalista                                             |
# Github: https://github.com/oTropicalista                         |
# Repository: https://github.com/oTropicalista/verbose-pineapple   |
# Data: 17/09/2020                                                 |
#------------------------------------------------------------------+

#To-do
# Tratamento de erros no instal() e no limpar_casa()
# 

import os
import time
import pycurl
import argparse
import subprocess
from io import BytesIO
from bs4 import BeautifulSoup
from configparser import ConfigParser

class params:
    cfg = ConfigParser()
    cfg.read('config.txt')

    NAME = cfg['app']['NAME']
    VERSION = cfg['app']['VERSION']
    DESCRIPTION = cfg['app']['DESCRIPTION']
    AUTOR = cfg['app']['AUTOR']
    GITHUB = cfg['app']['GITHUB']
    SEARCH_URL1 = cfg['params']['URL1']
    SEARCH_URL2 = cfg['params']['URL2']
    TITLE = """
      ____ ___  ___________  __  __
     / __ `/ / / / ___/ __ \/ / / /
    / /_/ / /_/ / /  / /_/ / /_/ / 
    \__,_/\__,_/_/  / .___/\__, /  
                   /_/    /____/ {}
    """.format(VERSION)

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def msg(name=None):
    return """
    + Autor: {}
    + Github: {}

    aurpy.py [options] package_name
    [-S, --install]
    [-d, --description]
    """.format(params.AUTOR, params.GITHUB)

def init():
    print(color.BLUE + color.BOLD + params.TITLE + color.END)
    
    # tratar os argumentos de entrada
    psr = argparse.ArgumentParser(description=''.format(), usage=msg())

    # argumentos
    psr.add_argument('Name',
                     metavar='name',
                     type=str,
                     help='nome do pacote')
    psr.add_argument('-S',
                     action='store_true',
                     help='instalar pacote')

    args = psr.parse_args()

    if args.S:
        download(args.Name)
    else:
        search_pkg(args.Name)


def search_pkg(pkgname):
    # pesquisar no AUR o nome passado
    print(color.BOLD + color.BLUE + "[=] Pesquisando por: " + color.END + "{}...\n".format(pkgname))

    url = f"{params.SEARCH_URL1}{pkgname}{params.SEARCH_URL2}"
    html = get_html(url)

    #TO-D0: tratamento de erro no get da pagina

    soup = BeautifulSoup(html,  'html.parser')

    tb_result = soup.find("table", class_="results")
    tratar_results(tb_result)


def tratar_results(table):
    # recebe todo o html da table de resultados, formata
    # e exibe para o usuário escolher

    print(color.BOLD + "Resultados\n===============" + color.END)

    for row in table.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) == 6:
            n = cells[0].find(text=True) #nome
            v = cells[1].find(text=True) #versao
            vv = cells[2].find(text=True) #votos
            p = cells[3].find(text=True) #popularidade
            d = cells[4].find(text=True) #descricao
            a = cells[5].find(text=True) #autor
            
            list_pkgs(n, v, vv, p, d, a)


def list_pkgs(name, version, votes, popularity, description, author):
    # recebe todos os atributos dos pacotes
    # exibir resultados para escolha
    print(color.BOLD + color.BLUE + "[+] {}".format(name) + " - v:{}".format(version) + color.END)
    print(description)


def get_html(url):
    # pegar pagina do AUR através da lib cUrl
    b_obj = BytesIO()
    crl = pycurl.Curl()

    crl.setopt(crl.URL, url)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform()
    crl.close() 

    get_body = b_obj.getvalue()

    return get_body.decode('utf-8')


def download(pkg):
    print(color.BOLD + color.BLUE + "[=] Pesquisando por: " + color.END + "{}...\n".format(pkg))
    url = "https://aur.archlinux.org/{}.git".format(pkg)
    download = subprocess.run(
        ["git", "clone", url], # clona o diretório do pacote
        capture_output=True  #captura saida
    )

    if "Cloning" in str(download.stderr, 'utf-8'):
        print(color.BLUE + color.BOLD + "[=] Pacote encontrado !" + color.END)

        # TO-DO v1.0: mostrar dados do pacote para conferência

        time.sleep(2)
        print(color.BLUE + color.BOLD + "[=] Entrando no diretório clonado..." + color.END)
        os.chdir(pkg) # entra no diretorio clonado
        time.sleep(1)
        instal(pkg)
    else:
        print(color.RED + color.BOLD + "[!] Erro: pacote não encontrado !\n" + color.END)
        exit()
    

def instal(name):
    #rodar makepkg e pacman -U
    print(color.BLUE + color.BOLD + "[=] Diretório atual: " + + color.END + os.getcwd())
    time.sleep(1)
    
    print(color.BLUE + color.BOLD + "[=] Pesquisando dependências..." + color.END)

    os.system("makepkg -s")
    time.sleep(2)
    print(color.GREEN + color.BOLD + "[+] Dependências instaladas." + color.END)

    print(color.BLUE + color.BOLD + "[=] Criando pkgbuild do pacote...." + color.END)
    time.sleep(2)

    print(color.BLUE + color.BOLD + "[=] Instalando pacote..." + color.END)
    os.system("sudo pacman -U {}".format(name))
    
    print("\n\n" + color.GREEN + color.BOLD + "[+] Pacote instalado com sucesso!" + color.END)
    limpar_casa(name)
    exit()

def limpar_casa(name):
    #apagar diretório criado
    print(color.BLUE + color.BOLD + "[=] Limpando a bagunça..." + color.END)

    os.chdir("../")
    os.system("rm -rf {}".format(name))
    
    print(color.BLUE + color.BOLD + "[+] Tudo limpo! Não há mais o que fazer aqui." + color.END)
    print(color.BLUE + color.BOLD + "[*] Até a próxima!" + color.END)


if __name__ == "__main__":
    init()
