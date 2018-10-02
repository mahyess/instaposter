from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import pyautogui
import pyperclip
import json

spoof_extension_id = "djflhoibgkdhkhhcedjiklpkjnoahfmg"


data = json.load(open('insta.json'))
username = data["instauser"]
password = data["instapw"]
keyword = data["keywords"]


# open instagram and enter login credentials
def instaOpen(username, password):
	# go to the instagram login page
	driver.get("https://www.instagram.com/accounts/login/")

	time.sleep(2)

	# find the element that's id is -> username field id
	username_field = driver.find_element_by_name("username")

	# type in the search
	username_field.send_keys(username)

	# same for password
	password_field = driver.find_element_by_name("password")
	password_field.send_keys(password)
	password_field.submit()
	

	WebDriverWait(driver, 10).until(EC.title_contains("Instagram"))
	print(driver.title)
	
	time.sleep(2)

def spoofSetting():
	driver.get(r"chrome-extension://djflhoibgkdhkhhcedjiklpkjnoahfmg/options.html")
	# driver.find_element_by_id("menu_import").click()
	# driver.find_element_by_name("import_file").send_keys(r"E:\chromedriver_win32\user_agent_export.json")	
	driver.find_element_by_id("menu_spoof").click()
	driver.find_element_by_id("add_domain").send_keys(r"www.instagram.com")
	driver.find_element_by_xpath("//select[@id='options']/option[text()='iPhone 6']").click()
	driver.find_element_by_id("add_entry_button").click()
	time.sleep(2)

def unsplashCrawl(keyword):
	driver.get("https://unsplash.com/explore")

	driver.find_element_by_name("searchKeyword").send_keys(keyword[np.random.randint(len(keyword))])
	time.sleep(15)
	# imageload and get caption
	i=driver.find_element_by_css_selector("._2zEKz")
	i.click()

	# download button
	try:
		driver.find_element_by_css_selector("._2Aga-").click()
	except:
		download_link = driver.find_element_by_xpath("//a[@title='Download photo']").get_attribute('href')
		driver.get(download_link)
	# print(1111)
	photographer = None
	photographer = driver.find_element_by_xpath("//a[contains(concat(' ', @class, ' '), ' _3XzpS _1ByhS ')]").text
	# photographer = driver.find_element_by_xpath("//a[@class='_3XzpS _1ByhS']").text

	caption = None

	try:
		caption = i.get_attribute('alt')
		print(caption)
	except:
		pass
		# print(333)
		
	return caption, photographer
	
def getDownloadedImageName():
	driver.get(r"chrome://downloads/")
	namelist = driver.find_element_by_xpath("//*[@class='']").text
	namelist = namelist.splitlines()
	for item in namelist:
		if '.jpg' in item:
			name = item
			break
	if '[1]' in name:
		print("This photo is already uploaded")
		raise SystemExit

	pyperclip.copy(''.join(["E:\\chromedriver_win32\\Pictures\\", name]))
	# print(pyperclip.paste())

def clickUpload():
	try:
		driver.find_element_by_xpath("//div[contains(concat(' ', @class, ' '), ' coreSpriteFeedCreation ')]").click()
	except:
		driver.get("https://www.instagram.com/")
		clickUpload()

def imageUpload(captionInsta):
	driver.get("https://www.instagram.com/")
	clickUpload()
	# driver.find_element_by_xpath("//div[contains(concat(' ', @class, ' '), ' coreSpriteFeedCreation ')]").send_keys(r"C:\Users\laptop1\Pictures\002.jpg")
	time.sleep(3)
	pyautogui.hotkey('ctrl','v')
	pyautogui.press("enter")
	time.sleep(2)
	print('before')

	pyautogui.press(['tab', 'tab', 'tab', 'enter'])
	# try:
	# 	print('try')
	# 	driver.find_element_by_xpath("//span[contains(concat(' ', @class, ' '), ' createSpriteExpand ')]").click()

	# except:
	# 	print('except')
	# 	driver.find_element_by_css_selector('.createSpriteExpand').click()

	# 	pass
	# driver.execute_script('''var x = document.getElementsByClassName("_8az64");
	# 	var i;
	# 	for (i = 0; i < x.length; i++) {
	# 		x[i].style.width = 100%;
	# 		x[i].style.left = 0%;
	# 		x[i].style.top = auto;
	# 		x[i].style.transform-origin = none;
	# 	}''')
	# driver.find_element_by_css_selector('._j7nl9').click()
	time.sleep(5)
	# driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' _9glb8 ')]").click()
	driver.find_element_by_xpath("//*[contains(text(), 'Next')]").click()

	time.sleep(2)
	pyautogui.press(['tab', 'tab', 'tab'])
	pyperclip.copy(captionInsta)
	pyautogui.hotkey('ctrl','v')
	print('copied')
	time.sleep(5)
	# driver.find_element_by_tag_name('textarea').click().send_keys(captionInsta)

	driver.find_element_by_css_selector('._9glb8').click()

def hashtagGeneration(keyword):
	driver.get(r'https://displaypurposes.com/')
	a = []
	for i in keyword:
		a.extend(['#',i,' '])
	driver.find_element_by_tag_name("input").send_keys(a)
	time.sleep(3)
	driver.find_element_by_css_selector('.primary').click()
	time.sleep(2)
	tags = driver.find_element_by_css_selector('.content').text
	return tags

def captionWriter(imgCaption, photographer, hashtags):
	return ''.join(['By ',photographer,'\n', imgCaption, '\n', 'Tag a friend who would love this..', hashtags])


# Create a new instance of the Chrome driver
options = Options()
options.add_experimental_option("prefs", {
		"download.default_directory": r"E:\chromedriver_win32\Pictures",
		"download.prompt_for_download": False,
		"download.directory_upgrade": True,
		"safebrowsing.enabled": True
	})
options.add_extension(r"E:\chromedriver_win32\spoof.crx")
driver = webdriver.Chrome(chrome_options=options)


instaOpen(username, password)
spoofSetting()
hashtags = hashtagGeneration(keyword)
caption, photographer = unsplashCrawl(keyword)
# getDownloadedImageName()
# captionInsta = captionWriter(caption, photographer, hashtags)
# imageUpload(captionInsta)
	
	

	# try:
	#     # we have to wait for the page to refresh, the last thing that seems to be updated is the title
	#     # WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

	#     # You should see "cheese! - Google Search"
	#     print(driver.title)

	# finally:
	# 	time.sleep(200)
	# 	driver.quit()



