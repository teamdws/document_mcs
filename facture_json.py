from flask import Blueprint, make_response, request
import  requests
import  json
from fpdf import FPDF
from datetime import *

facture=Blueprint("facture", __name__)

@facture.route('pdf',methods = ['POST', 'GET'])
def facture_pdf():
    #------------------------------------set endpoint
    id_facture= request.args.get('facture')
    #URL_FACTURE = "https://back-mcs-v1.herokuapp.com/web/facture?id="+str(id_contrat)
    URL_FACTURE = "https://back-mcs-v1.herokuapp.com/web/facture?id="+str(id_facture)
    facture_data_response= requests.get(URL_FACTURE)
    facture_data= json.loads(facture_data_response.content.decode('utf-8'))
    ligne_facture_response=requests.get("https://back-mcs-v1.herokuapp.com/web/lignefactues?query=%7B%22facture_idfacture%22:"+str(id_facture)+"}&ascending=1&byColumn=1&type=1")
    ligne_facture= json.loads(ligne_facture_response.content.decode('utf-8'))
    #API_CONTRAT = "https://applocation.directwebsolutions.fr/web/contrat?id="+str(facture_data['idcontrat'])
    API_CONTRAT = "https://back-mcs-v1.herokuapp.com/web/contrat?id="+str(facture_data['idcontrat'])
    contrat_data_response= requests.get(API_CONTRAT)
    contrat_data= json.loads(contrat_data_response.content.decode('utf-8'))
    if contrat_data['client']!=False:
      #client_adresse_response= requests.get("https://applocation.directwebsolutions.fr/web/client?id="+str(contrat_data['client']['idclient']))
      client_adresse_response= requests.get("https://back-mcs-v1.herokuapp.com/web/client?id="+str(contrat_data['client']['idclient']))
      client_adresse= json.loads(client_adresse_response.content.decode('utf-8')) 
    #---------------client adresses --------------------
    adresse_chantier=[]
    adresse_facturation=[]
    contact_facturation=[]
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
                    if client_adresse['contactes'][k]['type']=="facturation":
                      contact_facturation=client_adresse['contactes'][k]  
    #-----------PDF creation
    pdf = FPDF()
    pdf.add_page()
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/7
    th = pdf.font_size
    date_fin=date.fromisoformat(facture_data['date_fin'])
    date_debut=date.fromisoformat(facture_data['date_debut'])
    duree=date_fin-date_debut
    date_facturation=date.fromisoformat(facture_data['datefact'])
    date_limite=date_fin + timedelta(days=30)
    montantTotalHT=0
    type_document="Facture   " if facture_data['avoir'] == 0 else "Avoir   "
    frais_financier=float(facture_data['fraisfinancier']) if facture_data['fraisfinancier'] != None else 0
    #logo------------------------------------
    pdf.image("./logo.png", 75, 8, 60)
    pdf.set_font('Times','',10.0) 
    pdf.ln(20)
    #header---------------------------------------------
    pdf.set_font('Arial','B',14) 
    pdf.cell(epw, 0.0, type_document+str(contrat_data['idagence'])+"/"+str(ligne_facture['data'][0]['facture_idfacture']), align='')
    pdf.ln(7)
    pdf.set_fill_color(220)
    pdf.ln(1)
    pdf.cell(col_width, 2*th, fill=True, txt="N° Devis", align='C', border=1)
    pdf.cell(col_width, 2*th, fill=True, txt="N° Contrat",align='C', border=1)
    pdf.cell(col_width, 2*th, fill=True,txt= "Ref client",  align='C', border=1)
    pdf.cell(40)
    pdf.set_font('Arial','B',8) 
    pdf.cell(col_width, 2*th, txt=str(contrat_data['raisonsocial']), align = 'A')
    pdf.ln(2*th) 
    pdf.cell(col_width, 2*th, align='C', border=1)
    pdf.cell(col_width, 2*th, txt=str(contrat_data['idcontrat']),align='C', border=1)
    pdf.cell(col_width, 2*th, txt=str(contrat_data['client_idclient']), align='C', border=1)
    pdf.cell(40)
    pdf.set_font('Arial','B',8) 
    pdf.cell(col_width, 2*th, txt=adresse_facturation['STREET_NUMBER']+ " " +adresse_facturation['ROUTE'], align = 'A')
    pdf.ln(7)
    pdf.cell(col_width, 2*th, fill=True, txt="Date",  align='C', border=1)
    pdf.cell(col_width, 2*th, fill=True, txt="N° Client",  align='C', border=1)
    pdf.cell(col_width, 2*th, fill=True, txt="Cpte client",  align='C', border=1)
    pdf.cell(40)
    pdf.set_font('Arial','B',8) 
    pdf.cell(col_width, 2*th, txt=str(adresse_facturation['codepostal'])+ " " +adresse_facturation  ['ville'], align = 'A')
    pdf.ln(2*th)
    pdf.cell(col_width, 2*th, str(date_facturation.strftime("%d/%m/%Y")),align='C', border=1)
    pdf.cell(col_width, 2*th, txt=str(contrat_data['client_idclient']),align='C', border=1)
    pdf.cell(col_width, 2*th, txt=str(contrat_data['compte_comptable']),align='C', border=1)    
    pdf.cell(40)
    pdf.set_font('Arial','B',8) 
    pdf.cell(col_width, 2*th, txt="Contact :"+str(contact_facturation['civilite'])+ " " +contact_facturation['prenom']+ " " +contact_facturation['nom'], align = 'A')
    pdf.ln(3)
    pdf.cell(121.5)
    pdf.set_font('Arial','B',8) 
    pdf.cell(col_width, 2*th, txt="Tel :"+str(contact_facturation['telmobile']), align = 'A')
    pdf.ln(20)
    pdf.set_font('Arial','B',10) 
    pdf.cell(epw/4, 2*th, fill=True, txt="Lieu utilisation" , align='C', border=1)
    pdf.cell(epw/4, 2*th, fill=True, txt="Date début de facturation",align='C', border=1)
    pdf.cell(epw/4, 2*th, fill=True, txt="Date fin de facturation",  align='C', border=1)
    pdf.cell(epw/4, 2*th, fill=True, txt="Durée de facturation",  align='C', border=1)
    pdf.ln(2*th) 
    pdf.set_font('Arial','B',6) 
    pdf.cell(epw/4, 2*th, str(str(adresse_chantier['TITRE']) if len(adresse_chantier)>0 else ""), align='C', border=1)
    pdf.set_font('Arial','B',10) 
    pdf.cell(epw/4, 2*th, str(date_debut.strftime("%d/%m/%Y")), align='C', border=1)
    pdf.cell(epw/4, 2*th, str(date_fin.strftime("%d/%m/%Y")), align='C', border=1)
    pdf.cell(epw/4, 2*th, str(duree.days+1)+" Jours", align='C', border=1)
    pdf.ln(10)
    #line of invoice--------------------------
    pdf.cell(  epw/15, 2*th, fill=True, txt="Qté", align='C', border=1)
    pdf.cell(  113, 2*th, fill=True, txt="Description",align='C', border=1)
    pdf.cell(  epw/10, 2*th, fill=True, txt="PU BRUT",  align='C', border=1)
    pdf.cell(  epw/20, 2*th, fill=True, txt="R"+ " "+facture_data['type_remise'],  align='C', border=1)
    pdf.cell(  epw/10, 2*th, fill=True, txt="PU NET ",  align='C', border=1)
    pdf.cell(  epw/11, 2*th, fill=True, txt="MT HT ",  align='C', border=1)
    pdf.ln(2*th)    
    for i in range(len(ligne_facture['data'])):
        if ligne_facture['data'][i]['type_remise']=="e":
          montant_net=float(ligne_facture['data'][i]['puht'])-float(ligne_facture['data'][i]['remise'])
        else: 
          montant_net=float(ligne_facture['data'][i]['puht'])*float(ligne_facture['data'][i]['remise'])/100
       
        montantTTC=(montant_net*(duree.days+1))*(1+(float(ligne_facture['data'][i]['tva'])/100))
        pdf.cell(epw/15, 2*th, txt=str(ligne_facture['data'][i]['qty']),align='C')
        pdf.set_font('Arial',size=8) 
        pdf.cell(113, 2*th, txt=str(ligne_facture['data'][i]['description']),align='A', )
        pdf.set_font('Arial','B',10) 
        pdf.cell(  epw/10, 2*th, txt=str(ligne_facture['data'][i]['puht']), align='C')
        pdf.cell(  epw/20, 2*th, txt=str(ligne_facture['data'][i]['remise']), align='C')
        pdf.cell(  epw/10, 2*th, txt=str(montant_net), align='C')
        pdf.cell(  epw/10, 2*th, txt=str(montantTTC), align='C')
        montantTotalHT=montantTotalHT+montantTTC
        pdf.ln(2*th) 
    pdf.set_y(185)
    pdf.set_font('Arial','B',10) 
    pdf.multi_cell(190, 5, txt="Merci d'adresser tous vos réglements à l'agence de Paris", align = 'C',border=1)
    pdf.ln(1)
    pdf.multi_cell(190, 5, txt="La renonciation à recours s'applique par \n décompte, en jours calendaires, sur le tarif de base du prix de location négocié.Une indemnité forfaitaire de 40.00 Euros est due au créancier en cas de retard de paiement", align='C', border=1)
    pdf.ln(1)
    pdf.cell(50, 2*th, "Eco-contribution "+str(frais_financier),  align='C', border=1)
    pdf.cell(82.5, 2*th,  txt="CONDITIONS DE REGLEMENT",align='C', border=1)
    pdf.cell(epw/6, 2*th,  fill=True,txt="MONTANT HT",  align='C', border=1)
    pdf.cell(26, 2*th,  txt=str( montantTotalHT), align='C', border=1)
    pdf.ln(2*th)
    reglement=facture['reglement'] if facture_data['reglement'] != None else ""
    pdf.cell(epw/4, 2*th, txt="Analyse T.V.A N° T.V.A",align='A', border=1)
    pdf.cell(85, 2*th,  txt=str(reglement), align='C',border=1)
    pdf.cell(epw/6, 2*th, fill=True, txt="TOTAL TVA", align='C', border=1)
    totalTVA= montantTotalHT*20/100
    total_ttc=frais_financier+ montantTotalHT+totalTVA
    pdf.cell(26, 2*th,  txt=str(totalTVA),align='C', border=1)
    pdf.ln(2*th)
    pdf.cell(67.5, 2*th,  txt="CODE  TAUX%  BASE  MONTANT",  align='C', border=1)
    pdf.cell(65, 2*th,   "DATE LIMITE DE REGLEMENT",  align='C', border=1)
    pdf.cell(epw/6, 2*th,  fill=True, txt="MONTANT TTC",align='C', border=1)
    pdf.cell(26, 2*th,  str(total_ttc),  align='C', border=1)
    pdf.ln(2*th)
    pdf.cell(67.5, 2*th,  txt="STD      "+"20.00%" "      "+str(montantTotalHT)+"      "+str(totalTVA),align='C', border=1)   
    pdf.cell(65, 2*th,  str(date_limite.strftime("%d/%m/%Y")),align='C', border=1)
    pdf.cell(epw/4, 2*th, "")
    pdf.cell(epw/4, 2*th, "")
    pdf.ln(10)
    #footer---------------------------
    pdf.set_font('Arial','B',12) 
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
    pdf.set_font('Arial','I',8) 
    pdf.multi_cell(190, 5, txt="SARL AU CAPITAL DE 301200 Fax : 01.43.89.64.35 Email : contact@stmp-location.com \nR.C.S B 389 856 261 00026 - APE 46669 INTRA T.V.A FR 25 389 856 261", align = 'C')
    response = make_response(pdf.output(dest='S'))
    response.headers.set('Content-Type', 'application/pdf')
    return response

if __name__ == '__main__':
	facture.run(debug = True)