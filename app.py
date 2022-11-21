import os
os.environ['KIVY_IMAGE'] = 'pil'
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import partial

import requests
from bs4 import BeautifulSoup
from kivy.clock import mainthread
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.card import MDCard
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import android


class RunningPopup(Popup):
    fpop = None

    def set_pop(self, pwin):
        self.fpop = pwin

    def close(self):
        self.fpop.dismiss()


class ScreenUI(Screen):
    def __init__(self):
        super().__init__()

    list_website = []

    def on_checkbox_active(self, instance, value, website):
        if value:
            if website not in self.list_website:
                self.list_website.append(website)
        else:
            if website in self.list_website:
                self.list_website.remove(website)

        print(self.list_website)


class Search(Screen):
    info_amazon = []
    info_flip = []
    info_snap = []
    info_ajio = []

    def __init__(self):
        super().__init__()

    def opens(self, li, temp):
        if li[0] == 'Amazon' or li[0] == 'Flipkart':
            prod_url = li[6]
        else:
            prod_url = li[5]

        s = Service(r'web_driver\chromedriver.exe')
        global driver
        driver = webdriver.Chrome(service=s)
        driver.get(prod_url)
        driver.implicitly_wait(5)

    def on_proceed(self):
        self.ids.scroll_list.clear_widgets()
        self.pop_up = RunningPopup()
        self.pop_up.open()
        self.info_amazon = self.info_ajio = self.info_snap = self.info_flip = []

        thread2 = threading.Thread(target=self.scrapping_start)
        thread2.start()

    def scrapping_start(self):
        value = self.ids.product.text

        if "amazon" in ScreenUI.list_website:
            self.info_amazon = self.scrapping_amazon(value)
            print(len(self.info_amazon))

        if "flipkart" in ScreenUI.list_website:
            self.info_flip = self.scrapping_flipkart(value)

        if "snapdeal" in ScreenUI.list_website:
            self.info_snap = self.scrapping_snapdeal(value)

        if "ajio" in ScreenUI.list_website:
            self.info_ajio = self.scrapping_ajio(value)

        print("SCRAPED")

        self.display_results(self.info_amazon, self.info_flip, self.info_ajio, self.info_snap)

    @mainthread
    def display_results(self, info_amazon, info_flip, info_ajio, info_snap):
        max_items = max(len(info_amazon), len(info_snap), len(info_ajio), len(info_flip))
        for i in range(max_items):

            try:  # --->> AMAZON
                img_div = BoxLayout()
                img = AsyncImage(source=info_amazon[i][5], pos_hint={'center_x': 0}, size=(self.width, self.height))
                img_div.add_widget(img)
                inner_div = BoxLayout(orientation='vertical')
                crop_title = info_amazon[i][1]
                t1 = slice(18)
                prod_name = crop_title[t1]

                inner_div.add_widget(Label(text=str(info_amazon[i][0]), color=[0, 0, 0, 1]))
                site_button = MDRoundFlatIconButton(text=str(prod_name), text_color='black',
                                                    pos_hint={"center_x": 0.5}, icon='fullscreen')
                site_button.bind(on_press=partial(self.opens, (info_amazon[i])))
                inner_div.add_widget(site_button)
                inner_div.add_widget(Label(text='Rs.' + str(info_amazon[i][2]), color=[0, 0, 0, 1]))
                inner_div.add_widget(Label(text='Rating : ' + str(info_amazon[i][3]), color=[0, 0, 0, 1]))
                inner_div.add_widget(Label(text='Total Ratings : ' + str(info_amazon[i][4]), color=[0, 0, 0, 1]))

                card = MDCard(orientation='horizontal', pos_hint={'center_x': 0.5, 'center_y': 0.7}, size_hint=(.9, None), height=210, md_bg_color=[1, 1, 1, 1])
                card.add_widget(img_div)
                card.add_widget(inner_div)

                self.ids.scroll_list.add_widget(card)

            except IndexError:
                pass

            try:  # --->> SNAPDEAL
                img_div = BoxLayout()
                img = AsyncImage(source=info_snap[i][4], pos_hint={'center_x': 0}, size=(self.width, self.height))
                img_div.add_widget(img)
                inner_div = BoxLayout(orientation='vertical')
                crop_title = info_snap[i][1]
                t1 = slice(18)
                prod_name = crop_title[t1]

                inner_div.add_widget(Label(text=str(info_snap[i][0]), color=[0, 0, 0, 1]))
                site_button = MDRoundFlatIconButton(text=str(prod_name), text_color='black',
                                                    pos_hint={"center_x": 0.5}, icon='fullscreen')
                site_button.bind(on_press=partial(self.opens, (info_snap[i])))
                inner_div.add_widget(site_button)
                inner_div.add_widget(Label(text=info_snap[i][2], color=[0, 0, 0, 1]))
                inner_div.add_widget(Label(text=' Total Ratings : ' + str(info_snap[i][3]), color=[0, 0, 0, 1]))

                card = MDCard(orientation='horizontal', pos_hint={'center_x': 0.5, 'center_y': 0.7}, size_hint=(.9, None), height=210, md_bg_color=[1, 1, 1, 1] )
                card.add_widget(img_div)
                card.add_widget(inner_div)
                self.ids.scroll_list.add_widget(card)

            except IndexError:
                pass

            try:  # --->> FLIPKART
                img_div = BoxLayout()
                img = AsyncImage(source=info_flip[i][5], pos_hint={'center_x': 0}, size=(self.width, self.height))
                img_div.add_widget(img)
                inner_div = BoxLayout(orientation='vertical')
                crop_title = info_flip[i][1]
                t1 = slice(18)
                prod_name = crop_title[t1]

                inner_div.add_widget(Label(text=str(info_flip[i][0]), color=[0, 0, 0, 1]))
                site_button = MDRoundFlatIconButton(text=str(prod_name), text_color='black',
                                                           pos_hint={"center_x": 0.5}, icon='fullscreen')
                site_button.bind(on_press=partial(self.opens, (info_flip[i])))
                inner_div.add_widget(site_button)
                inner_div.add_widget(Label(text=info_flip[i][2], color=[0, 0, 0, 1]))
                inner_div.add_widget(Label(text=' Total Ratings : ' + str(info_flip[i][3]), color=[0, 0, 0, 1]))

                card = MDCard(orientation='horizontal', pos_hint={'center_x': 0.5, 'center_y': 0.7},size_hint=(.9, None), height=210, md_bg_color=[1, 1, 1, 1])
                card.add_widget(img_div)
                card.add_widget(inner_div)
                self.ids.scroll_list.add_widget(card)

            except IndexError:
                pass

            try:  # --->> AJIO
                img_div = BoxLayout()
                img = AsyncImage(source=info_ajio[i][4], pos_hint={'center_x': 0}, size=(self.width, self.height))
                img_div.add_widget(img)
                inner_div = BoxLayout(orientation='vertical')

                crop_title = info_ajio[i][1]
                t1 = slice(18)

                if crop_title == None:
                    continue
                else:
                    prod_name = crop_title[t1]

                inner_div.add_widget(Label(text=str(info_ajio[i][0]), color=[0, 0, 0, 1]))
                inner_div.add_widget(MDRoundFlatIconButton(text=str(prod_name), text_color='black',
                                                           pos_hint={"center_x": 0.5}, icon='fullscreen'))
                inner_div.add_widget(Label(text=info_ajio[i][2], color=[0, 0, 0, 1]))
                inner_div.add_widget(Label(text=' Total Ratings : ' + str(info_ajio[i][3]), color=[0, 0, 0, 1]))

                card = MDCard(orientation='horizontal', pos_hint={'center_x': 0.5, 'center_y': 0.7}, size_hint=(.9, None), height=210, md_bg_color=[1, 1, 1, 1])
                card.add_widget(img_div)
                card.add_widget(inner_div)
                self.ids.scroll_list.add_widget(card)

            except IndexError:
                pass

        print("DISPLAYED")
        self.pop_up.dismiss()

    def scrapping_snapdeal(self, prod):
        prod.replace(' ', '%20')
        url = 'https://www.snapdeal.com/search?keyword={}&santizedKeyword=&catId=0&categoryId=0&suggested=false&vertical=p&noOfResults=20&searchState=&clickSrc=go_header&lastKeyword=&prodCatId=&changeBackToAll=false&foundInAll=false&categoryIdSearched=&cityPageUrl=&categoryUrl=&url=&utmContent=&dealDetail=&sort=rlvncy'.format(prod)
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        product_title_list = []
        product_price_list = []
        product_no_rating_list = []
        product_info_snapdeal = []
        product_img_link = []
        product_link_list = []
        products = soup.find_all('div', class_='product-desc-rating')
        i = int(0)
        images_snap = soup.find_all('picture', attrs={'class': 'picture-elem'})

        try:
            for image in images_snap:
                link = image.find('source')['srcset']
                product_img_link.append(link)
        except AttributeError:
            pass

        for product in products:
            try:
                product_title_list.append(product.find('p', class_='product-title').text)
            except AttributeError:
                product_title_list.append('NA')
            try:
                product_price_list.append(product.find('span', class_='lfloat product-price').text)
            except AttributeError:
                product_price_list.append('NA')
            try:
                product_no_rating_list.append(product.find('p', class_='product-rating-count').text)
            except AttributeError:
                product_no_rating_list.append('NA')
            try:
                product_link_list.append(product.a['href'])
            except AttributeError:
                product_link_list.append('NA')

            try:
                product_info_snapdeal.append(('Snapdeal', product_title_list[i], product_price_list[i], product_no_rating_list[i], product_img_link[i], product_link_list[i]))
            except IndexError:
                product_info_snapdeal.append(('Snapdeal', 'NA'))

            i += 1

        return product_info_snapdeal

    def scrapping_flipkart(self, prod):
        prod_name = prod.replace(' ', '%20')
        url = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'.format(prod_name)
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        products = soup.find_all('div', attrs={'class': '_4ddWXP'})
        if products:
            scrape = 1
            product_links_all = soup.find_all('a', attrs={'class': 's1Q9rs'})
        else:
            products = soup.find_all('div', attrs={'class': '_2B099V'})
            scrape = 2
            product_links_all = soup.find_all('a', attrs={'class': '_2UzuFa'})
            if products:
                pass
            else:
                products = soup.find_all('div', attrs={'class': '_3pLy-c row'})
                scrape = 3
                product_links_all = soup.find_all('a', attrs={'class': '_1fQZEK'})

        images_flip = soup.find_all('img', attrs={'class': '_396cs4 _3exPp9'})
        if images_flip:
            x = 0
        else:
            x = 1
            images_flip = soup.find_all('img', attrs={'class': '_2r_T1I'})

        product_title_list = []
        product_img_link = []
        product_link = []
        product_price_list = []
        product_rating_list = []
        product_no_rating_list = []
        product_info_flipkart = []

        for p in product_links_all:
            plink = 'https://www.flipkart.com' + p['href']
            product_link.append(plink)
        i = int(0)
        try:
            if x == 0:
                for image in images_flip:
                    link = image['src']
                    product_img_link.append(link)
            else:
                for image in images_flip:
                    link = image['src']
                    product_img_link.append(link)
        except AttributeError:
            pass

        for product in products:
            try:
                if scrape == 1:
                    title = product.find('a', attrs={'class': 's1Q9rs'})['title']
                    product_title_list.append(title)
                elif scrape == 2:
                    title = product.find('a', attrs={'class': 'IRpwTa'})['title']
                    product_title_list.append(title)
                else:
                    title = product.find('div', attrs={'class': '_4rR01T'}).text
                    product_title_list.append(title)
            except AttributeError:
                product_title_list.append("NA")

            try:
                if scrape == 1:
                    price = product.find('a', attrs={'class': '_8VNy32'}).div.div.text
                    product_price_list.append(price)
                elif scrape == 2:
                    price = product.find('a', attrs={'class': '_3bPFwb'}).div.div.text
                    product_price_list.append(price)
                else:
                    price = product.find('div', attrs={'class': 'col col-5-12 nlI3QM'}).div.div.div.text
                    product_price_list.append(price)
            except AttributeError:
                product_price_list.append('NA')

            try:
                if scrape == 1:
                    rating = product.find('div', attrs={'class': 'gUuXy- _2D5lwg'}).span.div.text
                    product_rating_list.append(rating)
                elif scrape == 2:
                    product_rating_list.append("NA")
                else:
                    r = product.find('div', attrs={'class': 'col col-7-12'})
                    rating = r.find('div', attrs={'class': 'gUuXy-'}).span.div.text
                    product_rating_list.append(rating)
            except AttributeError:
                product_rating_list.append('NA')

            try:
                if scrape == 1:
                    rating = product.find('div', attrs={'class': 'gUuXy- _2D5lwg'})
                    nrating = rating.find('span', attrs={'class': '_2_R_DZ'}).text
                    product_no_rating_list.append(nrating)
                elif scrape == 2:
                    product_no_rating_list.append("No Rating")
                else:
                    r = product.find('div', attrs={'class': 'col col-7-12'})
                    nrating = r.find('span', attrs={'class': '_2_R_DZ'}).span.span.text
                    product_no_rating_list.append(nrating)
            except AttributeError:
                product_no_rating_list.append('NA')

            try:
                product_info_flipkart.append(('Flipkart', product_title_list[i], product_price_list[i], product_rating_list[i], product_no_rating_list[i], product_img_link[i], product_link[i]))
            except IndexError:
                product_info_flipkart.append(('Flipkart', 'NA'))
            i += 1

        return product_info_flipkart

    def scrapping_ajio(self, prod):
        product_info_ajio = []
        prod = prod.replace(' ', '%20')
        if 'small' in prod:
            prod = prod.replace('small', '')
        if 'big' in prod:
            prod = prod.replace('big', '')
        if 'short' in prod:
            prod = prod.replace('short', '')
        if 'large' in prod:
            prod = prod.replace('large', '')
        if 'medium' in prod:
            prod = prod.replace('medium', '')
        if 'tall' in prod:
            prod = prod.replace('tall', '')
        url = 'https://www.ajio.com/api/search?fields=SITE&currentPage=0&pageSize=50&format=json&query={}%3Arelevance&sortBy=relevance&text={}&customerType=Existing&gridColumns=3&advfilter=true&platform=Desktop'.format(prod, prod)
        p_url = 'https://www.ajio.com/api/p/{}'
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        response = requests.session().get(url, headers=headers).json()
        try:
            products = response['products']
            urls = []
            titles = []
            images_url = []
            price_list = []

            for product in products:
                urls.append(p_url.format(product['fnlColorVariantData']['colorGroup']))

            def info_ajio(link):
                item = requests.session().get(link, headers=headers).json()
                try:
                    t = item["baseOptions"][0]["options"][0]["modelImage"]["altText"]
                except:
                    t = None
                try:
                    img_url = item['baseOptions'][0]['options'][0]['modelImage']['url']
                except:
                    img_url = None
                try:
                    price = item['baseOptions'][0]['options'][0]['priceData']['formattedValue']
                except:
                    price = None

                titles.append(t)
                images_url.append(img_url)
                price_list.append(price)
                product_info_ajio.append(('Ajio', t, price, '--', img_url))

            with ThreadPoolExecutor() as executor:
                executor.map(info_ajio, urls)

            return product_info_ajio
        except:
            product_info_ajio = []
            return product_info_ajio

    def scrapping_amazon(self, prod):
        prod_name = prod.replace(' ', '+')
        product_info_amazon = []
        s = Service(r'web_driver\chromedriver.exe')
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        adriver = webdriver.Chrome(service=s, options=options)
        url = 'https://www.amazon.in/s?k={}'.format(prod_name)
        adriver.get(url)
        soup = BeautifulSoup(adriver.page_source, 'html.parser')

        adriver.close()
        products = soup.find_all('div', attrs={'data-component-type': 's-search-result'})
        for i in range(len(products)):
            title = products[i].find('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).span.text
            try:
                price = products[i].find('span', attrs={'class': 'a-price-whole'}).text
            except AttributeError:
                price = "NA"
            try:
                rating = products[i].find('span', attrs={'class': 'a-icon-alt'}).text
            except AttributeError:
                rating = "NA"
            try:
                num_rating = products[i].find('span', attrs={'class': 'a-size-base s-underline-text'}).text
            except AttributeError:
                num_rating = "NA"
            try:
                img_link = products[i].find('img', attrs={'class': 's-image'})['src']
            except AttributeError:
                img_link = "NA"
            try:
                prod_link = 'https://www.amazon.in' + products[i].find('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
            except AttributeError:
                prod_link = "NA"
            product_info_amazon.append(('Amazon', title, price, rating, num_rating, img_link, prod_link))

        return product_info_amazon


class ScrapeApp(MDApp):
    def build(self):
        Builder.load_file("app.kv")
        self.theme_cls.theme_style = "Dark"
        sm = Factory.ScreenManager()
        sm.add_widget(ScreenUI())
        sm.add_widget(Search())
        return sm


ScrapeApp().run()

