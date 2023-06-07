import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Selenium webdriver
driver = webdriver.Chrome()  # Replace with the path to your chromedriver executable

base_url = "https://fishpix.kahaku.go.jp/fishimage-e/search?FAMILY_OPT=0&FAMILY="

# make folder_path where you want images saved custom for own device
folder_path = "/Users/anish/OneDrive/Desktop/fishpix_image"

file_path = "familynames.txt"  # Replace with the path to your text file
family_names = []  # Array to store the lines

# create pandas dataframe
column_names = ['image_id', 'family', 'Name']
fish_pix_df = pd.DataFrame(columns=column_names)


with open(file_path, "r") as file:
    for line in file:
        family_names.append(line.strip())  # Add each line as a string to the array


for x in family_names:

    driver.get(base_url + x)

    # Find all the image captions
    captions = driver.find_elements(By.CLASS_NAME, "result")

    # Extract the text from each caption and store it in an array
    caption_texts = []
    for caption in captions:
        caption_texts.append(caption.text.strip())

    loc_count = 0

    # add caption into data frame

    # Send a GET request to the website
    response = requests.get(base_url + x)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all image tags in the HTML
    image_tags = soup.find_all("img")

    # Download and save the images

    count = 0
    for tag in image_tags:
        # Get the image URL
        image_url = urljoin(base_url, tag["src"])

        # Send a GET request to the image URL
        image_response = requests.get(image_url)

        # Get the file name from the image URL
        file_name = os.path.basename(x + "image" + str(count) + ".jpg")

        # store image name into dataframe

        # Save the image file
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "wb") as file:
            file.write(image_response.content)
            print(f"Image saved: {file_name}")
        count = count + 1

    print("Image scraping and downloading completed.")
    # for testing purposes
    break


print(fish_pix_df)

# write dataframe to local txt file

# close selenium webdriver
driver.quit()
