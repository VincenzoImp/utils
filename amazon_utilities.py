from selenium.webdriver.common.by import By
import time
from amazoncaptcha import AmazonCaptcha

def is_captcha(browser):
    """Check if the current page is an amazon captcha page.
    Args:
        browser: Selenium webdriver object.
    Returns:
        bool: True if the page is a captcha page, False otherwise.
    """
    try:
        browser.find_element(By.ID, 'captchacharacters')
    except:
        return False
    return True

def resolve_capcha(browser, img_path):
    """
    Resolve the amazon captcha.
    Args:
        browser: Selenium webdriver object.
        img_path: Path where to save the captcha image.
    """
    try:
        text_box = browser.find_element(By.ID, 'captchacharacters')
        img = browser.find_element(By.TAG_NAME, 'img')
        button = browser.find_element(By.CLASS_NAME, 'a-button-inner')
        img.screenshot(img_path)
        time.sleep(0.1)
        captcha = AmazonCaptcha(img_path)
        solution = captcha.solve()
        text_box.send_keys(solution)
        button.click()
    except:
        pass

def is_product_page(browser):
    """
    Check if the current page is an amazon product page.
    Args:
        browser: Selenium webdriver object.
    Returns:
        bool: True if the page is a product page, False otherwise.
    """
    try:
        browser.find_element(By.ID, 'productTitle')
    except:
        return False
    return True

def load_page(driver, image_path, asin):
    """
    Load the page of the book.
    Args:
        driver: Selenium webdriver object.
        asin: ASIN of the book.
    """
    url = f'https://www.amazon.com/dp/{asin}'
    driver.get(url)
    time.sleep(4)
    i = 0
    while is_captcha(driver) and i < 5:
        resolve_capcha(driver, image_path)
        i += 1
    return 

def get_data(driver):
    """
    Get the data of a book from its amazon page.
    Args:
        driver: Selenium webdriver object.
    Returns:
        dict: Dictionary containing the data of the book.
    """
    def get_description(driver):
        """
        Get the description of the book.
        Args:
            driver: Selenium webdriver object.
        Returns:
            str: Description of the book.
        """
        try:
            driver.find_element(By.ID, 'centerCol').find_element(By.CLASS_NAME, 'a-expander-prompt').click()
            string = driver.find_element(By.ID, 'centerCol').text
            mid = driver.find_element(By.ID, 'centerAttributesColumns').text
            string = string.partition(mid)[2]
            mid = driver.find_element(By.ID, 'richProductInformation_feature_div').text
            string = string.partition(mid)[0]
            string = string.strip()
            mid = driver.find_element(By.ID, 'centerCol').find_element(By.CLASS_NAME, 'a-expander-prompt').text
            description = string[:-len(mid)].strip()
        except:
            description = None
        return description

    def get_details(driver):
        """
        Get the details of the book.
        Args:
            driver: Selenium webdriver object.
        Returns:
            dict: Details of the book.
        """
        try:
            d = {}
            for ul in driver.find_element(By.ID, 'detailBullets_feature_div').find_elements(By.TAG_NAME, 'ul'):
                for li in ul.find_elements(By.TAG_NAME, 'li'):
                    try:
                        d[li.text.split(':')[0].strip()] = li.text.split(':')[1].strip().split('\n')
                    except:
                        pass
        except:
            try:
                d = {}
                for tr in driver.find_element(By.ID, 'audibleProductDetails').find_element(By.TAG_NAME, 'table').find_elements(By.TAG_NAME, 'tr'):
                    d[tr.find_element(By.TAG_NAME, 'th').text] = tr.find_element(By.TAG_NAME, 'td').text.split('\n')
            except:
                d = None
        return d

    def get_authors(driver):
        """
        Get the authors of the book.
        Args:
            driver: Selenium webdriver object.
        Returns:
            list: List of authors of the book.
        """
        try:
            driver.find_element(By.ID, 'bylineInfo').find_element(By.CLASS_NAME, 'more').click()
        except:
            pass
        try:
            authors = []
            for author in driver.find_element(By.ID, 'bylineInfo').find_elements(By.CLASS_NAME, 'author'):
                a = author.find_element(By.TAG_NAME, 'a')
                name = a.text
                link = a.get_attribute('href')
                role = author.text.partition(a.text)[2]
                role = role[role.find('(')+1:role.find(')')]
                authors.append({'name': name, 'role': role, 'link': link})
        except:
            authors = None
        return authors

    def get_price(driver):
        """
        Get the price of the book.
        Args:
            driver: Selenium webdriver object.
        Returns:
            dict: Price of the book.
        """
        try:
            for swatchElement in driver.find_element(By.ID, 'tmmSwatches').find_elements(By.CLASS_NAME, 'swatchElement'):
                if swatchElement.find_element(By.TAG_NAME, 'a').get_attribute('href') == 'javascript:void(0)':
                    title = swatchElement.find_element(By.CLASS_NAME, 'slot-title').text
                    price = swatchElement.find_element(By.CLASS_NAME, 'slot-price').text
                    try:
                        extraMessage = swatchElement.find_element(By.CLASS_NAME, 'slot-extraMessage').text
                    except:
                        extraMessage = None
                    return {'title': title, 'price': price, 'extraMessage': extraMessage}
        except:
            pass
        return None

    def get_banner(driver):
        try:
            banner = driver.find_element(By.ID, 'bookslegalcompliancebanner_feature_div').text
        except:
            banner = None
        return banner
        
    title = driver.find_element(By.ID, 'productTitle').text
    try:
        subtitle = driver.find_element(By.ID, 'productSubtitle').text
    except:
        subtitle = None
    try:
        rating = float(driver.find_element(By.ID, 'acrPopover').text)
    except:
        rating = None
    try:
        n_reviews = int(driver.find_element(By.ID, 'acrCustomerReviewText').text.replace(',', '').split()[0])
    except:
        n_reviews = None
    try:
        wayfinding = driver.find_element(By.ID, 'wayfinding-breadcrumbs_feature_div').text.split('\n›\n')
    except:
        wayfinding = None
    description = get_description(driver)
    details = get_details(driver)
    authors = get_authors(driver)
    price = get_price(driver)
    banner = get_banner(driver)
    banner = None if banner == '' else banner
    data = {
        'title': title,
        'subtitle': subtitle,
        'rating': rating,
        'n_reviews': n_reviews,
        'wayfinding': wayfinding,
        'description': description,
        'details': details,
        'authors': authors,
        'price': price,
        'banner': banner
    }
    return data
    
def get_book_data(driver, image_path, asin):
    """
    Scrape all the asins of the book starting from given asin.
    Args:
        driver: Selenium webdriver object.
        image_path: Path where to save the captcha image.
        asin: ASIN of the book.
    Returns:
        dict: Dictionary containing the data of the book for each asin.
    """
    data = {}
    asin = asin.upper()
    load_page(driver, image_path, asin)
    if is_product_page(driver):
        other_asin = [a.get_attribute('href').partition('/dp/')[2].partition('/')[0].upper() for a in driver.find_element(By.ID, 'tmmSwatches').find_elements(By.TAG_NAME, 'a')]
        other_asin = [a for a in other_asin if a != '']
        data[asin] = get_data(driver)
        for asin in other_asin:
            load_page(driver, image_path, asin)
            if is_product_page(driver):
                data[asin] = get_data(driver)
    return data