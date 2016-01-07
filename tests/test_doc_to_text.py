import os

from doc_to_text.doc_to_text import *


dirname = os.path.dirname(os.path.realpath(__file__))
path = dirname + '/data/'


def test_doc_to_text():
    filename_doc = 'cinnamon.doc'
    text = doc_to_text(path + filename_doc)
    assert 'a' in text


def test_pdf_to_text():
    filename_pdf = 'Wikilinks2012.pdf'
    text = doc_to_text(path + filename_pdf)
    assert 'a' in text


def test_docx_to_text():
    filename_docx = 'AppBody-Sample-English.docx'
    text = doc_to_text(path + filename_docx)
    assert 'a' in text


def test_url_to_text_pdf():
    pdf_url = 'http://www.cs.bgu.ac.il/~orlovm/teaching/saya/reports/saya-web-interface-report.pdf'
    text = url_to_text(pdf_url)
    assert 'feature' in text


def test_url_to_text_html():
    html_url = 'http://kasunweranga.blogspot.de/2010/11/intelij-idea-shortcut-keys.html'
    text = url_to_text(html_url)
    assert 'Java' in text