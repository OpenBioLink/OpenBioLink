import json
import pandas
import urllib
import urllib.request




def url_to_json(base_url, page_url, pages, out_file):
    f = open(out_file, 'w+' )
    f.write('{"mappings":[' )
    page=0
    while True:
        page += 1
        url = base_url+page_url+str(page)
        page_content = urllib.request.urlopen(url).read()
        if not json.loads(page_content)['collection']:
            break
        if page != 1:
            f.write(',')
        print(page_content)
        f.write(page_content.decode("utf-8") )
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
            dic['OMIM:'+ omimid] = 'DOID:'+ doid
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
        dic['ORPHA:' + orpha] = 'DOID:' + doid


df = pandas.DataFrame.from_records(list(dic.items()), columns=['ORPHA', 'DOID'] )
df.to_csv('D:\\Anna Breit\\master thesis\\playground\\orpha_do.csv', sep=';', index=None, header=None)
print(no_entry)












def create_db_file(in_file_path, id1_prefix,id2_prefix, cols, extract_id1_lambda, extract_id2_lambda, out_file_path):
    with open(in_file_path) as json_file:
        data = json.load(json_file)
    dic = {}
    for page in data['mappings']:
        for entry in page['collection']:
            idField1 = entry['classes'][0]['@id']
            idField2 = entry['classes'][1]['@id']
            id1 = extract_id1_lambda(idField1)
            id2 = extract_id2_lambda(idField2)
            if id1 is not None and id2 is not None:
                dic[id1_prefix + id1] = id2_prefix + id2
    df = pandas.DataFrame.from_records(list(dic.items()), columns=cols )
    df.to_csv(out_file_path, sep=';', index=None, header=None)
    print(no_entry)

extract_do_id = lambda a : a.split('_')[1]
extract_orpha_id = lambda a : a.split('_')[1]
extract_omim_id = lambda a : (a.split('/')[-1].find('MTHU') == -1) if a.split('/')[-1] else None
