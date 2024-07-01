from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

from apps.models.models import db, OfficalSite, PhishingSite, ReccurentDomain, Score

from apps.models.questions import Questions
from apps.models.post import Post
from analyse_phishing.main import Main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


#toto=Questions().get_table_with_id(Score)
#print(toto)

allData = Main("https://www.orange.fr").main()
#print(allData["checkURL"])

upload = PhishingSite(id_offical_site=1, url=str(allData["checkURL"]), list_url=str(allData["extractURL"]), logo=str(allData["extractLogo"]), key_word=str(allData["extractKeyword"]), certificate=str(allData["extractCert"]), template=str(allData["extractTemplate"]))
#Post().insert_table(upload=my_phish_site)

with app.app_context():
    db.session.add(upload)
    db.session.commit()