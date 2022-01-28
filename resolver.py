import time
import cv2
import base64
from selenium_stealth import stealth
from selenium.webdriver import ActionChains
from seleniumwire import webdriver
import urllib
import selenium

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(r"user-data-dir=C:\Users\Knyz_\source\repos\lolz_auto\User Data")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(
    options=chrome_options,
)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.get('https://lolz.guru/forums/contests/')


def findPuzzle(big, small):
    img = cv2.imread(big, 0)
    img2 = img.copy()
    template = cv2.imread(small, 0)
    w, h = template.shape[::-1]
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    for meth in methods:
        img = img2.copy()
        method = eval(meth)
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    return top_left[0]


def capcha(URL):
    driver.get(URL)
    driver.implicitly_wait(5)
    photo_big = driver.find_element_by_css_selector('div.captchaBlock > div > div> img').get_attribute('src')
    photo_small = driver.find_element_by_css_selector('div.captchaBlock > div > div> img:nth-child(2)').get_attribute(
        'src')

    def get_file_content_chrome(driver, uri):
        result = driver.execute_async_script("""
        var uri = arguments[0];
        var callback = arguments[1];
        var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';
        xhr.onload = function(){ callback(toBase64(xhr.response)) };
        xhr.onerror = function(){ callback(xhr.status) };
        xhr.open('GET', uri);
        xhr.send();
        """, uri)
        if type(result) == int:
            raise Exception("Request failed with status %s" % result)
        return base64.b64decode(result)

    with open('1.png', 'wb') as binary_file:
        binary_file.write(get_file_content_chrome(driver, photo_big))

    with open('2.png', 'wb') as binary_file:
        binary_file.write(get_file_content_chrome(driver, photo_small))

    x = findPuzzle("1.png", '2.png')
    slider = driver.find_element_by_css_selector('div.captchaBlock svg')
    elem = driver.find_element_by_xpath("//span[contains(.,'Проведите...')]")
    ActionChains(driver).move_to_element_with_offset(elem, 1, 1).pause(0.1).move_to_element_with_offset(elem, 2,
                                                                                                        1).pause(
        0.1).move_to_element_with_offset(elem, 3, 1).pause(0.1).move_to_element_with_offset(elem, 4, 1).pause(
        0.1).move_to_element_with_offset(elem, 5, 1).pause(0.1).perform()
    ActionChains(driver).move_to_element_with_offset(elem, 6, 2).pause(0.1).move_to_element_with_offset(elem, 7,
                                                                                                        2).pause(
        0.1).move_to_element_with_offset(elem, 8, 3).pause(0.1).move_to_element_with_offset(elem, 9, 3).pause(
        0.1).move_to_element_with_offset(elem, 10, 2).pause(0.1).perform()
    ActionChains(driver).move_to_element_with_offset(elem, 11, 2).pause(0.1).move_to_element_with_offset(elem, 12,
                                                                                                         2).pause(
        0.1).move_to_element_with_offset(elem, 13, 3).pause(0.1).move_to_element_with_offset(elem, 14, 3).pause(
        0.1).move_to_element_with_offset(elem, 15, 2).pause(0.1).perform()

    ActionChains(driver).move_to_element(elem).click_and_hold(slider).move_by_offset(xoffset=x / 4, yoffset=2).pause(
        0.2).move_by_offset(xoffset=x / 4, yoffset=0).pause(0.2).move_by_offset(xoffset=x / 4, yoffset=1).pause(
        0.2).move_by_offset(xoffset=x / 4, yoffset=2).pause(0.2).release().perform()


driver.get('https://lolz.guru/forums/contests/')
time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)
urls = []
for i in driver.find_elements_by_css_selector('div.discussionListItem:not([class="unread"]) > div > a'):
    urls += [i.get_attribute('href')]

driver.set_page_load_timeout(20)
i = 1
lens = len(urls)
for url in urls:
    try:

        capcha(url)
        print(f'{i}/{lens} | GOOD')
        i += 1
    except:
        print(f'{i}/{lens} | BAD')
        i += 1
driver.quit()