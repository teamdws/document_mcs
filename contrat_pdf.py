# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, make_response, request
import  requests
import  json
from fpdf import FPDF
from datetime import *

contrat=Blueprint("contrat", __name__)
@contrat.route('/pdf',methods = ['POST', 'GET'])
def contrat_pdf():
    id_contrat= request.args.get('contrat')
    #API_CONTRAT = "https://applocation.directwebsolutions.fr/web/contrat?id="+str(id_contrat)
    API_CONTRAT = "https://back-mcs-v1.herokuapp.com/web/contrat?id="+str(id_contrat)
    contrat_data_response= requests.get(API_CONTRAT)
    contrat_data= json.loads(contrat_data_response.content.decode('utf-8'))
    if contrat_data['client']!=False:
      #client_adresse_response= requests.get("https://applocation.directwebsolutions.fr/web/client?id="+str(contrat_data['client']['idclient']))
      client_adresse_response= requests.get("https://back-mcs-v1.herokuapp.com/web/client?id="+str(contrat_data['client']['idclient']))
      client_adresse= json.loads(client_adresse_response.content.decode('utf-8')) 
    pdf = FPDF('P', 'mm', 'A4' )
    pdf.add_page()
    epw = pdf.w - 2*pdf.l_margin
    th = pdf.font_size
    pdf.set_fill_color(220)
    date_creation=date.fromisoformat(contrat_data['datedebcont']) if contrat_data['statutcont'] != "Brouillon" else date.today()
    date_debut=date.fromisoformat(contrat_data['datedebcont']) if contrat_data['datedebcont'] != None else date.today()
    date_fin=date.fromisoformat(contrat_data['datefincont']) if contrat_data['datefincont'] != None else date.today()
    montantTotalHT=0.0
    poids_equipement=0
    totalTVA=0.0
    adresse_chantier=[]
    adresse_facturation=[]
    contact_facturation=[]
    contact_chantier=[]
    frais_financier=contrat_data['fraisfinancier'] if contrat_data['fraisfinancier'] != None else 0
 
    #logo------------------------------------
    pdf.image("./logo.png", 75, 8, 60)
    pdf.set_font('Times','',10.0) 
    pdf.ln(20)
    type_document="Contrat N° : " if contrat_data['statutcont'] != "Brouillon" else "Devis N° : "
    if contrat_data['statutcont'] != "Brouillon":
      filename="contrat_"+str(contrat_data['idcontrat'])+"_"+str(str(client_adresse['raisonsocial']) if contrat_data['client']!=False else "" )+"_"+str(date.today().strftime("%d/%m/%Y"))
    else:
           filename="devis_"+str(contrat_data['idcontrat'])+"_"+str(str(client_adresse['raisonsocial']) if  contrat_data['client']!=False else "" )+"_"+str(date.today().strftime("%d/%m/%Y"))
    pdf.ln(4*th)
    #header---------------------------------------------
    tmpVarX = pdf.get_x()
    tmpVarY = pdf.get_y()
    pdf.multi_cell(epw/2.3, th,type_document+str(contrat_data['idcontrat'])+" Date : "+str(date_creation.strftime("%d/%m/%Y"))+'\n'
    ""+ "Suivi par : "+ str(str(contrat_data['commercial']) if contrat_data['commercial']!=None else "" ),  border=1)
    pdf.ln(1) 
    if contrat_data['contacts'] and client_adresse:
    #affichage de contact et adresses-------------------------------------------------
      for i in range(len(contrat_data['contacts'])): 
                #parcourir les adresses du client  
                for j in range(len(client_adresse['adresses'])):
                  if client_adresse['adresses'][j]['idadresse']==contrat_data['contacts'][i]['adresse_idadresse']:
                    if client_adresse['adresses'][j]['type']=="chantier":
                      adresse_chantier=client_adresse['adresses'][j]
                    else:
                      adresse_facturation=client_adresse['adresses'][j]
                #parcourir les contacts du client  
                for k in range(len(client_adresse['contactes'])):
                  if client_adresse['contactes'][k]['idcontact']==contrat_data['contacts'][i]['idcontact']:
                    if client_adresse['contactes'][k]['type']=="chantier":
                      contact_chantier=client_adresse['contactes'][k]      
                    else:
                      contact_facturation=client_adresse['contactes'][k]

      pdf.cell(epw/2.3, th, fill=True, txt="Lieu d'utilisation ", align="C", border=1)
      pdf.ln(8) 
      pdf.multi_cell(epw/2.3, th, str(adresse_chantier['TITRE'] if adresse_chantier else "" )+'\n'+
      str(adresse_chantier['STREET_NUMBER'] +" "+ adresse_chantier['ROUTE'] if adresse_chantier else "" )+'\n'+
      str(str(adresse_chantier['codepostal']) +"    "+str(adresse_chantier['ville']) if adresse_chantier else "" )+'\n'
      "Contact : "+str(contact_chantier['civilite']+ " " +contact_chantier['prenom']+ " " +contact_chantier['nom'] if contact_chantier else "") +'\n'+
      "Tél : "+str(contact_chantier['telmobile'] if contact_chantier else "" ), border=1)
      pdf.set_xy(tmpVarX+100,tmpVarY)
      pdf.multi_cell(epw/2.3, th,"CLIENT N° : "+str(contrat_data['client']['idclient'])+'\n'+
      str(client_adresse['raisonsocial'])+'\n'+
      str(adresse_facturation['STREET_NUMBER']+ " " +adresse_facturation['ROUTE'] if adresse_facturation else "" )+'\n'+
      str(str(adresse_facturation['codepostal'])+ " " +adresse_facturation['ville'] if adresse_facturation else "" )+'\n\n'+
      "Demandé par : "+str(contact_facturation['civilite']+ " " +contact_facturation['prenom']+ " " +contact_facturation['nom'] if contact_facturation else "" )+'\n'+
      "Tél : "+str(contact_facturation['telmobile'] if contact_facturation else "") +'\n'+
      "Fax : " ,border=1)
      pdf.ln(7)
    else:    
      pdf.cell(epw/2.3, th, fill=True, txt="Lieu d'utilisation :", align="C", border=1)
      pdf.ln(8)     
      pdf.multi_cell(epw/2.3, th, '\n'+'\n'+'\n'+
      "Contact : "+""+ " " +""+ " " +""+'\n'+
      "Tél : "+"", border=1)
      pdf.set_xy(tmpVarX+100,tmpVarY)
      pdf.multi_cell(epw/2.3, th,"CLIENT N° : "+str(str(contrat_data['client_idclient']) if contrat_data['client_idclient']!=None else "")+'\n'+
      ""+'\n'+
      ""+ " " +""+'\n'+
      ""+ " " +""+'\n\n'+
      "Demandé par : "+""+ " " +""+ " " +""+'\n'+
      "Tél : "+""+'\n'+
      "Fax : " ,border=1)
    pdf.ln(7)
    tmpVarX = pdf.get_x()
    tmpVarY = pdf.get_y()
    pdf.multi_cell(epw/2.3, th, "Date debut contrat : "+str(date_debut.strftime("%d/%m/%Y"))+'\n'+
    "Date fin contrat : "+str(date_fin.strftime("%d/%m/%Y"))+'\n'+
    "Période de location : "+str(contrat_data['nbdays'])+" Jours"+'\n'+
    "Facturation sur : "+str(str(contrat_data['frequencefacturation']) if contrat_data['frequencefacturation']!=None else "")+"  mois"
    ,border=1)
    pdf.set_xy(tmpVarX+100,tmpVarY)
    pdf.multi_cell(epw/2.3, th,"Nos tarifs sont dégressifs, la valeur des prix varie\n"
    "en fonction de location. Toute reprise anticipée\n"
    "avant la date prévue par le contrat de location\n"
    "entrainera une revalorisation des prix à la hausse. ", border=1)
    pdf.ln(10)
    #affichage line of contrat-------------------------------------------------------
    if contrat_data['statutcont'] != "Brouillon":
      pdf.cell(  epw/30, 2*th, fill=True, txt="Qté", align='C', border=1)
      pdf.cell(  epw/7, 2*th, fill=True, txt="Ref.",  align='C', border=1) 
      pdf.cell(  113, 2*th, fill=True, txt="Description",align='C', border=1)
      pdf.cell(  epw/10, 2*th, fill=True, txt="PU BRUT",  align='C', border=1)
      pdf.cell(  epw/11, 2*th, fill=True, txt="MT HT ",  align='C', border=1) 
    else:
      pdf.cell(  epw/15, 2*th, fill=True, txt="Qté", align='C', border=1)
      pdf.cell(  120, 2*th, fill=True, txt="Description",align='C', border=1)
      pdf.cell(  epw/8, 2*th, fill=True, txt="PU BRUT",  align='C', border=1)
      pdf.cell(  epw/8, 2*th, fill=True, txt="MT HT ",  align='C', border=1) 
    pdf.ln(2*th)  
    #affichage des équipements si le tableau n'est pas vide------------------------------------
    if len(contrat_data['equipements'])>=0:
        for i in range(len(contrat_data['equipements'])):      
            montant_net=float(contrat_data['equipements'][i]['prix'])
            montantTTC=(int(contrat_data['equipements'][i]['Qte'])*int(contrat_data['nbdays']))*float(contrat_data['equipements'][i]['prix'])-float(contrat_data['equipements'][i]['remise'])
            pdf.set_font('Arial','B',10) 
            pdf.cell(epw/30, 2*th, txt=str(contrat_data['equipements'][i]['Qte']),align='C', border=1)
           
            if contrat_data['statutcont'] != "Brouillon":  #affichage de la colone ref s'il sagit d'un contrat
              if contrat_data['equipements'][i]['reference']!=None:  #vérifier su la colone référence est renseignée oun pas
                #parcourir le detail des équipements pour trouver la référence interne de chaque article 
                if  contrat_data['equipements'][i]['serialisable']==1: #and contrat_data['equipements'][i]['statut_preparation']=1:
                    for k in range(len(contrat_data['detailequipements'])): 
                      if contrat_data['equipements'][i]['idcategorie']==contrat_data['detailequipements'][k]['categorie_idcategorie']:
                          pdf.cell(epw/7, 2*th, txt=str(contrat_data['detailequipements'][k]['refinterne']),align='C', border=1)
                          break
                      
                #elif contrat_data['equipements'][i]['serialisable']==1 and contrat_data['equipements'][i]['statut_preparation']!=1:
                    #pdf.cell(epw/7, 2*th, txt=str(contrat_data['detailequipements'][k]['refinterne']),align='C', border=1) 
                elif  contrat_data['equipements'][i]['serialisable']==0: pdf.cell(epw/7, 2*th,align='C', border=1)
              else:         
                pdf.cell(epw/7, 2*th, txt=str(contrat_data['equipements'][i]['reference']),align='C', border=1)
           
              pdf.set_font('Arial',"B",size=6) 
              tmpVarX = pdf.get_x()
              tmpVarY = pdf.get_y()              
              pdf.multi_cell(113,  3, txt=str(contrat_data['equipements'][i]['denomination']),align='A' )
              pdf.set_xy(tmpVarX+113,tmpVarY)
              pdf.set_font('Arial','B',10) 
              pdf.cell(epw/10, 2*th, txt=str(round(montant_net,2))+" "+chr(128), align='C', border=1)
              pdf.cell(  epw/11, 2*th, txt=str(round(montantTTC,2))+" "+chr(128), align='C', border=1)
            else :
              pdf.set_font('Arial',size=8) 
              pdf.multi_cell(120, 2*th, txt=str(contrat_data['equipements'][i]['denomination']),align='A', border=1 )
              pdf.set_font('Arial','B',10) 
              pdf.cell(  epw/8, 2*th, txt=str(round(montant_net,2))+" "+chr(128), align='C', border=1)
              pdf.cell(  epw/8, 2*th, txt=str(round(montantTTC,2))+" "+chr(128), align='C', border=1)
            totalTVA=float(totalTVA+(montantTTC*(float(contrat_data['equipements'][i]['tva'])/100)))
            montantTotalHT=montantTotalHT+montantTTC
            if contrat_data['equipements'][i]['poids']:
              poids_equipement=poids_equipement+float(contrat_data['equipements'][i]['poids'])          
            pdf.ln(2*th) 
    #affichage des services -------------------------------------------------
    if len(contrat_data['services'])>=0:
     for i in range(len(contrat_data['services'])):
            montant_net_service=float(contrat_data['services'][i]['prixdefautservice'])
            montantTTC_service=float(contrat_data['services'][i]['prix'])
            pdf.set_font('Arial','B',10) 
            pdf.cell(epw/30, 2*th, txt=str(contrat_data['services'][i]['Qte']),align='C', border=1)
            pdf.cell(epw/7, 2*th, "",align='C', border=1)
            pdf.set_font('Arial',size=8) 
            pdf.cell(113, 2*th, txt=str(contrat_data['services'][i]['description']),align='A', border=1 )
            pdf.set_font('Arial','B',10) 
            pdf.cell(  epw/10, 2*th, txt=str(montant_net_service)+" "+chr(128), align='C', border=1)
            pdf.cell(  epw/11, 2*th, txt=str(montantTTC_service)+" "+chr(128), align='C', border=1)
            
            montantTotalHT=montantTotalHT+montantTTC_service         
            pdf.ln(2*th) 
    #affichage mentions-----------------------------------------------------
    pdf.ln(5)
    pdf.set_font('Arial',size=8) 
    if len(contrat_data['mentions'])>=0:
         for i in range(len(contrat_data['mentions'])):
            pdf.multi_cell(190, th, str(contrat_data['mentions'][i]['contenuoption']).replace("€", chr(128)))
            pdf.ln(1) 
    pdf.multi_cell(100, 2*th)
    pdf.cell(60) 
    pdf.cell(10, 2*th,"Poids (Kg) :       "+str(poids_equipement))
    pdf.ln(2*th)
    #affichage du footer---------------------------------------
    tmpVarX = pdf.get_x()
    tmpVarY = pdf.get_y()
    pdf.multi_cell(120, 4*th,"Fait à ______________________________________, Le _________________________"'\n'
    'Signature et cachet précédés de la mention "BON POUR ACCORD" ', align='C',  border=1)
    #Replace le positionnement du curseur coin supérieur droit de la cellule créée
    pdf.set_xy(tmpVarX+130,tmpVarY)
    pdf.cell(50, 2*th,"Eco-contribution    "+str(frais_financier)+"  Euro(s)")
    pdf.cell(10, 2*th," ")
    pdf.ln(2*th) 
    pdf.cell(tmpVarX+120)
    pdf.cell(30, 2*th,fill=True, txt="Total HT :" , align="C",border=1)
    pdf.cell(30, 2*th, str(montantTotalHT)+" "+chr(128) ,border=1)
    pdf.ln(2*th) 
    pdf.cell(tmpVarX+120)
    pdf.cell(30, 2*th, fill=True, txt="TVA :" , align="C",border=1)
    pdf.cell(30, 2*th,str(totalTVA)+" "+chr(128),border=1)
    pdf.ln(2*th) 
    pdf.cell(tmpVarX+120)
    pdf.cell(30, 2*th,fill=True, txt="Total TTC :", align="C",border=1)
    pdf.cell(30, 2*th, str(montantTotalHT+float(frais_financier)+totalTVA)+" "+chr(128) ,border=1)
    pdf.ln(10)
    #mentions----------------------------------
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
    #pdf.line(10, 30, 110, 30)
    pdf.multi_cell(190, 3, txt="ETG LOCATION - 531 994 317 RCS Agen - APE : 7732Z - SARL au capital de 1000"+chr(128)+" -N° TVA : FR59531994317\n Web : www.etg-location.fr - Email : etglocationparis@gmail.com - Tél : 0553483294 -Fax : 0970616386", align = 'C')
    response = make_response(pdf.output(dest='S'))
    #response.headers.set('Content-Disposition', 'attachment', filename=filename + '.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response

if __name__ == '__main__': 
	contrat.run(debug = True)