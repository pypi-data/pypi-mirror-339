mordred
=======
molecular descriptor calculator.

.. image:: https://coveralls.io/repos/github/mordred-descriptor/mordred/badge.svg?branch=master
    :target: https://coveralls.io/github/mordred-descriptor/mordred?branch=master

.. image:: https://codeclimate.com/github/mordred-descriptor/mordred/badges/gpa.svg
   :target: https://codeclimate.com/github/mordred-descriptor/mordred
   :alt: Code Climate

.. image:: https://anaconda.org/mordred-descriptor/mordred/badges/version.svg
    :target: https://anaconda.org/mordred-descriptor/mordred

.. image:: https://img.shields.io/pypi/v/mordred.svg
    :target: https://pypi.python.org/pypi/mordred

.. image:: https://img.shields.io/badge/doi-10.1186%2Fs13321--018--0258--y-blue.svg
   :target: https://doi.org/10.1186/s13321-018-0258-y

.. image:: https://img.shields.io/badge/slack-mordred--descriptor-brightgreen.svg
    :target: https://join.slack.com/t/mordred-descriptor/shared_invite/enQtMzc1MzkyODk1NTY5LTdlYzM4MWUzY2YwZmEwMWYzN2M4YTVkMGRlMDY0ZjU2NjQ1M2RiYzllMzVjZGE4NGZkNWZjODBjODE0YmExNjk

number of descriptors
---------------------
.. code:: python

    >>> from mordred import Calculator, descriptors
    >>> n_all = len(Calculator(descriptors, ignore_3D=False).descriptors)
    >>> n_2D = len(Calculator(descriptors, ignore_3D=True).descriptors)
    >>> print("2D:    {:5}\n3D:    {:5}\n------------\ntotal: {:5}".format(n_2D, n_all - n_2D, n_all))
    2D:     1613
    3D:      213
    ------------
    total:  1826

Installation
------------

pip
~~~

#. install mordred

.. code:: console

    pip install https://github.com/OlivierBeq/mordred/tarball/master

Testing the installation
------------------------

.. code:: console

    python -m mordred.tests

Python examples
---------------

.. code:: python

    >>> from rdkit import Chem
    >>> from mordred import Calculator, descriptors

    # create descriptor calculator with all descriptors
    >>> calc = Calculator(descriptors, ignore_3D=True)

    >>> len(calc.descriptors)
    1613

    >>> len(Calculator(descriptors, ignore_3D=True, version="1.0.0"))
    1612

    # calculate single molecule
    >>> mol = Chem.MolFromSmiles('c1ccccc1')
    >>> calc(mol)[:3]
    [4.242640687119286, 3.9999999999999996, 0]

    # calculate multiple molecule
    >>> mols = [Chem.MolFromSmiles(smi) for smi in ['c1ccccc1Cl', 'c1ccccc1O', 'c1ccccc1N']]

    # as pandas
    >>> df = calc.pandas(mols)
    >>> df['SLogP']
    0    2.3400
    1    1.3922
    2    1.2688
    Name: SLogP, dtype: float64

see `examples <https://github.com/mordred-descriptor/mordred/tree/develop/examples>`_

Citation
--------
Moriwaki H, Tian Y-S, Kawashita N, Takagi T (2018) Mordred: a molecular descriptor calculator. Journal of Cheminformatics 10:4 . doi: `10.1186/s13321-018-0258-y <https://doi.org/10.1186/s13321-018-0258-y>`__

Documentation
-------------

-  `master <http://mordred-descriptor.github.io/documentation/master>`__
-  `develop <http://mordred-descriptor.github.io/documentation/develop>`__

-  `v1.1.0 <http://mordred-descriptor.github.io/documentation/v1.1.1>`__
-  `v1.0.0 <http://mordred-descriptor.github.io/documentation/v1.0.0>`__
