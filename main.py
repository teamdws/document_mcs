from flask import Flask
from facture_json import facture
from contrat_pdf import contrat
from bon_livraison import bon_livraison


app = Flask(__name__)
app.register_blueprint(facture, url_prefix="/facture")
app.register_blueprint(contrat, url_prefix="/contrat")
app.register_blueprint(bon_livraison, url_prefix="/bon/livraison")

#@app.route("/")
#def home():
 #   return "hello"

if __name__ == '__main__':
  app.run(debug=True)
