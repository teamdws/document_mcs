# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unicodedata
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
    print (API_CONTRAT)
    contrat_data_response= requests.get(API_CONTRAT)
    contrat_data= json.loads(contrat_data_response.content.decode('utf-8'))
    print (contrat_data)
    if contrat_data['client']!=False:
      #client_adresse_response= requests.get("https://applocation.directwebsolutions.fr/web/client?id="+str(contrat_data['client']['idclient']))
      client_adresse_response= requests.get("https://back-mcs-v1.herokuapp.com/web/client?id="+str(contrat_data['client']['idclient']))
      client_adresse= json.loads(client_adresse_response.content.decode('utf-8')) 
    pdf = FPDF()
    pdf.add_page()
    epw = pdf.w - 2*pdf.l_margin
    th = pdf.font_size
    pdf.set_fill_color(220)
    date_creation=date.fromisoformat(contrat_data['datedebcont']) if contrat_data['statutcont'] != "Brouillon" else date.today()
    date_debut=date.fromisoformat(contrat_data['datedebcont'])
    date_fin=date.fromisoformat(contrat_data['datefincont'])
    montantTotalHT=0
    poids_equipement=0
    prix_services=0
    totalTVA=0.0
    adresse_chantier=[]
    adresse_facturation=[]
    contact_facturation=[]
    contact_chantier=[]
    a=('EURO',chr(128));
    frais_financier=contrat_data['fraisfinancier'] if contrat_data['fraisfinancier'] != None else 0
 
    #logo------------------------------------
    pdf.image("./logo.png", 75, 8, 60)
    pdf.set_font('Times','',10.0) 
    pdf.ln(20)
    type_document="Contrat N° : " if contrat_data['statutcont'] != "Brouillon" else "Devis N° : "
    filename="contrat-"+str(contrat_data['idcontrat']) if contrat_data['statutcont'] != "Brouillon" else "devis-"+str(contrat_data['idcontrat'])
    pdf.ln(4*th)
    #header---------------------------------------------
    tmpVarX = pdf.get_x()
    tmpVarY = pdf.get_y()
    pdf.multi_cell(epw/2.3, th,type_document+str(contrat_data['idcontrat'])+" Date : "+str(date_creation.strftime("%d/%m/%y"))+'\n'
    ""+ "Suivi par : "+contrat_data['commercial'],  border=1)
    pdf.ln(1) 
    if contrat_data['contacts'] and client_adresse:
    #parcour les contacts dans un contrat
      for i in range(len(contrat_data['contacts'])): 
                #parcourir les adresses du client  
                for j in range(len(client_adresse['adresses'])):
                  #if client_adresse['adresses'][j]['type']=="chantier":
                  if client_adresse['adresses'][j]['idadresse']==contrat_data['contacts'][i]['adresse_idadresse']:
                    if client_adresse['adresses'][j]['type']=="chantier":
                      adresse_chantier=client_adresse['adresses'][j]
                    else:
                      adresse_facturation=client_adresse['adresses'][j]
                #parcourir les contacts du client  
                for k in range(len(client_adresse['contactes'])):
                  #if client_adresse['adresses'][j]['type']=="chantier":
                  if client_adresse['contactes'][k]['idcontact']==contrat_data['contacts'][i]['idcontact']:
                    if client_adresse['contactes'][k]['typecontact']=="chantier":
                      contact_chantier=client_adresse['contactes'][k]      
                    else:
                      contact_facturation=client_adresse['contactes'][k]

      pdf.cell(epw/2.3, th, fill=True, txt="Lieu d'utilisation :", align="C", border=1)
      pdf.ln(8) 
      pdf.multi_cell(epw/2.3, th, str(adresse_chantier['TITRE'] if adresse_chantier else "" )+'\n'+
      str(adresse_chantier['STREET_NUMBER'] +" "+ adresse_chantier['ROUTE'] if adresse_chantier else "" )+'\n'+
      str(str(adresse_chantier['codepostal']) +"    "+str(adresse_chantier['ville']) if adresse_chantier else "" )+'\n'
      "Contact : "+str(contact_chantier['civilite']+ " " +contact_chantier['prenom']+ " " +contact_chantier['nom'] if contact_chantier else "") +'\n'+
      "Tel : "+str(contact_chantier['telmobile'] if contact_chantier else "" ), border=1)
      pdf.set_xy(tmpVarX+100,tmpVarY)
      pdf.multi_cell(epw/2.3, th,"CLIENT N° : "+str(contrat_data['client']['idclient'])+'\n'+
      str(client_adresse['raisonsocial'])+'\n'+
      str(adresse_facturation['STREET_NUMBER']+ " " +adresse_facturation['ROUTE'] if adresse_facturation else "" )+'\n'+
      str(str(adresse_facturation['codepostal'])+ " " +adresse_facturation['ville'] if adresse_facturation else "" )+'\n\n'+
      "Demandé par : "+str(contact_facturation['civilite']+ " " +contact_facturation['prenom']+ " " +contact_facturation['nom'] if adresse_facturation else "" )+'\n'+
      "Tel : "+str(contact_facturation['telmobile'] if adresse_facturation else "") +'\n'+
      "Fax : " ,border=1)
      pdf.ln(7)
    else:    
      pdf.cell(epw/2.3, th, fill=True, txt="Lieu d'utilisation :", align="C", border=1)
      pdf.ln(8)     
      pdf.multi_cell(epw/2.3, th, '\n'+'\n'+'\n'+
      "Contact : "+""+ " " +""+ " " +""+'\n'+
      "Tel : "+"", border=1)
      pdf.set_xy(tmpVarX+100,tmpVarY)
      pdf.multi_cell(epw/2.3, th,"CLIENT N° : "+str(contrat_data['client']['idclient'] if contrat_data['client']!=False else "")+'\n'+
      ""+'\n'+
      ""+ " " +""+'\n'+
      ""+ " " +""+'\n\n'+
      "Demandé par : "+""+ " " +""+ " " +""+'\n'+
      "Tel : "+""+'\n'+
      "Fax : " ,border=1)
    pdf.ln(7)
    tmpVarX = pdf.get_x()
    tmpVarY = pdf.get_y()
    pdf.multi_cell(epw/2.3, th, "Date debut contrat : "+str(date_debut.strftime("%d/%m/%y"))+'\n'+
    "Date fin contrat : "+str(date_fin.strftime("%d/%m/%y"))+'\n'+
    "Période de location : "+str(contrat_data['nbdays'])+" Jours"+'\n'+
    "Type Facturation  : "+str(contrat_data['frequencefacturation'])+"  mois"
    ,border=1)
    pdf.set_xy(tmpVarX+100,tmpVarY)
    pdf.multi_cell(epw/2.3, th,"Nos tarifs sont dégressifs, la valeur des prix varie\n"
    "en fonction de location. Toute reprise anticipée\n"
    "avant la date prévue par le contrat de location\n"
    "entrainera une revalorisation des prix à la hausse. ", border=1)
    pdf.ln(10)
    #line of invoice--------------------------
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
    #for i in range(len(contrat_data['services'])):
            #prix_services=prix_services+contrat_data['services'][i]['prix']
    for i in range(len(contrat_data['equipements'])):
          
        montant_net=float(contrat_data['equipements'][i]['prix'])
        montantTTC=(int(contrat_data['equipements'][i]['Qte'])*int(contrat_data['nbdays']))*float(contrat_data['equipements'][i]['prix'])-float(contrat_data['equipements'][i]['remise'])
        pdf.set_font('Arial','B',10) 
        if contrat_data['statutcont'] != "Brouillon":
          pdf.cell(epw/30, 2*th, txt=str(contrat_data['equipements'][i]['Qte']),align='C', border=1)
          pdf.cell(epw/7, 2*th, txt=str(contrat_data['equipements'][i]['reference']),align='C', border=1)
          pdf.set_font('Arial',size=8) 
          pdf.cell(113, 2*th, txt=str(contrat_data['equipements'][i]['denomination']),align='A', border=1 )
          pdf.set_font('Arial','B',10) 
          pdf.cell(  epw/10, 2*th, txt=str(montant_net)+" "+chr(128), align='C', border=1)
          pdf.cell(  epw/11, 2*th, txt=str(montantTTC)+" "+chr(128), align='C', border=1)
        else :
          pdf.cell(epw/15, 2*th, txt=str(contrat_data['equipements'][i]['Qte']),align='C', border=1)
          pdf.set_font('Arial',size=8) 
          pdf.cell(120, 2*th, txt=str(contrat_data['equipements'][i]['denomination']),align='A', border=1 )
          pdf.set_font('Arial','B',10) 
          pdf.cell(  epw/8, 2*th, txt=str(montant_net)+" "+chr(128), align='C', border=1)
          pdf.cell(  epw/8, 2*th, txt=str(montantTTC)+" "+chr(128), align='C', border=1)
        totalTVA=float(totalTVA+(montantTTC*(float(contrat_data['equipements'][i]['tva'])/100)))
        montantTotalHT=montantTotalHT+montantTTC
        if contrat_data['equipements'][i]['poids']:
          poids_equipement=poids_equipement+float(contrat_data['equipements'][i]['poids'])          
        pdf.ln(2*th) 
    #footer----------------------------------------------------------------
    pdf.set_y(185)
    pdf.set_font('Arial',size=8) 
    pdf.cell(100, 2*th, "Un transport à vide sera facturé en cas de passage inutile dû aux éventuelles prolongations.")
    pdf.ln(3) 
    pdf.cell(100, 2*th,"Merci de prévenir à l'avance afin d'éviter ce coût supplémentaire.")
    pdf.ln(3) 
    pdf.cell(100, 2*th,"Une indemnité forfaitaire de 40.00 euros est due au créancier en cas de retard de paiement.")
    pdf.ln(3) 
    pdf.cell(100, 2*th,"Le locataire déclare avoir pris connaissance des conditions générales de location et de")
    pdf.ln(3) 
    pdf.cell(100, 2*th,"les accepter sans réserves (LE CLIENT DECLARE AVOIR PRIS CONNAISSANCE DES CONDITIONS).")
    pdf.ln(3) 
    pdf.cell(100, 2*th,"Nous vous rappelons que les réservations sont seulement valables après acceptation de ce contrat.")
    pdf.cell(60) 
    pdf.cell(10, 2*th,"Poids (Kg) :       "+str(poids_equipement))
    pdf.ln(2*th)
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
    texte="Total TTC  "
    pdf.cell(30, 2*th,fill=True, txt=texte, align="C",border=1)
    pdf.cell(30, 2*th, str(montantTotalHT+float(frais_financier))+" "+chr(128) ,border=1)
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
    pdf.cell(epw/5, 2*th,  txt="Tel : 01.43.89.06.00", align='C')
    pdf.cell(epw/5, 2*th,  txt="Tel : 04.37.58.44.26", align='C')
    pdf.cell(epw/5, 2*th,  txt="Tel : 01.60.09.81.31", align='C')
    pdf.cell(epw/5, 2*th,  txt="Tel : 05.53.48.32.94", align='C')
    pdf.cell(epw/5, 2*th,  txt="Tel : 04.90.87.18.08", align='C')
    pdf.ln(th*2)
    pdf.set_font('Arial','I',10)  
    pdf.multi_cell(190, 5, txt="SARL AU CAPITAL DE 301200 Fax : 01.43.89.64.35 Email : contact@stmp-location.com \nR.C.S B 389 856 261 00026 - APE 46669 INTRA T.V.A FR 25 389 856 261", align = 'C')
    response = make_response(pdf.output(dest='S'))
    response.headers.set('Content-Type', 'application/pdf', filename=filename + '.pdf')
    return response

if __name__ == '__main__': 
	contrat.run(debug = True)