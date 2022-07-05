import requests

class Dropbox():
    """The Class incharge of managing txt files from dropbox."""
    def __init__(self, share_link:str, log:bool=False):
        self.share_link = self.validate_link(share_link)
        self.log = log

    def read_file(self):
        return requests.get(self.share_link).text

    def validate_link(self, share_link:str) -> str:
        """Tries to return a correctly formated dropbox link."""
        
        if share_link[-1:] == "?":
            return share_link + "dl=1"

        if not share_link[-5:] in ["?dl=1", "?dl=0"]:
            return share_link + "?dl=1"

        if share_link[-5:] == "?dl=0":
            return share_link[:-5] + "?dl=1"