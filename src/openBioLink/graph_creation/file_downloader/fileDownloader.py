import logging
import sys
import urllib.error
import urllib.request


class FileDownloader():
    @staticmethod
    def download(url, o_file_path):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        try:
            urllib.request.urlretrieve(url, o_file_path)
        except urllib.error.HTTPError as err:
            logging.error('HTTP %s %s:  %s' % (err.code, err.msg, err.geturl()))
            sys.exit()
