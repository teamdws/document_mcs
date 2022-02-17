# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, make_response, request
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import  requests
import  json
from datetime import * 
from fpdf import FPDF, HTMLMixin
from fpdf import FlexTemplate
import functools

contrat=Blueprint("contrat", __name__)
class AESCipher:
    def __init__(self, key, iv):
        self.key = hashlib.sha256(key.encode('utf-8')).hexdigest()[:32].encode("utf-8")
        self.iv = hashlib.sha256(iv.encode('utf-8')).hexdigest()[:16].encode("utf-8")

  

    def encrypt( self, raw ):
        raw = raw.encode('utf-8')
        raw = pad(raw, AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv )
        return unpad(cipher.decrypt(enc) , AES.block_size )
poids = float(0)   
totalht = 0   
totalttc = 0  

        
@contrat.route('/pdf',methods = ['POST', 'GET'])
def contrat_pdf():
    cipher = AESCipher('12lrtkjhy', 'muni1yyyft23')
    contratdt= cipher.decrypt(base64.b64decode(request.form.get('contrat'))).decode("utf-8")
    contrat_data= json.loads(contratdt)
    date_creation=date.fromisoformat(contrat_data['datedebcont']) if contrat_data['statutcont'] != "Brouillon" else date.today()
    date_debut=date.fromisoformat(contrat_data['datedebcont']) if contrat_data['datedebcont'] != None else date.today()
    date_fin=date.fromisoformat(contrat_data['datefincont']) if contrat_data['datefincont'] != None else date.today()
     
    frais_financier=float(contrat_data['fraisfinancier']) if contrat_data['fraisfinancier'] != None else 0
    class PDF(FPDF, HTMLMixin):

        def header(self):
            # Rendering logo:
            self.image( self.logo , 10, 8, 33)
            self.set_font("Roboto","B", size=18)
            self.cell(80)
            
            self.cell(0, 10, self.Title, 0, 0, "R")
            self.set_font("Roboto","", size=10)
            self.ln()
            self.cell(0, 0, "Date : "+self.dte+" Suivi par : "+self.commercial, 0, 0, "R")
            self.code39( str(contrat_data['idcontrat']), x= pdf.l_margin  , y=25, w=1, h=5)
            self.ln(20)
            
        def utilisation(self):
            tmpVarY = self.get_y()
            self.set_fill_color(222 , 85 , 90)
            self.set_text_color(255 , 255 , 255)
            self.cell(epw/3, self.font_size + 5, fill=True, txt="Lieu d'utilisation ", align="C", border=0)
            self.set_text_color(0 , 0 , 0)
            self.ln(self.font_size + 5)
            tmpVarX = self.get_x() + epw/3
            if hasattr( self, 'chantier') and self.chantier['adresse']:
                if self.chantier['adresse']['TITRE']:
                    self.cell(0,  self.font_size + 2, self.chantier['adresse']['TITRE'], 0, 1)
                self.cell(0,  self.font_size +2 , str(self.chantier['adresse']['STREET_NUMBER']) +" "+ str(self.chantier['adresse']['ROUTE']) , 0, 1)
                self.cell(0,  self.font_size +2 ,str(self.chantier['adresse']['codepostal']) +"    "+str(self.chantier['adresse']['ville']), 0, 1)
                self.cell(0,  self.font_size +2 ,"Contact : "+str(self.chantier['civilite'])+ " " +self.chantier['prenom']+ " " +self.chantier['nom'], 0, 1)
                self.cell(0,  self.font_size +2 ,"Tél : "+str(self.chantier['telmobile']), 0, 1)
            self.set_xy(tmpVarX+ epw/3,tmpVarY)
            self.set_fill_color(222 , 85 , 90)
            self.set_text_color(255 , 255 , 255)
            self.cell(epw/3, self.font_size + 5, fill=True, txt="CLIENT N° : "+str(contrat_data['client']['idclient']) , align="C", border=0)
            self.set_text_color(0 , 0 , 0)
            self.set_xy(tmpVarX+epw/3,tmpVarY+ self.font_size + 5)
            if hasattr( self, 'facturation') and self.facturation['adresse']:
                if self.facturation['adresse']['TITRE']:
                    self.cell(0,  self.font_size + 2, str(contrat_data['client']['raisonsocial']), 0, 1)
                    self.set_x(tmpVarX+ epw/3)
                    self.cell(0,  self.font_size + 2, self.facturation['adresse']['TITRE'], 0, 1)
                    self.set_x(tmpVarX+ epw/3)
                self.cell(0,  self.font_size +2 , str(self.facturation['adresse']['STREET_NUMBER']) +" "+ str(self.facturation['adresse']['ROUTE']) , 0, 1)
                self.set_x(tmpVarX+ epw/3)
                self.cell(0,  self.font_size +2 ,str(self.facturation['adresse']['codepostal']) +"    "+str(self.facturation['adresse']['ville']), 0, 1)
                self.set_x(tmpVarX+ epw/3)
                self.cell(0,  self.font_size +2 ,"Contact : "+str(self.facturation['civilite'])+ " " +self.facturation['prenom']+ " " +self.facturation['nom'], 0, 1)
                self.set_x(tmpVarX+epw/3)
                self.cell(0,  self.font_size +2 ,"Tél : "+str(self.facturation['telmobile']), 0, 1)
            self.ln(7)
            line_height = pdf.font_size * 2
            col_width = pdf.epw / 4
            TABLE_COL_NAMES = ("Date de début du contrat", "Date de fin du contrat", "Période de location", "Facturation sur")
            TABLE_DATA = (str(date_debut.strftime("%d/%m/%Y")), str(date_fin.strftime("%d/%m/%Y")), str(contrat_data['nbdays'])+" Jours", str(str(contrat_data['frequencefacturation']) if contrat_data['frequencefacturation']!=None else "")+"  mois")
            self.set_fill_color(222 , 85 , 90)
            self.set_text_color(255 , 255 , 255)
            for col_name in TABLE_COL_NAMES:
                self.cell(col_width, line_height, col_name, border=0 ,fill=True)
            self.ln(line_height)
            self.set_text_color(0 , 0 , 0)
            self.set_draw_color(222 , 85 , 90)
            for col_name in TABLE_DATA:
                self.cell(col_width, line_height, col_name, border=1 ,fill=False)
            self.ln(line_height)
            
            self.multi_cell(0, pdf.font_size +3,"""Nos tarifs sont dégressifs, la valeur des prix varie en fonction de location. Toute reprise anticipée avant la date prévue par le contrat de location entrainera une revalorisation des prix à la hausse. """, border=1)
            self.ln(4)
        

        def tabledata(self):
            def transformservice(n):
                s = {}
                global totalht
                global totalttc
                s['Qte'] = n['Qte']
               
                s['reference'] = ""
                s['denomination'] = str(n['titreservice']) if n['titreservice'] !=None else " "
                s['montant_net'] = float(n['prix'])  if n['prix'] !=None else 0
                s['tva'] = float(n['tva'])  if n['tva'] !=None else 0
                try:
                    s['montantHT'] =  (int(n['Qte'])* s['montant_net']) * (1 - float(n['remise'])/100)
                except:
                    s['montantHT'] =  0 
                totalht = totalht+ s['montantHT']
                totalttc = totalttc+ s['montantHT'] * (1+ s['tva']/100)
                return s
                
            def transform(n):
                s = {}
                global poids
                global totalht
                global totalttc
                s['Qte'] = int(n['Qte']) if n['Qte']!=None else 0
                s['poids'] = float(n['poids']) if n['poids']!=None else 0
                s['tva'] = float(n['tva'])  if n['tva'] !=None else 0
                poids = poids + s['Qte'] * s['poids']

                ref = ""
                if  n['serialisable']==0:
                    ref = str(n['reference']) if n['reference']!=None else "" 
                elif n['serialisable']==1 and n['equipement_idequipement'] !=None:
                    a =  (x for x in contrat_data['detailequipements'] if n['idcategorie']== x['categorie_idcategorie'])
                    ref = (next(a))['refinterne']
                s['reference'] = ref
                s['denomination'] = n['denomination'] if n['denomination'] !=None else " "
                s['montant_net'] = float(n['prix'])  if n['prix'] !=None else 0
                try:
                    s['montantHT'] = (int(n['Qte'])* s['montant_net'] * contrat_data['nbdays']) * (1 - float(n['remise'])/100)
                    
                except:
                    s['montantHT'] =  0 
                totalht = totalht+ s['montantHT']
                totalttc = totalttc+ s['montantHT'] * (1+ s['tva']/100)
                return s
            
            def render_table_header():
                self.set_fill_color(222 , 85 , 90)
                self.set_text_color(255 , 255 , 255)
                self.cell(  epw/16, self.font_size +3, fill=True, txt="Qté", align='C', border=1)
                self.cell(  epw/8,  self.font_size +3, fill=True, txt="Ref",  align='C', border=1) 
                self.cell(  (9*epw)/16, self.font_size +3, fill=True, txt="Description",align='C', border=1)
                self.cell(  epw/8, self.font_size +3, fill=True, txt="PU BRUT",  align='C', border=1)
                self.cell(  epw/8, self.font_size +3, fill=True, txt="MT HT ",  align='C', border=1) 
                self.set_text_color(0 , 0 , 0)
                self.ln( self.font_size +3)
            render_table_header()
            if len(contrat_data['equipements'])>=0:
                result = map(transform, contrat_data['equipements'])
                self.set_font("Roboto","" ,10)
                for r in result:
                    
                    self.cell(  epw/16, self.font_size +3, fill=False, txt= str(r['Qte']), align='L', border=1)
                    self.cell(  epw/8,  self.font_size +3, fill=False, txt= str( r['reference']),  align='L', border=1) 
                    self.cell(  (9*epw)/16, self.font_size +3, fill=False, txt= (r['denomination'])[:60],align='L', border=1)
                    self.cell(  epw/8, self.font_size +3, fill=False, txt= str(round(r['montant_net'],2))+" €",  align='L', border=1)
                    self.cell(  epw/8, self.font_size +3, fill=False, txt= str(round(r['montantHT'],2))+" €",  align='L', border=1) 
                    self.ln( self.font_size +3)
                if len(contrat_data['services']) >=0 :
                    
                    self.set_font("Roboto", "I", 10)
                    result1 = map(transformservice, contrat_data['services'])
                    for r in result1 :
                        self.cell(  epw/16, self.font_size +3, fill=False, txt= str(r['Qte']), align='L', border=1)
                        self.cell(  epw/8,  self.font_size +3, fill=False, txt= str( r['reference']),  align='L', border=1) 
                        self.cell( (9*epw)/16, self.font_size +3, fill=False, txt= (r['denomination'])[:60],align='L', border=1)
                        self.cell(  epw/8, self.font_size +3, fill=False, txt= str(round(r['montant_net'],2))+" €",  align='L', border=1)
                        self.cell(  epw/8, self.font_size +3, fill=False, txt= str(round(r['montantHT'],2))+" €",  align='L', border=1) 
                        self.ln( self.font_size +3)
                    self.set_font("Roboto","" ,12)
                if len(contrat_data['mentions'])>=0:
                    
                    self.set_font("Roboto","B" ,12)
                    for i in range(len(contrat_data['mentions'])):
                        self.multi_cell(  epw, self.font_size +3, fill=False, txt=  str(contrat_data['mentions'][i]['contenuoption']),  align='L', border=1) 
                        self.ln(0) 
                    self.set_font("Roboto","" ,12)
        def total(self):
            self.cell(0, self.font_size +3,"Poids (Kg): "+str(poids) , align="R" ,border=0)
            self.ln(self.font_size +3)
            
            self.set_font("Roboto","" ,10)
            if self.will_page_break((self.font_size +5) * 8):
                self.ln((self.font_size +5) * 8)
             
            self.cell(3*epw /5)
            tmpVarY = pdf.get_y()
            self.set_text_color(255 , 255 , 255)
            self.multi_cell(epw /5, self.font_size +5,'Eco-contribution :\nTotal HT :\nTVA :\nTotal TTC :' ,fill=True, align='R',  border=1)
            self.set_text_color(0 , 0 , 0)
            self.set_y(tmpVarY )
            self.cell(4*epw /5)
            self.multi_cell(epw /5, self.font_size +5 ,str(round(frais_financier,2))+'\n'+str(round(totalht,2))+'\n'+str(round((totalttc - totalht),2))+'\n'+str(round((totalttc + frais_financier) ,2)) ,fill=False, align='C',  border=1)
            self.ln( self.font_size +5)
            if self.will_page_break((self.font_size +5) * 4):
                self.ln((self.font_size +5) * 4)
            self.multi_cell(0, self.font_size +5,"Fait à ______________________________________, Le _________________________"'\n'
            '\nSignature et cachet précédés de la mention \n "BON POUR ACCORD" ''\n\n' , align='L',  border=1)
            self.ln( self.font_size +3)
            
        def footer(self):
            self.set_y(-50)
            self.set_font("Roboto", "B" ,size=8)
            line_height = self.font_size + 3
            col_width = epw / 5  # distribute content evenly
            data_header = ("AGENCE PARIS", "AGENCE LYON", "AGENCE MEAUX", "AGENCE AGEN", "AGENCE AVIGNON")
            data = ("100 Avenue de choisy\n94190 Villeneuve St Georges\nTél : 01.43.89.06.00",
                    "6 Rue des Catelines \n69720 St Laurent de Mure\nTél : 04.37.58.44.26",
                    "2 Rue de la Briqueterie \n77470 Poincy\n Tél : 01.60.09.81.31",
                    "89 Rue Joseph Teulère \nZ.A. de Trignac 47240 Castelculier\nTél : 05.53.48.32.94",
                    "135 Avenue Pierre Sémard \n MIN BAT.3 84000 Avignon \nTél : 04.90.87.18.08")
            
            for row in data_header:
                self.multi_cell(col_width, line_height, row, align='C',border=0, ln=3, max_line_height=self.font_size + 3)
            self.ln(line_height)
            self.set_font("Roboto", "I" ,size=8)
            for row in data:
                self.multi_cell(col_width, line_height, row,align='C', border=0, ln=3, max_line_height=pdf.font_size + 3)
            self.set_y(-20)
            self.cell(0, line_height, "ETG LOCATION - 531 994 317 RCS Agen - APE : 7732Z - SARL au capital de 1000€ -N° TVA : FR59531994317",align='C', border=0, ln=3 )
            self.cell(0, line_height, " Web : www.etg-location.fr - Email : etglocationparis@gmail.com - Tél : 0553483294 -Fax : 0970616386",align='C', border=0, ln=3)
            self.set_font("Roboto", "I", 8)
            self.set_y(-10)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, "R")
    
    pdf = PDF('P', 'mm', 'A4')
    epw = pdf.w - 2*pdf.l_margin
    pdf.logo = "logo.png"
    pdf.Title = "Contrat N° : "+str(contrat_data['idcontrat']) if contrat_data['statutcont'] != "Brouillon" else "Devis N° : "+str(contrat_data['idcontrat'])
    filename = ""
    if contrat_data['statutcont'] != "Brouillon":
        filename="contrat_"+str(contrat_data['idcontrat'])+"_"+str(str(contrat_data['client']['raisonsocial']) if contrat_data['client']!=False else "" )+"_"+str(date.today().strftime("%d%m%Y"))
    else:
        filename="devis_"+str(contrat_data['idcontrat'])+"_"+str(str(contrat_data['client']['raisonsocial']) if  contrat_data['client']!=False else "" )+"_"+str(date.today().strftime("%d%m%Y"))

    pdf.dte = str(date_creation.strftime("%d/%m/%Y"))
    pdf.commercial = str(contrat_data['commercial']) if contrat_data['commercial']!= None else ""
    if contrat_data['contacts'] and contrat_data['clientadresses']:
        for c in contrat_data['contacts'] :
            a =  (x for x in contrat_data['clientadresses'] if x['idadresse'] == c['adresse_idadresse'])
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
