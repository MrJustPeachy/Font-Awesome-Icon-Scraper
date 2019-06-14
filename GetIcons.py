import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# url = 'https://fontawesome.com/cheatsheet/pro'
# req = requests.get(url)
# markup = req.text
# print(markup)

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome()
browser.get("https://fontawesome.com/cheatsheet/pro")
delay = 15  # seconds
icon_list = '<select>\n\t<option value="">No icon</option>\n'


def make_icon_format_string(font_awesome_icon):
    return "\t<option>" + font_awesome_icon + '</option>'


# Please enter in blacklist items in the following format
blacklist = ['far fa-reply', 'fal fa-reply', 'fas fa-reply', 'far fa-republican', 'fal fa-republican',
             'fas fa-republican', 'fab fa-youtube-square', 'fas fa-angle-up',
             'fas fa-hand-middle-finger', 'far fa-hand-middle-finger', 'fal fa-hand-middle-finger',
             'fas fa-bong', 'fal fa-bong', 'far fa-bong', 'fas fa-cannabis', 'fal fa-cannabis', 'far fa-cannabis',
             'fas fa-mosque', 'far fa-mosque', 'fal fa-mosque', 'fal fa-church', 'far fa-church', 'fas fa-church',
             'far fa-clipboard', 'far fa-democrat', 'fas fa-democrat', 'fal fa-democrat']
blacklist = [make_icon_format_string(string) for string in blacklist]

try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'reply')))
    soup = BeautifulSoup(browser.page_source, features='html.parser')

    solid_icons = soup.find("section", {'id': 'solid'}).find_all('article')
    solid_icon_values = ['\t<option>fas fa-' + x.attrs['id'] + '</option>' for x in solid_icons
                         if '\t<option>fas fa-' + x.attrs['id'] + '</option>' not in blacklist]
    icon_list += '\n'.join(solid_icon_values)

    regular_icons = soup.find("section", {'id': 'regular'}).find_all('article')
    regular_icon_values = ['\t<option>far fa-' + x.attrs['id'] + '</option>' for x in regular_icons
                           if '\t<option>far fa-' + x.attrs['id'] + '</option>' not in blacklist]
    icon_list += '\n'.join(regular_icon_values)

    light_icons = soup.find("section", {'id': 'light'}).find_all('article')
    light_icon_values = ['\t<option>fal fa-' + x.attrs['id'] + '</option>' for x in light_icons
                         if '\t<option>fal fa-' + x.attrs['id'] + '</option>' not in blacklist]
    icon_list += '\n'.join(light_icon_values)

    brand_icons = soup.find("section", {'id': 'brands'}).find_all('article')
    brand_icon_values = ['\t<option>fab fa-' + x.attrs['id'] + '</option>' for x in brand_icons
                         if '\t<option>fab fa-' + x.attrs['id'] + '</option>' not in blacklist]
    icon_list += '\n'.join(brand_icon_values)

except TimeoutException:
    print('timeout exception')

icon_list += '\n</select>'

with open('fa-icons.txt', 'w+') as file:
    file.write(icon_list)