from flask import Flask
from facture_json import facture
from contrat_pdf import contrat
from bp import bp
from bon_livraison import bon_livraison
from echange import be
from reparation import br


app = Flask(__name__)
app.register_blueprint(facture, url_prefix="/facture")
app.register_blueprint(contrat, url_prefix="/contrat")
app.register_blueprint(bon_livraison, url_prefix="/bon/livraison")
app.register_blueprint(bp, url_prefix="/bp")
app.register_blueprint(be, url_prefix="/bon/echange")
app.register_blueprint(br, url_prefix="/bon/reparation")

#@app.route("/")
#def home():
 #   return "hello"

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")
