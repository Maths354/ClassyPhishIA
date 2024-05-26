from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

from apps.models.models import db, OfficalSite, PhishingSite, ReccurentDomain, Score

from apps.models.questions import Questions
from apps.models.post import Post
from analyse_phishing.main import Main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

official_links=["https://x.com",
               "https://www.orange.fr",
               "https://www.youtube.com/",
               "https://www.twitch.tv/",
               "https://www.google.com/",
               "https://www.netflix.com/",
               "https://www.amazon.fr/"]

for official_link in official_links:
    allDatas = Main(official_link).main("")

    datas=allDatas["datas"]

    my_off_site = OfficalSite(url=official_link, list_url=str(datas["extractURL"]), logo=str(datas["extractLogo"]), key_word=str(datas["extractKeyword"]), certificate=str(datas["extractCert"]), template=str(datas["extractTemplate"]))
    Post().insert_table(upload=my_off_site)
    