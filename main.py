from flask import Flask
from facture_json import facture
from contrat_pdf import contrat
from bp import bp
from bon_livraison import bon_livraison


app = Flask(__name__)
app.register_blueprint(facture, url_prefix="/facture")
app.register_blueprint(contrat, url_prefix="/contrat")
app.register_blueprint(bon_livraison, url_prefix="/bon/livraison")
app.register_blueprint(bp, url_prefix="/bp")

#@app.route("/")
#def home():
 #   return "hello"

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")
