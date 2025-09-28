import requests
import os

fonts = {
    "Roboto_Condensed": "https://github.com/google/fonts/raw/main/apache/robotocondensed/RobotoCondensed-Regular.ttf",
    "Roboto_Slab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab-Regular.ttf",
    "Libre_Franklin": "https://github.com/google/fonts/raw/main/ofl/librefranklin/LibreFranklin-Regular.ttf",
    "Raleway": "https://github.com/google/fonts/raw/main/ofl/raleway/static/Raleway-Regular.ttf",
    "Inter": "https://github.com/rsms/inter/raw/main/docs/font-files/Inter-Regular.ttf",
    "Source_Sans_Pro": "https://github.com/google/fonts/raw/main/ofl/sourcesanspro/SourceSansPro-Regular.ttf",
    "Poppins": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Regular.ttf",
    "DM_Sans": "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans-Regular.ttf",
    "Playfair_Display": "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-Regular.ttf",
    "Rubik": "https://github.com/google/fonts/raw/main/ofl/rubik/Rubik-Regular.ttf",
    "Lora": "https://github.com/google/fonts/raw/main/ofl/lora/Lora-Regular.ttf"
}

os.makedirs("static/fonts", exist_ok=True)

for name, url in fonts.items():
    print(f"Downloading {name}...")
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(f"static/fonts/{name}.ttf", "wb") as f:
            f.write(r.content)
        print(f"Saved {name} to static/fonts/{name}.ttf")
    except Exception as e:
        print(f"Failed to download {name}: {e}")

print("All done! Check your static/fonts folder.")
