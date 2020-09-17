#!/usr/bin/python
#--------------------------
# Name: aurpy.py
# Autor: oTropicalista
# Github: https://github.com/oTropicalista
# Repository: https://github.com/oTropicalista/verbose-pineapple
# Data: 17/09/2020

import os
import time
import pycurl
import argparse
import subprocess
from io import BytesIO
from bs4 import BeautifulSoup

SEARCH_URL1 = "https://aur.archlinux.org/packages/?O=0&SeB=nd&K="
SEARCH_URL2 = "&outdated=&SB=n&SO=a&PP=50&do_Search=Go"

class params:
    version = "v0.1"
    title = """
      ____ ___  ___________  __  __
     / __ `/ / / / ___/ __ \/ / / /
    / /_/ / /_/ / /  / /_/ / /_/ / 
    \__,_/\__,_/_/  / .___/\__, /  
                   /_/    /____/ {}
    """.format(version)

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
    + Autor: oTropicalista
    + Github: https://github.com/oTropicalista

    aurpy.py [options] package_name
    [-S, --install]
    [-d, --description]
    """

def init():
    print(color.BLUE + color.BOLD + params.title + color.END)
    
    # tratar os argumentos de entrada
    psr = argparse.ArgumentParser(description='Ferramenta para pesquisa e instalação de pacotes do Arch User Repository', usage=msg())

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

    url = f"{SEARCH_URL1}{pkgname}{SEARCH_URL2}"
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
    print(color.BLUE + color.BOLD + "[=] Iniciando a instalação do pacote..." + color.END)
    #executar makepkg -si e pacman -U
    print("Current", os.getcwd()) #printa diretório atual
    i = "makepkg -si"
    making = subprocess.check_output(i, shell=True)
    
    print("\n\n" + color.GREEN + color.BOLD + "[+] Pacote instalado com sucesso!" + color.END)
    exit()


if __name__ == "__main__":
    init()
