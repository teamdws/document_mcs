# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, make_response, request
import  requests
import  json
from fpdf import FPDF
from datetime import *
bon_livraison=Blueprint("bon/livraison", __name__)

def footer(pdf):
  pdf.set_auto_page_break(False)
  epw = pdf.w - 2*pdf.l_margin
  th = pdf.font_size
  # Go to 1.5 cm from bottom
  pdf.set_y(-30)
  #company----------------------------------
  pdf.set_font('Arial','B',9) 
  pdf.cell(epw/5, 2*th,  txt="AGENCE PARIS", align='C')
  pdf.cell(epw/5, 2*th, txt="AGENCE LYON",align='C')
  pdf.cell(epw/5, 2*th, txt= "AGENCE MEAUX",  align='C')
  pdf.cell(epw/5, 2*th,  txt="AGENCE AGEN",align='C')
  pdf.cell(epw/5, 2*th, txt= "AGENCE AVIGNON",  align='C')
  pdf.ln(th)
  pdf.set_font('Arial',size=8) 
  pdf.cell(epw/5, 2*th,  txt="100 Avenue de choisy", align='C')
  pdf.cell(epw/5, 2*th,  txt="6 Rue des Catelines", align='C')
  pdf.cell(epw/5, 2*th,  txt="2 Rue de la Briqueterie", align='C')
  pdf.cell(epw/5, 2*th,  txt="89 Rue Joseph Teulère", align='C')
  pdf.cell(epw/5, 2*th,  txt="135 Avenue Pierre Sémard", align='C')
  pdf.ln(th)
  pdf.cell(epw/5, 2*th,  txt="94190 Villeneuve St Georges", align='L')
  pdf.cell(epw/5, 2*th,  txt="69720 St Laurent de Mure", align='R')
  pdf.cell(epw/6, 2*th,  txt="77470 Poincy", align='C')
  pdf.cell(epw/4, 2*th,  txt="Z.A. de Trignac 47240 Castelculier", align='L')
  pdf.cell(epw/5, 2*th,  txt="MIN BAT.3 84000 Avignon", align='R')
  pdf.ln(th)
  pdf.cell(epw/5, 2*th,  txt="Tél : 01.43.89.06.00", align='C')
  pdf.cell(epw/5, 2*th,  txt="Tél : 04.37.58.44.26", align='C')
  pdf.cell(epw/5, 2*th,  txt="Tél : 01.60.09.81.31", align='C')
  pdf.cell(epw/5, 2*th,  txt="Tél : 05.53.48.32.94", align='C')
  pdf.cell(epw/5, 2*th,  txt="Tél : 04.90.87.18.08", align='C')
  pdf.ln(th*2)
  pdf.set_font('Arial','I',8)  
  #pdf.multi_cell(190, 5, txt="SARL AU CAPITAL DE 301200 Fax : 01.43.89.64.35 Email : contact@stmp-location.com \nR.C.S B 389 856 261 00026 - APE 46669 INTRA T.V.A FR 25 389 856 261", align = 'C')
  pdf.multi_cell(190, 3, txt="ETG LOCATION - 531 994 317 RCS Agen - APE : 7732Z - SARL au capital de 1000"+chr(128)+" -N° TVA : FR59531994317\n Web : www.etg-location.fr - Email : etglocationparis@gmail.com - Tél : 0553483294 -Fax : 0970616386", align = 'C')
  pdf.cell(0, 10, 'Page %s' % pdf.page_no(), 0, 0, 'C')

@bon_livraison.route('/pdf',methods = ['POST', 'GET'])
def contrat_pdf():
  pdf = FPDF('P', 'mm', 'A4' )
  pdf.add_page()
  epw = pdf.w - 2*pdf.l_margin
  th = pdf.font_size
  pdf.set_fill_color(220)


  #logo------------------------------------
  pdf.image("./logo.png", 75, 8, 60)
  pdf.set_font('Times','',10.0) 
  pdf.ln(20)
  pdf.set_left_margin(8)
  pdf.set_right_margin(8)

  pdf.ln(4*th)
  #header---------------------------------------------
  tmpVarX = pdf.get_x()
  tmpVarY = pdf.get_y()
  pdf.set_font('Arial','B',17) 
  pdf.multi_cell(epw/2.3, 2*th, "Bon de livraison", align="C", border=1)
  pdf.ln(1)   
  pdf.set_font('Arial',size=10) 
  pdf.cell(epw/2.3, th,  align="C", border=1)
  pdf.ln(8)     
  pdf.multi_cell(epw/2.3, th, '\n'+'\n'+'\n'+"Contact : "+""+ " " +""+ " " +""+'\n'+"Tél : "+"", border=1)
  pdf.set_xy(tmpVarX+112,tmpVarY)
  pdf.multi_cell(epw/2.3, 2*th, "Lieu d'utilisation : ", align="C", border=1)
  pdf.ln(1)   
  pdf.set_xy(tmpVarX+112,tmpVarY)
  pdf.multi_cell(epw/2.3, th, ""+'\n'+
  ""+'\n'+""+ " " +""+'\n'+""+ " " +""+'\n\n'+"Demandé par : "+""+ " " +""+ " " +""+'\n'+"Tél : "+""+'\n'+"Fax : " ,border=1)
  pdf.ln(7)
  tmpVarX = pdf.get_x()
  tmpVarY = pdf.get_y()
  pdf.multi_cell(epw/2.3, th, ""+'\n'+'\n'+'\n' ,border=1)
  pdf.set_xy(tmpVarX+112,tmpVarY)
  pdf.multi_cell(epw/2.3, th,"\n\n\n", border=1)
  pdf.ln(4)
  #affichage line of livraison-------------------------------------------------------
  pdf.set_font('Arial','B',10.0) 
  pdf.cell(  epw/30 , 2*th, fill=True, txt="Qté", align='C', border=1)
  pdf.cell(  epw/7, 2*th, fill=True, txt="Référence",  align='C', border=1) 
  pdf.cell(  125.10, 2*th, fill=True, txt="Dénomination",align='C', border=1)
  pdf.cell(  36.5, 2*th, fill=True, txt="Observation",  align='C', border=1)
  pdf.ln(2*th)  
  response = make_response(pdf.output(dest='S'))
  #response.headers.set('Content-Disposition', 'attachment', filename=filename + '.pdf')
  response.headers.set('Content-Type', 'application/pdf')
  return response

if __name__ == '__main__': 
	bon_livraison.run(debug = True)
