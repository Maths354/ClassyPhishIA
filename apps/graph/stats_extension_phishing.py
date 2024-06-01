
import tldextract # type: ignore

class CamamberExtension:

    def __init__(self, dataPhish):
        self.dataPhish = dataPhish

    def extract_url_extension(self):
        extensions = []
        for entry in self.dataPhish:
            if 'phishing_url' in entry:
                url = entry['phishing_url']
                ext = tldextract.extract(url).suffix
                extensions.append(ext)     
                
        counts = {}
        for ext in extensions:
            counts[ext] = counts.get(ext, 0) + 1
        
        labels = list(counts.keys())
        data = list(counts.values())

        return labels, data