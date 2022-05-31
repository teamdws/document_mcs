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
from reparationclass import PDF


br=Blueprint("br", __name__)
        
@br.route('/pdf',methods = ['POST', 'GET'])
def reparation():

    pdf = PDF('P', 'mm', 'A4')
    cipher = AESCipher('12lrtkjhy', 'muni1yyyft23')
    contratdt= cipher.decrypt(base64.b64decode(request.form.get('intervention'))).decode("utf-8")
    pdf.contrat_data= json.loads(contratdt)
    pdf.date=date.fromisoformat(pdf.contrat_data['dateprevue']) if pdf.contrat_data['dateprevue'] != None else date.today()
    pdf.datecreation= datetime.strptime(pdf.contrat_data['dateheurecreat'], '%Y-%m-%d %H:%M:%S') if pdf.contrat_data['dateheurecreat'] != None else date.today()
    
    pdf.epw()
    epw = pdf.w - 2*pdf.l_margin
    pdf.logo = "logo.png"
    pdf.Title = "Ordre de réparation : "+str(pdf.contrat_data['idintervention']) 
    
    filename = "Ordre_de_réparation_"+str(pdf.contrat_data['idintervention']) 
   
    pdf.dte = str(pdf.date.strftime("%d/%m/%Y"))
    pdf.dtec = str(pdf.datecreation.strftime("%d/%m/%Y"))
    pdf.commercial = str(pdf.contrat_data['user']) if pdf.contrat_data['user']!= None else ""
    if 'contacts' in pdf.contrat_data and 'clientadresses' in pdf.contrat_data :
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
    pdf.set_auto_page_break(True, margin=10)
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
	br.run(debug = True)
