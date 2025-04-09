import os
import requests

def random() -> str:
    """Get a random quote on each request.
    
    Returns:
        str: A string of the random quote.
    """
    try:
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status
        data = response.json()[0]
        return f'"{data["q"]}" — {data["a"]}'
    except Exception as e:
        print(f"Error: Could not fetch quote. ({e})")
        return None

def today() -> str:
    """Get the quote of the day on each request.

    Returns:
        str: A string of today's quote.
    """
    try:
        response = requests.get("https://zenquotes.io/api/today")
        response.raise_for_status
        data = response.json()[0]
        return f'"{data["q"]}" — {data["a"]}'
    except Exception as e:
        print(f"Error: Could not fetch quote. ({e})")
        return None
    
def get_bulk_quotes() -> list[str]:
    """Get 50 random quotes on each request.

	Returns:
        list[str]: A list where each element is a formatted string containing a quote and its author.
	"""
    try:
        response = requests.get("https://zenquotes.io/api/quotes")
        response.raise_for_status()
        quotes_data = response.json()
        return [f'"{quote["q"]}" — {quote["a"]}' for quote in quotes_data]
    except Exception as e:
        print(f"Error fetching quotes: {e}")
        return None

def image(save_path: str = 'quote_image.jpg') -> str:
    """Get a random inspirational image on each request.
    Args:
        save_path (str): The file path where the image will be saved. Defaults to 'quote_image.jpg' in the current working directory.

    Returns:
        str: The file path where the image has been saved
    """
    try:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        
        response = requests.get("https://zenquotes.io/api/image", stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        # print(f"Quote image successfully saved to {save_path}")
        return save_path
    except Exception as e:
        print(f"Error fetching the quote image: {e}")
        return None

def attribution() -> str:
    """Inspirational quotes provided by ZenQuotes API ( https://zenquotes.io )"""
    return "Inspirational quotes provided by ZenQuotes API (https://zenquotes.io)"
