
import tkinter as tk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from io import BytesIO
import pyttsx3

engine = pyttsx3.init()  # Initialize the text-to-speech engine

def search_image(animal):
    # Search for images on Google Images
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={animal}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Add User Agent header to avoid blocking
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        if len(images) > 1:  # First image usually is Google logo
            return images[1]['src']  # Return URL of the second image

    return None

def translate_to_persian(text):
    # Simulate translation (replace this with an actual API call)
    translations = {
        "dog": "dog is animal 1",
        "cat": "dog is animal 2",
        "bird": "dog is animal 3",
        "fish": "dog is animal 4"
    }
    return translations.get(text.lower(), "Translation not found.")

def show_image():
    animal = entry.get()
    
    # Search for images using Google Images API
    image_url = search_image(animal)

    if image_url:
        response_image = requests.get(image_url)
        
        try:
            image_data = Image.open(BytesIO(response_image.content))
            
            # Resize the image to fit within your GUI window
            resized_img = image_data.resize((400, 300))  

            img_tk = ImageTk.PhotoImage(resized_img)
            
            # Update the label with new image reference
            image_label.config(image=img_tk)
            image_label.image = img_tk
            
            # Speak out loud what we're searching for
            speak_text(f"Searching for {animal}...")
            
            # Translate and display in Persian
            translated_text = translate_to_persian(animal)
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, f"Translation: {translated_text}")
            
        except Exception as e:
             print("Error fetching or processing image:", e)
             
    else:
          text_box.delete(1.0, tk.END)
          text_box.insert(tk.END,"No image found.")

# Function to convert text to speech and play it back
def speak_text(text):
      engine.say(text)
      engine.runAndWait()

# Create main application window
root = tk.Tk()
root.title("Animal Image Search")

button = tk.Button(root, text="Show Image", command=show_image)
button.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=20)

# Create a scrolled text box for displaying messages
image_label = tk.Label(root)
image_label.pack(pady=20)

text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
text_box.pack(pady=20)

speak_text("Welcome! Please enter an animal name:")

# Run event loop until user closes app
root.mainloop()
