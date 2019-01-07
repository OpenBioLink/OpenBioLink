import pandas as pd
import gzip

class PostgresDumpParser():

    @staticmethod
    def table_to_df(f, table_name, cols = None):

        data_started = False
        df = None
        for line in f:
            line = line.strip()
            if data_started:
                if line.startswith('\.'):
                    break
                row = line.split('\t')
                row = [x.strip() for x in row]
                if df is None:
                    df = pd.DataFrame([row], columns=cols)
                else:
                    if len(row)== len(cols):
                        df = df.append(pd.DataFrame([row], columns=cols), ignore_index=True)
                    else:
                        print('row ignored: ')
                        print(row)
            if line.startswith("COPY public." + table_name): #todo ohne public?
                data_started = True
                entry_list = line.split('(')[1].split(')')[0].split(',')
                if cols == None:
                    cols = [x.strip() for x in entry_list]
                else:
                    if not(len(cols)== len(entry_list)) :
                        pass# todo throw error
        return df