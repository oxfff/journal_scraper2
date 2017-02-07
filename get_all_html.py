import os, threading
from urllib import FancyURLopener

template  = 'wget  --header="Accept: text/html" --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0"  http://www.sciencedirect.com/science/journal/01933973/%d -O html_source/%d.html' 

template2 = 'http://www.sciencedirect.com/science/journal/01933973/%d' 

class MyOpener(FancyURLopener, object):
    #version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    version = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0"      

class download_thread(threading.Thread):

    def __init__ (self, threadID):
        global template2
        threading.Thread.__init__(self)
        self.threadID = threadID
        print 'my id is %d' % self.threadID
        self.template = template2
    
    def run(self):
        global template

        offset = 10
        myopener = MyOpener()
        start = 0
        end = 0
        if self.threadID == 1:
            start = 1
            end = 11 # 
        else:
            start = self.threadID * 10
            end = start + 10

        for i in xrange(start, end):
            #cmd = template % (i, i)
            #full_url = self.template % i
            print '[thread-%d] trying to get %d....' % (self.threadID , i)
            #os.system(cmd)
            #myopener.retrieve(full_url, "html_source/%d.html" % i)
            os.system(template % (i,i))
def main():
    pool = []
    for i in xrange(1, 5):
        pool.append(download_thread(i))
    for t in pool:
        t.start()
    for t in pool:
        t.join()


if __name__ == '__main__':
    main()
    print 'done'
