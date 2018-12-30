import pandas as pd
import gzip

class PostgresDumpParser():

    @staticmethod
    def table_to_df(f, table_name):

        data_started = False
        cols = []
        df = None
        for line in f:
            line = line.strip()
            if data_started:
                if line.startswith('COPY public.'):
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
            if line.startswith("COPY public." + table_name):
                data_started = True
                entry_list = line.split('(')[1].split(')')[0].split(',')
                cols = [x.strip() for x in entry_list]
        return df