#!/bin/python3
import time
import os
import telebot
import requests
import re
from bs4 import BeautifulSoup
## Settings
update_interval = 10 # seconds
## Webscraping

def webscrape():
    os.rename('new_links.txt', 'old_links.txt')
    url_head = 'https://www.hermes.com'
    url = 'https://www.hermes.com/hk/en/category/women/bags-and-small-leather-goods/bags-and-clutches/#|'
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all the links on the page and filter the links containing "/hk/en/product/"
    links = [link.get("href") for link in soup.find_all("a") if "/hk/en/product/" in link.get("href")]
    # Write the filtered links to a file named "links.txt"
    with open("new_links.txt", "w") as f:
        for link in links:
            f.write(url_head + link + "\n")

    with open("new_links.txt", "r") as new_links:
        lines1 = set(new_links.readlines())
    # Open the second file for reading
    with open("old_links.txt", "r") as old_links:
        # Read the contents of the second file into a set of lines
        lines2 = set(old_links.readlines())

    # Use set operations to find the unique lines
    unique_lines = lines1.union(lines2) - lines1.intersection(lines2)
    with open ('message.txt', 'w') as m:
        for lines in unique_lines:
            m.write(lines)
    # Print the unique lines
    #for line in unique_lines:
    #    print(line.strip())

## Telegram Bot

API_key = os.getenv('API_KEY')
bot = telebot.TeleBot('6139828286:AAH7jdqJ69sclfP_DXtXltZXH_Yzx05d8x4')
links_file = '/scratch/lawrence/github/webscraper/message.txt'
mod_time = os.path.getmtime(links_file)
def check_for_updates():
    file_size = os.path.getsize(links_file)
    if file_size > 0:
        with open(links_file, 'r') as file:
            contents = file.read()
        bot.send_message(chat_id='-1001232515471', text=contents)
        os.remove('message.txt')
    
while True:
    webscrape()
    check_for_updates()
    time.sleep(update_interval)
