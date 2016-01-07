from distutils.core import setup

setup(
    name='doc_to_text',
    version='0.1',
    packages=['tests', 'doc_to_text'],
    url='',
    install_requires=[
        'python-docx>=0.8.5',
        'beautifulsoup4>=4.3'
    ],
    license='MIT',
    author='Artem Revenko (artreven)',
    author_email='artreven@gmail.com',
    description='Casting documents to text'
)
