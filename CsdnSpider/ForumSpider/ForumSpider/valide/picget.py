# This is a program for IP limit using picture recognition.
# URL:	http://bbs.csdn.net/human_validations/new
# Input: human validations page
# Get the jpeg from the url.
# use picture recognition to get the string from the picture.
# Authentication pass!
# 
# this is try to use selenuim to login
import re,os,sys
import time
import urllib2
import cookielib
import urllib
from cookielib import CookieJar

import pytesseract
from selenium import webdriver
from PIL import Image,ImageFilter,ImageEnhance
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys

class PicGet:

	def image_to_text(self, img):
		text = pytesseract.image_to_string(img)
		text = re.sub('[\W]', '', text)
		return text

	def imageToString(self,picname):
		image = Image.open(picname)
		ValidCode = self.image_to_text(image)
		image.save('captcha.png')
		return ValidCode

	def validlogin(self,driver,cookie,validcode):
		# use the validcode to authentication
		PostUrl = "http://bbs.csdn.net/human_validations"		
		elem = driver.find_element_by_id("captcha")
		elem.send_keys(validcode)
		elem.send_keys(Keys.TAB)
		time.sleep(3)
		driver.find_element_by_xpath('//button[@type="submit"]').send_keys(Keys.ENTER)
		#submit_button.send_keys(Keys.ENTER)
		print "test"
		cur_url = driver.current_url
		# print (cur_url)
		if cur_url == PostUrl:
			return True
		else:
			return False
	
	def validImageGet(self):
		AuthUrl = "http://bbs.csdn.net/human_validations/new"
		picname = 'captcha.png'
					
		sel = webdriver.Chrome()
		sel.get(AuthUrl)
		cookie = sel.get_cookies()
		auth_token = sel.find_element_by_xpath('//input[@name="authenticity_token"]')
		captcha_key = sel.find_element_by_xpath('//input[@id="captcha_key"]')

		# submit_button = sel.find_element_by_xpath('//button[@type="submit"]')
		# submit_button.submit()		
		time.sleep(0.3)
		picItem = sel.find_element_by_xpath('//img[@alt="captcha"]')
		# submit_button = sel.find_element_by_xpath('//button[@type="submit"]')
		sel.save_screenshot(picname)
		left = int(picItem.location['x'])
		top = int(picItem.location['y'])
		right = int(picItem.location['x'] + picItem.size['width'])
		bottom = int(picItem.location['y'] + picItem.size['height'])
		im = Image.open(picname) 
		# print (left,top,right,bottom)
		im = im.crop((left, top, right, bottom))
		im.save(picname)
		# validcode picture recognize
		time.sleep(0.5)

		validcode = self.imageToString(picname)
		print (validcode)

		validcode = "RCNCUB"
		#validcode = input("please input:")
		if re.match('[A-Z]{6}',validcode):
			if self.validlogin(sel,cookie,validcode):
				print ('Auth Success!')
		else:
			print ('Auth Fail!')
			#picItem.send_keys(Keys.TAB)
			#submit_button.send_keys(Keys.ENTER)
			#submit_button.click()
			# try:
			# 	submit_button.click()
			# except Exception,e: 
			# 	print (Exception,":",e)

		# validcode = input("please input:")
		# if True: # if (len(validcode) == 6) & validcode.isalnum():
		# 	if self.validpost(cookie,auth_token,validcode,captcha_key):# if self.validlogin(sel,cookie,validcode):
		# 		print ('Authentication Pass!')
		# 		break
		# else:
		# 	submit_button.click()

		time.sleep(5)
		sel.quit()

if __name__ == '__main__':
	ValidTest = PicGet()
	ValidTest.validImageGet()