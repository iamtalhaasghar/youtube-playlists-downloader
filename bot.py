class InvidiousBot:

    def __init__(self):
        pass

    def __getFirefoxDriver(self):
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options

        options = Options()
        #options.headless = True
        #geckoDriver = '/home/talha/Programs/geckodriver'
        browser = webdriver.Chrome()
        #browser = webdriver.Firefox(options=options, executable_path=geckoDriver)
        
        return browser

    def scrapVideosOfChannel(self, channelId, alreadyScrapedVideoList=None):
        from bs4 import BeautifulSoup as Soup
        from datetime import date
        browser = self.__getFirefoxDriver()
        channelUrl = 'https://invidious.snopyta.org/channel/%s' % channelId
        isThereNextPage = True
        alreadyScraped = False
        pageNumber = 1
        scrapedVideos = list()
        while not alreadyScraped and isThereNextPage:
            print(channelUrl, pageNumber)
            browser.get('%s?page=%d' % (channelUrl, pageNumber))
            videoDivs = browser.find_elements_by_xpath('//h5/parent::div')
            index = 0
            while not alreadyScraped and index < len(videoDivs):
                div = videoDivs[index]
                index += 1
                divHtml = div.get_attribute('innerHTML')
                soup = Soup(divHtml, 'lxml')
                text = soup.text
                href = soup.a.get('href')
                videoId = href.split('=')[1]
                tempData = list()  # [length, title, channel, date, views]
                for i in text.splitlines():
                    i = i.strip()
                    if len(i) != 0:
                        tempData.append(i)
                if('Premieres' in tempData[2]):
                    tempData.insert(0,'00:00')
                videoData = {
                    'length': tempData[0],
                    'title': tempData[1],
                    'channel': tempData[2],
                    'upload_date': tempData[3],
                    'views': tempData[4],
                    'video_id': videoId,
                    'channel_id': channelId,
                    'scraped_date': str(date.today())
                }
                print(videoData)
                if alreadyScrapedVideoList is not None and videoData['video_id'] in alreadyScrapedVideoList:
                    alreadyScraped = True
                    print('Already Scraped')
                else:
                    scrapedVideos.append(videoData)

            if not alreadyScraped:
                try:
                    browser.find_element_by_link_text('Next page')
                    pageNumber += 1
                except Exception as ex:
                    isThereNextPage = False
                    print(ex)
        browser.close()
        return scrapedVideos



if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        channelIds = sys.argv[1:]
        for channel in channelIds:
            print('Scraping: ', channel)
            filePath = '%s.html' % (channel)
            ytChannel = InvidiousBot()        
            videos = ytChannel.scrapVideosOfChannel(channel)        
            f = open(filePath, 'w', encoding='utf-8')
            f.write('<ol>\n')
            for i in videos:
                f.write('<li><a href="https://www.youtube.com/watch?v=%s">%s</a></li>\n' % (i['video_id'], i['title']))
            f.write('</ol>')
            f.close()
    
    else:
        print("Please provide some channel ids.")

        











        
        

