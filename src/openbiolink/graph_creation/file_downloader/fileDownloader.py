import logging
import sys
import urllib.error
import urllib.request
from tqdm.auto import tqdm
from openbiolink.gui.tqdmbuf import TqdmBuffer
from openbiolink import globalConfig as globConst


class FileDownloader:

    @staticmethod
    def download_progress_hook(t):
        last_b = [0]

        def update_to(b=1, bsize=1, tsize=None):
            if tsize not in (None, -1):
                t.total = tsize
            t.update((b - last_b[0]) * bsize)
            last_b[0] = b

        return update_to

    @staticmethod
    def download(url, o_file_path):
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        urllib.request.install_opener(opener)
        try:
            tqdmbuffer = TqdmBuffer() if globConst.GUI_MODE else None
            with tqdm(unit="B", unit_scale=True, file=tqdmbuffer) as t:
                reporthook = FileDownloader.download_progress_hook(t)
                urllib.request.urlretrieve(url, o_file_path, reporthook)
        except urllib.error.HTTPError as err:
            logging.error("HTTP %s %s:  %s" % (err.code, err.msg, err.geturl()))
            sys.exit()
        except urllib.error.URLError as err:
            logging.error("Url Error: %s" % (err.msg))
            sys.exit()
