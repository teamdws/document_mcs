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
            data_header = {1:"AGENCE PARIS", 8:"AGENCE LYON", 5:"AGENCE MEAUX", 7:"AGENCE AGEN", 4:"AGENCE AVIGNON",6:"Agence LE MANS"}

            self.image( self.logo , 10, 8, 33)
            self.set_font("Roboto","B", size=18)
            self.cell(80)
            
            self.cell(0, 10, self.Title, 0, 0, "R")
            self.set_font("Roboto","", size=10)
            self.ln()
            self.cell(0, 0, "Date  prévue: "+self.dte+" Technicien : "+self.commercial.capitalize(), 0, 0, "R")
            self.ln(5)
            self.cell(0, 0, "Date de création: "+self.dtec, 0, 0, "R")
            self.ln(5)
            
            self.cell(0, 0, "Atelier: "+str(data_header.get(int(self.contrat_data["equipement"]["idagence"]) , 1 )), 0, 0, "R")
            self.ln(5)
            self.cell(0, 0, "Type: "+str(self.contrat_data["type"]).capitalize(), 0, 0, "R")
            
            self.ln(20)
            
        def utilisation(self):
            self.set_font("Roboto","", size=8)
            data_header = {1:"AGENCE PARIS", 8:"AGENCE LYON", 5:"AGENCE MEAUX", 7:"AGENCE AGEN", 4:"AGENCE AVIGNON",6:"Agence LE MANS"}
            data = {1:"100 Avenue de choisy\n94190 Villeneuve St Georges\nTél : 01.43.89.06.00",
                    8:"6 Rue des Catelines \n69720 St Laurent de Mure\nTél : 04.37.58.44.26",
                    5:"2 Rue de la Briqueterie \n77470 Poincy\n Tél : 01.60.09.81.31",
                    7:"89 Rue Joseph Teulère \nZ.A. de Trignac 47240 Castelculier\nTél : 05.53.48.32.94",
                    4:"135 Avenue Pierre Sémard \n MIN BAT.3 84000 Avignon \nTél : 04.90.87.18.08",
                    6:""}
            self.code39( "*"+str(self.contrat_data['idintervention'])+"*", x= self.l_margin  , y=25, w=2, h=10)

            tmpVarY = self.get_y()
            
            self.set_fill_color(222 , 85 , 90)
            self.set_text_color(255 , 255 , 255)
            if hasattr( self, 'chantier') and self.chantier['adresse']:
                self.cell(self.epw/3, self.font_size + 5, fill=True, txt="Lieu d'utilisation ", align="C", border=0)
            self.set_text_color(0 , 0 , 0)
            self.ln(self.font_size + 5)
            tmpVarX = self.get_x() + self.epw/3
            if hasattr( self, 'chantier') and self.chantier['adresse']:
                if self.chantier['adresse']['TITRE']:
                    self.cell(0,  self.font_size + 2, self.chantier['adresse']['TITRE'], 0, 1)
                self.cell(0,  self.font_size +2 , str(self.chantier['adresse']['STREET_NUMBER']) +" "+ str(self.chantier['adresse']['ROUTE']) , 0, 1)
                self.cell(0,  self.font_size +2 ,str(self.chantier['adresse']['codepostal']) +"    "+str(self.chantier['adresse']['ville']), 0, 1)
                self.cell(0,  self.font_size +2 ,"Contact : "+str(self.chantier['civilite'])+ " " +self.chantier['prenom']+ " " +self.chantier['nom'], 0, 1)
                self.cell(0,  self.font_size +2 ,"Tél : "+str(self.chantier['telmobile']), 0, 1)
            tmpVarYchatier = self.get_y()
            self.set_xy(tmpVarX+ self.epw/3,tmpVarY)
            self.set_fill_color(222 , 85 , 90)
            self.set_text_color(255 , 255 , 255)
            if  'client' in self.contrat_data :
                self.cell(self.epw/3, self.font_size + 5, fill=True, txt="CLIENT N° : "+str(self.contrat_data['client']['idclient']) , align="C", border=0)
            self.set_text_color(0 , 0 , 0)
            self.set_xy(tmpVarX+self.epw/3,tmpVarY+ self.font_size + 5)
            if hasattr( self, 'facturation') and self.facturation['adresse'] and  'client' in self.contrat_data :
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
            tmpVarY = self.get_y() if  self.get_y() > tmpVarYchatier else tmpVarYchatier
            self.set_y(tmpVarY)
            self.ln(7)
            line_height = self.font_size * 2
            
            col_width = self.epw / 4
            
            #TABLE_COL_NAMES = ("Date de début du contrat", "Date de fin du contrat", "Période de location", "Facturation sur")
            #TABLE_DATA = (str(self.date_debut.strftime("%d/%m/%Y")), str(self.date_fin.strftime("%d/%m/%Y")), str(self.contrat_data['nbdays'])+" Jours", str(str(self.contrat_data['frequencefacturation']) if self.contrat_data['frequencefacturation']!=None else "")+"  mois")
            #self.set_fill_color(222 , 85 , 90)
            #self.set_text_color(255 , 255 , 255)
            #for col_name in TABLE_COL_NAMES:
            #    self.cell(col_width, line_height, col_name, border=0 ,fill=True)
            #self.ln(line_height)
            #self.set_text_color(0 , 0 , 0)
            #self.set_draw_color(222 , 85 , 90)
            #for col_name in TABLE_DATA:
            #    self.cell(col_width, line_height, col_name, border=1 ,fill=False)
            #self.ln(line_height)
            
            #self.multi_cell(0, self.font_size +3,"""Nos tarifs sont dégressifs, la valeur des prix varie en fonction de location. Toute reprise anticipée avant la date prévue par le contrat de location entrainera une revalorisation des prix à la hausse. """, border=1)
            self.ln(4)
            
        

        def tabledata(self):
           
           
            self.set_font("Roboto","", size=8)
            self.set_draw_color(222 , 85 , 90)

            
            def render_table_header():
                self.set_fill_color(222 , 85 , 90)
                self.set_text_color(255 , 255 , 255)
                self.cell(  self.epw/6,  self.font_size +3, fill=True, txt="Ref",  align='C', border=1) 
                self.cell(  self.epw/2, self.font_size +3, fill=True, txt="Description",align='C', border=1)
                self.cell(  self.epw/3, self.font_size +3, fill=True, txt="Numéro de serie",  align='C', border=1)
           
                self.set_text_color(0 , 0 , 0)
                self.ln( self.font_size +3)
            def render_moeu_header():
                
                self.cell(  self.epw,  self.font_size +3, fill=False, txt= "Main d'oeuvre:",  align='L', border=0)
                self.ln( self.font_size +3)
                self.set_fill_color(222 , 85 , 90)
                self.set_text_color(255 , 255 , 255)
                self.cell(  self.epw/12,  self.font_size +3, fill=True, txt="Date",  align='L', border=1) 
                self.cell(  self.epw/6, self.font_size +3, fill=True, txt="Technicien",align='L', border=1)
                self.cell(  self.epw/2, self.font_size +3, fill=True, txt="Libellé",  align='L', border=1)
                self.cell(  self.epw/12,  self.font_size +3, fill=True, txt="Tarif",  align='L', border=1) 
                self.cell(  self.epw/12, self.font_size +3, fill=True, txt="Heures",align='L', border=1)
                self.cell(  self.epw/12, self.font_size +3, fill=True, txt="Coût",  align='L', border=1)
                self.set_text_color(0 , 0 , 0)
                self.ln( self.font_size +3)
                self.cell(  self.epw,  self.font_size +20, fill=False, txt="",  align='C', border=1) 
                
                self.ln( self.font_size +20)
            def render_pf_header():
                
                self.cell(  self.epw,  self.font_size +3, fill=False, txt= "Pièces et Fournitures:",  align='L', border=0)
                self.ln( self.font_size +3)
                self.set_fill_color(222 , 85 , 90)
                self.set_text_color(255 , 255 , 255)
                self.cell(  self.epw/5,  self.font_size +3, fill=True, txt="Référence",  align='L', border=1) 
                self.cell(  self.epw/2, self.font_size +3, fill=True, txt="Description",align='L', border=1)
                self.cell(  self.epw/10, self.font_size +3, fill=True, txt="Qté",  align='L', border=1)
                self.cell(  self.epw/10,  self.font_size +3, fill=True, txt="Prix U HT ",  align='L', border=1) 
                self.cell(  self.epw/10, self.font_size +3, fill=True, txt="Prix Total",align='L', border=1)
                self.set_text_color(0 , 0 , 0)
                self.ln( self.font_size +3)
                self.cell(  self.epw,  self.font_size +20, fill=False, txt="",  align='C', border="TLR") 
                self.ln( self.font_size +20)
                self.cell(  self.epw,  self.font_size +3, fill=False, txt="____________€",  align='R', border="LR") 
                self.ln( self.font_size +3)
                self.cell(  self.epw,  self.font_size +20, fill=False, txt="Informations complémentaires / Détails",  align='L', border="LRB") 
                
                self.ln( self.font_size +20)
            self.cell(  self.epw,  self.font_size +3, fill=False, txt= "Matériel:",  align='L', border=0) 
            self.ln( self.font_size +3)
            render_table_header()
            
            r = self.contrat_data['equipement']
                    
            self.cell(  self.epw/6,  self.font_size +3, fill=False, txt= str( r['refinterne']),  align='L', border=1) 
            self.cell(  self.epw/2, self.font_size +3, fill=False, txt= (r['complementdenomination'])[:60],align='L', border=1)
            self.cell(  self.epw/3, self.font_size +3, fill=False, txt= str(r['numserie']),  align='L', border=1)
            self.ln( self.font_size +3)
            self.cell(  self.epw,  self.font_size +3, fill=False, txt= "Description des travaux:",  align='L', border=0)
            self.ln( self.font_size +3)
            self.cell(  self.epw,  self.font_size +3, fill=False, txt=  str(self.contrat_data['taches']),  align='L', border=1)
            self.ln( self.font_size +3)
            render_moeu_header()
            if self.will_page_break(self.font_size +52):
                self.ln(self.font_size +52)
            render_pf_header()
            self.ln( self.font_size +3)

                
        def total(self):
           
            
            
             
            
            
            if self.will_page_break(self.font_size +5):
                self.ln(self.font_size +5)
            self.multi_cell(self.epw, self.font_size +5,"\n\nSignature Client: ______________________________________"'\n'
            '\nSignature Technicien: ______________________________________ ''\n\n' , align='L',  border=1)
            self.ln( self.font_size +5)
            
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
            #self.cell(0, line_height, "ETG LOCATION - 531 994 317 RCS Agen - APE : 7732Z - SARL au capital de 1000€ - N° TVA : FR59531994317",align='C', border=0, ln=3 )
            #self.cell(0, line_height, " Web : www.etg-location.fr - Email : contact@etg-location.fr - Tél : 0553483294 - Fax : 0970616386",align='C', border=0, ln=3)
            #self.cell(0, line_height, "ETG Location - siège social situé à 100 avenue de Choisy 94 190 Villenueve-Saint-Georges",align='C', border=0, ln=3 )
            #self.cell(0, line_height, "Société au capital de 1000€ Immatriculée au registre du commerce et de sociétés sous le numéro  531 994 317 00026 RCS Créteil  code APE 7732Z",align='C', border=0, ln=3)

            self.set_font("Roboto", "I", 8)
            self.set_y(-10)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, "R")
