from flask import Blueprint, make_response, request
import  requests
import  json
from fpdf import FPDF
from datetime import *

contrat=Blueprint("contrat", __name__)

@contrat.route('/pdf',methods = ['POST', 'GET'])
def contrat_pdf():
    id_contrat= request.args.get('contrat')
    API_CONTRAT = "https://back-mcs-v1.herokuapp.com/web/contrat?id="+str(id_contrat)
    contrat_data_response= requests.get(API_CONTRAT)
    contrat_data= json.loads(contrat_data_response.content.decode('utf-8'))
    URL_CLIENT="https://back-mcs-v1.herokuapp.com/web/client?id="+str(contrat_data['client']['idclient'])
    facture_adresse_response= requests.get(URL_CLIENT)
    facture_adresse= json.loads(facture_adresse_response.content.decode('utf-8'))
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
    adresse_chantier=""
    adresse_facturation=0
    adresse=0
    frais_financier=contrat_data['fraisfinancier'] if contrat_data['fraisfinancier'] != None else 0
    
    #boucle sur l'adrsse de client
    for i in range(len(facture_adresse['adresses'])):
          if facture_adresse['adresses'][i]['type']=="chantier":
              for j in range(len(contrat_data['contacts'])):
                if facture_adresse['adresses'][i]['idadresse']==contrat_data['contacts'][j]['adresse_idadresse']:
                  adresse_chantier=facture_adresse['adresses'][i]
                  contact_chantier=contrat_data['contacts'][j]        
          else:
           for j in range(len(contrat_data['contacts'])):
                if facture_adresse['adresses'][i]['idadresse']==contrat_data['contacts'][j]['adresse_idadresse']:
                  adresse_facture=facture_adresse['adresses'][i]
                  contact_facture=contrat_data['contacts'][j]
    #logo------------------------------------
    pdf.image("./logo.png", 75, 8, 60)
    pdf.set_font('Times','',10.0) 
    pdf.ln(20)
    type_document="Contrat N° : " if contrat_data['statutcont'] != "Brouillon" else "Devis N° : "
    pdf.ln(4*th)
    #header---------------------------------------------
    tmpVarX = pdf.get_x()
    tmpVarY = pdf.get_y()
    pdf.multi_cell(epw/2.3, th,type_document+str(contrat_data['idcontrat'])+" Date : "+str(date_creation.strftime("%d/%m/%y"))+'\n'
    ""+ "Suivi par : "+contrat_data['commercial'],  border=1)
    pdf.ln(1)
    pdf.cell(epw/2.3, th, fill=True, txt="Lieu d'utilisation :", align="C", border=1)
    pdf.ln(8)
    pdf.multi_cell(epw/2.3, th, str(adresse_chantier['TITRE'])+'\n'+
    str(adresse_chantier['STREET_NUMBER']+" "+adresse_chantier['ROUTE'] )+'\n'+
    str(adresse_chantier['codepostal'])+"    "+adresse_chantier['ville']+'\n'+
    "Contact : "+str(contact_chantier['civilite'])+ " " +str(contact_chantier['prenom'])+ " " +str(contact_chantier['nom'])+'\n'+
    "Tel : "+str(contact_chantier['telmobile']), border=1)
  
    pdf.set_xy(tmpVarX+100,tmpVarY)
    pdf.multi_cell(epw/2.3, th,"CLIENT N° : "+str(contrat_data['client']['idclient'])+'\n'+
    str(facture_adresse['raisonsocial'])+'\n'+
    str(adresse_facture['STREET_NUMBER'])+ " " +str(adresse_facture['ROUTE'])+'\n'+
    str(adresse_facture['codepostal'])+ " " +adresse_facture['ville']+'\n\n'+
    "Demandé par : "+str(contact_facture['civilite'])+ " " +str(contact_facture['prenom'])+ " " +str(contact_facture['nom'])+'\n'+
    "Tel : "+str(contact_facture['telmobile'])+'\n'+
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
    for i in range(len(contrat_data['services'])):
            prix_services=prix_services+contrat_data['services'][i]['prix']
    for i in range(len(contrat_data['equipements'])):
          
        montant_net=float(contrat_data['equipements'][i]['prix'])
        montantTTC=float((contrat_data['equipements'][i]['Qte']*contrat_data['nbdays'])*float(contrat_data['equipements'][i]['prix'])-contrat_data['equipements'][i]['remise']  )
        pdf.set_font('Arial','B',10) 
        if contrat_data['statutcont'] != "Brouillon":
          pdf.cell(epw/30, 2*th, txt=str(contrat_data['equipements'][i]['Qte']),align='C', border=1)
          pdf.cell(epw/7, 2*th, txt=str(contrat_data['equipements'][i]['reference']),align='C', border=1)
          pdf.set_font('Arial',size=8) 
          pdf.cell(113, 2*th, txt=str(contrat_data['equipements'][i]['denomination']),align='A', border=1 )
          pdf.set_font('Arial','B',10) 
          pdf.cell(  epw/10, 2*th, txt=str(round(montant_net,2)), align='C', border=1)
          pdf.cell(  epw/11, 2*th, txt=str(round(montantTTC,2)), align='C', border=1)
        else :
          pdf.cell(epw/15, 2*th, txt=str(contrat_data['equipements'][i]['Qte']),align='C', border=1)
          pdf.set_font('Arial',size=8) 
          pdf.cell(120, 2*th, txt=str(contrat_data['equipements'][i]['denomination']),align='A', border=1 )
          pdf.set_font('Arial','B',10) 
          pdf.cell(  epw/8, 2*th, txt=str(round(montant_net,2)), align='C', border=1)
          pdf.cell(  epw/8, 2*th, txt=str(round(montantTTC,2)), align='C', border=1)
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
    pdf.cell(30, 2*th, str(montantTotalHT) ,border=1)
    pdf.ln(2*th) 
    pdf.cell(tmpVarX+120)
    pdf.cell(30, 2*th, fill=True, txt="TVA :" , align="C",border=1)
    pdf.cell(30, 2*th,str(round(totalTVA,2)),border=1)
    pdf.ln(2*th) 
    pdf.cell(tmpVarX+120)
    pdf.cell(30, 2*th,fill=True, txt="Total TTC :" , align="C",border=1)
    pdf.cell(30, 2*th, str(round(montantTotalHT+float(frais_financier),2)) ,border=1)
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
    response.headers.set('Content-Type', 'application/pdf')
    return response

if __name__ == '__main__': 
	contrat.run(debug = True)