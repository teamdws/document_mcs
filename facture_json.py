from flask import Blueprint, make_response, request
import base64
import  requests
import  json
from fpdf import FPDF
from datetime import *
from facturepdfclass import PDF
from myencryptor import AESCipher

facture=Blueprint("facture", __name__)


@facture.route('pdf',methods = ['POST', 'GET'])
def facture_pdf():

   
    pdf = PDF('P', 'mm', 'A4')
    cipher = AESCipher('12lrtkjhy', 'muni1yyyft23')
    facturedt = cipher.decrypt(base64.b64decode(request.form.get('facture'))).decode("utf-8")
    pdf.facture_data= json.loads(facturedt)


    pdf.logo = "logo.png"
    type_document="Facture" if str(pdf.facture_data['avoir']) == "0" else "Avoir"
    filename = type_document+"_"+ str(pdf.facture_data['idfacture'])+"_"+str(pdf.facture_data['leclient']['raisonsocial'])+"_"+str(date.today().strftime("%d/%m/%Y"));
    frais_financier= pdf.facture_data['fraisfinancier'] if pdf.facture_data['fraisfinancier'] != None else 0
    pdf.date_limite= str(date.fromisoformat(pdf.facture_data['date_limite']).strftime("%d/%m/%Y")) if pdf.facture_data['date_limite'] != None else ""
    pdf.date_creation=date.fromisoformat(pdf.facture_data['datefact']) 
    pdf.date_debut=date.fromisoformat(pdf.facture_data['date_debut']) if pdf.facture_data['date_debut'] != None else date.today()
    pdf.date_fin=date.fromisoformat(pdf.facture_data['date_fin']) if pdf.facture_data['date_fin'] != None else date.today()
    pdf.duree=pdf.date_fin - pdf.date_debut 
    pdf.dte = str(pdf.date_creation.strftime("%d/%m/%Y"))
    pdf.contrat = ""
    pdf.boncommande = ""
    try:
       if 'contrat' in pdf.facture_data :
        num =  pdf.facture_data['contrat']['idagence'] 
        pdf.contrat = "N° Contrat : "+str(pdf.facture_data['contrat']['idcontrat'] )
        pdf.boncommande =  "Bon de commande : "+str(pdf.facture_data['contrat']['boncommande'] )  if pdf.facture_data['contrat']['boncommande'] != None else ""
        
       else : num = 0
    except AttributeError: num = 0
    
    pdf.Title = type_document+" N° : "+str(num)+"/"+str(pdf.facture_data['idfacture']) 
    pdf.totalht = 0   
    pdf.totalttc = 0 
    pdf.epw()
    epw = pdf.w - 2*pdf.l_margin
    pdf.add_font('Roboto', '', 'Roboto-Regular.ttf', uni=True)
    pdf.add_font('Roboto', 'B', 'Roboto-Bold.ttf', uni=True)
    pdf.add_font('Roboto', 'I', 'Roboto-Italic.ttf', uni=True)
    pdf.set_auto_page_break(True, margin=40)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.utilisation()
    pdf.tabledata()
    pdf.total()
    pdf.set_font("Roboto", size=12)
    response = make_response(pdf.output(dest='S'))
    response.headers.set('Content-Disposition', 'inline', filename=filename + '.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response

if __name__ == '__main__':
	facture.run(debug = True)
