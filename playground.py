import json
import pandas
import urllib
import urllib.request




def url_to_json(base_url, page_url, pages, out_file):
    f = open(out_file, 'a' )
    f.write('{"mappings":[' )
    f.close()
    for page in range (1,pages+1):
        url = base_url+page_url+str(page)
        page_content = urllib.request.urlopen(url).read()
        print(page_content)
        f = open(out_file, 'a' )
        f.write(page_content.decode("utf-8") )
        if page != pages:
            f.write(',')
        f.close()
    f = open(out_file, 'a' )
    f.write(']}')
    f.close()
    return

#todo create folder

base_url ='http://data.bioontology.org/mappings?ontologies=OMIM,DOID&apikey=541ff25a-641f-4963-b774-81df7d39e956'
page_url = '&page='
pages = 41
out_file1 = 'D:\\Anna Breit\\master thesis\\playground\\do_omim.json'
url_to_json(base_url, page_url, pages, out_file1)

base_url ='http://data.bioontology.org/mappings?ontologies=ORDO,DOID&apikey=541ff25a-641f-4963-b774-81df7d39e956'
page_url = '&page='
pages = 25
out_file = 'D:\\Anna Breit\\master thesis\\playground\\do_orpha.json'
url_to_json(base_url, page_url, pages, out_file)


with open(out_file1) as json_file:
    data = json.load(json_file)
dic = {}
no_entry  = 0
for page in data['mappings']:
    for entry in page['collection']:
        doid = entry['classes'][0]['@id'].split('_')[1]
        omimid = entry['classes'][1]['@id'].split('/')[-1]
        if (omimid.find('MTHU') == -1):
            dic[omimid] = doid
        else:
            no_entry += 1

df = pandas.DataFrame.from_records(list(dic.items()), columns=['OMIM', 'DOID'] )
df.to_csv('D:\\Anna Breit\\master thesis\\playground\\omim_do.csv', sep=';', index=None, header=None)
print(no_entry)


with open(out_file) as json_file:
    data = json.load(json_file)
dic = {}
for page in data['mappings']:
    for entry in page['collection']:
        doid = entry['classes'][0]['@id'].split('_')[1]
        orpha = entry['classes'][1]['@id'].split('_')[1]
        dic[orpha] = doid


df = pandas.DataFrame.from_records(list(dic.items()), columns=['ORPHA', 'DOID'] )
df.to_csv('D:\\Anna Breit\\master thesis\\playground\\orpha_do.csv', sep=';', index=None, header=None)
print(no_entry)

