import scrapy
import re
from datetime import date

class MoneyplSpider(scrapy.Spider):
    name = 'moneypl'
    allowed_domains = ['money.pl']
    start_urls = ['https://www.money.pl/gielda/spolki-gpw/']   


    def parse(self, response):
        table = response.xpath("//div[contains(@class,'rt-table')]/div[contains(@class,'rt-tbody')]")
        stocks = table.xpath(".//div[contains(@class,'rt-tr-group')]")

        for stock in stocks:
            name_stock = stock.xpath(".//a[contains(@class,'sc-18yizqs-0 sUail')]/div/text()").get()

            link_stock = stock.xpath(".//a[contains(@class,'sc-18yizqs-0 sUail')]/@href").get()
            url_stock = self.modify_url(link_stock)
            absolute_url = response.urljoin(url_stock)

            date_today = '10.05.2021'

            yield {
                'name' : name_stock,
                'URL' : absolute_url,
                'date' : date_today
            }
            #yield Request(url_stock, callback=self.parse_single_stock)

    def modify_url(self,extracted_link):
        modified_url = '';
        if extracted_link != None :
            modified_url = re.sub('^/gielda/spolki-gpw/','',extracted_link) 
            modified_url = re.sub('\.html$','',modified_url)  
            modified_url += ',finanse.html'
        return modified_url 

