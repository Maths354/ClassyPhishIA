<p align = "center">
<img src = "apps/static/logo_site.png"height = "100" width="auto">
</p>

## 🤖 ClassyPhishIA

Cet outil analyse à l'aide du machine learning, des sites de phishing et les compares à des sites légitimes afin de détecter des similarités.

## Capture-d'écran
<img src = "apps/static/home.png">
<p align = "center">
Page d'accueil
</p>

<img src = "apps/static/resultat.png">
<p align = "center">
Page des résultats (scores)
</p>

<img src = "apps/static/details.png">
<p align = "center">
Page des résultats (détails des données)
</p>

<img src = "apps/static/tableau.png">
<p align = "center">
Page des résultats (tableau points positifs/négatifs)
</p>

## 📃 Fonctionnalités

Les fonctionnalités actuellement disponible dans l'outil sont :
* Scanner un site à partir d'une URL insérée.
* Permettre une analyse supplémentaire avec VirusTotal (nécessite au préalable la détention d'une clé API).
* Consulter une page d'analyse qui référence l'ensemble des résultats et statistiques générales.
* Signaler le site au gouvernement en cas de soupçons.

## 🔧 Aspect technique de l'outil

### 🧠 Le machine learning
Pour fonctionner, ClassyPhishIA s'appuie sur :
* Un apprentissage supervisé (utilise des données annotés et préparés)
* Un modèle de Classification (faire une prédiction en fonction de caractéristiques)
* Un algorithme de régression logistique (interprétation par des variables unique à coefficient)

### 📊 Données analysés 

Pour réaliser une prédiction, le modèle de ClassyPhishIA se base sur divers artéfacts de sites web :
* Logo
* URL
* URL balises
* Mots-clés
* Certificats
* Balises HTML

### 💾 Affichage & intéractions sous Flask/SQLite

ClassyPhishIA utilise le framework web Flask, qui permet de créer facilement des applications et des sites locaux d'une façon légère et extensible. Il intéragit avec la base de données SQLite pour afficher les données.

## 🛠️ Installation

#### Makefile
```
git clone https://github.com/Maths354/ClassyPhishIA.git
cd ClassyPhishIA/
make
```

:warning: L'exécution de cet outil ne fonctionne pour l'instant que sur Linux🐧 

:warning: Un environnement venv Python est créé afin de vous permettre d'exécuter et d'utiliser l'outil correctement, sans casser les distributions Python présentes sur votre système.
## 🗃️ Insertions des données dans la base

#### Makefile
```
make add_datas
```

:warning: Lors de l'exécution de l'outil, une erreur peut apparaître en fonction de la distribution Linux utilisée, cela est dû à un paquet manquant `libgl1`. 

:warning: Les sites insérés dans la base de données font partie d'une liste de sites légitimes et vérifiés stockés sous la forme d'un fichier texte accessible dans 'inject_db/official_sites_XXX.txt'. La durée d'insertion des données dépend de la quantité de sites, mais aussi des sécurités présentes qui peuvent empêcher la récupération des données complètes.

## ✅ Lancement de l'outil

### 📚 Exemple CLI

#### Avec un Makefile
```
make run
```

## Remerciements spéciaux

* Nous tenons à remercier toutes les personnes qui nous ont soutenus tout au long de notre projet. 

* Nous exprimons notre profonde gratitude à notre tuteur, Maxime, dont la connaissance approfondie de la formation, des aspects techniques et des attentes du jury nous a permis de nous organiser plus efficacement et de préparer le projet de manière optimale. 

* Nous remercions également l’ensemble des intervenants de la formation pour leurs précieuses informations sur les différentes méthodes de machine learning. 

* Enfin, nous remercions chaleureusement Aurélien de la société Orange Innovation pour avoir répondu à certaines de nos questions et nous avoir apporté son éclairage.

## Information

Ce projet est destiné uniquement à des fins éducatives et défensives. Les créateurs et contributeurs ne sont pas responsables de toute utilisation abusive ou malveillante de cet outil. Utilisez-le de manière responsable et éthique, en respectant toutes les lois et réglementations pertinentes.

## Problèmes connus

* Il est est possible qu'un bannissement soit réalisé à votre encontre si trop de requêtes sont effectués à partir d'une même adresse IP, nous vous conseillons donc d'insérer les sites dans la base de données par petites quantités afin d'éviter tout dysfonctionnement.

* Due à des sécurités avancés sur certains sites légitimes et également les sites douteux, il est possible que certaines données ne soient pas récupérés correctement et empêche ainsi d'obtenir une analyse concrète. Des évolutions sont donc envisagés dans une prochaine version.
