class OboParser(object):

    @staticmethod
    def parse_hpo_obo_from_file(path: str):
        with open(path) as content:
            hpo_terms = []
            lines = content.readlines()
            hpo_term = None
            for line in lines:
                if line.startswith('[Term]'):
                    if hpo_term is not None:
                        hpo_terms.append(hpo_term)
                    hpo_term = OboTerm()
                if line.startswith('id') or line.startswith('alt_id'):
                    elements = line.split(' ')
                    hpo_term.ids.append(elements[1].strip())
                if line.startswith('xref: UMLS:'):
                    elements = line.split(':')
                    hpo_term.umls_links.append(elements[2].strip())
                if line.startswith('is_a'):
                    elements = line.split(' ')
                    hpo_term.is_a_links.append(elements[1].strip())
        return hpo_terms

    @staticmethod
    def parse_do_obo_from_file(path: str):
        with open(path) as content:
            do_terms = []
            lines = content.readlines()
            do_term = None
            for line in lines:
                if line.startswith('[Term]'):
                    if do_term is not None:
                        do_terms.append(do_term)
                    do_term = OboTerm()
                if line.startswith('id') or line.startswith('alt_id'):
                    elements = line.split(' ')
                    do_term.ids.append(elements[1].strip())
                if line.startswith('xref: UMLS_CUI:'):
                    elements = line.split(':')
                    do_term.umls_links.append(elements[2].strip())
                if line.startswith('is_a'):
                    elements = line.split(' ')
                    do_term.is_a_links.append(elements[1].strip())
        return do_terms

    @staticmethod
    def parse_go_obo_from_file(path: str):
        with open(path) as content:
            go_terms = []
            lines = content.readlines()
            go_term = None
            for line in lines:
                if line.startswith('[Term]'):
                    if go_term is not None:
                        go_terms.append(go_term)
                    go_term = OboTerm()
                if line.startswith('id') or line.startswith('alt_id'):
                    elements = line.split(' ')
                    go_term.ids.append(elements[1].strip())
                if line.startswith('xref: UMLS_CUI:'):
                    elements = line.split(':')
                    go_term.umls_links.append(elements[2].strip())
                if line.startswith('is_a'):
                    elements = line.split(' ')
                    go_term.is_a_links.append(elements[1].strip())
        return go_terms









class OboTerm():
    ids = []
    umls_links = []
    is_a_links = []
    def __init__(self):
        self.ids = []
        self.umls_links = []
        self.is_a_links = []

    def to_dict(self):
        return {
            'ID': self.to_string(self.ids),
            'UMLS': self.to_string(self.umls_links),
            'IS_A': self.to_string(self.is_a_links)
        }

    def to_string(self, list):
        string = ''
        for e in list:
            if string =='':
                string = e
            else:
                string = string + ';' + e
        return string




