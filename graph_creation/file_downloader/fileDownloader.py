import urllib, urllib.request

class FileDownloader ():
    @staticmethod
    def download(url, o_file_path):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, o_file_path)
        #fixme httpError handling

