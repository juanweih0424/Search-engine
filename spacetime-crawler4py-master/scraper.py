
import re
from urllib.parse import urlparse, urljoin
import urllib.robotparser
import requests                                             # Updated on Sunday
from bs4 import BeautifulSoup                               # You can run it and follow the comments to see how this works, there are still work to do, but this scraper function is very complete right now.
from utils import response                                  # To do: How many subdomains did you find in the ics.uci.edu domain? Submit the list of subdomains ordered alphabetically and the number of unique pages detected in each subdomain. The content of this list should be lines containing URL, number, for example:http://vision.ics.uci.edu, 10 (not the actual number here)
from collections import defaultdict                         # To do: Did it avoid traps? (penalties for falling in traps)  && Did it avoid sets of pages with low information value? (penalties for crawling useless families of pages - you must decide and discuss within your group on a reasonable definition for a low information value page and be able to defend it during the interview with the TAs)
"""
Check this comment block first

Scraper.py generates 'Token_File.txt', in the same directory, there is a helper
py file called 'reportGenetor.py', run Scraper.py first and then run reportGenerator.py
will create a Report.txt file that answers required questions from Assignment2 shell

Warnings: DELETE TOKEN_FILE.TXT after it finishes running on frontier, otherwise
TOKEN_FILE.TXT WILL GET LARGER AND LARGER, DELETE IT EVERYTIME YOU RUN THIS FILE
"""
def similarity(dictA, dictB, threshold = 0.9):
    numberOfTimes = 0
    total = 1
    totalA = 0
    totalB = 0
    for k, v in dictA.items():
        if k in dictB:
            numberOfTimes += min(v, dictB[k])
    for k in dictA:
        totalA += dictA[k]
    for k in dictB:
        totalB += dictB[k]
    total = max(totalA, totalB)
    if total == 0:
        total = 1
    result = numberOfTimes / total
    if result >= 0.9:
        return True
    else:
        return False


def noContent(dictA, threshold=10):   
    if len(dictA) <= threshold:
        return True
    else:
        return False

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]
    # write all url tokens to a file 

def extract_next_links(url, resp):

    # Implementation required.
    urls = set()
    sub = defaultdict(int) # default dictionary for subdomain
    stopwords = {'hello', 'y', 'followed', 'tell', 'co', 'sup', 'afterwards', 
                        'last', 'to', 'que', 'would', 'use', 'welcome', 'widely', 'about', 
                        'see', 'approximately', 'off', 'whereupon', 'uses', 'those', 'everywhere', 
                        'able', 'you', 'anyone', 'themselves', 'contains', 'not', 'don', 'information', 
                        'wont', 'shall', 'her', 'wherever', 'beyond', 'seven', 'successfully', 'these', 
                        'asking', 'containing', 'comes', 'selves', 'unfortunately', 'during', 'nor', 'are', 
                        'the', 'actually', 'shed', 't', 'right', 'n', 'indicate', 'resulted', 'if', 'first', 
                        'whose', 'also', 'alone', 'else', 'hereupon', 'later', 'thereby', 'immediately', 'youd', 
                        'sure', 'eighty', 'ever', 'his', 'somewhere', 'five', 'briefly', 'll', 'apparently', 'my', 
                        'seemed', 'put', 'several', 'outside', 'already', 'therefore', 'until', 'we', 'gotten', 
                        'thereof', 'allow', 'necessary', 'beginnings', 'anywhere', 'b', 'within', 'million', 'very', 
                        'across', 'therere', 'www', 'thanks', 'according', 'getting', 'one', 'seems', 'nevertheless',
                        'indicates', 'need', 'him', 'research', 'part', 'whereby', 'various', 'is', 'unto', 'affects', 
                        'whats', 'section', 'whomever', 'on', 'how', 'accordingly', 'appear', 'even', 'respectively', 
                        'beside', 'specified', 'hereby', 'nd', 'th', 'begin', 'for', 'have', 'regardless', 'has', 'hed',
                        'lets', 'amongst', 'sorry', 'enough', 'did', 'thorough', 'wherein', 'poorly', 'been', 'does', 
                        'than', 'further', 'sometimes', 'possibly', 'line', 'ups', 'hers', 'home', 'didn', 'lest', 'show', 
                        'wants', 'go', 'showns', 'makes', 'our', 'once', 'everybody', 'as', 'got', 'and', 'came', 'viz', 
                        'besides', 'over', 'non', 'sometime', 'stop', 'mostly', 'probably', 'allows', 'promptly', 'thereafter',
                        'done', 'said', 'just', 'above', 'inc', 'rather', 'help', 'taking', 'important', 'mustn', 'make', 
                        'neither', 'heres', 'needs', 'k', 'went', 'think', 'specify', 'ought', 'meantime', 'al', 'edu', 'give', 
                        'want', 'value', 'definitely', 'an', 'fifth', 'every', 'youre', 'currently', 'serious', 'accordance', 
                        'anything', 'become', 'usefulness', 'seeming', 'sensible', 'quite', 'at', 'somethan', 'itd', 
                        'particular', 'maybe', 'page', 'up', 'shows', 'aside', 'similar', 'almost', 'obviously', 'especially', 
                        'doing', 'usually', 'miss', 'anyway', 'haven', 'largely', 'because', 'specifically', 'whom', 'had', 'both', 
                        'ran', 'given', 'four', 'yours', 'apart', 'thats', 'id', 'former', 'beforehand', 'placed', 'a', 'im', 'm', 
                        'whereafter', 'thou', 'can', 'let', 'twice', 'appropriate', 'says', 'whether', 'vol', 'proud', 'ex', 'whod', 
                        'became', 'someone', 'though', 'less', 'auth', 'since', 'hence', 'somehow', 'she', 'thoughh', 'old', 'he', 
                        'better', 'predominantly', 'much', 'corresponding', 'wasn', 'upon', 'gave', 'rd', 'wheres', 'significantly', 
                        'itself', 'they', 'yourselves', 'gone', 'after', 'with', 'hither', 'may', 'down', 'cant', 'u', 'et', 'their', 
                        'different', 'of', 'between', 'could', 'few', 'x', 'goes', 'into', 'himself', 'available', 'changes', 'thered', 
                        'its', 'ah', 'past', 'what', 'say', 'noted', 'why', 'gives', 'cause', 'moreover', 'really', 'whereas', 'giving', 
                        'affecting', 'yes', 'secondly', 'relatively', 'tip', 'no', 'contain', 'qv', 'self', 'against', 'd', 'q', 'using', 
                        'being', 'quickly', 'from', 'saying', 'certainly', 'mr', 'insofar', 'elsewhere', 'below', 'onto', 'ok', 'tends', 
                        'around', 'furthermore', 'liked', 'do', 'little', 'throughout', 'somebody', 'wish', 'owing', 'exactly', 'beginning', 
                        'ff', 'never', 'under', 'ts', 'ninety', 'ord', 'causes', 'whatever', 'inward', 'potentially', 'becomes', 'announce',                    # This is the stopword list
                        'going', 'necessarily', 'specifying', 'seen', 'present', 'shown', 've', 'nine', 'anybody', 'more', 'act', 'g', 
                        'latter', 'something', 'wouldn', 'via', 'z', 'suggest', 'refs', 'inasmuch', 'hes', 'unlikely', 'previously', 'hasn', 
                        'appreciate', 'ca', 'when', 'thank', 'per', 'end', 'nearly', 'all', 'won', 'having', 'f', 'hadn', 'inner', 'before', 
                        'likely', 'downwards', 'except', 'only', 'come', 'hereafter', 'whence', 'til', 're', 'seriously', 'pages', 'anyways', 
                        'course', 'saw', 'there', 'then', 'na', 'ending', 'tries', 'soon', 'particularly', 'vs', 'reasonably', 'index', 'thru', 
                        'theyre', 'among', 'everyone', 'might', 'myself', 'nay', 'away', 'third', 'me', 'sub', 'that', 'namely', 'e', 'thence', 
                        'similarly', 'used', 'ourselves', 'wonder', 'please', 'sufficiently', 'other', 'c', 'pp', 'readily', 'most', 'begins', 
                        'entirely', 'again', 'perhaps', 'however', 'j', 'must', 'second', 'cannot', 'abst', 'example', 'hardly', 'means', 'shes', 
                        'without', 'I', 'herein', 'it', 'keep', 'concerning', 'by', 'whim', 'them', 'mainly', 'v', 'should', 'near', 'considering', 
                        'others', 'well', 'keeps', 'none', 'this', 'either', 'i', 'thus', 'some', 'willing', 'ours', 'nobody', 'best', 'whole', 'in', 
                        'run', 'sent', 'obtain', 'okay', 'obtained', 'such', 'while', 'known', 'looking', 'ignored', 'slightly', 'aren', 'truly', 
                        'many', 'zero', 'knows', 'was', 'com', 'happens', 'next', 'gets', 'made', 'but', 'nonetheless', 'eg', 'arent', 'sec', 
                        'whos', 'name', 'ml', 'here', 'novel', 'taken', 'yourself', 'look', 'ie', 'shan', 'hundred', 'added', 'thanx', 'kept', 
                        'were', 'each', 'own', 'throug', 'howbeit', 'am', 'unlike', 'biol', 'herself', 'still', 'who', 'km', 'forth', 'follows', 
                        'always', 'thoroughly', 'date', 'couldn', 'be', 'anymore', 'nothing', 'new', 'your', 'trying', 'following', 'described', 
                        'like', 'overall', 'due', 'nowhere', 'theyd', 'somewhat', 'yet', 'too', 'found', 'l', 'through', 'eight', 'tried', 'wasnt', 
                        'strongly', 'noone', 'took', 'certain', 'along', 'omitted', 'two', 'seeing', 'useful', 'showed', 'affected', 'least', 'latterly', 
                        'anyhow', 'recent', 'whoever', 'o', 'lately', 'ones', 'where', 'us', 'p', 'out', 'ed', 'possible', 'or', 'etc', 'despite', 'greetings', 
                        'theirs', 'adj', 'will', 'kg', 'consequently', 'primarily', 'becoming', 'indeed', 'another', 'shouldn', 'plus', 'towards', 'ain', 'whither', 
                        'everything', 'take', 'know', 'r', 'fix', 'whenever', 'couldnt', 'far', 'try', 'invention', 'ref', 'related', 'any', 'ask', 'awfully', 'mrs', 
                        'mg', 'h', 'wed', 'theres', 'ltd', 'so', 'merely', 'presumably', 'now', 'thereupon', 'hid', 'regards', 'usefully', 'behind', 'six', 'doesn', 
                        'looks', 'immediate', 'resulting', 'although', 'unless', 'toward', 'believe', 'world', 'seem', 'otherwise', 'indicated', 'clearly', 'consider', 
                        'w', 'significant', 'hi', 'mean', 'often', 'meanwhile', 'way', 'together', 'mon', 's', 'weren', 'oh', 'get', 'normally', 'provides', 
                        'thousand', 'therein', 'instead', 'un', 'results', 'associated', 'three', 'effect', 'regarding', 'words', 'which', 'isn', 'hopefully', 
                        'back', 'thereto', 'wouldnt', 'brief', 'arise', 'recently', 'nos', 'substantially', 'importance', 'werent', 'same', 'formerly', 'mug', 'vols'}
    try:
        #print('in try')
        domain = urlparse(url).netloc
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        #----------------------------------Tokenizing the url that we passed in------------------------------------
        text = ''
        tknz_dict = dict()
        #print('Tokenizing url')
        for data in soup.find_all("p"):
            text += data.get_text() 
        tknz_url = Tokenization(url, text)
        tknz_url.tokenize()
        url_content_dict = tknz_url.computeWordFrequencies()
        #do the comparison on two dictionary
        #----------------------------------Tokenizing the url that we passed in------------------------------------
        for a_tag in soup.findAll("a"):
            href = a_tag.get("href")
            if href == "" or href is None:
                continue
            else:
                if 200 <= resp.status < 400 and resp.status != 204:
                    #print("valid link")
                    ## filter english stop words in file after running crawler
                    #tokenize here to count unique words and determine if site is high content
                    href = urljoin(url, href)
                    parsed_href = urlparse(href)
                    #subdomain = parsed_href.hostname.split('.')[0] # subdomain
                    href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                    #sub_url = parsed_href.scheme + "://" + subdomain + ".ics.uci.edu" # FOR REPORT
                    if '.' in urlparse(url).path and url in href:
                        #print(". in path")
                        #if there's a '.' in the path, basically, this is a file or something. We will check if the href contain the url. If yes, then this is a infinite trap
                        continue #break the for loop
                            #print(url, "found in href")
                            # this is a infinite trap!!!
                            
                    else:
                        if href not in urls: # Checking visited urls (should we also check the http and https?)
                            if is_valid(href):
                                #print('we can cralw')
                                
                                # FOR REPORT ######
                                #if re.match(r"(.*\.)?ics\.uci\.edu\/.*?", domain):
                                #if domain == "www.ics.uci.edu":    
                                #    if sub_url in sub:
                                #        sub[sub_url] += 1
                                #    else:
                                #        sub[sub_url] = 1
                                ###################
                                
                                soup_page = BeautifulSoup(requests.get(href).text, "html.parser")
                                text_page = ''
                                #print('Getting token')
                                for data in soup_page.find_all("p"):
                                    text_page += data.get_text()            # This for loop will collect all the information in each page we found under the url, and put the content string into text_page(string)
                                Tknz = Tokenization(href, text_page)
                                Tknz.tokenize()
                                temp_dict = Tknz.computeWordFrequencies()
                                if similarity(tknz_dict, temp_dict) or len(tknz_dict) == len(temp_dict):
                                    continue
                                tknz_dict = Tknz.computeWordFrequencies()
                                print(len(tknz_dict))
                                #then compare the two dictionary
                                #print(len(tkSet), "-", len(tkSet1))         # This just help visualize the process, many adjustments should be made when we are running it in openlab.
                                # To do: add if statement which check the amount of textual information in the website, if heavy text, add, if not don't add.
                                #if (len(tkSet) - len(tkSet1)) > 0: # Haven't decided the amount
                                if requests.get(href).status_code == 200 and noContent(tknz_dict):
                                    #print('not ok')
                                    continue
                                if not similarity(url_content_dict, tknz_dict) and not noContent(tknz_dict):
                                    #print('ok added to set')
                                    tkSet = Tknz.run()                          # Then tokenized the string
                                    tkSet1 = tkSet.difference(stopwords)        # This will remove the stopwords in the token set, to do: improve efficiency.
                                    urls.add(href)
        # Runs after the for-loop
        #alpha = sorted(sub.items()) # sorting the subdomain items alphabetically
        #with open("subdomain.txt", "w") as f:
            #for i in alpha:
                #f.write(str(i[0])+", "+str(i[1])+"\n")
        return urls
    except Exception as e:
        print (e, "\n")
        return set()

def checkURL(url): 
    #This function checks if url is matched as in requirement. Other sites are prohibited to crawl
    requiredURL = ["www.ics.uci.edu", "www.cs.uci.edu", "www.informatics.uci.edu", "www.stat.uci.edu", "today.uci.edu/department/information_computer_sciences"]
    ics = r"(.*\.)?ics\.uci\.edu\/.*?" # .ics.uci.edu
    cs = r"(.*\.)?cs\.uci\.edu\/.*?"
    in4max = r"(.*\.)?informatics\.uci\.edu\/.*?"
    stat = r"(.*\.)?stat\.uci\.edu\/.*?"
    today = r"today\.uci\.edu\/department\/information_computer_sciences\/.*?"
    if re.match(ics, url) or re.match(cs, url) or re.match(in4max, url) or re.match(stat, url) or re.match(today, url):
        return True
    return False

def is_valid(url):
    """
    returns true only if:
        *.ics.uci.edu/*
        *.cs.uci.edu/*
        *.informatics.uci.edu/*
        *.stat.uci.edu/*
        today.uci.edu/department/information_computer_sciences/*
    """
    try:
        parsed = urlparse(url) 
        if parsed.scheme not in set(["http", "https"]):
            return False

        if not checkURL(url):
            return False

        # checking robots.txt file for allowed URLS
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(parsed.scheme + '://' + parsed.netloc + "/robots.txt")
        rp.read()
        
        fileType = re.match(
            # finds groups that are not webpages
            r".*\.(css|js|bmp|gif|jpe?g|ico|img"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|pdf|ppsx)$", parsed.path.lower())
        
        # returns true if URL valid and is a webpage
        return rp.can_fetch('*', url) and not fileType

    except TypeError:
        print ("TypeError for ", parsed)
        #raise

###################################################################################
class Tokenization(object):
    def __init__(self, url, content):
            self.text = content.lower()
            self.link = url
            self.rawDataList = []
            self.tkSet = set()
            self.tkDict = defaultdict(int)

    def tokenize(self):  # return List<Token>
        try:
            self.rawDataList = re.findall(r"[A-Za-z0-9]+", self.text)  
            self.tkSet = set(self.rawDataList)
            return self.tkSet
        except IOError as e1:  
            errMsg = "\nTokenization.__init__(): " + str(e1)
            print(errMsg)
            return -1


    def computeWordFrequencies(self):  # return Map<Token,Count> // dict
        for tk in self.rawDataList:
            self.tkDict[tk] += 1 
        return self.tkDict


    def tkFileWrite(self):  # void // print highest freq first
        with open("Token_File.txt", "a") as f:
            urlStr = "-----" + self.link + "\n"
            f.write(urlStr)
            for tk in sorted(self.tkDict, key=lambda x:(self.tkDict[x], [-ord(c) for c in x]), reverse=True):
                tempStr = tk + "=" + str(self.tkDict[tk]) +"\n"
                f.write(tempStr)
                # token = 50
    def run(self):
        self.tokenize()
        self.computeWordFrequencies()
        self.tkFileWrite()
        return self.tkSet
###################################################################################



"""Locally debug for functionality
if __name__ == "__main__":

    #resp_dict = {'url': 'https://www.cs.uci.edu/', 'status': 200, 'error':None}
    #resp = response.Response(resp_dict)
    #print(extract_next_links(resp_dict['url'], resp))

    resp_dict1 = {'url': 'https://www.ics.uci.edu/', 'status': 200, 'error':None}
    resp1 = response.Response(resp_dict1)
    print(extract_next_links(resp_dict1['url'], resp1))

    #parsed = urlparse('https://merong.ics.uci.edu/eventweb-15-participatory-urban-sensing#1')
    #print(parsed)"""

    
