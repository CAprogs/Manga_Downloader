import os
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
import re
import pandas as pd
import yaml

#============================================================= Chargement des datas ====================================================================================
mangas_path = '/Users/charles-albert/Desktop/Manga Downloader/mangas.csv'
chapters_path = '/Users/charles-albert/Desktop/Manga Downloader/mangas_chapters.yml'

print('\nChargement des datas ...')
mangas_df = pd.read_csv(mangas_path)
with open(chapters_path) as chapters_file:
    chapters_yml = yaml.safe_load(chapters_file)

#==================================================================== Fonctions =========================================================================================
# Fonction pour attribuer le bon format au chapitre / volume
def chapter_or_volume(chapter_name):
    if 'chapitre' in chapter_name:
        result = chapter_name.replace('chapitre ','')
    else:
        result = chapter_name.replace(' ','-')
    return result

# Fonction pour crop l'image
def crop(path_image,size):

    # Récupérer l'image capturée
    image = Image.open(path_image)

    # Dimensions de l'image initiale
    initial_width = size['width'] # Largeur initiale image
    initial_height = size['height'] # Hauteur initiale image

    # Dimensions du screenshot
    screen_width = image.width # Largeur screenshot
    screen_height = image.height # Hauteur screenshot

    # Calculer les coordonnées de recadrage
    x = (screen_width - initial_width) // 2
    y = (screen_height - initial_height) // 2
    a = 25 # Nbre de pixels à ajuster pour la bonne taille
    b = 80 # Nbre de pixels à ajuster pour la bonne taille
    
    if initial_width > initial_height: # Si l'image est en mode paysage
        # Recadrer l'image en ajustant pour conserver la largeur initiale
        x = ( x // 2 ) + b
        image = image.crop((x,0,screen_width - x,screen_height))
    else:
        # Recadrer l'image pour ne conserver que l'élément souhaité
        image = image.crop((x-a, y-a, x + initial_width+a, y + initial_height+a))
    
    # Enregistrer l'image recadrée
    image.save(path_image)

# #====================================================== Configuration de Selenium pour utiliser Chrome ================================================================
# Chemin vers le profil Chrome
chrome_profile_path = '/Users/charles-albert/Library/Application Support/Google/Chrome/Default'
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + chrome_profile_path)
driver = webdriver.Chrome(options=options,executable_path='/Users/charles-albert/Desktop/chromedriver_mac_arm64/chromedriver') # Chemin vers l'exécutable chromedriver
driver.maximize_window() # Ouvrir le navigateur en full size
# =======================================================================================================================================================================

print(f'\n {len(mangas_df)} Mangas disponibles') # afficher le nombre de mangas disponibles

manga_name = 'jujutsu-kaisen'     # changer à mangas_df['name'][0]      # nom manga

print(f'\n Manga séléctionné : {manga_name}') 
nom_fichier= f'/Users/charles-albert/Desktop/Manga Downloader/{manga_name}/' # Chemin fichier à créer
# Création du Dossier du manga
if not os.path.exists(nom_fichier):
    os.makedirs(nom_fichier)


# Boucler de 0 jusque n-1 chapitres ( du dernier chapitre sorti au n-1 ieme chapitre ):
# for i in range()
chapter_name = chapters_yml[manga_name][0] # nom chapitre
# Afficher le nombre de chapitres disponibles 
print(f'\n {len(chapter_name)} Chapitres disponibles') 

nom_chapitre = nom_fichier + f'{chapter_name}/' # chemin du chapitre/volume à créer
# Création du Dossier du chapitre correspondant
if not os.path.exists(nom_chapitre):
    os.makedirs(nom_chapitre)

chapter_number = chapter_or_volume(chapter_name)

page = 1 # Page de départ
lien_chapitre = str(f'https://www.japscan.lol/lecture-en-ligne/jujutsu-kaisen/{chapter_number}/{page}.html')  # Lien du chapitre

# Accès à la page avec Selenium
driver.get(lien_chapitre)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# récupérer le nombre de pages du chapitre
try:
    element = driver.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/p[6]') # chemin vers l'élément qui contient le nombre de pages
    element_nombre_pages = element.text.strip() # conversion en string

    resultat = re.search(r'\d+', element_nombre_pages) # Utiliser une expression régulière pour extraire le chiffre
    if resultat: # Si on trouve le nombre de pages, on le récupère
        nombre_pages = int(resultat.group(0))
        print(f"""\n Téléchargement en cours ...
              
              {chapter_name}
              {nombre_pages} pages """)
    else:
        print("Aucun chiffre trouvé.")
except:
    print("Pas d'informations trouvées.")


# Rechercher l'image => Faire un screenshot => Redimensionner l'image => la sauvegarder
while page <= nombre_pages:

    # Obtention de la balise contenant l'URL de l'image
    image_element = soup.find('div', id='single-reader')

    # Obtention de l'URL de l'image
    image_url = image_element.find('img', class_='img-fluid')['src']

    # Trouver l'élément souhaité sur la page à partir de l'URL de l'image
    element = driver.find_element_by_xpath('//*[@id="single-reader"]/img')
    size = element.size

    driver.get(image_url)

    # chemin de sauvegarde de l'image
    path_image = f"{nom_fichier}/page{page}.png"

    # prendre le screenshot de la page entière
    driver.save_screenshot(path_image)
    
    # Crop l'image aux bonnes dimensions et la sauvegarder
    crop(path_image,size)

    print(f"Page {page} téléchargée.")

    # Accès à la page suivante
    page += 1
    if page > nombre_pages:
        break
    else:
        lien_chapitre=str(f'https://www.japscan.lol/lecture-en-ligne/jujutsu-kaisen/{chapter_number}/{page}.html')
        driver.get(lien_chapitre)
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # Analyse de la nouvelle page
    
# Fermeture du navigateur
driver.quit()

print(f"\nTéléchargement {chapter_name} terminé.")
