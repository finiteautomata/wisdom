wisdom
======

Word sense disambiguation algorithms for Python.

Install
-------
    $ pip install -e git+https://github.com/geekazoid/wisdom#egg=wisdom


Usage
-----
    In [1]: from wisdom import lesk

    In [2]: sent = 'I went to the bank to deposit my money'

    In [3]: lesk(sent, 'bank')
    Out[3]: Synset('depository_financial_institution.n.01')