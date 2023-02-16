from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup


def scroll_to_bottom(driver):
    x = 0
    old_position = 0
    new_position = None

    while new_position != old_position and x < 10:
        time.sleep(1)

        # Get old scroll position
        old_position = driver.execute_script(
            ("return (window.pageYOffset !== undefined) ?"
             " window.pageYOffset : (document.documentElement ||"
             " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(3)
        driver.execute_script((
            "var scrollingElement = (document.scrollingElement ||"
            " document.body);scrollingElement.scrollTop ="
            " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
            ("return (window.pageYOffset !== undefined) ?"
             " window.pageYOffset : (document.documentElement ||"
             " document.body.parentNode || document.body);"))
        x += 1


class FacebookScraper:
    def __init__(self, url) -> None:
        self.url = url

    def scrape_post(self):
        try:
            links = []
            nb_likes = []
            nb_comments = []
            texts = []
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(self.url)
            scroll_to_bottom(driver)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            section = soup.findAll('div', {'class': '_3drp'})
            for a in section[:100]:
                try:
                    x = a.find('div', attrs={
                               'class': '_52jc _5qc4 _78cz _24u0 _36xo'})
                    post_link = x.find('a')['href']
                    links.append("https://www.facebook.com/"+post_link)

                except:
                    links.append('nan')

                try:
                    like = a.find('span', attrs={'class': 'like_def'})
                    if (len(like) == 0):
                        like = 0
                    nb_likes.append(self.format(like.get_text(
                        strip=True).split(' ')[0]+' likes'))
                except:
                    nb_likes.append(0)

                try:

                    text = a.find('div', {'class': '_5rgt _5nk5 _5msi'})
                    post_text = text.find('p')
                    if (len(post_text) == 0):
                        post_text = " "
                    texts.append(post_text.get_text(strip=True))
                except:
                    texts.append('nan')
                try:

                    comment = a.find('span', attrs={'class': 'cmt_def'})
                    nb_comments.append(self.format(comment.get_text(
                        strip=True).split(' ')[0]+' comments'))

                except:
                    nb_comments.append(0)

                    pass

            return (links, texts, nb_likes, nb_comments)
        except Exception as e:
            print(e)
            return

    @staticmethod
    def format(val):
        return int(val.split(' ')[0])
