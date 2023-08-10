import requests
import os
from pathlib import Path
from lxml import html

# Fonction de téléchargement
def download_image_from_xpath(response_url, xpath, save_path, i):

    if response_url.status_code == 200:
        # Parser le contenu HTML
        tree = html.fromstring(response_url.content)

        # Trouver l'élément à partir du xpath donné
        image_element = tree.xpath(xpath)

        if image_element:
            # Extraire l'URL de l'image à partir de l'attribut 'src'
            image_url = image_element[0].get('src')

            # Télécharger l'image
            image_response = requests.get(image_url)

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
            print("Aucun élément trouvé pour le xpath donné.")
            return False
    else:
        print(f"Échec de la requête HTTP. Code d'état : {response_url.status_code}")
        return False

# Obtenir le chemin absolu du répertoire contenant le script
script_directory = Path(os.path.dirname(os.path.realpath(__file__)))

# ========================================== Variables initiales ==================================================================

url = "https://scantrad-vf.co/manga/jujutsu-kaisen/chapitre-1/?style=list" # Lien vers le chapitre à télécharger
i = 0 # Page de départ 
File_name = 'jujutsu-kaisen' # Nom du fichier à créer
chapter = 'chapitre-1' # Nom du dossier à créer contenant les images

# =================================================================================================================================

nom_fichier = script_directory / File_name
if not os.path.exists(nom_fichier): # Si le fichier n'existe pas on le crée
    os.makedirs(nom_fichier)

nom_chapitre = nom_fichier / chapter
if not os.path.exists(nom_chapitre):
    os.makedirs(nom_chapitre)

# Effectuer une requête HTTP sur l'URL donnée
response_url = requests.get(url)

while True: # Téléchargement des images
    xpath = f'//*[@id="image-{i}"]'
    save_path = f"{nom_chapitre}/{i}.jpg"  # Chemin où sauvegarder les images
    response = download_image_from_xpath(response_url, xpath, save_path, i)
    if response == True:
        i += 1
    else:
        print("Téléchargement terminé.") 
        break