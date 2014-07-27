#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Fernando Oliveira >>> boletim_ifal.py  - 04/02/2014

# Instalação do mechanize - sudo pip install mechanize
# Instalação do texttable - sudo pip install texttable

import mechanize
import cookielib
import re
from texttable import Texttable
from datetime import date

current_year = date.today().year

#cria um navegador, um browser de codigo...
br = mechanize.Browser()
url = 'http://boletim.ifal.edu.br/' 
matricula = raw_input('Informe a sua matricula [20121T1104002T6]: ') or '20121T1104002T6' 
ano = raw_input('Informe o ano que deseja consultar [%s]: ' % current_year) or current_year

# Prepara para tratar cookies...
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Ajusta algumas opções do navegador...
br.set_handle_equiv(True)
br.set_handle_gzip(False)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Configura o user-agent.
# Do ponto de vista do servidor, o navegador agora é o Firefox.
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11;\
 U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615\
Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Acessando a URL usando o método HTTP GET
br.open(url)

# Para abrir o primeiro formulário, você pode selecionar com: #0
br.select_form(nr=0)

# Para mostrar os formularios e ver os campos a serem preenchidos,
# use um for sobre o br.forms()
for f in br.forms():
	pass
#	print f

# Preencher o formulário com os dados de login...
br.form['matricula'] = matricula
br.form['ano'] = ano

# Enviar o formulário usando o método HTTP POST
br.submit()

# E finalmente, busque o HTML retornado:
html = br.response().read()

# remove comentarios do html
def removeHtmlComments(raw_html):
	cleanr =re.compile('<!--.*?>')
	cleantext = re.sub(cleanr,'', raw_html)
	return cleantext

inicial_index = html.find('<!-- Mostrando as notas -->')

html = html[inicial_index:]
html = html[:html.find('</table>')]
html = removeHtmlComments(html)
html = html.replace('</tr>\n', '')
html = html.replace('\t', '')
html = html.replace('\n', '')

dictHtml = html.split('<tr>')

listaNotas = [['DISCIPLINA', 'PERÍODO', 'AV1', 'AV2', 'SUBS', 'FINAL', 'MEDIA', 'FALTAS', 'CONCEITO']]

for disciplina in dictHtml[1:]:
	disciplina = disciplina.strip()
	disciplina = disciplina.replace('   <td>', '')
	disciplina = disciplina.replace('<td>', '')
	disciplina = disciplina.split('</td>')

	disciplina[0] = disciplina[0].decode('iso-8859-1').encode('utf8')
	listaNotas.append(disciplina[:-1])

table = Texttable()
table.set_cols_dtype(['t', 't', 'f', 'f', 'f', 'f', 'f', 'i', 't']) 
table.set_cols_width([40,10,10,10,10,10,10,10,10])

table.add_rows(listaNotas)
print table.draw() + '\n'
