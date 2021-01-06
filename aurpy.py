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
from rich.console import Console
from rich.table import Table
from rich import print

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

def msg(name=None):
    return """
    + Autor: {}
    + Github: {}

    aurpy.py [options] package_name
    [-S, --install]
    [-d, --description]
    """.format(params.AUTOR, params.GITHUB)

def init():
    print("[bold blue]{}[/bold blue]".format(params.TITLE))
    
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
    print("[bold blue][=] Pesquisando por:[/bold blue] {}...\n".format(pkgname))

    url = f"{params.SEARCH_URL1}{pkgname}{params.SEARCH_URL2}"
    html = get_html(url)

    #TO-D0: tratamento de erro no get da pagina

    soup = BeautifulSoup(html,  'html.parser')

    tb_result = soup.find("table", class_="results")
    tratar_results(tb_result)


def tratar_results(table):
    # recebe todo o html da table de resultados, formata
    # e exibe para o usuário escolher
    print("[bold blue]Resultados\n===============[/bold blue]")
    console = Console()
    tablee = Table(show_header=True)
    tablee.add_column("Nome")
    tablee.add_column("Versão")
    tablee.add_column("Descrição")


    for row in table.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) == 6:
            n = cells[0].find(text=True) #nome
            v = cells[1].find(text=True) #versao
            vv = cells[2].find(text=True) #votos
            p = cells[3].find(text=True) #popularidade
            d = cells[4].find(text=True) #descricao
            a = cells[5].find(text=True) #autor
            
            #list_pkgs(n, v, vv, p, d, a)
            
            tablee.add_row(n, v, d)
    console.print(tablee)


def list_pkgs(name, version, votes, popularity, description, author):
    # recebe todos os atributos dos pacotes
    # exibir resultados para escolha
    print("[bold blue][+] {}".format(name) + " - v:{}[/bold blue]".format(version))
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
    ''''
    Get the package snapshot
    '''
    print("[bold blue][=] Pesquisando por: [/bold blue] {}...\n".format(pkg))
    url = "https://aur.archlinux.org/{}.git".format(pkg)
    download = subprocess.run(
        ["git", "clone", url], # clona o diretório do pacote
        capture_output=True  #captura saida
    )

    if "Cloning" in str(download.stderr, 'utf-8'):
        print("[bold blue][=] Pacote encontrado ![/bold blue]")

        # TO-DO v1.0: mostrar dados do pacote para conferência

        time.sleep(2)
        print("[blue bold][=] Entrando no diretório clonado...[/blue bold]")
        os.chdir(pkg) # entra no diretorio clonado
        time.sleep(1)
        instal(pkg)
    else:
        print("[bold red][!] Erro: pacote não encontrado ![/bold red]\n")
        exit()

def direct_instal():
    # está no diretorio do pkgbuild
    os.system("makepkg -si")

def instal(name):
    #rodar makepkg e pacman -U
    print("[blue bold][=] Diretório atual: [/bold blue]" + os.getcwd())
    time.sleep(1)
    
    print("[blue bold][=] Pesquisando dependências...[/blue bold]")

    os.system("makepkg -s")
    time.sleep(2)
    print("[green bold][+] Dependências instaladas.[/green bold]")

    print("[blue bold][=] Criando pkgbuild do pacote....[/bold blue]")
    time.sleep(2)

    print("[blue bold][=] Instalando pacote...[/blue bold]")
    os.system("sudo pacman -U {}".format(name))
    
    print("\n\n[bold green][+] Pacote instalado com sucesso![bold green]")
    limpar_casa(name)
    exit()

def limpar_casa(name):
    #apagar diretório criado
    print("[bold blue][=] Limpando a bagunça...[/bold blue]")

    os.chdir("../")
    os.system("rm -rf {}".format(name))
    
    print(color.BLUE + color.BOLD + "[+] Tudo limpo! Não há mais o que fazer aqui." + color.END)
    print("[blue bold][*] Até a próxima![/bold blue]")


if __name__ == "__main__":
    init()
