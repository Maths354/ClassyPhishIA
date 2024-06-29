import os
import sys

libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(libs_path)

from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from apps.config import Config

from apps.models.models import db, OfficalSite

from apps.models.post import Post
from inject_db.main import Main



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


with open("inject_db/official_sites.txt") as official_links:
    for official_link in official_links:
        print(f"{official_link.rstrip()} début ajout")
        allDatas = Main(official_link.rstrip()).main()
        datas=allDatas["datas"]
        print(f"{official_link.rstrip()} infos du sites récupérées")

        my_off_site = OfficalSite(url=official_link.rstrip(), list_url=str(datas["extractURL"]), logo=str(datas["extractLogo"]), key_word=str(datas["extractKeyword"]), certificate=str(datas["extractCert"]), template=str(datas["extractTemplate"]))
        Post().insert_table(upload=my_off_site)
        print(f"{official_link.rstrip()} ajouté dans la bdd")