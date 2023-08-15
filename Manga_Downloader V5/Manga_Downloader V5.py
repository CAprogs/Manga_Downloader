import requests
import zipfile
import io
import os

# "https://fmteam.fr/api/download/{manga_name}/fr/ch/{chapter_number}" ( Pattern de téléchargement si chapter_number = int)
# "https://fmteam.fr/api/download/{manga_name}/fr/ch/{chapter_number_1}/sub/{chapter_number_2}" ( Pattern de téléchargement si chapter_number = float)

url = "https://fmteam.fr/api/download/hajime-no-ippo/fr/ch/1429" 
response = requests.get(url)

if response.status_code == 200:
    # Utilisez io.BytesIO pour créer un flux binaire à partir du contenu de la réponse
    zip_stream = io.BytesIO(response.content)

    # Spécifiez le nouveau nom du dossier
    new_folder_name = "hajime-no-ippo"

    # Créez le répertoire de destination avec le nouveau nom
    extract_path = os.path.join("/Users/charles-albert/Desktop/PandaScan", new_folder_name)  # crée un dossier contenant les dossiers téléchargés
    os.makedirs(extract_path, exist_ok=True)

    # Créez un objet zipfile.ZipFile à partir du flux binaire
    with zipfile.ZipFile(zip_stream, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    print("Téléchargement et extraction réussis.")
else:
    print("Échec du téléchargement.")