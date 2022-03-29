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
            
            self.cell(0, 10, self.Title, 0, 0, "R")
            self.set_font("Roboto","", size=10)
            self.ln()
            self.cell(0, 0, "Date : "+self.dte+"  "+self.contrat, 0, 0, "R")
            self.ln(20)
                
        def utilisation(self):
        
            tmpVarY = self.get_y()
            
            self.set_fill_color(222 , 85 , 90)
            self.set_text_color(255 , 255 , 255)
            
            self.cell(self.epw/3, self.font_size + 5, fill=True, txt="Lieu d'utilisation ", align="C", border=0)
            self.set_text_color(0 , 0 , 0)
            self.ln(self.font_size + 5)
            tmpVarX = self.get_x() + self.epw/3
            if  'chantier' in self.facture_data and self.facture_data["chantier"] != None:
                if self.facture_data["chantier"]['TITRE']:
                    self.cell(0,  self.font_size + 2, self.facture_data["chantier"]['TITRE'], 0, 1)
                self.cell(0,  self.font_size +2 , str(self.facture_data["chantier"]['STREET_NUMBER']) +" "+ str(self.facture_data["chantier"]['ROUTE']) , 0, 1)
                self.cell(0,  self.font_size +2 ,str(self.facture_data["chantier"]['codepostal']) +"    "+str(self.facture_data["chantier"]['ville']), 0, 1)
                self.cell(0,  self.font_size +2 ,"Contact : "+str(self.facture_data["chantier"]['civilite'])+ " " +self.facture_data["chantier"]['prenom']+ " " +self.facture_data["chantier"]['nom'], 0, 1)
                self.cell(0,  self.font_size +2 ,"Tél : "+str(self.facture_data["chantier"]['telmobile']), 0, 1)
            
            self.set_xy(tmpVarX+ self.epw/3,tmpVarY)
            self.set_fill_color(222 , 85 , 90)
            self.set_text_color(255 , 255 , 255)
            self.cell(self.epw/3, self.font_size + 5, fill=True, txt="CLIENT N° : "+str(self.facture_data['leclient']['idclient']) , align="C", border=0)
            self.set_text_color(0 , 0 , 0)
            self.set_xy(tmpVarX+self.epw/3,tmpVarY+ self.font_size + 5)
            if 'contact' in self.facture_data and self.facture_data["contact"] != None:
                if self.facture_data['contact']['TITRE']:
                    self.cell(0,  self.font_size + 2, str(self.facture_data["leclient"]['raisonsocial']), 0, 1)
                    self.set_x(tmpVarX+ self.epw/3)
                    self.cell(0,  self.font_size + 2, self.facture_data['contact']['TITRE'], 0, 1)
                    self.set_x(tmpVarX+ self.epw/3)
                self.cell(0,  self.font_size +2 , str(self.facture_data['contact']['STREET_NUMBER']) +" "+ str(self.facture_data['contact']['ROUTE']) , 0, 1)
                self.set_x(tmpVarX+ self.epw/3)
                self.cell(0,  self.font_size +2 ,str(self.facture_data['contact']['codepostal']) +"    "+str(self.facture_data['contact']['ville']), 0, 1)
                self.set_x(tmpVarX+ self.epw/3)
                self.cell(0,  self.font_size +2 ,"Contact : "+str(self.facture_data['contact']['civilite'])+ " " +str(self.facture_data['contact']['prenom'])+ " " +str(self.facture_data['contact']['nom']), 0, 1)
                self.set_x(tmpVarX+self.epw/3)
                self.cell(0,  self.font_size +2 ,"Tél : "+str(self.facture_data['contact']['telmobile']), 0, 1)
            self.ln(4)
            self.set_draw_color(222 , 85 , 90)
            if(self.boncommande != ""):
                self.multi_cell(0, self.font_size +3,str(self.boncommande), border=1)
                self.ln(0)
            if(self.facture_data['titre'] != ""):
                self.multi_cell(0, self.font_size +3,"Objet : "+str(self.facture_data['titre']), border=1)
            self.ln(4)    
            self.set_font("Roboto", size=8)
            line_height = self.font_size * 2
            col_width = self.epw / 5
            
            TABLE_COL_NAMES = ("Date début de facturation", "Date fin de facturation", "Durée de facturation","Date limite de reglement", "Compte client")
            TABLE_DATA = (str(self.date_debut.strftime("%d/%m/%Y")), str(self.date_fin.strftime("%d/%m/%Y")), str(self.duree.days + 1)+" Jours",self.date_limite, str(self.facture_data['leclient']['compte_comptable']))
            self.set_fill_color(222 , 85 , 90)
            self.set_draw_color(222 , 85 , 90)
            self.set_text_color(255 , 255 , 255)
            for col_name in TABLE_COL_NAMES:
                self.cell(col_width, line_height, col_name, border=1 ,fill=True)
            self.ln(line_height)
            self.set_text_color(0 , 0 , 0)
            self.set_draw_color(222 , 85 , 90)
            for col_name in TABLE_DATA:
                self.cell(col_width, line_height, col_name, border=1 ,fill=False)
            self.ln(line_height)
            self.ln(4)
            
        
        
        def tabledata(self):
              
            def transform(n):
                s = {}
                s['qty'] = int(n['qty']) if n['qty']!=None else 0
                s['tva'] = float(n['tva'])  if n['tva'] !=None else 0
                s['Qte'] = str(s['qty'])
                s['denomination'] = n['description'] if n['description'] !=None else " "
                s['montant_net'] = float(n['puht'])  if n['puht'] !=None else 0
                s['remise'] = float(n['remise'])  if n['remise'] !=None else 0
                try:
                    if int(n['service']) == 0 : 
                        s['montantHT'] = (int(n['qty'])* s['montant_net'] * (self.duree.days +1)) * (1 - float(n['remise'])/100)
                        s['Qte'] = str(s['qty'])+ " x "+ str(self.duree.days +1)+" jours"
                    else :
                        s['montantHT'] = int(n['qty'])* s['montant_net'] * (1 - float(n['remise'])/100)
                    
                except:
                    s['montantHT'] =  0 
                self.totalht = self.totalht+ s['montantHT']
                self.totalttc = self.totalttc+ s['montantHT'] * (1+ s['tva']/100)
                return s
            
            def render_table_header():
                self.set_fill_color(222 , 85 , 90)
                self.set_text_color(255 , 255 , 255)
                self.cell(  (2*self.epw)/12, self.font_size +3, fill=True, txt="Qté", align='C', border=1)
                self.cell(  ( self.epw)/2, self.font_size +3, fill=True, txt="Description",align='C', border=1)
                self.cell(  self.epw/12, self.font_size +3, fill=True, txt="PU BRUT",  align='C', border=1)
                self.cell(  self.epw/12, self.font_size +3, fill=True, txt="TVA",  align='C', border=1)
                self.cell(  self.epw/12, self.font_size +3, fill=True, txt="Remise",  align='C', border=1)
                self.cell(  self.epw/12, self.font_size +3, fill=True, txt="MT HT ",  align='C', border=1) 
                self.set_text_color(0 , 0 , 0)
                self.ln( self.font_size +3)
            render_table_header()
            if len(self.facture_data['lignes'])>=0:
                result = map(transform, self.facture_data['lignes'])
                self.set_font("Roboto","" ,8)
                for r in result:
                    
                    self.cell(  2 * self.epw/12, self.font_size +3, fill=False, txt= str(r['Qte']), align='L', border=1)
                    self.cell(  (self.epw)/2, self.font_size +3, fill=False, txt= (r['denomination'])[:60],align='L', border=1)
                    self.cell(  self.epw/12, self.font_size +3, fill=False, txt= str(round(r['montant_net'],2))+" €",  align='L', border=1)
                    self.cell(  self.epw/12, self.font_size +3, fill=False, txt= str(round(r['tva'],2))+" %",  align='L', border=1)
                    self.cell(  self.epw/12, self.font_size +3, fill=False, txt= str(round(r['remise'],2))+" %",  align='L', border=1)
                    self.cell(  self.epw/12, self.font_size +3, fill=False, txt= str(round(r['montantHT'],2))+" €",  align='L', border=1) 
                    self.ln( self.font_size +3)
                
                
            self.multi_cell(0, self.font_size +3,"""Merci d'adresser tous vos réglements à l'agence de Paris""", border=1)
            self.ln(4)
            self.set_font("Roboto","" ,12)
        
        def total(self):
            self.ln(self.font_size +3)
            
            self.set_font("Roboto","" ,10)
            if self.will_page_break((self.font_size +5) * 8):
                self.ln((self.font_size +5) * 8)
             
            self.cell(3*self.epw /5)
            tmpVarY = self.get_y()
            self.set_text_color(255 , 255 , 255)
            self.multi_cell(self.epw /5, self.font_size +5,'Eco-contribution :\nTotal HT :\nTVA :\nTotal TTC :' ,fill=True, align='R',  border=1)
            self.set_text_color(0 , 0 , 0)
            self.set_y(tmpVarY )
            self.cell(4*self.epw /5)
            self.multi_cell(self.epw /5, self.font_size +5 ,str(round(float(self.facture_data["fraisfinancier"]),2))+" €"+'\n'+str(round(self.totalht,2))+" €"+'\n'+str(round((self.totalttc - self.totalht),2))+" €"+'\n'+str(round((self.totalttc + float(self.facture_data["fraisfinancier"])) ,2))+" €" ,fill=False, align='C',  border=1)
            
        def footer(self):
            self.set_y(-50)
            self.set_font("Roboto", "" ,size=8)
            line_height = self.font_size + 3
            col_width = self.epw / 5  # distribute content evenly
            """
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
                self.multi_cell(col_width, line_height, row,align='C', border=0, ln=3, max_line_height=self.font_size + 3)
            """
            self.set_y(-20)
            self.cell(0, line_height, "ETG LOCATION - 531 994 317 RCS Agen - APE : 7732Z - SARL au capital de 1000€ - N° TVA : FR59531994317",align='C', border=0, ln=3 )
            self.cell(0, line_height, " Web : www.etg-location.fr - Email : etglocationparis@gmail.com - Tél : 0553483294 - Fax : 0970616386",align='C', border=0, ln=3)
            self.set_font("Roboto", "I", 8)
            self.set_y(-10)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, "R")
