import json
import pandas
import urllib.request

#class BioPortalMappingParser():
#
#    @staticmethod
#    def create_db_file(in_file_path, id1_prefix, id2_prefix, cols, extract_id1_lambda, extract_id2_lambda,
#                       out_file_path):
#        with open(in_file_path) as json_file:
#            data = json.load(json_file)
#        dic = {}
#        for page in data['mappings']:
#            for entry in page['collection']:
#                idField1 = entry['classes'][0]['@id']
#                idField2 = entry['classes'][1]['@id']
#                id1 = extract_id1_lambda(idField1)
#                id2 = extract_id2_lambda(idField2)
#                if id1 is not None and id2 is not None:
#                    dic[id1_prefix + id1] = id2_prefix + id2
#        df = pandas.DataFrame.from_records(list(dic.items()), columns=cols)
#        df.to_csv(out_file_path, sep=';', index=None, header=None)
#
#    @staticmethod
#    def url_to_json(base_url, out_file, api_key):
#        params = '&apikey=' + api_key + '&page='
#        f = open(out_file, 'w+')
#        f.write('{"mappings":[')
#        page = 0
#        while True:
#            page += 1
#            url = base_url + params + str(page)
#            page_content = urllib.request.urlopen(url).read()
#            if not json.loads(page_content)['collection']:
#                break
#            if page != 1:
#                f.write(',')
#            f.write(page_content.decode("utf-8"))
#        f.write(']}')
#        f.close()
#        return
#