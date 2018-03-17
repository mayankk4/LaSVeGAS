pip install Scrapy
Follow: https://doc.scrapy.org/en/latest/intro/tutorial.html


cd src/channels/goodreads/goodreads_spider/
scrapy startproject goodreads_spider
mkdir topbooks
scrapy crawl topbooks

This will generate a dump containing 52k ids of top books
sharded in 500+ files.

Merge into a single file:
cat topbooks/* > merged_top_books.txt
wc -l merged_top_books.txt
mv merged_top_books.txt topbooks/


Extract descriptions
scrapy crawl bookdescription


Debugging:
scrapy shell https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1
