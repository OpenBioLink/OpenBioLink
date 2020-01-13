class FileWriter():
    @staticmethod
    def wirte_to_file(data, out_path, sep=';'):
        data.to_csv(out_path, sep=sep, index=False, header=False)
