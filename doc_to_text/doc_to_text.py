"""
Stores functions for fetching documents from the web.
"""

import urllib.request
import tempfile
from subprocess import Popen, PIPE
from docx import Document
from bs4 import BeautifulSoup


def doc_to_text(doc_path, extension=None):
    """
    Convert document to text. Supported types: .doc, .docx, .odt, .pdf.
    Extension should be either included in doc_path or supplied separately.

    .. warning::
        you need the programms 'antiword', 'odt2txt', 'pdftotext' be installed and callable in your terminal.
    """
    if (extension and extension == 'doc') or doc_path[-4:] == ".doc":
        cmd = ['antiword', doc_path]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode('ascii', 'ignore')
    elif (extension and extension == 'docx') or doc_path[-5:] == ".docx":
        document = Document(doc_path)
        paratextlist = [x.text for x in document.paragraphs]
        return '\n\n'.join(paratextlist)
    elif (extension and extension == 'odt') or doc_path[-4:] == ".odt":
        cmd = ['odt2txt', doc_path]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode('ascii', 'ignore')
    elif (extension and extension == 'pdf') or doc_path[-4:] == ".pdf":
        cmd = ['pdftotext', doc_path, '-']
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode('ascii', 'ignore')


def url_to_text(url):
    """
    Get text from url.

    .. seealso:: 'doc_to_text' function.
    """
    if any(url.endswith(x) for x in ['doc', 'docx', 'pdf', 'odt']):
        extension = url[url.rfind('.')+1:]
        data = urllib.request.urlopen(url, timeout=1).read()
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(data)
        f.close()
        return doc_to_text(f.name, extension)
    else:
        html = urllib.request.urlopen(url, timeout=1).read()
        soup = BeautifulSoup(html)
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator=' ')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text


def texts_iterator(urls, avoid_duplicates=False):
    """
    :param urls: urls
    :param avoid_duplicates: avoid duplicate urls
    :return: iterator over texts extracted from the urls
    """
    seen_urls = set()
    for doc_url in urls:
        if avoid_duplicates:
            if doc_url in seen_urls:
                continue
            else:
                seen_urls.add(doc_url)
        try:
            doc_text = url_to_text(doc_url)
            yield doc_text
        # Skip all possible errors related to http requests. Wildcard after except is bad, but I use it as the number of
        # found exceptions keeps growing. Hope no other exception happens.
        #  (urllib.error.URLError, ConnectionResetError, socket.timeout,
        #         http.client.IncompleteRead, http.client.BadStatusLine, ssl.CertificateError,
        #         docx.opc.exceptions.PackageNotFoundError)
        except:
            pass
