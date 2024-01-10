import pdfkit
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

urls = [
    "https://author.today/reader/312385/2881790",
    "https://author.today/reader/312385/2934761",
    "https://author.today/reader/312385/2910242",
    "https://author.today/reader/312385/2881861",
    "https://author.today/reader/312385/2933304",
    "https://author.today/reader/312385/2893735",
    "https://author.today/reader/312385/2890203",
    "https://author.today/reader/312385/2881804",
    "https://author.today/reader/312385/2881804",
    "https://author.today/reader/312385/2915147",
    "https://author.today/reader/312385/2882329",
    "https://author.today/reader/312385/2885146",
    "https://author.today/reader/312385/2928343",
    "https://author.today/reader/312385/2885150",
    "https://author.today/reader/312385/2916465",
    "https://author.today/reader/312385/2881953",
    "https://author.today/reader/312385/2881873",
    "https://author.today/reader/312385/2881907",
    "https://author.today/reader/312385/2917696",
    "https://author.today/reader/312385/2890258",
    "https://author.today/reader/312385/2881835",
    "https://author.today/reader/312385/2938369",
    "https://author.today/reader/312385/2899814",
    "https://author.today/reader/312385/2881892",
    "https://author.today/reader/312385/2900160",
    "https://author.today/reader/312385/2881822",
    "https://author.today/reader/312385/2905735",
    "https://author.today/reader/312385/2926115",
    "https://author.today/reader/312385/2894357",
    "https://author.today/reader/312385/2936784"
]

path_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'  # Обновите путь
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
cookie = "dxnmZsqINwluLr6ETYf9H8g78Ly-StOsAmv7e6JsP74Tk1Hq77PydVeAk-AIaKEP3Fxi-Yp2_nsaX1PAjKWU5ZyRFB2RY3u-ZVwfMwWPck9j0FEhxkltX-9LJJqntPuOIlipsDPPqcSGzQEwwVMYa33nw_1ia8xcwe6LGw-chTEHcFbW-sLAmRl4yq0ryIbgAw-EVU4gsiaq1v7SS1u-yYy5nB98wT1dIPsWByTMdwOkAKULkhg1a3g0VNIZ9a8ytXuH3sfFT1eHloMSRdfwD_r2AjkMz8izQUxwtMIDl6XYEXtvBfub50iUSYc9FzDCqGYlWTWCI4Z2LSR-qj9KuZiBwznLbLqplMCg8Inj7VtoW3q-3jsvBnrwXj1WMxEPcnLq9PPbLlakuCuHtC7wmgEVWzImJbuAANObOgRydShJ8_bgfyICd_1gUuOewE5gjxaby3dTP5WF1x_jTMR_RY8eRUkdN49O4jWuJtAo--aeQkrJ8cjMT9m76oLC9tgqCgdOV6USSnaGxmDk89TEOrDapsYvyndq8bO1YKsrRNZ1wMb4tYthqVs2ECaj0kHHxN80HLfHa37oGcg2JPXK9bK2h1AYE9eLLc8xhjT862bsobAU"
pdfoptions = {
    'encoding': 'UTF-8'
}
string = """<head>
    <link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
        }
    </style>
</head>"""

# Цикл для обработки каждого URL
for i in urls:
    options = uc.ChromeOptions() 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    # Установка Webdriver
    service = Service(ChromeDriverManager().install())
    # Инициализация драйвера с объектами Service и Options
    driver = uc.Chrome(options=options) 
    retry_count = 0
    while retry_count < 5:
        try:
            driver.get(i)
            
            driver.execute_script(f"window.open('{i}', '_blank')")
            time.sleep(2)
            driver.add_cookie({"name": "LoginCookie", "value": cookie, "path": "/"})
            driver.refresh()
            #driver.close()
            #driver.switch_to.window(driver.window_handles[1])
            time.sleep(15)
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "img")))
            time.sleep(10)
            print("МЯУ!")
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            # Найти конкретный элемент, который нужно сохранить
            target_element = soup.find('div', {'class': 'text-container'})

            # Удалить все остальные элементы из soup
            soup = BeautifulSoup(str(target_element), 'html.parser')
            if len(str(soup)) < 100:
                retry_count += 1
                continue
            string += str(soup)
            # Сохранить измененный HTML
            with open('output.html', 'w', encoding='utf-8') as file:
                file.write(string)
                pdfkit.from_file('output.html', 'output.pdf', configuration=config, options=pdfoptions)

        except Exception as e:
            print(f"Произошла ошибка: {e}")

        finally:
            driver.quit()
            time.sleep(3)
            break

pdfkit.from_file('input.html', 'output.pdf', configuration=config, options=pdfoptions) # Конвертация HTML в PDF