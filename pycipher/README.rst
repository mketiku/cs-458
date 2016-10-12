Example usage
-------------

::

    >>> from pycipher import ADFGVX
    >>> adfgvx = ADFGVX(key='PH0QG64MEA1YL2NOFDXKR3CVS5ZW7BJ9UTI8', keyword='GERMAN')
    >>> adfgvx.encipher("Hello world!")
    'FVFDAGXAFFFFGFAGADFG'
    >>> adfgvx.decipher(_)
    'HELLOWORLD'



To run the test suite::

    python setup.py test
