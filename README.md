<<<<<<< HEAD
# ClassyPhishIA

Objectif pour le model "main" : Avoir les résultat des modèles "enfants" (url_score, text_score, logo_similarity) pour ensuite les utiliser comme base d'entrainement afin de valider si le site de phishing usurpe bien un site présents dans la base de données.

# INFO DANS LA BASE DE DONNEE :
- ID, NAME, LOGO, BALISES

# Découpage du modèle :

# Structuration du programme :


=======
## 🤖 ClassyPhishIA

ClassyPhishIA est un outil d’analyse de phishing basé sur le machine learning, destiné à détecter la similarité entre des sites légitimes et des sites de phishing.

## 🛠️ Installation

#### With Makefile
```
git clone https://github.com/Maths354/ClassyPhishIA.git
cd ClassyPhishIA/
make
```

#### With Powershell
```
git clone https://github.com/Maths354/ClassyPhishIA.git
cd ClassyPhishIA/
.\build.ps1 -target all
```

## 🗃️ Populate Database

#### With Makefile 
```
make add_datas
```

#### With Powershell
```
.\build.ps1 -target add_datas
```

## ✅ Quick Start

### 📚 CLI Example

#### With Makefile 
```
make run
```

#### With Powershell
```
.\build.ps1 -target run
```

### 📈 Web display

AJOUTER UN GIF QUI MONTRE LE PROCESS DANALYSE
>>>>>>> dev
