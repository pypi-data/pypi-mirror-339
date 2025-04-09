# DCSV

Python module for serializing structured data to and from the Dublin Core 
Metadata Initiative DCSV format (Cox & Iannella, 2006).

## Installation

    $ pip install dscv


## Usage

    >>> import dcsv

    >>> dcsv.dumps({'foo': 2, 'bar': 3})
    'foo=2; bar=3'

    >>> dcsv.loads("pi=3.14")
    {'pi': 3.14}


## References

Cox, S. and Iannella, R. (2006) DCMI DCSV. 
Available at: https://www.dublincore.org/specifications/dublin-core/dcmi-dcsv/.
