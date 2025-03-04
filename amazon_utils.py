import time
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
import json
from scraper_utils import scrolldown as scrolldown
import numpy as np
import re
import requests
import shutil
import os
from fake_useragent import UserAgent
import urllib


###############
### General ###
###############


def get_amazon_product_id(url):
    if url.startswith('https://www.'):
        url = url.partition('https://www.')[2]
    if url.startswith('http://www.'):
        url = url.partition('http://www.')[2]
    if url.startswith('https://'):
        url = url.partition('https://')[2]
    if url.startswith('http://'):
        url = url.partition('http://')[2]
    if url.startswith('www.'):
        url = url.partition('www.')[2]
    url = url.replace('?', '/')
    url = url.replace(';', '/')
    url = url.replace(')', '/')
    url = url.replace(']', '/')
    url = url.replace('}', '/')
    url = url.replace('#', '/')
    if "/dp/" in url:
        asin = url.split("/dp/")[1].split('/')[0].upper()
    elif "/product/" in url:
        asin = url.split("/product/")[1].split('/')[0].upper()
    elif "/product-reviews/" in url:
        asin = url.split("/product-reviews/")[1].split('/')[0].upper()
    else:
        asin = np.nan
    if isinstance(asin, str):
        asin = asin[:10]
        if len(asin) != 10:
            asin = np.nan
    return asin


def get_amazon_tag_id(url):
    search_str = ''
    if 'tag=' in url:
        search_str = url.partition('tag=')[-1]
        if search_str != '' and '&' in search_str:
            search_str = search_str[:search_str.find('&')]
    search_str = np.nan if search_str == '' else search_str
    return search_str


def normalize_author(name):
    name = name.lower().replace('.', '').replace(',', '').replace(';', '').replace(':', '').replace('!', '').replace('?', '')
    name = re.sub(r'\s+', ' ', name)
    return name


################
### Drission ###
################


def is_captcha(driver):
    try:
        return driver.s_ele('tag=form').attr('action') == '/errors/validateCaptcha'
    except:
        return False


def resolve_capcha(driver, img_path):
    try:
        src = driver.s_ele('tag=form').s_ele('tag=img').attr('src')
        response = requests.get(src, stream=True, headers={'User-Agent': UserAgent().random})
        with open(img_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        time.sleep(0.1)
        captcha = AmazonCaptcha(img_path)
        solution = captcha.solve()
        driver.actions.move_to('#captchacharacters').click().type(solution)
        driver.actions.move_to('tag=button@type=submit').click()
        os.remove(img_path)
        time.wait(5)
    except:
        pass


def load_page(driver, img_path, url, black_list=['503 - Service Unavailable Error']):
    try:
        driver.get(url)
        if driver.title not in black_list:
            i = 0
            while is_captcha(driver) and i < 5:
                resolve_capcha(driver, img_path)
                i += 1
    except:
        pass
    if is_captcha(driver) or driver.title in black_list:
        raise Exception('Captcha')
    return


def get_asin_info(driver, img_path, asin):
    def get_description(driver):
        description = []
        try:
            for div in driver.s_ele('#centerCol').s_eles('tag=div@@class=celwidget'):
                if div.attr('id') in ['productOverview_feature_div', 'bookDescription_feature_div', 'featurebullets_feature_div']:
                    try:
                        text = div.s_ele('@class:a-section').text.strip()
                    except:
                        text = div.text.strip()
                    description.append(text)
        except:
            pass
        description = '\n\n\n'.join(description).strip().strip('\n')
        if description == '':
            return None
        return description

    def get_details(driver):
        details = {}
        try:
            for ul in driver.s_ele('#detailBullets_feature_div').s_eles('tag=ul'):
                for li in ul.s_eles('tag=li'):
                    try:
                        text = li.text.replace('\u200e', '').replace('\u200f', '')
                        details[text.split(':')[0].strip()] = text.split(':')[1].strip().split('\n')
                    except:
                        pass
            return details
        except:
            pass
        try:
            for tr in driver.s_ele('#audibleProductDetails').s_ele('tag=table').s_eles('tag=tr'):
                details[tr.s_ele('tag=th').text] = tr.s_ele('tag=td').text.split('\n')
            return details
        except:
            pass
        try:
            for tr in driver.s_ele('@id:productDetails_detailBullets_sections').s_eles('tag=tr'):
                details[tr.s_ele('tag=th').text] = tr.s_ele('tag=td').text.split('\n')
            return details
        except:
            pass
        return None

    def get_authors(driver):
        def get_data_from_link(url):
            if url.startswith('https://www.'):
                url = url.partition('https://www.')[2]
            if url.startswith('http://www.'):
                url = url.partition('http://www.')[2]
            if url.startswith('https://'):
                url = url.partition('https://')[2]
            if url.startswith('http://'):
                url = url.partition('http://')[2]
            if url.startswith('www.'):
                url = url.partition('www.')[2]
            if "/e/" in url:
                name = url.partition("/e/")[0].split('/')[-1]
                asin = url.partition("/e/")[2].split('/')[0]
            else:
                query = url.split('/')[-1].partition('?')[2]
                items = {}
                for item in query.split('&'):
                    items[item.split('=')[0]] = item.split('=')[1]
                if 'text' in items.keys():
                    name = items['text']
                elif 'field-keywords' in items.keys():
                    name = items['field-keywords']
                elif 'field-author' in items.keys():
                    name = items['field-author']
                elif 'field-artist' in items.keys():
                    name = items['field-artist']
                else:
                    name = None
                    for item in items.keys():
                        if item.startswith('field-'):
                            name = items[item]
                            break
                asin = None
            if name is not None:
                name = name.replace('+', ' ').replace('-', ' ').strip()
                name = re.sub(r'\s+', ' ', name)
            return name, asin
        authors = []
        try:
            for span in driver.s_ele('#bylineInfo').eles('tag=span@@class:author'):
                a = span.s_ele('tag=a')
                name = a.text
                link = a.attr('href')
                role = span.text.partition(a.text)[2]
                role = role[role.find('(')+1:role.find(')')]
                roles = role.split(',')
                if name != '':
                    for role in roles:
                        role = role.strip()
                        name, asin = get_data_from_link(link)
                        authors.append({'name': name, 'role': role, 'asin': asin, 'link': link})
        except:
            pass
        if authors == []:
            try:
                authors = set()
                element = driver.s_ele('#followTheAuthor_feature_div')
                for row in element.s_eles('tag=div@@class:a-row'):
                    for col in row.s_eles('tag=div@@class:a-column'):
                        a = col.s_ele('tag=a')
                        link = a.attr('href')
                        name = a.text
                        if name != 'Follow' and name != '':
                            name, asin = get_data_from_link(link)
                            object = {'name': name, 'role': 'Author', 'asin': asin}
                            object = json.dumps(object)
                            authors.add(object)
                            break
            except:
                pass
        if isinstance(authors, set):
            authors = [json.loads(author) for author in authors]
        if authors == []:
            authors = None
        return authors

    def get_price(driver):
        try:
            for swatchElement in driver.s_ele('#tmmSwatches').s_eles('tag=div@@class:swatchElement'):
                if swatchElement.s_ele('tag=a').attr('href') == 'javascript:void(0)':
                    title = swatchElement.s_ele('@class:slot-title').text.strip()
                    price = swatchElement.s_ele('@class:slot-price').text.strip()
                    try:
                        extraMessage = swatchElement.s_ele('@class:slot-extraMessage').text.strip()
                    except:
                        extraMessage = None
                    return {'title': title, 'price': price, 'extraMessage': extraMessage}
        except:
            pass
        try:
            price = driver.s_ele('#apex_offerDisplay_desktop').s_ele('#corePrice_feature_div').s_ele('@class:a-price')
            symbol = price.s_ele('@class=a-price-symbol').text
            whole = price.s_ele('@class=a-price-whole').text
            fraction = price.s_ele('@class=a-price-fraction').text
            price = f'{symbol}{whole}.{fraction}'.replace(',', '').replace('..', '.')
            return {'title': None, 'price': price, 'extraMessage': None}
        except:
            pass
        try:
            price = driver.s_ele('#corePriceDisplay_desktop_feature_div').s_ele('@class:a-price')
            symbol = price.s_ele('@class=a-price-symbol').text
            whole = price.s_ele('@class=a-price-whole').text
            fraction = price.s_ele('@class=a-price-fraction').text
            price = f'{symbol}{whole}.{fraction}'.replace(',', '').replace('..', '.')
            return {'title': None, 'price': price, 'extraMessage': None}
        except:
            pass
        return None
    
    def get_variants(driver):
        variants = {}
        try:
            for variant in driver.s_ele('@id=centerCol').s_eles('@data-csa-c-item-id'):
                variants[variant.attr('data-csa-c-item-id')] = {"title": variant.attr('title'), "price": variant.s_ele('@class:twisterSwatchPrice').text, "extraMessage": None}
        except:
            pass
        if variants == {}:
            return None
        return variants

    load_page(driver, img_path, f'https://www.amazon.com/dp/{asin}')
    try:
        title = driver.s_ele('#productTitle').text
    except:
        return None
    try:
        category = driver.s_ele('#dp').attr('class').split()[0]
    except:
        category = None
    try:
        subtitle = driver.s_ele('#productSubtitle').text
    except:
        subtitle = None
    try:
        rating = float(driver.s_ele('#acrPopover').attr('title').split()[0])
    except:
        rating = None
    try:
        n_reviews = int(driver.s_ele('#acrCustomerReviewText').text.replace(',', '').split()[0])
    except:
        n_reviews = None
    try:
        wayfinding = driver.s_ele('#wayfinding-breadcrumbs_feature_div').text.split('\n›\n')
    except:
        wayfinding = None
    try:
        banner = driver.s_ele('#bookslegalcompliancebanner_feature_div').text
        banner = None if banner == '' else banner
    except:
        banner = None
    description = get_description(driver)
    authors = get_authors(driver)
    price = get_price(driver)
    details = get_details(driver)
    variants = get_variants(driver)
    data = {
        'title': title,
        'category': category,
        'subtitle': subtitle,
        'rating': rating,
        'n_reviews': n_reviews,
        'wayfinding': wayfinding,
        'description': description,
        'details': details,
        'authors': authors,
        'price': price,
        'banner': banner,
        'variants': variants
    }
    return data


def get_cluster_asin_info(driver, img_path, asin):
    data = {}
    asin = asin.upper()
    load_page(driver, img_path, f'https://www.amazon.com/dp/{asin}')
    try:
        other_asin = [a.attr('href').partition('/dp/')[2].partition('/')[0].upper() for a in driver.s_ele('#tmmSwatches').s_eles('tag=a')]
        other_asin = [a for a in other_asin if a != '']
    except:
        other_asin = []
    other_asin.append(asin)
    for asin in other_asin:
        data[asin] = get_asin_info(driver, img_path, asin)
        if data[asin] is not None and data[asin]['variants'] is not None:
            for variant in data[asin]['variants']:
                data[variant] = data[asin]
    cluster_asin = sorted(list(data.keys()))
    for asin in data.keys():
        if data[asin] is not None:
            data[asin]['cluster_asin'] = cluster_asin
    return data


def get_related_asins_by_author(driver, img_path, name):
    items = ['stripbooks', 'digital-text', 'audible']
    asins = set()
    for item in items:
        page = 1
        while True:
            url = f'https://www.amazon.com/s?i={item}&page={page}&rh=p_27%3A{name.replace(" ", "+")}&s=relevancerank&text={name.replace(" ", "+")}'
            # url = f'https://www.amazon.com/s?k={name.replace(" ", "+")}&i={item}&page={page}'
            load_page(driver, img_path, url, black_list=['503 - Service Unavailable Error', 'Sorry! Something went wrong!'])
            stop = True
            for div in driver.eles('tag=div@@data-cel-widget:search_result'):
                try:
                    if div.attr('data-asin') not in ['', None]:
                        stop = False
                        text = div.s_ele('@data-cy=title-recipe').s_ele('@class=a-row').text
                        if urllib.parse.unquote(normalize_author(name)) in normalize_author(text):
                            asin = div.attr('data-asin').upper()
                            asins.add(asin)
                except:
                    pass
            if stop or page == 1000:
                break
            page += 1
    return list(asins)


################
### Selenium ###
################


def selenium_is_captcha(browser):
    try:
        browser.find_element(By.ID, 'captchacharacters')
    except:
        return False
    return True


def selenium_resolve_capcha(driver, img_path):
    try:
        text_box = driver.find_element(By.ID, 'captchacharacters')
        img = driver.find_element(By.TAG_NAME, 'img')
        button = driver.find_element(By.CLASS_NAME, 'a-button-inner')
        img.screenshot(img_path)
        time.sleep(0.1)
        captcha = AmazonCaptcha(img_path)
        solution = captcha.solve()
        text_box.send_keys(solution)
        button.click()
        os.remove(img_path)
        time.sleep(10)
    except:
        pass


def selenium_load_page(driver, img_path, url):
    try:
        driver.get(url)
        time.sleep(10)
        i = 0
        while selenium_is_captcha(driver) and i < 5:
            selenium_resolve_capcha(driver, img_path)
            i += 1
    except:
        pass
    if selenium_is_captcha(driver):
        raise Exception('Captcha')
    return


def selenium_get_related_asins_by_topic(driver, img_path, asin):
    selenium_load_page(driver, img_path, f'https://www.amazon.com/dp/{asin}')
    try:
        driver.find_element(By.ID, 'productTitle')
    except:
        return None
    scrolldown(driver)
    related_asins = set()
    try:
        for carusel in driver.find_elements(By.CLASS_NAME, 'a-carousel-container'):
            try:
                if carusel.find_element(By.TAG_NAME, 'h2').text == 'Products related to this item':
                    break
            except:
                pass
        driver.execute_script("arguments[0].scrollIntoView();", carusel)
        while True:
            ol = carusel.find_element(By.TAG_NAME, 'ol')
            for li in ol.find_elements(By.TAG_NAME, 'li'):
                asin = li.find_element(By.TAG_NAME, 'div').get_attribute('data-asin')
                related_asins.add(asin)
            if carusel.find_element(By.CLASS_NAME, 'a-carousel-page-current').text == carusel.find_element(By.CLASS_NAME, 'a-carousel-page-max').text:
                break
            carusel.find_element(By.CLASS_NAME, 'a-carousel-goto-nextpage').click()
            time.sleep(5)
    except:
        pass
    related_asins = related_asins - {None}
    return list(related_asins)