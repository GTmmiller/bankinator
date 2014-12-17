bankinator
==========

``bankinator`` is a python package that pulls transaction data from
banking websites. ``bankinator`` is made up of two parts. The
``bankinator`` package that features modules for accessing and
processing bank data, and the ``bankinate.py`` script that provides a
simple, command-line interface for using the modules in the
``bankinator`` package.

Setup
=====

Whether you want to hack on ``bankinator`` or you just want to run the
``bankinate.py`` script to pull some data, you’ll need to download a few
things first.

1. Install python 2.8.x
2. Install Beautiful Soup 4
3. Install Requests

That’s all you need to get up and running with ``bankinator``!

Usage
=====

Just run ``python bankinate.py`` and follow the instructions on the
command line to generate a dump of the transactions from the bank of
your choice.

Extending
=========

Extending ``bankinator`` for your favorite bank or output format is
easy. Simply follow the steps below:

Bank Module
-----------

In order to make a new bank module you need to create a python file in
``/bankinator/bank`` corresponding to your new module’s name.

Next, you’ll need to create a class named ``Bank`` in your new module
that inherits the abstract base class ``BankBase``.

From there you just need to override all of ``BankBase``\ ’s methods and
your new module will be complete.

Output Module
-------------

In order to make a new bank module you need to create a python file in
``/bankinator/output`` corresponding to your new module’s name.

Next, you’ll need to make a class named ``WriteOutput`` that inherits
the abstract base class ``OutputBase``.

From there you just need to override all of ``OutputBase``\ ’s methods
and your new module will be complete.

Your new modules will immediately be useable by the ``bankinate.py``
script once you’ve completed the previous steps.

Currently Supported Banks
=========================

-  BB&T Checking and Savings Accounts
-  BB&T Credit and Loan Accounts