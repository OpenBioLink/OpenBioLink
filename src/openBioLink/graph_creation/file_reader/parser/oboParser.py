import pandas


class OboParser(object):

    def obo_to_df(self, content, quadruple_list):
        """each quadruple consists of (1) beginning of the line, (2) split character,
        (3) index of split element being the id, (4) the name of dict entry (col_name)"""

        terms = []
        lines = content.readlines()
        term = {}
        for line in lines:
            if line.startswith('[Typedef]'):
                break
            if line.startswith('[Term]'):
                if term:
                    term = self.dic_list_to_dic_string(term)
                    terms.append(term)
                term = {}
                continue
            for tuple in quadruple_list:
                if line.startswith(tuple[0]):
                    elements = line.split(tuple[1])
                    if tuple[3] not in term:
                        term[tuple[3]] = [elements[tuple[2]].strip()]
                    else:
                        term[tuple[3]].append(elements[tuple[2]].strip())
                    break
        term = self.dic_list_to_dic_string(term)
        terms.append(term)
        content.close()
        df = pandas.DataFrame.from_records(terms)
        return df

    def dic_list_to_dic_string(self, dic):
        for k, v in dic.items():
            dic[k] = self.to_string(v)
        return dic

    def to_string(self, list):
        string = ''
        for e in list:
            if string == '':
                string = e
            else:
                string = string + ';' + e
        return string
