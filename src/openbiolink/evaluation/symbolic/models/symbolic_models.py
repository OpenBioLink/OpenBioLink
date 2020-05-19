import os
from openbiolink import globalConfig as globConf
from openbiolink.evaluation import evalConfig as evalConf
from openbiolink.evaluation.symbolic.models.model import Model


class AnyBURL(Model):

    def __init__(self):
        super().__init__()
        self.evaluation_path = os.path.join(globConf.WORKING_DIR, evalConf.EVAL_OUTPUT_FOLDER_NAME)
        self.config = self.default_config(self.evaluation_path)

        if not os.path.exists(self.config["path_predicitions"]):
            os.mkdir(self.config["path_predicitions"])
        if not os.path.exists(self.config["path_rules"]):
            os.mkdir(self.config["path_rules"])

    def train(self):
        learn_config_path = self.write_config_learn(self.config)
        anyburl_path = self.download_anyburl()
        from subprocess import Popen, PIPE
        process = Popen(
            ["java", "-Xmx12G", "-cp", anyburl_path, "de.unima.ki.anyburl.LearnReinforced", learn_config_path],
            stdout=PIPE, stderr=PIPE)
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
        process.communicate()

    def predict(self):
        apply_config_path = self.write_config_apply(self.config)
        irifab_path = self.download_irifab()
        from subprocess import Popen, PIPE
        process = Popen([irifab_path, apply_config_path], stdout=PIPE, stderr=PIPE)
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

    def download_anyburl(self):
        anyburl_path = os.path.join(self.evaluation_path, "AnyBURL-RE.jar")
        if not os.path.exists(os.path.join(self.evaluation_path, "AnyBURL-RE.jar")):
            import wget
            wget.download("http://web.informatik.uni-mannheim.de/AnyBURL/AnyBURL-RE.jar",
                          os.path.join(self.evaluation_path, "AnyBURL-RE.jar"))
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

    def default_config(self, evaluation_path):
        return dict(
            path_training=os.path.join(self.evaluation_path, "dataset", "train.txt"),
            path_test=os.path.join(self.evaluation_path, "dataset", "test.txt"),
            path_valid=os.path.join(self.evaluation_path, "dataset", "valid.txt"),
            path_predicitions=os.path.join(self.evaluation_path, "predicitions"),
            path_rules=os.path.join(self.evaluation_path, "rules"),
            policy=2,
            reward=5,
            epsilon=0.1,
            threshold_confidence=0.0001,
            snapshots_at=[10, 50, 100],
            worker_threads=7,
            unseen_negative_examples=5,
            discrimination_bound=1000,
            top_k_output=10,
            fast=1,
            discrimination_unique=0,
            intermediate_discrimination=1
        )

    def write_config_learn(self, config):
        config_learn_path = os.path.join(self.evaluation_path, "dataset", "config-learn.properties")
        with open(config_learn_path, "w") as config_learn:
            config_learn.write(f"PATH_TRAINING = {config['path_training']}")
            config_learn.write(f"PATH_OUTPUT = {config['path_output']}")
            config_learn.write(f"SNAPSHOTS_AT = {','.join(config['snapshots_at'])}")
            config_learn.write(f"WORKER_THREADS = {config['worker_threads']}")
            config_learn.write(f"POLICY = {config['policy']}")
            config_learn.write(f"REWARD = {config['reward']}")
            config_learn.write(f"EPSILON = {config['epsilon']}")
            config_learn.write(f"THRESHOLD_CONFIDENCE = {config['threshold_confidence']}")
        return config_learn_path

    def write_config_apply(self, config):
        config_apply_path = os.path.join(self.evaluation_path, "dataset", "config-apply.properties")
        with open(config_apply_path, "w") as config_apply:
            config_apply.write(f"PATH_TRAINING = {config['path_training']}")
            config_apply.write(f"PATH_TEST = {config['path_test']}")
            config_apply.write(f"PATH_VALID = {config['path_valid']}")
            config_apply.write(f"PATH_RULES = {config['path_rules']}")
            config_apply.write(f"PATH_OUTPUT = {config['path_predicitions']}")
            config_apply.write(f"UNSEEN_NEGATIVE_EXAMPLES = {config['unseen_negative_examples']}")
            config_apply.write(f"DISCRIMINATION_BOUND = {config['discrimination_bound']}")
            config_apply.write(f"TOP_K_OUTPUT = {config['top_k_output']}")
            config_apply.write(f"WORKER_THREADS = {config['worker_threads']}")
            config_apply.write(f"UNSEEN_NEGATIVE_EXAMPLES = {config['unseen_negative_examples']}")
            config_apply.write(f"THRESHOLD_CONFIDENCE = {config['threshold_confidence']}")
            config_apply.write(f"FAST = {config['threshold_confidence']}")
            config_apply.write(f"DISCRIMINATION_UNIQUE = {config['discrimination_unique']}")
            config_apply.write(f"INTERMEDIATE_DISCRIMINATION = {config['intermediate_discrimination']}")
        return config_apply_path
