
import scrapy
import re
import unicodedata

# Extracts ~52257 book titles and ids from 525 pages
class BookDescriptionSpider(scrapy.Spider):
    name = "bookdescription"

    def start_requests(self):
        urls = []

        fname = "topbooks/top-books-test.txt"
        with open(fname) as f:
            content = f.readlines()
        content = [x.strip() for x in content] 

        for book_id in content:
            url = "https://www.goodreads.com/book/show/" + str(book_id)
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print response.url

        title = response.xpath('//h1[@class="bookTitle"]/text()').extract_first().strip()

        desc_list = response.xpath('//div[@id="description"]/span')
        num_desc = len(desc_list)
        
        desc = ""
        if (num_desc == 0):
            desc = ""
        elif (num_desc == 1):
            desc =  response.xpath('//div[@id="description"]/span')[0].extract()
            unicodedata.normalize('NFKD', desc).encode('ascii','ignore')
            desc = re.sub('<[^>]+>', '', desc)
        else:
            temp_desc = ""
            for j in range(num_desc):
                temp_desc = response.xpath('//div[@id="description"]/span')[j].extract()
                unicodedata.normalize('NFKD', temp_desc).encode('ascii','ignore')
                temp_desc = re.sub('<[^>]+>', '', temp_desc)
                if len(temp_desc) > len(desc):
                    desc = temp_desc

        print "==============================================================="
        print title + ":::::" + desc
        print "==============================================================="
