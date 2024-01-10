import pdfkit
import time
options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'images': True,
    'no-outline': None
}
path_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
start = time.time()
pdfkit.from_file('output.html', 'output.pdf', options=options, configuration=config)
print(f"Время выполнения: {time.time() - start} секунд")