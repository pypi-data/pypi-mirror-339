##########
ka_uts_wdp
##########

Overview
********

.. start short_desc

**Dictionary 'Utilities'**

.. end short_desc

Installation
************

.. start installation

Package ``ka_uts_wdp`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_wdp

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_wdp

.. end installation

Package logging
***************

Standard or user specific Package logging of the package **ka_uts_wdp** is defined
in the static logging class **Log_** of Base module log\_.py of the Communication
Package **ka_uts_com**.
The default Logging configuration is defined by the yaml files **log.std.yml**
or **log.usr.yml** in the data directory of the Communication package.
The Logging configuration could be overriden by yaml files with the same names in the
data directory of the application package **ka_uts_wdp**.
Logging defines log file paths for the following log message types: .

#. *debug*
#. *error*
#. *info*
#. *log*

  .. Naming-conventions-for-logging-files-label:
  .. table:: *Naming conventions for logging file*

   +-------+--------------------------------------------+-------------------+
   |Type   |Directory                                   |File               |
   +=======+============================================+===================+
   |debug  |/data/<tenant>/RUN/<package>/<function>/debs|debs_<pid>_<ts>.log|
   +-------+--------------------------------------------+-------------------+
   |error  |/data/<tenant>/RUN/<package>/<function>/errs|errs_<pid>_<ts>.log|
   +-------+--------------------------------------------+-------------------+
   |warning|/data/<tenant>/RUN/<package>/<function>/errs|wrns_<pid>_<ts>.log|
   +-------+--------------------------------------------+-------------------+
   |info   |/data/<tenant>/RUN/<package>/<function>/logs|infs_<pid>_<ts>.log|
   +-------+--------------------------------------------+-------------------+
   |log    |/data/<tenant>/RUN/<package>/<function>/logs|logs_<pid>_<ts>.log|
   +-------+--------------------------------------------+-------------------+

  .. Naming examples-of-logging-files-label:
  .. table:: *Naming examples of logging file*

   +-------+-------------------------------+------------------------+
   |Type   |Directory                      |File                    |
   +=======+===============================+========================+
   |debug  |/data/umh/RUN/umh_otec/srr/debs|debs_9470_1737118199.log|
   +-------+-------------------------------+------------------------+
   |error  |/data/umh/RUN/umh_otec/srr/errs|errs_9470_1737118199.log|
   +-------+-------------------------------+------------------------+
   |warning|/data/umh/RUN/umh_otec/srr/errs|errs_9470_1737118199.log|
   +-------+-------------------------------+------------------------+
   |info   |/data/umh/RUN/umh_otec/srr/logs|logs_9470_1737118199.log|
   +-------+-------------------------------+------------------------+

Package files
*************

Classification
==============

The Files of Package ``ka_uts_wdp`` could be classified into the follwing file types:

#. *Special files*
#. *Dunder modules*
#. *Sub Package*
#. *Data files*

Special files
*************

  .. Special-files-of-package-ka_uts_wdp-label:
  .. table:: **Special files of package ka uts wdp**

   +--------+--------+-------------------------------------------------------------+
   |Name    |Type    |Description                                                  |
   +========+========+=============================================================+
   |py.typed|Type    |The py.typed file is a marker file used in Python packages to|
   |        |checking|indicate that the package supports type checking. This is a  |
   |        |marker  |part of the PEP 561 standard, which provides a standardized  |
   |        |file    |way to package and distribute type information in Python.    |
   +--------+--------+-------------------------------------------------------------+

Dunder Modules
**************

  .. Dunder-modules-label:
  .. table:: *Dunder-Modules*

   +--------------+---------+---------------------------------------------------+
   |Name          |Type     |Description                                        |
   +==============+=========+===================================================+
   |__init__.py   |Package  |The module is used to execute initialisation code  |
   |              |directory|or mark the directory it contains as a package.    |
   |              |marker   |The Module enforces explicit imports and thus clear|
   |              |file     |namespace use and call them with the dot notation. |
   +--------------+---------+---------------------------------------------------+
   |__version__.py|Version  |The module consist of Assignment Statements for    |
   |              |file     |system Variables used in Versioning.               |
   +--------------+---------+---------------------------------------------------+

Sub-packages
************

The Package ``ka_uts_wdp`` contains the sub-package ``pmeh``:

Sub-package pmeh
================

The Sub-package ``pmeh`` contains following files:

#. special file: py.typed
#. dunder module: __init__.py
#. modules: wdp.py

Module: wdp.py
--------------

The Module ``wdp.py`` contains the followinga classes:

   +-------------+------+---------------------------------------------+
   |Name         |Type  |Description                                  |
   +=============+======+=============================================+
   |CustomHandler|normal|Custom Handler of PatternMatchingEventHandler|
   +-------------+------+---------------------------------------------+
   |WdP          |static|Watch Dog Processor                          |
   +-------------+------+---------------------------------------------+

Class: CustomHandler
^^^^^^^^^^^^^^^^^^^^

The class ``CustomHandler`` contains the subsequent methods.

Methods
"""""""

  .. Methods-of-class-CustomHandlerlabel:
  .. table:: *Methods of class CustomHandler*

   +-----------+--------+-----------------------------------------------------+
   |Name       |Type    |Description                                          |
   +===========+========+=====================================================+
   |__init__   |instance|Initialise class CustomHandler                       |
   +-----------+--------+-----------------------------------------------------+
   |on_created |instance|Process event 'File refered by file path is created' |
   +-----------+--------+-----------------------------------------------------+
   |on_modified|instance|Process 'File refered by file path is modified' event|
   +-----------+--------+-----------------------------------------------------+

Class WdP
^^^^^^^^^

The static class ``WdP`` contains the subsequent methods.

Methods
"""""""

  .. Methods-of-class-WdP-label:
  .. table:: *Methods-of-class-WdP*

   +----+------+-------------------------------------------------+
   |Name|Type  |Description                                      |
   +====+======+=================================================+
   |pmeh|static|WatchDog Task for pattern matching of files paths|
   +----+------+-------------------------------------------------+

Appendix
********

.. contents:: **Table of Content**
