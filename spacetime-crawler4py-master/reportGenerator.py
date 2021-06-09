from urllib.parse import urlparse
from collections import defaultdict
import re


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
                        'back', 'thereto', 'wouldnt', 'brief', 'arise', 'recently', 'nos', 'substantially', 'importance', 'werent', 'same', 'formerly', 'mug', 'vols','1','2','3','4','5','6','7','8','9','0'}
def top_50(set_url):
    counter = 0
    tk_dict = dict()
    
    with open('Token_File.txt', 'r') as tk_f:
        ln = tk_f.readline()
        while True:
            
            #-----http://www.cs.uci.edu/
            if ln[:5] == '-----' and ln in set_url:
                counter +=1
                set_url.remove(ln)
                ln_tk = tk_f.readline()
                while True:
                    if ln_tk == '':
                        break
                    if ln_tk[:5] == '-----':
                        ln = ln_tk
                        break
                    key_val = ln_tk.split('=')
                    if key_val[0] != '':
                        if key_val[0] not in stopwords:
                            if key_val[0] in tk_dict:
                                tk_dict[key_val[0]] += int(key_val[1])
                                ln_tk = tk_f.readline()
                                continue
                            else:
                                tk_dict[key_val[0]] = 1
                                ln_tk = tk_f.readline()
                                continue
                    else:
                        break
                    ln_tk = tk_f.readline()
            else:
                ln = tk_f.readline()
                if ln == '':
                    break
            if ln_tk == '':
                break
    list_key = list(tk_dict.keys())
    Top_50 = sorted(list_key, key=lambda x: tk_dict[x], reverse=True)
    Top_50 = [(i, tk_dict[i]) for i in Top_50]
    return Top_50[:50]


def longest_page(set_url):
    with open('Token_File.txt', 'r') as tk_f:
        keyword_dict = dict()
        ln = tk_f.readline()
        while ln != '':
            if ln == '':
                return keyword_dict
            if ln[:5] == '-----' and ln in set_url:
                #count all the words
                set_url.remove(ln)
                url = ln[5:]
                word_url = 0
                ln_tk = tk_f.readline()
                while ln_tk != '' and ln != '':
                    if ln_tk == '':
                        return keyword_dict
                    if ln_tk[:5] == '-----':
                        break
                    else:
                        #do the work
                        word = ln_tk.split('=')
                        word_url += int(word[1])         # Include stopwords
                        #finished the work
                        ln_tk = tk_f.readline()
                keyword_dict[url] = word_url
                ln = ln_tk
            ln = tk_f.readline()
        list_rt = sorted(list(keyword_dict.keys()), key=lambda x: keyword_dict[x], reverse=True)
        return list_rt[0], keyword_dict[list_rt[0]]


def get_set_url():
    set_url = set()
    with open('Token_File.txt', 'r') as tk_f:
        while True:
            #-----http://www.cs.uci.edu/
            ln = tk_f.readline()
            if ln[:5] == '-----':
                #url line
                set_url.add(ln)
            if ln == '':
                break
    return set_url


def get_sub(urls):
    # get subdomains
    sub = defaultdict(int)
    for i in urls:
        parsed = urlparse(i)
        domain = parsed.netloc
        subdomain = parsed.hostname.split('.')[0]
        sub_url = parsed.scheme + "://" + subdomain + ".ics.uci.edu"
        if re.match(r"(.*\.)?ics\.uci\.edu", domain):
            if sub_url in sub:
                sub[sub_url] += 1
            else:
                sub[sub_url] = 1
    return sub

def write_file(sub):
    # Writes file for answering number 4 based on the subdomains that we gathered.
    alpha = sorted(sub.items())
    with open("Report.txt", "a") as a:
        a.write("Question 4: How many subdomains did you find in the ics.uci.edu domain?\n")
        for l in alpha:
            text = "Subdomain: "+str(l[0])+", "+str(l[1])+" times found\n"
            a.write(text)







if __name__ == '__main__':
    
    urls = get_set_url()
    with open("Report.txt", 'w') as rpt:
        rpt.write("Question 1: How many unique pages did we find?\n")
        rpt.write("We found total: "+str(len(urls))+" pages\n\n")
        
    
    list1 = top_50(urls)
    urls = get_set_url()
    with open('Report.txt', 'a') as rpt:
        rpt.write("Question 2: What is the longest page in terms of number of words?\n")
        rpt.write(str(longest_page(urls))+'\n\n')
        
    
    with open('Report.txt', 'a') as rpt:
        rpt.write("Question 3: What are the 50 common words for the pages we crawled under these domains?\n")
        for i in range(50):
            rpt.write(str(list1[i])+'\n')
        rpt.write('\n')

    write_file(get_sub(urls))
    
