def open_stealth_driver(headless=False, maximize=True, options=None):
    from selenium import webdriver
    from selenium_stealth import stealth
    if options is None:
        options = webdriver.ChromeOptions()
        if maximize:
            options.add_argument("start-maximized")
        if headless:
            options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver

def open_stealth_driver_wire(headless=False, maximize=True, options=None):
    from seleniumwire import webdriver
    from selenium_stealth import stealth
    if options is None:
        options = webdriver.ChromeOptions()
        if maximize:
            options.add_argument("start-maximized")
        if headless:
            options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver

def open_drission_driver(headless=False, no_imgs=True, no_audio=True, singleton_tab_obj=False, options=None):
    from DrissionPage import ChromiumOptions
    from DrissionPage import ChromiumPage
    from DrissionPage.common import Settings
    Settings.singleton_tab_obj = singleton_tab_obj
    if options is None:
        options = ChromiumOptions()
        if no_imgs:
            options.no_imgs()
        if no_audio:
            options.mute()
        if headless:
            options.headless()
    driver = ChromiumPage(addr_or_opts=options)
    return driver

def open_firefox_driver(headless=False, maximize=True, options=None):
    from selenium import webdriver
    if options is None:
        options = webdriver.FirefoxOptions()
        if maximize:
            options.add_argument("--start-maximized")
        if headless:
            options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    return driver

def open_firefox_driver_wire(headless=False, maximize=True, options=None):
    from seleniumwire import webdriver
    if options is None:
        options = webdriver.FirefoxOptions()
        if maximize:
            options.add_argument("--start-maximized")
        if headless:
            options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    return driver