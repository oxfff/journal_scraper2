from BeautifulSoup import BeautifulSoup as soup
from BeautifulSoup import Tag
import threading
import urllib2, json, os
from urllib import FancyURLopener

import os.path

def check_file_exist(full_path_to_file):
    return os.path.isfile(full_path_to_file) 

class MyOpener(FancyURLopener, object):
        version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'


dl_cmd  = 'wget  --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0" "%s" -O "%s/%s.pdf"'

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
schedule = {}

"""
1. download a html
2. spawn threads to download pdfs on the pdfs on the page
3. download the next page and prepare for JSON


"""



class threaded_downloader (threading.Thread):
    def __init__(self, threadID, data_dict):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.content = data_dict.get('content')
        self.vol =data_dict.get('vol')
        

    def download(self):
        myopener = MyOpener()
        counter = 0
        dl_log =  open('%d-dl-log', 'w')
        dl_log.write("=========== Vol %d (%d articles) ===========" % (self.vol, len(content)))
        error_dict = {}
        for article in self.content:
            save_as = article.title.replace(' ', '_')
            full_url = article.get('url')
            try:
                myopener.retrieve(full_url, "/Vol-%d/%s.pdf" % (self.vol, save_as))
                counter += 1
                dl_log.write('%s\n' % save_as)
                dl_log.write('%s\n' % full_url)
            except:
                dl_log.write('error happen when trying to open %s (%s)' % (full_url, save_as))
                error_dict 

        if counter == len(content):
            dl_log.write('got all')

        dl_log.close()
        
    def run(self):
        self.download()

class myThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def debug_thread_counter(self):
        with open('log-%d' %self.threadID, 'w') as log:

            for i in xrange(self.threadID, self.threadID+10):
                #print '%d-%d' % (self.threadID, i)
                log.write('%d\n'%i)
            log.close()

    def run(self):
        #self.debug_thread_counter()
        self.threaded_parser()


    def threaded_parser(self):
        logname = 'Vol_%d' % self.threadID
        
        my_id = self.threadID
        log = open(logname, 'w')
        counter = 1
        for x in xrange(my_id, my_id+10): 
            dir_name = 'Vol-%d' % x
            #cmd = 'mkdir %s' % dir_name
            #print '[thread-%d]: working on Vol-%d' % (my_id, x)
            #os.system(cmd)
            try:
                filename = 'html_source/%d.html' % x
                log.write('============== Vol. %d. ============\n\n' % x)
                
                with open(filename, 'r') as f:
                    s_html = soup(f.read())
                    article_tags  = s_html.findAll('ul', attrs={'class':'article'})
                    for a in article_tags:
                        try:
                            title = a.find('li', attrs={'class': 'title '}).find('h4').find('a').contents[0]
                            pdf = a.find('a', attrs={'class': 'cLink'})['href'][2:]
                            #print '%s\t%s' % (title, pdf[2:])
                            #log.write('%s\n%s\n\n' % (title, pdf[2:]))
                            exist = "%s/%s.pdf" (dir_name, title)
                            if check_file_exist(exist):
                                continue

                            cmd = dl_cmd % (pdf, dir_name, title)
                            #os.system(cmd) 
                            #log.write(cmd)
                            log.write('%s\n%s\n' % (title, pdf))
                            log.write('\n\n')
                            counter += 1
                            #print cmd
                        except:
                            print 'current x = %d' %x 

                    #print len(article_tags)
                log.write('\n')
                f.close()
            except:
                print 'error opening html_source/%d.html' % x
                pass
        #log.close()
        print '[thread-%d] counter = %d' % (self.threadID, counter)
        return

def main():
    pool = []
    for i in xrange(1, 40, 10):
            pool.append(myThread(i))
    for t in pool:
        t.start()

    for t in pool:
        t.join()
if __name__ == '__main__':
    main()
    print 'done'
