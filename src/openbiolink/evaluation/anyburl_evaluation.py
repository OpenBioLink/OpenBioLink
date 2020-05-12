from openbiolink import globalConfig as globConf
from openbiolink.evaluation import evalConfig as evalConf
import pandas as pd
import os


class AnyBURLEvaluation:
    def __init__(self, training_set_path: str, test_set_path: str, valid_path: str):
        """
        self.training_examples = pd.read_csv(training_set_path, sep="\t", names=globConf.COL_NAMES_SAMPLES)
        self.training_examples = self.training_examples[globConf.COL_NAMES_TRIPLES]

        self.test_examples = pd.read_csv(test_set_path, sep="\t", names=globConf.COL_NAMES_SAMPLES)
        self.test_examples = self.test_examples[globConf.COL_NAMES_TRIPLES]

        self.validation_examples = pd.read_csv(valid_path, sep="\t", names=globConf.COL_NAMES_SAMPLES)
        self.validation_examples = self.validation_examples[globConf.COL_NAMES_TRIPLES]
        """
        self.evaluation_path = os.path.join(globConf.WORKING_DIR, evalConf.EVAL_OUTPUT_FOLDER_NAME)

        if not os.path.exists(self.evaluation_path):
            os.mkdir(self.evaluation_path)
        """
        self.training_examples.to_csv(os.path.join(self.evaluation_path, "train.txt"), sep="\t", index=False, header=False)
        self.test_examples.to_csv(os.path.join(self.evaluation_path, "test.txt"), sep="\t", index=False, header=False)
        self.validation_examples.to_csv(os.path.join(self.evaluation_path, "valid.txt"), sep="\t", index=False, header=False)
        """
        self.anyburl_path = self.download_anyburl()
        self.irifab_path = self.download_irifab()

    def train(self, learn_config_path: str):
        from subprocess import Popen, PIPE
        process = Popen(["java", "-Xmx12G", "-cp", self.anyburl_path, "de.unima.ki.anyburl.LearnReinforced", learn_config_path], stdout=PIPE, stderr=PIPE)
        while True:
            nextline = process.stdout.readline().decode("utf-8")
            if nextline == '' and process.poll() is not None:
                break
            elif nextline != '':
                print(nextline, end='')
        while True:
            nextline = process.stderr.readline().decode("utf-8")
            if nextline == '' and process.poll() is not None:
                break
            elif nextline != '' and nextline != '\r':
                print(nextline, end='')
        output = process.communicate()

    def apply_rules(self, apply_config_path: str):
        from subprocess import Popen, PIPE
        process = Popen([self.irifab_path, apply_config_path], stdout=PIPE, stderr=PIPE)
        while True:
            nextline = process.stdout.readline().decode("utf-8")
            if nextline == '' and process.poll() is not None:
                break
            elif nextline != '':
                print(nextline, end='')
        while True:
            nextline = process.stderr.readline().decode("utf-8")
            if nextline == '' and process.poll() is not None:
                break
            elif nextline != '' and nextline != '\r':
                print(nextline, end='')
        output = process.communicate()

    def evaluate(self, eval_config_path: str, metrics: list, ks=None):
        pass

    def evaluate_ranked_metrics(self, ks, metrics, unfiltered_setting=True, filtered_setting=False):
        pass

    def evaluate_threshold_metrics(self, metrics):
        pass

    def download_anyburl(self):
        anyburl_path = os.path.join(self.evaluation_path, "AnyBURL-RE.jar")
        if not os.path.exists(os.path.join(self.evaluation_path, "AnyBURL-RE.jar")):
            import wget
            wget.download("http://web.informatik.uni-mannheim.de/AnyBURL/AnyBURL-RE.jar", os.path.join(self.evaluation_path, "AnyBURL-RE.jar"))
        return anyburl_path

    def download_irifab(self):
        import platform
        os_name = platform.system()
        if os_name == "Linux":
            irifab_name = "IRIFAB"
        elif os_name == "Windows":
            irifab_name = "IRIFAB.exe"
        else:
            print("OS not supported with IRIFAB")
            import sys
            sys.exit()

        irifab_path = os.path.join(self.evaluation_path, irifab_name)
        if not os.path.exists(irifab_path):
            import wget
            irifab_url = "https://github.com/OpenBioLink/IRIFAB/raw/master/resources/binaries/" + irifab_name
            wget.download(irifab_url, irifab_path)
        return irifab_path
