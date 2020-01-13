import logging
import sys

import pandas as pd


class PostgresDumpParser():

    @staticmethod
    def table_to_df(f, table_name, cols=None):

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
                    if len(row) == len(cols):
                        df = df.append(pd.DataFrame([row], columns=cols), ignore_index=True)
                    else:
                        logging.info('postgresParser -> row ignored: ', row)
            if line.startswith("COPY " + table_name):
                data_started = True
                entry_list = line.split('(')[1].split(')')[0].split(',')
                if cols is None:
                    cols = [x.strip() for x in entry_list]
                else:
                    if not (len(cols) == len(entry_list)):
                        logging.error(
                            "PostgresDumpParser: Number of columns provided for table %s are different from number found in table. %d provided, %d found" % (
                            table_name, len(cols), len(entry_list)))
                        sys.exit()
        return df
