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

class PDF(FPDF, HTMLMixin):
        
        def epw(self):
            self.epw = self.w - 2*self.l_margin

        def header(self):
            # Rendering logo:

            self.image( self.logo , 10, 8, 33)
            self.set_font("Roboto","B", size=18)
            self.cell(80)
            self.cell(0, 10,self.Title, 0, 0, "R")

            self.set_font("Roboto","", size=10)
            self.ln()
            self.cell(0, 10, "Contrat : "+str(self.contrat_data['idcontrat']), 0, 0, "R")
            self.ln()
            self.cell(0, 0, "Date : "+self.livraison_data['date'], 0, 0, "R")
            self.ln(self.font_size +2)
            self.cell(0, 0, "Livreur : "+self.livraison_data['nomlivreur'], 0, 0, "R")
            self.ln(20)
            
        def utilisation(self):
            data_header = {1:"AGENCE PARIS", 8:"AGENCE LYON", 5:"AGENCE MEAUX", 7:"AGENCE AGEN", 4:"AGENCE AVIGNON",6:"Agence LE MANS"}
            data = {1:"100 Avenue de choisy\n94190 Villeneuve St Georges\nTél : 01.43.89.06.00",
                    8:"6 Rue des Catelines \n69720 St Laurent de Mure\nTél : 04.37.58.44.26",
                    5:"2 Rue de la Briqueterie \n77470 Poincy\n Tél : 01.60.09.81.31",
                    7:"89 Rue Joseph Teulère \nZ.A. de Trignac 47240 Castelculier\nTél : 05.53.48.32.94",
                    4:"135 Avenue Pierre Sémard \n MIN BAT.3 84000 Avignon \nTél : 04.90.87.18.08",
                    6:""}
           
            
            self.code39( "*"+str(self.idlivraison)+"*", x= self.l_margin  , y=25, w=2, h=10)

            tmpVarY = self.get_y()
            
            self.set_fill_color(222 , 85 , 90)
            self.set_text_color(255 , 255 , 255)
            self.cell(self.epw/3, self.font_size + 5, fill=True, txt="Agence ", align="C", border=0)
            self.cell(self.epw/3, self.font_size + 5, fill=True, txt="Lieu d'utilisation ", align="C", border=0)
            self.cell(self.epw/3, self.font_size + 5, fill=True, txt="CLIENT N° : "+str(self.contrat_data['client']['idclient']) , align="C", border=0)
            self.set_text_color(0 , 0 , 0)
            self.ln(self.font_size + 5)
            tmpVarX = self.get_x() + self.epw/3
            self.multi_cell(self.epw /3,  self.font_size +2 , str(data_header.get(int(self.livraison_data["idagence"]) , 1 ))+"\n"+str(data.get(int(self.livraison_data["idagence"]) , 1))+"\nDemandé par :"+self.commercial.capitalize()  , 0, 1)
            
            if hasattr( self, 'chantier') and self.chantier['adresse']:
                self.set_xy(tmpVarX ,tmpVarY + self.font_size + 5)
                if self.chantier['adresse']['TITRE']:
                    
                    self.cell(0,  self.font_size + 2, self.chantier['adresse']['TITRE'], 0, 1)
                self.set_x(tmpVarX )
                self.cell(0,  self.font_size +2 , str(self.chantier['adresse']['STREET_NUMBER']) +" "+ str(self.chantier['adresse']['ROUTE']) , 0, 1)
                self.set_x(tmpVarX )
                self.cell(0,  self.font_size +2 ,str(self.chantier['adresse']['codepostal']) +"    "+str(self.chantier['adresse']['ville']), 0, 1)
                self.set_x(tmpVarX )
                self.cell(0,  self.font_size +2 ,"Contact : "+str(self.chantier['civilite'])+ " " +self.chantier['prenom']+ " " +self.chantier['nom'], 0, 1)
                self.set_x(tmpVarX )
                self.cell(0,  self.font_size +2 ,"Tél : "+str(self.chantier['telmobile']), 0, 1)

            self.set_fill_color(222 , 85 , 90)
            self.set_text_color(255 , 255 , 255)
            self.set_text_color(0 , 0 , 0)
            self.set_xy(tmpVarX+self.epw/3,tmpVarY+ self.font_size + 5)
            if hasattr( self, 'facturation') and self.facturation['adresse']:
                if self.facturation['adresse']['TITRE']:
                    self.cell(0,  self.font_size + 2, str(self.contrat_data['client']['raisonsocial']), 0, 1)
                    self.set_x(tmpVarX+ self.epw/3)
                    self.cell(0,  self.font_size + 2, self.facturation['adresse']['TITRE'], 0, 1)
                    self.set_x(tmpVarX+ self.epw/3)
                self.cell(0,  self.font_size +2 , str(self.facturation['adresse']['STREET_NUMBER']) +" "+ str(self.facturation['adresse']['ROUTE']) , 0, 1)
                self.set_x(tmpVarX+ self.epw/3)
                self.cell(0,  self.font_size +2 ,str(self.facturation['adresse']['codepostal']) +"    "+str(self.facturation['adresse']['ville']), 0, 1)
                self.set_x(tmpVarX+ self.epw/3)
                self.cell(0,  self.font_size +2 ,"Contact : "+str(self.facturation['civilite'])+ " " +self.facturation['prenom']+ " " +self.facturation['nom'], 0, 1)
                self.set_x(tmpVarX+self.epw/3)
                self.cell(0,  self.font_size +2 ,"Tél : "+str(self.facturation['telmobile']), 0, 1)
            self.ln(7)
            line_height = self.font_size * 2
            col_width = self.epw / 4
            TABLE_COL_NAMES = ("Date de début du contrat", "Date de "+str(self.livraison_data['type'].upper()), "Compte Client", "Bon de Commande")
            TABLE_DATA = (str(self.date_debut.strftime("%d/%m/%Y")), str(self.livraison_data['date']), str(self.contrat_data['client']['compte_comptable']), str(self.contrat_data['boncommande']))
            self.set_y(tmpVarY+ 9 * (self.font_size + 2))
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
            
            self.ln(4)
        

        def tabledata(self):
            
                
            
            
            def render_table_header():
                self.set_fill_color(222 , 85 , 90)
                self.set_text_color(255 , 255 , 255)
                self.cell(  self.epw/16, self.font_size +3, fill=True, txt="Qté", align='C', border=1)
                self.cell(  7 * self.epw/16,  self.font_size +3, fill=True, txt="Description",  align='C', border=1) 
                self.cell(  ( self.epw)/8, self.font_size +3, fill=True, txt="Rèf",align='C', border=1)
                self.cell( 6 * self.epw/16, self.font_size +3, fill=True, txt="Observation",  align='C', border=1)
                self.set_text_color(0 , 0 , 0)
                self.ln( self.font_size +3)
            render_table_header()
            if len(self.contrat_data['equipements'])>=0:
                result = self.contrat_data['equipements']
                self.set_font("Roboto","" ,8)
                for r in result:
                    ref = ""
                    n = r
                    if  int(n['serialisable'])==0:
                        ref = str(n['reference']) if n['reference']!=None else "" 
                    elif int(n['serialisable'])==1 and n['equipement_idequipement'] !=None:
                        a =  (x for x in self.contrat_data['detailequipements'] if n['equipement_idequipement']== x['idequipement'])
                        ref = (next(a))['refinterne']
                    
                    s = 'ID'+str(self.livraison_data['type'].upper())
                    if str(r[s]) == str(self.idlivraison) :
                        self.poids = self.poids + int(r.get('Qte' , 0)) * float(r.get('poids', 0))
                        self.cell(  self.epw/16, self.font_size +3, fill=False, txt= str(r['Qte']), align='L', border=1)
                        self.cell(  7 * self.epw/16,  self.font_size +3, fill=False, txt= str( r['denomination'])[:60],  align='L', border=1) 
                        self.cell(  (self.epw)/8, self.font_size +3, fill=False, txt= str(ref),align='L', border=1)
                        self.cell(  6 * self.epw/16, self.font_size +3, fill=False, txt= "" ,  align='L', border=1)
                        self.ln( self.font_size +3)
                
            self.set_font("Roboto","" ,12)
        
        
        def total(self):
            data_header = {1:"AGENCE PARIS", 8:"AGENCE LYON", 5:"AGENCE MEAUX", 7:"AGENCE AGEN", 4:"AGENCE AVIGNON",6:"Agence LE MANS"}

            self.cell(0, self.font_size +3,"poids (Kg): "+str(self.poids) , align="R" ,border=0)
           
            self.ln( self.font_size +5)
            if self.will_page_break((self.font_size +5) * 4):
                self.ln((self.font_size +5) * 4)
            self.set_font("Roboto", "" ,size=8)
            self.multi_cell(0, self.font_size +2,"""Un état des lieux de la machine sera effectué avant son retour dans notre atelier. Toute casse sera notifiée et refacturée.\n"""+str(data_header.get(int(self.livraison_data["idagence"]) , 1 ))+""" : ______________________________________, Enlevé par:  _________________________"""'\n'
            'Signature : ___________________________ \nDate _______________________________ Heure : ________________________ '"""\nEn signant ce document, le client s'engage à respecter les termes et conditions de location qui ont été signées lors du contrat.\n""" , align='L',  border=1)
            self.ln( self.font_size +3)
            
        def footer(self):
            #self.set_y(-50)
            #self.set_font("Roboto", "B" ,size=8)
            line_height = self.font_size + 3
            col_width = self.epw / 5  # distribute content evenly
            data_header = ("AGENCE PARIS", "AGENCE LYON", "AGENCE MEAUX", "AGENCE AGEN", "AGENCE AVIGNON")
            data = ("100 Avenue de choisy\n94190 Villeneuve St Georges\nTél : 01.43.89.06.00",
                    "6 Rue des Catelines \n69720 St Laurent de Mure\nTél : 04.37.58.44.26",
                    "2 Rue de la Briqueterie \n77470 Poincy\n Tél : 01.60.09.81.31",
                    "89 Rue Joseph Teulère \nZ.A. de Trignac 47240 Castelculier\nTél : 05.53.48.32.94",
                    "135 Avenue Pierre Sémard \n MIN BAT.3 84000 Avignon \nTél : 04.90.87.18.08")
            
            #for row in data_header:
            #    self.multi_cell(col_width, line_height, row, align='C',border=0, ln=3, max_line_height=self.font_size + 3)
            self.ln(line_height)
            self.set_font("Roboto", "I" ,size=8)
            #for row in data:
            #    self.multi_cell(col_width, line_height, row,align='C', border=0, ln=3, max_line_height=self.font_size + 3)
            self.set_y(-20)
            self.cell(0, line_height, "ETG LOCATION - 531 994 317 RCS Agen - APE : 7732Z - SARL au capital de 1000€ - N° TVA : FR59531994317",align='C', border=0, ln=3 )
            self.cell(0, line_height, " Web : www.etg-location.fr - Email : contact@etg-location.fr - Tél : 0553483294 - Fax : 0970616386",align='C', border=0, ln=3)
            self.set_font("Roboto", "I", 8)
            self.set_y(-10)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, "R")
