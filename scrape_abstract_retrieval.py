#### Import python packages
import requests                          # Traverse the web

from bs4 import BeautifulSoup            # Parse XML


#### Function: Identify first next available key name
# Not all content object keys added to dictionaries are unique. Update key name when key already exists in target dictionary.
def update_dict_key(old_key, target_dict):

    # Add key repetition count
    key_count = 1

    # If key is not in target dictionary, then return key as key, else identify first next available key name    
    if old_key in target_dict:

        # Identify first next available key name
        while old_key*key_count in target_dict:

            key_count += 1

        nk = old_key*key_count

    else:

        nk = old_key
        
    return nk


#### Function: traverse author contents within author
# Some author content objects are themselves dictionaries containing keys and values. This function check each content object. If the content object is not a dictionary it is processed and added to a new author content dictionary. If the content object is a dictionary, then call function traverse_contents.
def traverse_contents(node_contents, node_name):

    # Add author content dictionary
    ad = {}

    # Traverse content objects
    # i i.e. content object
    for i in node_contents:
        
        # If content object is has children, then call function traverse_contents, else extract key-value pair and add it to author content dictionary
        # Content objects with children are saved as a dictionary to author content dictionary
        if i.findChildren():

            ad.update({i.name : traverse_contents(i.findChildren(), i.name)})

        else:

            # If content object key does not exist in author content dictionary, then add key-value pair to author content dictionary, else update key name and add new key-value pair to author content dictionary
            if i.name in ad:

                #print '-'*80                
                #print i.name, i.contents
                #print '-'*80

                new_key = update_dict_key(i.name, ad)

                # If content object is not empty, then update key name and add new key-value pair to author content dictionary, else update key name and add None key value and add new key-value pair to author content dictionary
                if i.contents:

                    ad.update({new_key : i.contents[0]}) # What if key appears more than twice? Todo: write function to find next available name

                else:
                    
                    ad.update({new_key : None}) # What if key appears more than twice? Todo: write function to find next available name

            else:

                #print '*'*80
                #print i.name, i.contents
                #print '*'*80

                # If content object is not empty, then add key-value pair to author content dictionary, else add none.
                if i.contents:

                    ad.update({i.name : i.contents[0]})

                else:

                    ad.update({i.name : None})                    

    return ad


#### Function: scrape article info
def article_scrape(eid, get_citing_works, api_key):

    # GET request URL
    url = 'http://api.elsevier.com/content/abstract/eid/' + eid    
                                               
    # GET request parameters # Request response # POST API key
    header = {'Accept' : 'application/xml',    
              'X-ELS-APIKey' : api_key}     

    # Make GET request and store response
    resp = requests.get(url, headers=header)    

    #print 'API Response code:', resp.status_code # resp.status_code != 200 i.e. API response error i.e. check the response request worked as intended

    # Parse and decode response content 
    # Unicode to UTF-8 
    # Ignore encoding that cannot be decoded as specified 
    # Mantra: All UTF-8 is unicode, not all unicode is UTF-8 
    # Omit newline characters
    soup = BeautifulSoup(resp.content.replace('\n', '').decode('utf-8','ignore'), 'lxml')    

    # Extract author groups
    soup_author_groups = soup.find_all('author-group')    

    #print 'Number author groups:', len(soup_author_groups)

    # Add author dicitonary
    author_dict = {}    

    # Traverse author groups 
    # i.e. for each author group 
    # i i.e. author group object
    for i in soup_author_groups:    
    
        # Traverse authors within author groups
        # i.e. for each author in an author group
        # j i.e. author object
        for j in i.find_all('author'):
            
            # Add author to author_dict
            # Add author header attributes to author in author_dict
            author_dict[j.attrs['auid']] = {'author_header' : j.attrs}

            # Add author contents to author in author_dict
            # Call traverse_contents fuction to parse author contents
            author_dict[j.attrs['auid']].update({'author_name' : traverse_contents(j.contents, j.name)})

            # Add affiliation dictionary
            # Traverse affiliation contents
            # k i.e. affiliation content object
            affiliation = {}

            for k in i.find('affiliation'):

                new_key = update_dict_key(k.name, affiliation)

                affiliation.update({new_key : k.contents[0]})


            # Add affiliation header from author group
            affiliation_header = i.find('affiliation').attrs

            # Add affiliation header from author group to affilation dictionary
            affiliation.update({'affiliation_header' : affiliation_header})

            # Add affiliation dictionary to author dictionary
            author_dict[j.attrs['auid']].update({'affiliation' : affiliation})

    #print author_dict

    # Extract abstract
    # If abstract content object exists, then add abstract content, else add None
    if soup.find('abstract'):

        soup_abstract = soup.find('abstract').find('ce:para').contents[0]

    else:

        soup_abstract = None

    # Extract title
    # If title content object exists, then add title content, else add None
    if soup.find('titletext'):

        soup_title = soup.find('titletext').contents[0]

    else:

        soup_title = None

    # Extract eid
    # If eid content object exists, then add eid content, else add None
    if soup.find('eid'):

        soup_eid = soup.find('eid').contents[0]

    else:

        soup_eid = None

    # Add scopus link    
    # If eid content object exists, then add scopus link, else add None
    if soup.find('eid'):

        soup_scopus_link = 'http://www.scopus.com/record/display.url?eid='+soup_eid+'&origin=resultslist'
        
    else:

        soup_scopus_link = None

    # Extract publication info
    # If source content object exists, then add source content, else add None
    if soup.find('source'):
    
        # Extract source title
        # If source title content object exists, then add source title content, else add None
        if soup.find('source').find('sourcetitle'):
            
            soup_source_title = soup.find('source').find('sourcetitle').contents[0]

        else:

            soup_source_title = None

        # Extract source date
        # If source date content object exists, then add source title content, else add None
        if soup.find('source').find('publicationdate'):

            if soup.find('source').find('publicationdate').find('date-text'):

                soup_source_date = soup.find('source').find('publicationdate').find('date-text').contents[0]

            else:

                soup_source_date = None

        else:

            soup_source_date = None

        # Extract source volume, issue, and page numbers
        # If source volume issue content object exists, then add source volume issue content, else add None
        if soup.find('source').find('volisspag'):

            if soup.find('source').find('volisspag').find('voliss'):

                soup_source_volume_issue = soup.find('source').find('volisspag').find('voliss').attrs

            else:

                soup_source_volume_issue = {'volume' : None, 'issue' : None}

            if soup.find('source').find('volisspag').find('pagerange'):

                soup_source_pages = soup.find('source').find('volisspag').find('pagerange').attrs

            else:

                soup_source_pages = {'last' : None, 'first' : None}        
    
        else:

            soup_source_volume_issue = {'volume' : None, 'issue' : None}

            soup_source_pages = {'last' : None, 'first' : None}        

    else:

        soup_source_title = None

        soup_source_date = None

        soup_source_volume_issue = {'volume' : None, 'issue' : None}

        soup_source_pages = {'last' : None, 'first' : None}        

    # Add citing works
    # If citing works parameter is set to True, then add citing works, else add None
    if get_citing_works:
                
        # GET request URL
        url = 'http://api.elsevier.com/content/search/scopus?query=refeid%28'+eid+'%29&count=100'

        # Make GET request and store response
        # Request returns first 100 citing works
        # Todo: Add function to crawl through API and retreive more citing works
        resp = requests.get(url, headers=header)

        #print 'API Response code:', resp.status_code # resp.status_code != 200 i.e. API response error

        # Parse and decode response content 
        # Unicode to UTF-8 
        # Ignore encoding that cannot be decoded as specified 
        # Mantra: All UTF-8 is unicode, not all unicode is UTF-8 
        # Omit newline characters
        soup = BeautifulSoup(resp.content.replace('\n', '').decode('utf-8','ignore'), 'lxml')

        # Add number of citing works
        num_citing_works = len(soup.find_all('eid'))

        # If not citing works, then add citing works, else add None
        if num_citing_works != 0:

            # Add citing works ID list
            citing_works_eid_list = []
    
            # Add citing work IDs to list citing_works_eid_list
            # i i.e. ID number object
            for i in soup.find_all('eid'):

                citing_works_eid_list.append(i.contents[0])

            # Add citing works dictionary    
            citing_works_dict = {}

            # GET article data for each article ID
            # i i.e. ID number object
            for i in citing_works_eid_list:

                # Request article data 
                # Do not GET citing works data for each article            
                citing_works_dict[i] = article_scrape(eid=i, get_citing_works=False, api_key=api_key)

            #else:

                #citing_works_dict = None

        else:

            citing_works_dict = None

            num_citing_works = None

            citing_works_eid_list = None

    else:
        
        citing_works_dict = None

        num_citing_works = None

        citing_works_eid_list = None

    # Add source dictionary of source objects    
    source_dict = {'source_title' : soup_source_title, 'source_date' : soup_source_date, 'source_pages' : soup_source_pages, 'source_volume_issue' : soup_source_volume_issue}

    # Add article dictionary of article objects, source dictionary, citing works objects, citing works dictionary
    article = {'article_title' : soup_title, 'article_eid' : soup_eid, 'article_scopus_link' : soup_scopus_link, 'article_authors' : author_dict, 'article_abstract' : soup_abstract, 'article_source' : source_dict, 'num_citing_works' : num_citing_works, 'citing_works_eid_list' : citing_works_eid_list, 'citing_works' : citing_works_dict}

    #print article        

    # Return article dictionary
    return article
