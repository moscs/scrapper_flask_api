from os import name
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

logging.basicConfig(level=logging.INFO)

def insert_post(post: dict, db, Posts) -> None:
    new_post = Posts(title=post['title'], date=post['date'], author=post['author'], body=post['post_body'])
    db.session.add(new_post)
    db.session.commit()   

def set_chrome_options() -> None:
    """
    Chrome options for headless browser.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('incognito')
    chrome_options.add_argument('log-level=3')
    chrome_prefs = {}
    # chrome_options.experimental_options["prefs"] = chrome_prefs
    # chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def trip_scrapper(db, app, Posts) -> None:
    '''
    Scrap TripAdvisor forums in search of 'Threat' word.
    '''
    db.init_app(app)
    # Drop existing posts
    db.session.query(Posts).delete()
    db.session.commit()
    # Init chromeoptions
    options = set_chrome_options()
 
    # Init chrome webdriver
    logging.info('Starting webdriver')
    driver = webdriver.Chrome(options=options)

    # Load url
    url = 'https://www.tripadvisor.com/ForumHome'
    driver.get(url)

    # Accept privacy policy
    try:
        privacy_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "_evidon-accept-button")))
        privacy_button.click()
    except TimeoutException as timeout:
        logging.exception(timeout)
        pass

    # Search Threat
    search_buttons = driver.find_elements(By.NAME, 'q')

    for button in search_buttons:
        if button.get_attribute('type') == 'text':
            button.send_keys('threat')
            button.send_keys(Keys.ENTER)
            break

    # Get Authors and  date
    try:
        for i in range(5):
            # Get topic row and extract title, user and date
            row = driver.find_elements(By.CLASS_NAME, 'topicrow')[i]
            row_elements = row.find_elements(By.TAG_NAME,  'td')
            title = row_elements[0].text
            author =  row_elements[2].text
            date =  row_elements[3].text
            logging.info(f'Clicking on post {title}')

            # Click on title to go to post and extract body.
            post_link = row.find_element(By.TAG_NAME, 'a').get_attribute('href')
            row.find_element(By.TAG_NAME, 'a').click()

            post_body = driver.find_element(By.CLASS_NAME, 'postBody')

            post = {'title': title,
                    'post_link': post_link,
                    'author': author,
                    'date': date,
                    'post_body': post_body.text}

            insert_post(post, db, Posts)
            # Go back to results page
            driver.back()
        driver.close()
    except Exception as error:
        logging.error(error)
        driver.close()

if __name__ == "__main__":
    trip_scrapper()