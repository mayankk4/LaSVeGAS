"""

Script will download all the contents and titles and dump the data into a file

"""
import sys
from datetime import datetime
from datetime import timedelta
import urllib2
import json
import traceback


BLACKLIST_WIKI_ARTICLES_LIST = [
    'Main_Page', 'Special:Search', '404.php', 'Special:RecentChanges', 'Special:CreateAccount', 'Special:Book', 'XXX', 'Special:Watchlist', 'Special:MobileMenu', 'Special:CiteThisPage', 'Wikipedia', 'Special:ListUsers', 'Special:BlockList', 'Portal:Contents', 'Special:MobileOptions', 'Wiki', 'Wikipedia:About', 'Portal:Featured_content', '.xxx', 'Special:NewPagesFeed',
                                'Help:Contents', 'Wikipedia:General_disclaimer', 'Category:All_articles_with_unsourced_statements', "Wikipedia:Today's_featured_article/July_3,_2015", 'Wikipedia:Selected_anniversaries/July', 'Special:RecentChangesLinked', 'Special:Log', 'Special:GlobalUsage', 'Special:Export', "Wikipedia:Today's_featured_article/July_23,_2015", 'User:GoogleAnalitycsRoman/google-api', 'Special:LinkSearch']

WIKI_GET_TOP_ARTICLE_URL_API = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/$$PROJECT/$$ACCESS/$$YEAR/$$MONTH/$$DAY"

WIKI_GET_DESCRIPTION_BY_TITLE_API = "https://en.wikipedia.org/w/api.php?format=json&action=query&generator=search&gsrnamespace=0&gsrsearch=$$TITLE&gsrlimit=$$SERCH_LIMIT&prop=pageimages%7Cextracts&pilimit=max&exintro&explaintext&exsentences=$$SENTENCE_LIMIT&exlimit=max"

TITLE_DESCRIPTION_MAX_CHAR_LENGTH = 330
SEARCH_LIMIT = 1

'''
	Method returns day, month and year of the given date
'''


def parseDate(date):
    return date.strftime("%d"), date.strftime("%m"), date.strftime("%Y")


'''
	get top 1k titles
'''


def GetTopArticles(year, month, day, access='all-access', project='en.wikipedia.org'):
    url = WIKI_GET_TOP_ARTICLE_URL_API.replace("$$PROJECT", project).replace(
        "$$ACCESS", access).replace("$$YEAR", year).replace("$$MONTH", month).replace("$$DAY", day)
    # print url
    titles = []
    data = ""
    try:
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        for o in data['items']:
            for article in o['articles']:
                titles.append(article['article'].encode('utf-8'))
        return titles
    except:
        print "Error fetching url: " + str(url)
    return titles


'''
	method returns a dictionary for all the titles and their description, imageurl
'''


def ExtractDetailedDescriptionByTitle(title, sentence_limit=3, search_limit=1):
    detailedTitlesInfo = []
    url = WIKI_GET_DESCRIPTION_BY_TITLE_API.replace("$$SENTENCE_LIMIT", str(
        sentence_limit)).replace("$$SERCH_LIMIT", str(search_limit)).replace("$$TITLE", title)
    print url
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    for k, v in data['query']['pages'].items():
        if 'extract' in v:
            d = {}
            d['title'] = v['title'].encode('utf-8')
            d['desc'] = v['extract'].encode(
                'utf-8').replace("\n", "").replace("\t", "")
            detailedTitlesInfo.append(d)
    return detailedTitlesInfo


'''
	method filter duplicates and blacklist titles
'''


def FilterTitles(titles, allTitles, exclude_blacklist_titles):
    filteredTitles = []
    if exclude_blacklist_titles:
        filteredTitles = [
            x for x in titles if x not in BLACKLIST_WIKI_ARTICLES_LIST]
    newFilteredTitles = [x for x in filteredTitles if x not in allTitles]
    return newFilteredTitles


'''
	dump the titles and description into a tile/mysql
'''


def DumpTitles(titles):
    target = open(TITLE_FILE, 'w')
    for t in titles:
        target.write(str(t) + '\n')


'''
	for date in range get top articles and dump the data
'''


def AllTitlesByRange(startDate, endDate, hop, exclude_blacklist_titles=True):
    start = datetime.strptime(startDate, "%Y-%m-%d")
    stop = datetime.strptime(endDate, "%Y-%m-%d")
    allTitles = []
    while start < stop:
        start = start + timedelta(days=hop)
        day, month, year = parseDate(start)
        titles = GetTopArticles(year, month, day)
        print "\t" + str(len(titles))
        filteredTitles = FilterTitles(
            titles, allTitles, exclude_blacklist_titles)
        allTitles.extend(filteredTitles)
        print len(allTitles)
    DumpTitles(allTitles)


'''
Checks if description of title is under allowed limit

'''


def IsDescriptionUnderAllowedCharLimit(titleDetailedInfo):
    for d in titleDetailedInfo:
        if 'desc' in d:
            if len(d['desc']) > TITLE_DESCRIPTION_MAX_CHAR_LENGTH:
                return False
    return True


'''

	generate detailed titles info, currently only supports search_limit as 1

'''


def GenerateDetailedTitlesInfo():
    count = 1
    print OUTPUT_FILE
    target = open(OUTPUT_FILE, 'w')
    with open(TITLE_FILE) as f:

        titles = f.read().splitlines()
        for title in titles:
            sentence_limit = 3
            print str(count)
            try:
                titleDetailedInfo = ExtractDetailedDescriptionByTitle(
                    title, sentence_limit, SEARCH_LIMIT)

                while not IsDescriptionUnderAllowedCharLimit(titleDetailedInfo) and sentence_limit >= 1:
                    print "Refetching with sentence_limit: " + str(sentence_limit)
                    sentence_limit = sentence_limit - 1
                    titleDetailedInfo = ExtractDetailedDescriptionByTitle(
                        title, sentence_limit, SEARCH_LIMIT)

                for d in titleDetailedInfo:
                    if len(d['desc']) < TITLE_DESCRIPTION_MAX_CHAR_LENGTH and len(d['desc']) > 0:
                        target.write(str(d['title']) +
                                     "\t" + str(d['desc']) + '\n')
                        target.flush()
                    else:
                        print "Skipping title length issue, length: " + str(len(d['desc']))
            except Exception, err:
                print "Error in procssing"
                print(traceback.format_exc())
            count = count + 1

 # __main() ###########
TITLE_FILE = str(sys.argv[1])
OUTPUT_FILE = str(sys.argv[2])
start_date = "2015-07-01"
stop_date = "2017-02-02"
hop = 1
# AllTitlesByRange(start_date, stop_date, hop)
GenerateDetailedTitlesInfo()
