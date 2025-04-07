import requests

API_URL = "https://steamworkshopdownloader.up.railway.app/download"

def download_mod(workshop_url: str):
    """
    Descarga la URL del mod de Steam Workshop a través de la API.
    Retorna un diccionario con `download_url` y `thumbnail_url`.
    """
    try:
        workshop_id = workshop_url.split("?id=")[-1]
        params = {
            "workshopUrl": workshop_url,
            "workshopId": workshop_id
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[SWL] Error al intentar descargar el mod: {e}")
        return None
