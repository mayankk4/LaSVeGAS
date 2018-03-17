
import scrapy


# Extracts ~52257 book titles and ids from 525 pages
class TopBooksSpider(scrapy.Spider):
    name = "topbooks"

    def start_requests(self):
        urls = []
        for i in range(1, 526):
            url = "https://www.goodreads.com/list/show/1.Best_Books_Ever?page=" + str(i)
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        book_ids = []
        book_titles = response.css(".bookTitle")
        for title in book_titles:
            book_title = str(title.css("a::attr(href)").extract_first().split('/')[-1])
            book_id = str(book_title.split('.')[0].split('-')[0])
            book_ids.append(book_id)

        print len(book_ids)

        page_id = str(response.url.split('=')[-1])
        filename = 'topbooks/top-books-%s.txt' % page_id
        with open(filename, 'wb') as f:
            for item in book_ids:
                f.write("%s\n" % item)
