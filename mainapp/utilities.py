""" filename: script.py """

# -------- Import libraries ----------------
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import csv
from selenium.webdriver.common.action_chains import ActionChains

def get_search(driver, query, page=None):

	if ' ' in query:
		query = query.replace(' ', '%20')

	if page == None:
		url = 'https://www.linkedin.com/search/results/all/?keywords=%s&origin=GLOBAL_SEARCH_HEADER' %query
		
		driver.get(url)
		sleep(0.5)

		people_button = driver.find_element_by_xpath("//button[starts-with(@class,'search-vertical-filter__filter-item-button artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view')]")
		people_button.click()
		sleep(0.5)
	
	else:
		url = 'https://www.linkedin.com/search/results/people/?keywords=%s&origin=SWITCH_SEARCH_VERTICAL&page=%d' %(query, page)
		
		driver.get(url)
		sleep(0.5)


def scroll(driver):
	# Scroll down to bottom
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
	sleep(1)

	# Scroll down to bottom
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
	sleep(1)

	# Scroll down to bottom
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
	sleep(1)

	# Scroll down to bottom/2
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	sleep(1)

	# Scroll down to bottom/2
	driver.execute_script("window.scrollTo(0, 0);")
	sleep(1)



def get_10(driver):
	people_list = driver.find_elements_by_xpath("//li[starts-with(@class,'search-result search-result__occluded-item ember-view')]")

	links2 = []

	for elem in people_list:
		href = elem.find_element_by_css_selector('a').get_attribute('href')
		
		if 'https://www.linkedin.com/in' in href:
			links2.append(href)

	return links2

# ---------------- Extract first set of linkedin search----------
# list of people in linkedin search
# query = 'HR manager'

# num_people = 85

# links = []

# get_search(query)
# sleep(0.5)

# scroll()
# sleep(0.5)

# links += get_10()

# page = 2

# # -------------- Loop through number of people after that 
# for i in range(int(num_people/10)):
# 	if len(set(links)) <= num_people:
# 		get_search(query, page)
# 		sleep(0.5)
		
# 		scroll()
# 		sleep(0.5)

# 		links += get_10()
# 		page += 1
# 	else:
# 		break

# # ------------- Select limited number of people --------

# links = links[:num_people]

# ------------ Scrape data through each profile, save to csv and connect ----------

# function to ensure all key data fields have a value
def validate_field(field):
	# if field is present pass 
	if field:
		pass
	# if field is not present print text 
	else:
		field = 'No results'
	return field

def connect(driver, name, add_note=False, text=None):
	
	try:
		connect_button = driver.find_element_by_xpath("//button[starts-with(@class,'pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view')]")
		connect_button.click()
		sleep(0.5)
		
		if add_note == True:
			add_note_button = driver.find_element_by_xpath("//button[starts-with(@class,'mr1 artdeco-button artdeco-button--muted artdeco-button--3 artdeco-button--secondary ember-view')]")
			add_note_button.click()
			
			message = driver.find_element_by_id('custom-message')
			message.send_keys(text)
			print("Succeffuly send the note to:", name)
			
			send_button = driver.find_element_by_xpath("//button[starts-with(@class,'ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view')]")
			send_button.click()
			sleep(0.5)
			
			print("Connected Succeffuly to connection:", name)
			
		else:
			send_button = driver.find_element_by_xpath("//button[starts-with(@class,'ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view')]")
			send_button.click()
			sleep(0.5)
			print("Connected Succeffuly to connection:", name)
		
	except:
		print("Can`t Connect to connection:", name)
		
def list_withdraw(driver):
	driver.get('https://www.linkedin.com/mynetwork/invitation-manager/sent/')

	sleep(0.5)

	scll(driver)
	sleep(0.5)

	people_list = driver.find_elements_by_xpath("//li[starts-with(@class,'invitation-card artdeco-list__item ember-view')]")

	people_dict = {}

	for i, people in enumerate(people_list):
		ago = people.find_element_by_tag_name('time')
		ago = ago.text.split(' ')[:2]

		if ago[1] == 'week' or ago[1] == 'weeks' or ago[1] == 'month' or ago[1] == 'months':

			people_dict[i] = people.get_attribute('id')

	people_idx = people_dict.keys()

	button_list = driver.find_elements_by_xpath("//button[starts-with(@class,'invitation-card__action-btn artdeco-button artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view')]")

	for i, button in enumerate(button_list):

		if i in people_idx:

			actions = ActionChains(driver)
			actions.move_to_element(button).perform()


			try:

				button.click()

				sleep(0.5)

				confirm_button = driver.find_element_by_xpath("//button[starts-with(@class,'artdeco-modal__confirm-dialog-btn artdeco-button artdeco-button--2 artdeco-button--primary ember-view')]")
				confirm_button.click()

				sleep(0.5)

				print("Succeffuly Withdraw Request")

			except:

				print("Can`t Withdraw request right now")

		else:
			pass

					
def save(driver, linkedin_urlz,add_note=False, text=None):

	save_to = []

	for name in linkedin_urlz:

		driver.get(name)

		sleep(5)

		driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

		sleep(1.5)

		sel = Selector(text = driver.page_source)

		# xpath to extract the text from the class containing the name
		name = sel.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract_first()

		if name:
			name = name.strip()

		# xpath to extract the text from the class containing the job title

		headline = sel.xpath('//*[starts-with(@class, "mt1 t-18 t-black t-normal break-words")]/text()').extract_first()

		if headline:
			headline = headline.strip()

		location = sel.xpath('//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract_first()

		if location:
			location = location.strip()

		headings = driver.find_elements_by_class_name('pv-profile-section__card-heading')
		headings = [x.text for x in headings]
		headings = ''.join(headings)		

		highlights = driver.find_elements_by_xpath("//ul[starts-with(@class,'pv-highlights-section__list list-style-none')]")
		highlights = [x.text for x in highlights]
		highlights = ''.join(highlights)		

		summary = sel.xpath('//*[starts-with(@class, "lt-line-clamp__line")]/text()').extract_first()

		if summary:
			summary = summary.strip()

		activity = driver.find_elements_by_xpath("//section[starts-with(@class,'pv-profile-section pv-recent-activity-section-v2 artdeco-container-card artdeco-card ember-view')]")
		activity = [x.text for x in activity]
		activity = ''.join(activity)		

		edu = driver.find_elements_by_xpath("//ul[starts-with(@class,'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more')]")
		edu = [x.text for x in edu]
		edu = ''.join(edu)		

		skills = driver.find_elements_by_xpath("//ol[starts-with(@class,'pv-skill-categories-section__top-skills pv-profile-section__section-info section-info pb1')]")
		skills = [x.text for x in skills]
		skills = ''.join(skills)		

		interests = driver.find_elements_by_xpath("//ul[starts-with(@class,'pv-profile-section__section-info section-info display-flex justify-flex-start overflow-hidden')]")
		interests = [x.text for x in interests]
		interests = ''.join(interests)		

		url = driver.current_url

		# validating if the fields exist on the profile
		name = validate_field(name)
		headline = validate_field(headline)
		location = validate_field(location)
		headings = validate_field(headings)
		highlights = validate_field(highlights)
		summary = validate_field(summary)
		activity = validate_field(activity)
		edu = validate_field(edu)
		skills = validate_field(skills)
		interests = validate_field(interests)
		url = validate_field(url)

		details_dict = {
			'name':name,
			'headline':headline,
			'location':location,
			'headings':headings,
			'highlights':highlights,
			'summary':summary,
			'activity':activity,
			'education':edu,
			'skills':skills,
			'interests':interests,
			'url':url}

		# # writing the corresponding values to the header
		# writer.writerow([name.encode('utf-8'),
  #                headline.encode('utf-8'),
  #                location.encode('utf-8'),
  #                headings.encode('utf-8'),
  #                highlights.encode('utf-8'),
  #                summary.encode('utf-8'),
  #                activity.encode('utf-8'),
  #                edu.encode('utf-8'),
  #                skills.encode('utf-8'),
  #                interests.encode('utf-8'),
  #                url.encode('utf-8')])

		print(name, ": Scraping Done, Trying to connect")

		save_to.append(details_dict)

		connect(driver, name, add_note=add_note, text=text)

	return save_to

scarpe_details = []

# scarpe_details += save(links)

def send_message1(driver, list_contact=None, message1=None):
	driver.get('https://www.linkedin.com/messaging/thread/new/')
	sleep(1)

	contact = driver.find_element_by_xpath("//input[starts-with(@class, 'msg-connections-typeahead__search-field msg-connections-typeahead__search-field--no-recipients ml1 mv1')]")


	if len(list_contact) == 0:
		print('Please enter a contact name')

	elif len(list_contact) == 1:

		contact.send_keys(list_contact[0])
		sleep(1)
		contact.send_keys(Keys.ENTER)
		sleep(1)

	else:

		for cntct in list_contact:
			
			contact.send_keys(cntct)
			sleep(5)
			contact.send_keys(Keys.ENTER)
			sleep(5)

	message = driver.find_element_by_xpath("//div[starts-with(@class, 'msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate')]")
	message.send_keys(message1)
	sleep(0.5)

	send = driver.find_element_by_xpath("//button[starts-with(@class,'msg-form__send-button artdeco-button artdeco-button--1')]")
	send.click()

def greetings(driver, message1='None'):
	'''
	Send greeting message to people connected 24 hour ago
	'''

	driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
	sleep(0.5)

	for i in range(2):
		scroll(driver)
		sleep(0.5)

	people_list = driver.find_elements_by_xpath("//li[starts-with(@class,'mn-connection-card artdeco-list ember-view')]")

	people_dict = {}

	for i, people in enumerate(people_list):
		ago = people.find_element_by_tag_name('time')
		ago = ago.text.split(' ')[:3]

		if ago[2] == 'second' or ago[2] == 'seconds' or ago[2] == 'minute' or ago[2] == 'minutes' or ago[2] == 'hour' or ago[2] == 'hours':

			people_dict[i] = people.get_attribute('id')

	people_idx = people_dict.keys()

	button_list = driver.find_elements_by_xpath("//button[starts-with(@class,'message-anywhere-button artdeco-button artdeco-button--secondary')]")

	for i, button in enumerate(button_list):

		if i in people_idx:

			actions = ActionChains(driver)
			actions.move_to_element(button).perform()


			try:

				button.click()

				sleep(0.5)

				message = driver.find_element_by_xpath("//div[starts-with(@class, 'msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate')]")

				message.send_keys(message1)

				sleep(0.5)

				send = driver.find_element_by_xpath("//button[starts-with(@class,'msg-form__send-button artdeco-button artdeco-button--1')]")

				send.click()

				sleep(0.5)

				print("Succeffuly Send Greeting Message")

			except:

				print("Can`t Send Message request right now")

		else:
			pass

# # Logout of linkedin
# driver.get('https://www.linkedin.com/m/logout/?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_people%3BezDT999kTce8ugkRrUzQLg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_search_srp_people-nav.settings_signout')

# # Exit the driver
# driver.quit()