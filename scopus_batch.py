#### Scopus API
# Registered on: 07 Oct 2015
# Website URL: http://oeie.ksu.edu/
# Scopus API key: 8c07aef23a3dfa6051c24dc4b022fb64


#### Todo
# Extract street names and numbers

# Can I request multiple responses with a single resource request from the Scopus API instead of asking one at a time? Would there be any difference?


#### Import python packages
import json                              # JSON tools 

import io                                # Write file tools

import scopus_api_key                    # Import Scopus API key

from scrape_abstract_retrieval import update_dict_key, traverse_contents, article_scrape         # Import code scrape

import csv

import unicodecsv                        # Write to CSV, unicode


#### Add API key
my_api_key = scopus_api_key.get_api_key()    # Scopus API key. Provides access to Scopus API. Allows GET requests.

    
#### Add list of article ID codes
with open('eid_list.csv', 'rU') as infile:
    eid_list = [item for sublist in csv.reader(infile) for item in sublist]

print 'List of unique eids: ', eid_list

#eid_list = ['2-s2.0-84898664430', '2-s2.0-84912014389', '2-s2.0-84893613312', '2-s2.0-84903170614', '2-s2.0-84898919790', '2-s2.0-84880767928', '2-s2.0-84876309901', '2-s2.0-84920495370', '2-s2.0-84923284926', '2-s2.0-84923108032', '2-s2.0-84903640795', '2-s2.0-84905869743', '2-s2.0-84905859493', '2-s2.0-84905463440', '2-s2.0-84905460020', '2-s2.0-84902651495', '2-s2.0-84918784767', '2-s2.0-84899884487', '2-s2.0-84906736737', '2-s2.0-84926287456', '2-s2.0-84894454394', '2-s2.0-84922470444', '2-s2.0-84875020851']

#eid_list = ['2-s2.0-84875020851']
#eid_list = ['2-s2.0-0037070197']
#eid_list = ['2-s2.0-0000201308'] # Bridges and Steen
#eid_list = ['2-s2.0-73449111286'] # TypeError: 'NoneType' object is not iterable

print 'Number of article IDs: ', len(eid_list) # Print number of article IDs # 23


#### GET article data for each article ID
# eid i.e. ID number object
for eid in eid_list:

    # Print current article ID
    print 'Article:', eid    

    # Request article data 
    # GET citing works data for each article
    article = article_scrape(eid=eid, get_citing_works=True, api_key=my_api_key)

    # Write article data to a JSON file
    with io.open('citation_data_json/'+eid+'.json', 'w', encoding='utf8') as outfile:
        f = json.dumps(article, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
        outfile.write(unicode(f))

    
    # Write article data to a CSV file
    with open('citation_data_csv/'+eid+'.csv', 'wb+') as outfile:

        article_csv = unicodecsv.writer(outfile, encoding='utf-8')

        article_csv.writerow(['article_eid', 'article_authors_auid', 'author_name_ce_given_name', 'author_name_ce_index_name', 'author_name_ce_initials', 'author_name_ce_surname', 'author_name_ce_e_address', 'author_name_preferred_name_ce_given_name', 'author_name_preferred_name_ce_indexed_name', 'author_name_preferred_name_ce_initials', 'author_name_preferred_name_ce_surname', 'article_abstract', 'article_eid', 'article_scopus_link', 'article_source_source_date', 'article_source_source_pages_first', 'article_source_source_pages_last', 'article_source_source_title', 'article_source_source_volume_issue_issue', 'article_source_source_volume_issue_volume', 'article_title', 'article_source_id', 'num_citing_works', 'affiliation_affiliation_header_afid', 'affiliation_affiliation_header_country', 'affiliation_affiliation_header_dptid', 'affiliation_city_group', 'affiliation_country', 'affiliation_organization1', 'affiliation_organization2', 'affiliation_organization3', 'affiliation_postal_code', 'affiliation_city', 'affiliation_state', 'affiliation_address_part', 'affiliation', 'author_header_auid', 'author_header_seq', 'author_header_type'])
    
        for auth in article['article_authors'].iteritems():
        
            article_csv.writerow([article.get('article_eid', ''),
                                  str(auth[0]),
                                  auth[1].get('author_name', '').get('ce:given-name', ''),
                                  auth[1].get('author_name', '').get('ce:indexed-name', ''),
                                  auth[1].get('author_name', '').get('ce:initials', ''),
                                  auth[1].get('author_name', '').get('ce:surname', ''),
                                  auth[1].get('author_name', '').get('ce:e-address', ''),
                                  auth[1].get('author_name', '').get('preferred-name', '').get('ce:given-name', ''),
                                  auth[1].get('author_name', '').get('preferred-name', '').get('ce:indexed-name', ''),
                                  auth[1].get('author_name', '').get('preferred-name', '').get('ce:initials', ''),
                                  auth[1].get('author_name', '').get('preferred-name', '').get('ce:surname', ''),
                                  article.get('article_abstract', ''),
                                  article.get('article_eid', ''),
                                  article.get('article_scopus_link', ''),
                                  article.get('article_source', '').get('source_date', ''),
                                  article.get('article_source', '').get('source_pages', '').get('first', ''),
                                  article.get('article_source', '').get('source_pages', '').get('last', ''),
                                  article.get('article_source', '').get('source_title', ''),
                                  article.get('article_source', '').get('source_volume_issue', '').get('issue', ''),
                                  article.get('article_source', '').get('source_volume_issue', '').get('volume', ''),
                                  article.get('article_title', ''),
                                  article.get('article_source_id', ''),
                                  article.get('num_citing_works', ''),
                                  auth[1].get('affiliation', '').get('affiliation_header', '').get('afid', ''),
                                  auth[1].get('affiliation', '').get('affiliation_header', '').get('country', ''),
                                  auth[1].get('affiliation', '').get('affiliation_header', '').get('dptid', ''),
                                  auth[1].get('affiliation', '').get('city-group', ''),
                                  auth[1].get('affiliation', '').get('country', ''),
                                  auth[1].get('affiliation', '').get('organization', ''),
                                  auth[1].get('affiliation', '').get('organizationorganization', ''),
                                  auth[1].get('affiliation', '').get('organizationorganizationorganization', ''),
                                  auth[1].get('affiliation', '').get('postal-code', ''),
                                  auth[1].get('affiliation', '').get('city', ''),
                                  auth[1].get('affiliation', '').get('state', ''),
                                  auth[1].get('affiliation', '').get('address-part', ''),
                                  auth[1].get('affiliation', ''),
                                  auth[1].get('author_header', '').get('auid', ''),
                                  auth[1].get('author_header', '').get('seq', ''),
                                  auth[1].get('author_header', '').get('type', '')])

        for cw in article['citing_works'].iteritems():
            
            for auth in cw[1]['article_authors'].iteritems():
        
                article_csv.writerow([article.get('article_eid', ''),
                                      str(auth[0]),
                                      auth[1].get('author_name', '').get('ce:given-name', ''),
                                      auth[1].get('author_name', '').get('ce:indexed-name', ''),
                                      auth[1].get('author_name', '').get('ce:initials', ''),
                                      auth[1].get('author_name', '').get('ce:surname', ''),
                                      auth[1].get('author_name', '').get('ce:e-address', ''),
                                      auth[1].get('author_name', '').get('preferred-name', '').get('ce:given-name', ''),
                                      auth[1].get('author_name', '').get('preferred-name', '').get('ce:indexed-name', ''),
                                      auth[1].get('author_name', '').get('preferred-name', '').get('ce:initials', ''),
                                      auth[1].get('author_name', '').get('preferred-name', '').get('ce:surname', ''),
                                      cw[1].get('article_abstract', ''),
                                      cw[1].get('article_eid', ''),
                                      cw[1].get('article_scopus_link', ''),
                                      cw[1].get('article_source', '').get('source_date', ''),
                                      cw[1].get('article_source', '').get('source_pages', '').get('first', ''),
                                      cw[1].get('article_source', '').get('source_pages', '').get('last', ''),
                                      cw[1].get('article_source', '').get('source_title', ''),
                                      cw[1].get('article_source', '').get('source_volume_issue', '').get('issue', ''),
                                      cw[1].get('article_source', '').get('source_volume_issue', '').get('volume', ''),
                                      cw[1].get('article_title', ''),
                                      cw[1].get('num_citing_works', ''),
                                      auth[1].get('affiliation', '').get('affiliation_header', '').get('afid', ''),
                                      auth[1].get('affiliation', '').get('affiliation_header', '').get('country', ''),
                                      auth[1].get('affiliation', '').get('affiliation_header', '').get('dptid', ''),
                                      auth[1].get('affiliation', '').get('city-group', ''),
                                      auth[1].get('affiliation', '').get('country', ''),
                                      auth[1].get('affiliation', '').get('organization', ''),
                                      auth[1].get('affiliation', '').get('organizationorganization', ''),
                                      auth[1].get('affiliation', '').get('organizationorganizationorganization', ''),
                                      auth[1].get('affiliation', '').get('postal-code', ''),
                                      auth[1].get('affiliation', '').get('city', ''),
                                      auth[1].get('affiliation', '').get('state', ''),
                                      auth[1].get('affiliation', '').get('address-part', ''),
                                      auth[1].get('affiliation', ''),
                                      auth[1].get('author_header', '').get('auid', ''),
                                      auth[1].get('author_header', '').get('seq', ''),
                                      auth[1].get('author_header', '').get('type', '')])


    
    #print article    
    #print '-'*80


