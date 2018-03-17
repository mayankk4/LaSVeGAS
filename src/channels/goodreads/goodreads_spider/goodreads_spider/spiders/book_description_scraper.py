
import scrapy
import re
import unicodedata

# Extracts ~52257 book titles and ids from 525 pages
class BookDescriptionSpider(scrapy.Spider):
    name = "bookdescription"

    def start_requests(self):
        urls = []

        fname = "topbooks/merged_top_books.txt"
        with open(fname) as f:
            content = f.readlines()
        content = [x.strip() for x in content] 

        for book_id in content:
            url = "https://www.goodreads.com/book/show/" + str(book_id)
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('//h1[@class="bookTitle"]/text()').extract_first().strip()
        title = unicodedata.normalize('NFKD', title).encode('ascii','ignore')

        desc_list = response.xpath('//div[@id="description"]/span')
        num_desc = len(desc_list)
        
        desc = ""
        if (num_desc == 0):
            desc = ""
        elif (num_desc == 1):
            desc =  desc_list[0].extract()
        else:
            temp_desc = ""
            for j in range(num_desc):
                temp_desc = desc_list[j].extract()
                if len(temp_desc) > len(desc):
                    desc = temp_desc

        # process the description
        # replace non-utf-8 chars with space
        desc = ''.join([i if ord(i) < 128 else ' ' for i in desc])
        # convert string to utf-8
        desc = unicodedata.normalize('NFKD', desc).encode('ascii','ignore')
        # replace text betewen < > with ' '
        desc = re.sub('<[^>]+>', ' ', desc)
        # replace multiple whitespaces with one
        desc = ' '.join(desc.split())
        
        data = title + ":::::" + desc

        book_id = str(response.url.split('/')[-1].split('.')[0].split('-')[0])
        filename = 'description/book-%s.txt' % book_id
        with open(filename, 'wb') as f:
            f.write("%s\n" % data)
