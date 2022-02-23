# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, make_response, request
import base64
import hashlib
import  requests
import  json
from datetime import * 
from fpdf import FPDF, HTMLMixin
from fpdf import FlexTemplate
import functools
sys.path.append(".")
from myencryptor import AESCipher
from contratpdfclass import PDF


contrat=Blueprint("contrat", __name__)
        
@contrat.route('/pdf',methods = ['POST', 'GET'])
def contrat_pdf():

    pdf = PDF('P', 'mm', 'A4')
    cipher = AESCipher('12lrtkjhy', 'muni1yyyft23')
    contratdt= cipher.decrypt(base64.b64decode(request.form.get('contrat'))).decode("utf-8")
    pdf.contrat_data= json.loads(contratdt)
    pdf.date_creation=date.fromisoformat(pdf.contrat_data['datedebcont']) if pdf.contrat_data['statutcont'] != "Brouillon" else date.today()
    pdf.date_debut=date.fromisoformat(pdf.contrat_data['datedebcont']) if pdf.contrat_data['datedebcont'] != None else date.today()
    pdf.date_fin=date.fromisoformat(pdf.contrat_data['datefincont']) if pdf.contrat_data['datefincont'] != None else date.today()
    pdf.frais_financier=float(pdf.contrat_data['fraisfinancier']) if pdf.contrat_data['fraisfinancier'] != None else 0
    pdf.poids = float(0)   
    pdf.totalht = 0   
    pdf.totalttc = 0 
    pdf.epw()
    epw = pdf.w - 2*pdf.l_margin
    pdf.logo = "logo.png"
    pdf.Title = "Contrat N° : "+str(pdf.contrat_data['idcontrat']) if pdf.contrat_data['statutcont'] != "Brouillon" else "Devis N° : "+str(pdf.contrat_data['idcontrat'])
    
    filename = ""
    if pdf.contrat_data['statutcont'] != "Brouillon":
        filename="contrat_"+str(pdf.contrat_data['idcontrat'])+"_"+str(str(pdf.contrat_data['client']['raisonsocial']) if pdf.contrat_data['client']!=False else "" )+"_"+str(date.today().strftime("%d%m%Y"))
    else:
        filename="devis_"+str(pdf.contrat_data['idcontrat'])+"_"+str(str(pdf.contrat_data['client']['raisonsocial']) if  pdf.contrat_data['client']!=False else "" )+"_"+str(date.today().strftime("%d%m%Y"))

    pdf.dte = str(pdf.date_creation.strftime("%d/%m/%Y"))
    pdf.commercial = str(pdf.contrat_data['commercial']) if pdf.contrat_data['commercial']!= None else ""
    if pdf.contrat_data['contacts'] and pdf.contrat_data['clientadresses']:
        for c in pdf.contrat_data['contacts'] :
            a =  (x for x in pdf.contrat_data['clientadresses'] if x['idadresse'] == c['adresse_idadresse'])
            c['adresse'] = next(a)
            if c['adresse']['type'] == 'chantier':
                pdf.chantier = c
            elif  c['adresse']['type'] == 'facturation':
                pdf.facturation = c

    pdf.add_font('Roboto', '', 'Roboto-Regular.ttf', uni=True)
    pdf.add_font('Roboto', 'B', 'Roboto-Bold.ttf', uni=True)
    pdf.add_font('Roboto', 'I', 'Roboto-Italic.ttf', uni=True)
    pdf.set_auto_page_break(True, margin=60)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.utilisation()
    pdf.tabledata()
    pdf.total()
    pdf.set_font("Roboto", size=12)
    response = make_response(pdf.output(dest='S'))
    response.headers.set('Content-Disposition', 'attachment', filename=filename + '.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response

  
      
if __name__ == '__main__': 
	contrat.run(debug = True)
