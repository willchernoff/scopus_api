#### Scopus API
# Registered on: 06 Jul 2015
# Website URL: http://www.willchernoff.com


#### Todo
# Extract street names and numbers

# Can I request multiple responses with a single resource request from the Scopus API instead of asking one at a time? Would there be any difference?


#### Import python packages
import json                              # JSON tools 

import io                                # Write file tools

import scopus_api_key                    # Import Scopus API key

from scrape_abstract_retrieval import update_dict_key, traverse_contents, article_scrape         # Import code scrape




#### Add API key
my_api_key = scopus_api_key.get_api_key()    # Scopus API key. Provides access to Scopus API. Allows GET requests.

    
#### Add list of article ID codes
eid_list = ['2-s2.0-84898664430', '2-s2.0-84912014389', '2-s2.0-84893613312', '2-s2.0-84903170614', '2-s2.0-84898919790', '2-s2.0-84880767928', '2-s2.0-84876309901', '2-s2.0-84920495370', '2-s2.0-84923284926', '2-s2.0-84923108032', '2-s2.0-84903640795', '2-s2.0-84905869743', '2-s2.0-84905859493', '2-s2.0-84905463440', '2-s2.0-84905460020', '2-s2.0-84902651495', '2-s2.0-84918784767', '2-s2.0-84899884487', '2-s2.0-84906736737', '2-s2.0-84926287456', '2-s2.0-84894454394', '2-s2.0-84922470444', '2-s2.0-84875020851']

#eid_list = ['2-s2.0-84875020851']

print len(eid_list) # Print number of article IDs # 23

#eid = eid_list[0]
#eid = '2-s2.0-0037070197'


#### GET article data for each article ID
# eid i.e. ID number object
for eid in eid_list:

    # Print current article ID
    print 'Article:', eid    

    # Request article data 
    # GET citing works data for each article
    article = article_scrape(eid=eid, get_citing_works=True, api_key=my_api_key)    

    # Write article data to a JSON file
    with io.open('citation_data/'+eid+'.json', 'w', encoding='utf8') as outfile:
        f = json.dumps(article, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
        outfile.write(unicode(f))

    # Print article data
    print article    
    print '-'*80


