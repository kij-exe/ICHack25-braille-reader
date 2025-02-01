from bs4 import BeautifulSoup as bs
import requests as rq

UPLOAD_URL = "https://angelina-reader.ru/upload_photo/?src=3"

def convert_image_to_braille(image_path: str) -> str:
  """
    Convert Braille Image to Braille text using Angelina Reader and web scraping.
    
    Args:
        image_path (str): Path to the input image file
    
    Returns:
        str: Extracted Braille text from the image
    
    Raises:
        RuntimeError: Redirect and scraping errors
    """
    
  # POST request payload
  files = {"file": open(image_path, "rb")}
  data = {
    "lang": "EN",
    "find_orientation": "True",
    "process_2_sides": "False"
  }

  res = rq.post(UPLOAD_URL, files=files, data=data, allow_redirects=False)
  
  # The request is expected to redirect to the result page  
  redirect_url = res.headers.get("Location")
  if not redirect_url: raise RuntimeError("Failed to fetch the result page.")
  
  res = rq.get(redirect_url)

  # Extract the Braille text from the result page
  soup = bs(res.text, "html.parser")
  candidates = soup.find_all("div", class_="read-card__text") 
  
  # The Braille output should appear inside the second occurrence of div.read-card__text
  if len(candidates) < 2: raise RuntimeError("Failed to locate Braille text to extract.")
  return candidates[1].get_text().strip()