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
        #self.evaluation_path = os.path.join(globConf.WORKING_DIR, evalConf.EVAL_OUTPUT_FOLDER_NAME)

        #if not os.path.exists(self.evaluation_path):
         #   os.mkdir(self.evaluation_path)
        """
        self.training_examples.to_csv(os.path.join(self.evaluation_path, "train.txt"), sep="\t", index=False, header=False)
        self.test_examples.to_csv(os.path.join(self.evaluation_path, "test.txt"), sep="\t", index=False, header=False)
        self.validation_examples.to_csv(os.path.join(self.evaluation_path, "valid.txt"), sep="\t", index=False, header=False)
        """
        #self.anyburl_path = self.download_anyburl()
        #self.irifab_path = self.download_irifab()

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
        prediction_paths = self.get_prediction_paths(eval_config_path)
        for prediction_path in prediction_paths:
            predictions = self.read_prediction(prediction_path)

            ranks_heads = list()
            ranks_tails = list()
            for prediction in predictions:
                if prediction.head_rank != float('inf'):
                    ranks_heads.append(prediction.head_rank)
                if prediction.tail_rank != float('inf'):
                    ranks_tails.append(prediction.tail_rank)
            from openbiolink.evaluation.metrics import Metrics
            print(Metrics.calculate_hits_at_k([1,3,10], ranks_heads, ranks_tails, len(predictions)))





    def get_prediction_paths(self, eval_config_path: str):
        with open(eval_config_path) as f:
            file_content = '[root]\n' + f.read()

        from configparser import ConfigParser
        config_parser = ConfigParser()
        config_parser.read_string(file_content)

        predictions_path = config_parser["root"]["PATH_PREDICTIONS"]
        if "|" in predictions_path:
            prefix, values, _ = predictions_path.split("|")
            postfixes = values.split(",")
            predictions_path = list()
            for postfix in postfixes:
                predictions_path.append(prefix + postfix)
        else:
            predictions_path = [predictions_path]
        return predictions_path

    def read_prediction(self, prediction_path: str):
        file_content = None
        with open(prediction_path) as pred_file:
            file_content = pred_file.readlines()
        file_content = [x.strip() for x in file_content]
        predictions = list()
        for i in range(0, len(file_content), 3):
            triple = file_content[i].split(" ")
            heads = list(filter(None, file_content[i+1][7:].strip("\t").split("\t")))
            tails = list(filter(None, file_content[i+2][7:].strip("\t").split("\t")))

            head_nodes = list()
            head_confidences = list()
            for j in range(0, len(heads), 2):
                head_nodes.append(heads[j])
                head_confidences.append(heads[j+1])

            tail_nodes = list()
            tail_confidences = list()
            for j in range(0, len(tails), 2):
                tail_nodes.append(tails[j])
                tail_confidences.append(tails[j+1])
            predictions.append(Prediction(triple[0], triple[1], triple[2], head_nodes, head_confidences, tail_nodes, tail_confidences))
        return predictions

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

class Prediction:
    def __init__(self, head, relation, tail, head_predictions, head_confidences, tail_predictions, tail_confidences):
        self.tail_confidences = tail_confidences
        self.tail_predictions = tail_predictions
        self.head_confidences = head_confidences
        self.head_predictions = head_predictions
        self.tail = tail
        self.relation = relation
        self.head = head
        self.head_rank = self.calc_rank(head, head_predictions)
        self.tail_rank = self.calc_rank(tail, tail_predictions)

    def calc_rank(self, true: str, predictions: list):
        for i in range(len(predictions)):
            if predictions[i] == true:
                return i
        return float('inf')
