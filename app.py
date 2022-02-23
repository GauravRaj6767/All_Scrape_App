from functools import partial

import requests
from bs4 import BeautifulSoup
from kivy.app import App

from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep


class TheApp(App):
    pass


class WindowManager(ScreenManager):
    pass


class Start(Screen):
    list_website = []

    def on_checkbox_active(self, instance, value, website):
        if value:
            if website not in self.list_website:
                self.list_website.append(website)
        else:
            if website in self.list_website:
                self.list_website.remove(website)


class FirstScreen(Screen):
    scroll = BooleanProperty(False)
    progress = NumericProperty(0)
    global driver

    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)

    def on_proceed(self, widget, value):
        self.ids.container.clear_widgets()
        self.scroll = True
        info_flip = info_snap = info_amazon = []
        if "amazon" in Start.list_website:
            info_amazon = self.scrapping_amazon(value)
            self.progress += 0.15
        if "flipkart" in Start.list_website:
            info_flip = self.scrapping_flipkart(value)
            self.progress += 0.30
        if "snapdeal" in Start.list_website:
            info_snap = self.scrapping_snapdeal(value)
            self.progress += 0.50

        max_items = max(len(info_flip), len(info_snap), len(info_amazon))
        # print(len(info_flip) + len(info_snap))
        scroll_lay = BoxLayout(spacing=5, orientation='vertical', size=self.size)
        self.ids.container.add_widget(scroll_lay)

        for i in range(max_items):
            try:  # --->> AMAZON
                div = BoxLayout(spacing=15)
                inner_div = BoxLayout(orientation='vertical', spacing=5)
                site_button = Button(text=str(info_amazon[i][0]), size_hint=(0.2, 1), pos_hint={'x': 0.4})
                site_button.bind(on_press=partial(self.opens, (info_amazon[i])))
                inner_div.add_widget(site_button)
                crop_title = info_amazon[i][1]
                t1 = slice(40)
                title = crop_title[t1]
                title_button = Button(text=str(title))
                title_button.bind(on_press=partial(self.opens, (info_amazon[i])))
                inner_div.add_widget(title_button)
                inner_div.add_widget(Label(text='Rs.' + str(info_amazon[i][2])))
                inner_div.add_widget(Label(text='Rating : ' + str(info_amazon[i][3])))
                inner_div.add_widget(Label(text='Total Ratings : ' + str(info_amazon[i][4])))
                img = AsyncImage(source=info_amazon[i][5], pos=self.pos, size=self.size)
                div.add_widget(img)
                div.add_widget(inner_div)
                scroll_lay.add_widget(div)
            except IndexError:
                pass
            try:  # --->> FLIPKART
                div = BoxLayout(spacing=15)
                inner_div = BoxLayout(orientation='vertical', spacing=5)
                site_button = Button(text=str(info_flip[i][0]), size_hint=(0.2, 1), pos_hint={'x': 0.4})
                site_button.bind(on_press=partial(self.opens, (info_flip[i])))
                inner_div.add_widget(site_button)
                crop_title = info_flip[i][1]
                t1 = slice(40)
                title = crop_title[t1]
                title_button = Button(text=str(title))
                title_button.bind(on_press=partial(self.opens, (info_flip[i])))
                inner_div.add_widget(title_button)
                inner_div.add_widget(Label(text=str(info_flip[i][2])))
                inner_div.add_widget(Label(text='Rating : ' + str(info_flip[i][3])))
                inner_div.add_widget(Label(text=' Total Ratings : ' + str(info_flip[i][4])))
                img = AsyncImage(source=info_flip[i][5], pos=self.pos, size=(self.width, self.height))
                div.add_widget(img)
                div.add_widget(inner_div)
                scroll_lay.add_widget(div)
            except IndexError:
                pass
            try:  # --->> SNAPDEAL
                div = BoxLayout(spacing=15)
                inner_div = BoxLayout(orientation='vertical', spacing=5)
                site_button = Button(text=str(info_snap[i][0]), size_hint=(0.2, 1), pos_hint={'x': 0.4})
                site_button.bind(on_press=partial(self.opens, (info_snap[i])))
                inner_div.add_widget(site_button)
                crop_title = info_snap[i][1]
                t1 = slice(40)
                title = crop_title[t1]
                title_button = Button(text=str(title))
                title_button.bind(on_press=partial(self.opens, (info_snap[i])))
                inner_div.add_widget(title_button)
                inner_div.add_widget(Label(text=str(info_snap[i][2])))
                inner_div.add_widget(Label(text=' Total Ratings : ' + str(info_snap[i][3])))
                img = AsyncImage(source=info_snap[i][4], pos=self.pos, size=(self.width, self.height))
                div.add_widget(img)
                div.add_widget(inner_div)
                scroll_lay.add_widget(div)
            except IndexError:
                pass
            if i == max_items - 1:
                self.progress = 1

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
            images_flip = soup.find_all('div', attrs={'class': '_3ywSr_'})

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
                    link = image.div.img['src']
                    product_img_link.append(link)
        except AttributeError:
            pass

        print(product_img_link)

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

            self.progress += 0.025
            try:
                product_info_flipkart.append(('Flipkart', product_title_list[i], product_price_list[i], product_rating_list[i], product_no_rating_list[i], product_img_link[i], product_link[i]))
            except IndexError:
                product_info_flipkart.append(('Flipkart', 'NA'))
            i += 1

        return product_info_flipkart

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

            self.progress += 0.025
            try:
                product_info_snapdeal.append(('Snapdeal', product_title_list[i], product_price_list[i], product_no_rating_list[i], product_img_link[i], product_link_list[i]))
            except IndexError:
                product_info_snapdeal.append(('Snapdeal', 'NA'))

            i += 1

        return product_info_snapdeal

    def scrapping_amazon(self, prod):
        prod_name = prod.replace(' ', '+')
        product_info_amazon = []
        s = Service(r'C:\WebDriver\chromedriver.exe')
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        adriver = webdriver.Chrome(service=s, options=options)
        url = 'https://www.amazon.in/s?k={}'.format(prod_name)
        adriver.get(url)
        sleep(1)
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
                num_rating = products[i].find('span', attrs={'class': 'a-size-base'}).text
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
            self.progress += 0.25

        return product_info_amazon

    def opens(self, li, temp):
        if li[0] == 'Amazon' or li[0] == 'Flipkart':
            img_url = li[5]
            prod_url = li[6]
        else:
            img_url = li[4]
            prod_url = li[5]

        s = Service(r'C:\WebDriver\chromedriver.exe')
        self.driver = webdriver.Chrome(service=s)
        self.driver.get(prod_url)
        self.driver.implicitly_wait(5)

    def remove_all_widgets(self):
        self.ids.container.clear_widgets()
        self.progress = 0


TheApp().run()
