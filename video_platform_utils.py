import parser_utilities as pu
from selenium.webdriver.common.by import By
import re
import time
import numpy as np
import time
import json
import brotli

def add_https(url):
    # retrieve url
    if url.startswith('http'):
        url = 'https://'+'/'.join(url.split('/')[2:])
    else:
        url = 'https://'+url
    url = url.split(')')[0]
    return url

def get_rumble_channel_url(url, stealth_driver, sleep_time=5):
    if not url.startswith('https://'):
        url = add_https(url)
    # open url
    try:
        stealth_driver.get(url)
    except:
        return None
    time.sleep(sleep_time)
    if stealth_driver.current_url in ['https://rumble.com/our-apps', 'https://rumble.com/videos', 'https://rumble.com/editor-picks', 'https://rumble.com/s/terms', 'https://rumble.com/c', 'https://rumble.com/']:
        return np.nan
    if stealth_driver.current_url.startswith('https://rumble.com/videos?sort='):
        return np.nan
    channel_url = None
    # wrong page
    if channel_url is None:
        try:
            if not stealth_driver.current_url.startswith('https://rumble.com/'):
                channel_url = np.nan
        except:
            pass
    # login page
    if channel_url is None:
        try:
            if stealth_driver.current_url.startswith('https://rumble.com/login.php?next='):
                channel_url = np.nan
        except:
            pass
    # register page
    if channel_url is None:
        try:
            if stealth_driver.current_url.startswith('https://rumble.com/register/'):
                url1 = 'https://rumble.com/c/'+stealth_driver.current_url[29:]
                channel_url = get_rumble_channel_url(url1, stealth_driver)
                if channel_url is None:
                    url2 = 'https://rumble.com/user/'+stealth_driver.current_url[29:]
                    channel_url = get_rumble_channel_url(url2, stealth_driver)
        except:
            pass
    # if is search results page
    if channel_url is None:
        try:
            if stealth_driver.current_url.startswith('https://rumble.com/search/'):
                channel_url = np.nan
        except:
            pass
    # page not found of video not found or private video
    if channel_url is None:
        try:
            if stealth_driver.find_element(By.XPATH, '/html/body/div').text in  ['Video not found']:
                channel_url = np.nan
        except:
            pass
    if channel_url is None:
        try:  
            if stealth_driver.find_element(By.XPATH, '/html/body/main/div/div/h1').text in  ['404 - Not found', '404 - Video is not found', '410 - Video is not found', '410 - Gone', '403 - Private channel']:
                channel_url = np.nan
        except:
            pass
    if channel_url is None:
        try:
            if stealth_driver.find_element(By.XPATH, '/html/body/main/div/h1').text in  ['This video is restricted/private']:
                channel_url = np.nan
        except:
            pass
    # channel or user page
    if channel_url is None:
        try:
            channel_url = stealth_driver.find_element(By.XPATH, '/html/body/main/div/div[3]/div/div[1]/a[1]').get_attribute('href')
        except:
            pass
    # channel or user page without background
    if channel_url is None:
        try:
            channel_url = stealth_driver.find_element(By.XPATH, '/html/body/main/div/div[2]/div/div[1]/a[1]').get_attribute('href')
        except:
            pass
    # embedded video
    if channel_url is None:
        try:
            new_url = stealth_driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/a').get_attribute('href')
            stealth_driver.get(new_url)
            time.sleep(sleep_time)
            channel_url = stealth_driver.find_element(By.XPATH, '/html/body/main/article/div[2]/div/div[1]/div[3]/div[2]/div[1]/a').get_attribute('href')
        except:
            pass
    # embedded video no redirect
    if channel_url is None:
        try:
            if stealth_driver.current_url.startswith('https://rumble.com/embedJS/'):
                url = 'https://rumble.com/embed/'+stealth_driver.current_url[27:]
                stealth_driver.get(url)
                time.sleep(sleep_time)
            if stealth_driver.current_url.startswith('https://rumble.com/embed/'):
                # get scring between script tag from page_source
                html = stealth_driver.page_source
                script = re.findall(r'<script(.+?)</script>', html, re.DOTALL)[-1]
                tmp = script[script.find('"author":')+len('"author":'):]
                tmp = tmp[:tmp.find('}')+1]
                author = json.loads(tmp)
                channel_url = author['url']
        except:
            pass
    # normal video
    if channel_url is None:
        try:
            channel_url = stealth_driver.find_element(By.XPATH, '/html/body/main/article/div[2]/div/div[1]/div[3]/div[2]/div[1]/a').get_attribute('href')
        except:
            pass
    if channel_url is None:
        try:
            channel_url = stealth_driver.find_element(By.XPATH, '/html/body/main/article/div[2]/div/div[1]/div[4]/div[2]/div[1]/a').get_attribute('href')
        except:
            pass
    # add to dataframe
    return channel_url

def get_rumble_channel_info(channel_url, stealth_driver, sleep_time=5):
    def parse_int(string):
        if string is None:
            return None
        integer = float(re.sub(r'[^.\d]', '', string))
        integer = integer * 1000 if 'K' in string else integer
        integer = integer * 1000000 if 'M' in string else integer
        integer = int(integer)
        return integer
    try:
        stealth_driver.get(f'{channel_url}/about')
        rumble_channel_info = {
            'name': None,
            'followers': None,
            'description': {
                'text': None, 
                'links': [],
                'emails': [],
                'addresses': {}
            },
            'social_links': [],
            'join_date': None,
            'video_number': None,
            'locals': {
                'url': None,
                'note': {
                    'text': None, 
                    'links': [], 
                    'emails': [],
                    'addresses': {}
                },
                'community_members': None,
                'posts': None,
                'comments': None,
                'likes': None
            }
        }
        # name
        try:
            rumble_channel_info['name'] = stealth_driver.find_element(By.CLASS_NAME, 'channel-header--title-wrapper').text
        except:
            pass
        # followers
        try:
            text = stealth_driver.find_element(By.CLASS_NAME, 'channel-header--followers').text.split(' ')[0]
            rumble_channel_info['followers'] = parse_int(text)
        except:
            pass
        # description
        try:
            description = []
            for p in stealth_driver.find_element(By.CLASS_NAME, 'channel-about--description').find_elements(By.TAG_NAME, 'p'):
                description.append(p.text)
            description = '\n'.join(description)
            rumble_channel_info['description']['text'] = description
            rumble_channel_info['description']['links'] = pu.get_links(description)
            rumble_channel_info['description']['emails'] = pu.get_emails(description)
            rumble_channel_info['description']['addresses'] = pu.get_addresses(description)
        except:
            pass
        # social links
        try:
            for a in stealth_driver.find_element(By.CLASS_NAME, 'channel-about--socials').find_elements(By.TAG_NAME, 'a'):
                rumble_channel_info['social_links'].append(a.get_attribute('href'))
        except:
            pass
        # join date
        try:
            month = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
            text = stealth_driver.find_element(By.CLASS_NAME, 'channel-about-sidebar').find_elements(By.TAG_NAME, 'p')[0].text.replace('Joined ', '').replace(',', '')
            for key in month.keys():
                text = text.replace(key, month[key])
            month, day, year = text.split(' ')
            rumble_channel_info['join_date'] = f'{year}-{month}-{day.zfill(2)}'
        except:
            pass
        # video number
        try:
            rumble_channel_info['video_number'] = int(stealth_driver.find_element(By.CLASS_NAME, 'channel-about-sidebar').find_elements(By.TAG_NAME, 'p')[1].text.replace(',', '').split(' ')[0])
        except:
            rumble_channel_info['video_number'] = 0
        # locals
        try:
            stealth_driver.find_element(By.CLASS_NAME, 'channel-header--container').find_element(By.CLASS_NAME, 'channel-header--content').find_element(By.CLASS_NAME, 'channel-header--buttons').find_element(By.CLASS_NAME, 'locals-button').click()
            time.sleep(sleep_time)
            rumble_channel_info['locals']['url'] = '/'.join(stealth_driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[2]/a').get_attribute('href').split('/')[:3])
            rumble_channel_info['locals']['note']['text'] = stealth_driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[1]/p').text
            rumble_channel_info['locals']['note']['links'] = pu.get_links(rumble_channel_info['locals']['note']['text'])
            rumble_channel_info['locals']['note']['emails'] = pu.get_emails(rumble_channel_info['locals']['note']['text'])
            rumble_channel_info['locals']['note']['addresses'] = pu.get_addresses(rumble_channel_info['locals']['note']['text'])
            rumble_channel_info['locals']['community_members'] = parse_int(stealth_driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[1]/ul[2]/li[1]/span').text)
            rumble_channel_info['locals']['posts'] = parse_int(stealth_driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[1]/ul[2]/li[3]/span').text)
            rumble_channel_info['locals']['comments'] = parse_int(stealth_driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[1]/ul[2]/li[2]/span').text)
            rumble_channel_info['locals']['likes'] = parse_int(stealth_driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[1]/ul[2]/li[4]/span').text)
        except:
            try:
                stealth_driver.find_element(By.CLASS_NAME, 'overlay').find_element(By.CLASS_NAME, 'overlay-heading').find_element(By.TAG_NAME, 'button').click()
                time.sleep(sleep_time)
                stealth_driver.find_element(By.CLASS_NAME, 'channel-subheader--menu').find_element(By.TAG_NAME, 'a').click()
                time.sleep(sleep_time)
                rumble_channel_info['locals']['url'] = '/'.join(stealth_driver.find_element(By.CLASS_NAME, 'media-locals-message').find_element(By.TAG_NAME, 'a').get_attribute('href').split('/')[:3])
            except:
                pass
        return rumble_channel_info
    except:
        pass
    return None

def get_odysee_channel_url(url, stealth_driver, sleep_time=5):
    if not url.startswith('https://'):
        url = add_https(url)
    if url.startswith('https://odysee.com/') and len(url.split('/')) > 3 and url.split('/')[3].startswith(':'):
        url = 'https://odysee.com/'+'/'.join(url.split('/')[4:])
    # open url
    try:
        stealth_driver.get(url)
    except:
        return None
    time.sleep(sleep_time)
    channel_url = None
    # wrong page
    if channel_url is None:
        try:
            if not stealth_driver.current_url.startswith('https://odysee.com/'):
                channel_url = np.nan
        except:
            pass
    # error page
    if channel_url is None:
        try:
            if stealth_driver.find_element(By.XPATH, '/html/body/pre').text in ['Invalid claim ID %claimId%.', 'Malicious Path', 'No modifier provided after separator #.', 'URL can not include a space']:
                channel_url = np.nan
        except:
            pass
    # page not found of video not found
    if channel_url is None:
        try:
            if stealth_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/main/div/div/div/div/h2').text in ['No Content Found']:
                stealth_driver.get('/'.join(stealth_driver.current_url.split("/")[:4]))
                time.sleep(sleep_time)
        except:
            pass
    # search page
    if channel_url is None:
        try:
            if stealth_driver.current_url.startswith('https://odysee.com/$/search?q='):
                channel_url = np.nan
        except:
            pass
    # playlist page
    if channel_url is None:
        try:
            if stealth_driver.current_url.startswith('https://odysee.com/$/playlist/'):
                channel_url = stealth_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/main/div/div[1]/div[2]/div[1]/div[1]/li/div/div/div[1]/div[1]/a').get_attribute('href')
        except:
            pass
    # page removed
    if channel_url is None:
        try:
            if stealth_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/main/div/section/div/div/div/div/div').text in ['This content violates the terms and conditions of Odysee and has been filtered.']:
                channel_url = np.nan
        except:
            pass
    # page not found of video not found
    if channel_url is None:
        try:
            if stealth_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/main/div/div/div/div/h2').text in ['Channel Not Found', 'No Content Found']:
                channel_url = np.nan
        except:
            pass
    # page not found of video not found
    if channel_url is None:
        try:
            if stealth_driver.find_element(By.XPATH, '/html/body/div/div/div[4]/div[2]/main/div/div/div/div/h2').text in ['No Content Found']:
                channel_url = np.nan
        except:
            pass
    # video embedded
    if channel_url is None:
        try:
            if stealth_driver.current_url.startswith('https://odysee.com/$/embed/'):
                new_url = stealth_driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/a').get_attribute('href')
                stealth_driver.get(new_url)
                time.sleep(sleep_time)
        except:
            pass
    # channel page
    if channel_url is None:
        try:
            stealth_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/main/header/div/div[1]/button[2]').click()
            time.sleep(sleep_time)
            channel_url = stealth_driver.find_element(By.XPATH, '/html/body/div[5]/div/div/section/div/div[2]/fieldset-section/input-submit/input').get_attribute('value')
        except:
            pass
    # normal video
    if channel_url is None:
        try:
            channel_url = stealth_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/main/div[1]/div[2]/section/section[1]/div/div[3]/li/div/div/div[1]/div[1]/a').get_attribute('href')
        except:
            try:
                if stealth_driver.find_element(By.CLASS_NAME, 'card__main-actions').find_element(By.CLASS_NAME, 'claim-preview__title').text == 'Anonymous':
                    channel_url = np.nan
            except:
                try:
                    if stealth_driver.find_element(By.CLASS_NAME, 'card__main-actions').find_element(By.CLASS_NAME, 'claim-preview--inline').text == 'Anonymous':
                        channel_url = np.nan
                except:
                    pass
    # post page (only anonymous)
    if channel_url is None:
        try:
            if stealth_driver.find_element(By.CLASS_NAME, 'post').find_element(By.XPATH, 'span').text == 'Anonymous':
                channel_url = np.nan
        except:
            pass
    # invite page 
    if channel_url is None:
        try:
            if stealth_driver.current_url.startswith('https://odysee.com/$/invite/'):
                channel_url = stealth_driver.find_element(By.XPATH, '/html/body/div/div/div[4]/div/main/section/div/div[2]/li/div/div/div/div[1]/a').get_attribute('href')
        except:
            if stealth_driver.current_url.startswith('https://odysee.com/$/invite/'):
                channel_url = np.nan
    # last resolution
    if channel_url is None:
        try:
            if stealth_driver.current_url.split('/')[3][0] == '@':
                new_url = '/'.join(stealth_driver.current_url.split('/')[:4])
                stealth_driver.get(new_url)
                time.sleep(sleep_time)
                try:
                    stealth_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/main/header/div/div[1]/button[2]').click()
                    time.sleep(sleep_time)
                    channel_url = stealth_driver.find_element(By.XPATH, '/html/body/div[5]/div/div/section/div/div[2]/fieldset-section/input-submit/input').get_attribute('value')
                except:
                    try:
                        channel_url = 'https://odysee.com/' + stealth_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/main/header/div/div[1]/a').get_attribute('href').split('/')[-1]
                    except:
                        pass
        except:
            pass
    # copyrigth page
    if channel_url is None:
        try:
            if stealth_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/main/div/section/div/div[2]/div/a').get_attribute('href') == 'https://help.odysee.tv/copyright/':
                channel_url = np.nan
        except:
            pass
    # Mature content
    if channel_url is None:
        try:
            if stealth_driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/main/div/div/label').text == 'Mature content':
                channel_url = np.nan
        except:
            pass
    # home page
    if channel_url is None:
        try:
            if stealth_driver.current_url in ['https://odysee.com/', 'https://odysee.com/?&sunset=lbrytv']:
                channel_url = np.nan
        except:
            pass
    return channel_url

def get_odysee_channel_info(channel_url, drission_tab, sleep_time=5):
    try:
        odysee_channel_info = {}
        drission_tab.listen.start(['resolve', 'sub_count', 'membership'])
        drission_tab.get(channel_url+'?view=membership')
        for request in drission_tab.listen.steps(timeout=sleep_time):
            if request.response.status == 200 and request.url == 'https://api.odysee.com/subscription/sub_count':
                odysee_channel_info['sub_count'] = request.response.body['data'][0]
            if request.response.status == 200 and request.url == 'https://api.na-backend.odysee.com/api/v1/proxy?m=resolve':
                odysee_channel_info['about'] = list(request.response.body['result'].values())[0]
            if request.response.status == 200 and request.url == 'https://api.odysee.com/membership/list':
                odysee_channel_info['membership'] = request.response.body['data']
            if len(odysee_channel_info) == 3:
                break
        drission_tab.listen.stop()
        if len(odysee_channel_info) == 3:
            odysee_channel_info['about']['sub_count'] = odysee_channel_info['sub_count']
            del odysee_channel_info['sub_count']
            if odysee_channel_info['membership'] is None:
                odysee_channel_info['membership'] = []
            return odysee_channel_info
    except:
        pass
    return None

def get_bitchute_channel_url(url, drission_tab, sleep_time=5):
    if not url.startswith('https://'):
        url = add_https(url)
    # open url
    try:
        drission_tab.get(url, timeout=sleep_time)
    except:
        return None
    drission_tab.timeout = 0
    channel_url = None
    # wrong page
    if channel_url is None:
        try:
            if not drission_tab.url.startswith('https://www.bitchute.com/'):
                channel_url = np.nan
        except:
            pass
    # video embedded 
    if channel_url is None:
        try:
            if drission_tab.url.split('/')[3] == 'embed':
                new_url = drission_tab.ele('tag:head').ele('tag:link').attr('href')
                drission_tab.get(new_url, timeout=sleep_time)
        except:
            pass
    # normal video
    if channel_url is None:
        try:
            channel_url = drission_tab.ele('@class:channel-banner').ele('@class:details').ele('tag:a').attr('href')
            if not channel_url.startswith('https://www.bitchute.com/channel/'):
                channel_url = None
        except:
            pass
    # channel page
    if channel_url is None:
        try:
            script = drission_tab.html
            index = script.find('channelRefreshCounts(')
            if index != -1:
                tmp = script[index+len('channelRefreshCounts('):]
                tmp = tmp[:tmp.find(')')]
                if len(tmp) > 0:
                    channel_url = 'https://www.bitchute.com/channel/'+tmp.split(',')[1].strip()[1:-1]+'/'
        except:
            pass
    # page not found of video not found
    if channel_url is None:
        try:
            if drission_tab.ele('@class:page-title').text in ['404 - Page not found', 'Channel Blocked', 'Channel Restricted', 'Video Blocked']:
                channel_url = np.nan
        except:
            pass
    return channel_url

def get_bitchute_channel_info(channel_url, drission_tab, sleep_time=5):
    return None

def get_youtube_channel_url(url, firefox_driver, sleep_time=2):
    if not url.startswith('https://'):
        url = add_https(url)
    # open url
    if url.startswith('https://apne.ws/'):
        url = 'http://'+url[8:]
    if url in ['https://youtube.com/null', 'https://www.youtube.com/null']:
        return np.nan
    try:
        firefox_driver.get(url)
    except:
        return None
    time.sleep(sleep_time)
    # no title
    try:
        if firefox_driver.find_element(By.XPATH, '/html/head/title').text == '':
            return np.nan
    except:
        return np.nan
    # home page
    if firefox_driver.current_url in ['https://www.youtube.com/', 'https://www.youtube.com/?app=desktop', 'https://www.youtube.com/embed']:
        return np.nan
    # wrong page
    if any([firefox_driver.current_url.startswith(url) for url in ['https://www.youtube.com/kids', 'https://www.youtube.com/howyoutubeworks', 'https://www.youtube.com/t/', 'https://www.youtube.com/intl', 'https://www.youtube.com/oops']]):
        return np.nan
    # wrong page
    if not firefox_driver.current_url.startswith('https://www.youtube.com/'):
        return np.nan
    # server not found
    try:
        if firefox_driver.find_element(By.XPATH, '/html/head/title').text in ['Server Not Found', 'Error 404 (Not Found)!!1', 'Error 400 (Bad Request)!!1', 'Oops']:
            return np.nan
    except:
        pass
    # reject cookies
    try:
        firefox_driver.find_element(By.XPATH, '/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div').click()
        time.sleep(sleep_time)
    except:
        try:
            firefox_driver.find_element(By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/div[1]/form[1]/div/div/button').click()
            time.sleep(sleep_time)
        except:
            pass
    channel_url = None
    # embedded video
    if channel_url is None:
        try:
            if firefox_driver.current_url.startswith('https://www.youtube.com/embed/'):
                firefox_driver.get('https://www.youtube.com/watch?v='+firefox_driver.current_url.split('/')[4])
                time.sleep(sleep_time)
        except:
            pass
    # home page
    if channel_url is None:
        try:
            if firefox_driver.current_url == 'https://www.youtube.com/':
                channel_url = np.nan
        except:
            pass
    # error page
    if channel_url is None:
        try:
            if  firefox_driver.page_source.startswith('<html lang="en" dir="ltr"><head><title>404 Not Found</title>'):
                channel_url = np.nan
        except:
            pass
    # redirect url
    if channel_url is None:
        try:
            if firefox_driver.current_url.startswith('https://www.youtube.com/redirect?'):
                firefox_driver.find_element(By.ID, 'redirect-container')
                channel_url = np.nan
        except:
            pass
    # hashtag page
    if channel_url is None:
        try:
            if firefox_driver.current_url.startswith('https://www.youtube.com/hashtag/'):
                channel_url = np.nan
        except:
            pass
    # results page
    if channel_url is None:
        try:
            if firefox_driver.current_url.startswith('https://www.youtube.com/results?'):
                channel_url = np.nan
        except:
            pass
    # private video or unavailable or removed
    if channel_url is None:
        try:
            reason = firefox_driver.find_element(By.ID, "player-error-message-container").find_element(By.ID, 'info').find_element(By.ID, 'reason').text
            if isinstance(reason, str):
                channel_url = np.nan
        except:
            pass
    # video unavailable
    if channel_url is None:
        try:
            if firefox_driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[4]/ytd-item-section-renderer/div[3]/ytd-background-promo-renderer/div[1]/div').text in ['Video unavailable', "This video isn't available anymore"]:
                channel_url = np.nan
        except:
            pass
    # shorts page
    if channel_url is None:
        try:
            channel_url = firefox_driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[3]/div/ytd-reel-video-renderer[1]/div[4]/ytd-reel-player-overlay-renderer/div[1]/div/reel-player-header-renderer/div[5]/div/ytd-channel-name/div/div/yt-formatted-string/a').get_attribute('href')
            if channel_url.startswith('https://www.youtube.com/channel/'):
                firefox_driver.get(channel_url)
                time.sleep(sleep_time)
                channel_url = None
        except:
            pass
    # playlist page
    if channel_url is None:
        try:
            channel_url = firefox_driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-playlist-header-renderer/div/div[2]/div[1]/div/div[1]/div[1]/div/yt-formatted-string[1]/a').get_attribute('href')
            if channel_url.startswith('https://www.youtube.com/channel/'):
                firefox_driver.get(channel_url)
                time.sleep(sleep_time)
                channel_url = None
        except:
            pass
    # video page
    if channel_url is None:
        try:
            channel_url = firefox_driver.find_element(By.ID, 'watch7-content').find_element(By.XPATH, 'span[1]/link[1]').get_attribute('href')
            if channel_url.startswith('https://www.youtube.com/channel/'):
                firefox_driver.get(channel_url)
                time.sleep(sleep_time)
                channel_url = None
        except:
            try:
                channel_url = firefox_driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[1]/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a').get_attribute('href')
                if channel_url.startswith('https://www.youtube.com/channel/'):
                    firefox_driver.get(channel_url)
                    time.sleep(sleep_time)
                    channel_url = None
            except:
                pass
    # channel page
    if channel_url is None:
        try:
            channel_url = 'https://www.youtube.com/'+firefox_driver.find_element(By.ID, 'channel-handle').text
        except:
            pass
    return channel_url

def get_youtube_channel_info(channel_url, firefox_driver_wire, sleep_time=2):
    def parse_int(string):
        if string is None:
            return None
        integer = float(re.sub(r'[^.\d]', '', string))
        integer = integer * 1000 if 'K' in string else integer
        integer = integer * 1000000 if 'M' in string else integer
        integer = int(integer)
        return integer
    try:
        youtube_channel_info = {
            'description': None,
            'subscriberCount': None,
            'viewCount': None,
            'joinedDate': None,
            'channelId': None,
            'videoCount': None,
            'links': [],
        }
        firefox_driver_wire.get(channel_url)
        time.sleep(sleep_time)
        # reject cookies
        try:
            firefox_driver_wire.find_element(By.XPATH, '/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div').click()
            time.sleep(sleep_time)
        except:
            try:
                firefox_driver_wire.find_element(By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/div[1]/form[1]/div/div/button').click()
                time.sleep(sleep_time)
            except:
                pass
        del firefox_driver_wire.requests
        try:
            firefox_driver_wire.find_element(By.ID, 'channel-tagline').find_element(By.ID, 'content').click()
        except:
            try:
                firefox_driver_wire.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-tabbed-page-header/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div/div/yt-page-header-renderer/yt-page-header-view-model/div/div[1]/div/yt-description-preview-view-model/truncated-text/truncated-text-content/button').click()
            except:
                pass
        start = time.time()
        data = None
        while True:
            for request in firefox_driver_wire.requests:
                if request.response.status_code == 200 and request.url == 'https://www.youtube.com/youtubei/v1/browse?prettyPrint=false':
                    data = brotli.decompress(request.response.body).decode()
                    data = json.loads(data)
                    data = data['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems'][0]['aboutChannelRenderer']['metadata']['aboutChannelViewModel']
                    description = data.get('description', None)
                    if description is not None:
                        youtube_channel_info['description'] = {
                            "text": description,
                            "links": pu.get_links(description),
                            "emails": pu.get_emails(description),
                            "addresses": pu.get_addresses(description)
                        },
                    youtube_channel_info['subscriberCount'] = parse_int(data.get('subscriberCountText', None))
                    youtube_channel_info['viewCount'] = parse_int(data.get('viewCountText', None))
                    try:
                        month = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
                        joinedDate = data['joinedDateText']['content'].replace(',', '').split()[1:]
                        joinedDate = f'{joinedDate[2]}-{month[joinedDate[0]]}-{joinedDate[1].zfill(2)}'
                        youtube_channel_info['joinedDate'] = joinedDate
                    except:
                        youtube_channel_info['joinedDate'] = None
                    youtube_channel_info['channelId'] = data.get('channelId', None)
                    youtube_channel_info['videoCount'] = parse_int(data.get('videoCountText', None))
                    try:
                        for link in data['links']:
                            try:
                                youtube_channel_info['links'].append(link['channelExternalLinkViewModel']['link']['content'])
                            except:
                                pass
                    except:
                        pass
                    break
            if data is not None or time.time() - start > sleep_time:
                break
        return youtube_channel_info
    except:
        pass
    return None