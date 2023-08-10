import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup

# Fonction de téléchargement
def download_image_from_xpath(response_url, save_path, i):

    if response_url.status_code == 200:
        # Parser le contenu HTML
        soup = BeautifulSoup(response_url.content, "html.parser")
        
        image_element = soup.find("img", src=True)
        if image_element:
            image_url = image_element["src"]

            # Télécharger l'image
            image_response = requests.get('https://lelscans.net/'+image_url)

            if image_response.status_code == 200:
                # Sauvegarder l'image dans le fichier spécifié
                with open(save_path, 'wb') as f:
                    f.write(image_response.content)
                print(f"Image {i} téléchargée.")
                return True
            else:
                print(f"Échec du téléchargement de l'image. Code d'état : {image_response.status_code}")
                return False
        else:
            print("Aucun élément trouvée.")
            return False
    else:
        print(f"Échec de la requête HTTP. Code d'état : {response_url.status_code}")
        return False

# Obtenir le chemin absolu du répertoire contenant le script
script_directory = Path(os.path.dirname(os.path.realpath(__file__)))

# ========================================== Variables initiales ==================================================================

File_name = 'beelzebub' # Nom du fichier à créer / nom du manga
chapter = 240 # numéro du chapitre à télécharger
chapter_file = f'chapitre-{chapter}' # Nom du dossier à créer contenant les images
i = 1 # Page de départ 

# =================================================================================================================================

nom_fichier = script_directory / File_name
if not os.path.exists(nom_fichier): # Si le fichier n'existe pas on le crée
    os.makedirs(nom_fichier)

nom_chapitre = nom_fichier / chapter_file
if not os.path.exists(nom_chapitre):
    os.makedirs(nom_chapitre)

while True: # Téléchargement des images
    url = f"https://lelscans.net/scan-{File_name}/{chapter}/{i}" # Lien vers le chapitre à télécharger
    response_url = requests.get(url) # Effectuer une requête HTTP sur l'URL donnée
    save_path = f"{nom_chapitre}/{i}.jpg"  # Chemin où sauvegarder les images
    response = download_image_from_xpath(response_url, save_path, i)
    if response == True:
        i += 1
    else:
        print("Téléchargement terminé.") 
        break