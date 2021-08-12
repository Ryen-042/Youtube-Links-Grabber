import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# print(os.path.abspath(__file__))                   # Prints the Absolute Path to the Current Working File.
# print(os.path.dirname(os.path.abspath(__file__)))  # Prints the Absolute Path to the Current Working Directory

# Because I use terminal from a directory different from the one that include this `.py` file, next line is used to
# change the current working directory to this file's path to save the text file that will be created next to this file.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Working in Normal Mode
# driver = webdriver.Chrome(ChromeDriverManager().install())

# Working in Headless Mode
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True

# Auto download `ChromeDriverManager`
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# To use a `ChromeDriverManager` you downloaded:
# driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)

# provide a youtube playlist link
URL = ""
driver.get(URL)

# Links of videos + Unwanted links
links = [elem.get_attribute("href") for elem in driver.find_elements_by_xpath("//a[@href]")]

# Filtering Results and removing unwanted links + Removing the duplicates:
# After filtering `links`, the result has 2 copies of links for each video, so we use slicing to remove the duplicates.
links = [i for i in links if 'index' in i][::2]

# To scroll till end of the page
for i in range(1, len(links)*3//10):
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)
    # driver.execute_script(f"scroll(0, {720*i})") # Another method for scrolling down
time.sleep(2)

# Contents -> (Video Number, Length, Name, Author)
contents = driver.find_element_by_id("contents")
contents = [i for i in contents.text.split("\n")]
contents = list(zip(contents[::4], contents[1::4], contents[2::4], contents[3::4]))

output = (
    '\n' + '-' * len(links[1]) + '-' * (len(str(len(links))) -1) + '\n'
).join([f"Track #{c[0]}: {c[2]}\nLength: {c[1]}   |   By: {c[3]}\n{l}" for c, l in zip(contents, links)])

with open('Link Grabber - Links.txt', 'w') as grabber_file:
    grabber_file.write('Found Links Are:\n' + '-' * 16 + '\n')
    grabber_file.write(output)
    # print("Found Links Are:\n\n" + output)

os.startfile('Link Grabber - Links.txt')
