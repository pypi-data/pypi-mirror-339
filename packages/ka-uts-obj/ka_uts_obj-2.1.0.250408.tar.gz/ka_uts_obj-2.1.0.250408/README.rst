##########
ka_uts_obj
##########

Overview
********

.. start short_desc

**Object 'Utilities'**

.. end short_desc

Installation
************

.. start installation

Package ``ka_uts_obj`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_obj

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_obj

.. end installation

This requires that the ``readme`` extra is installed:

.. code-block:: shell

	$ python -m pip install ka_uts_obj[readme]

Package logging
***************

Standard or user specific Package logging of the package **ka_uts_arr** is defined 
in the static logging class **Log_** of Base module log\_.py of the Communication
Package **ka_uts_com**.
The default Logging configuration is defined by the yaml files **log.standard.yml**
or **log.user.yml** in the data directory of the Communication package.
The Logging configuration could be overriden by yaml files with the same names in the
data directory of the application package **ka_uts_arr**.
Logging defines log file paths for the following log message types: .

#. *debug*
#. *error*
#. *info*
#. *log*

  .. Naming-conventions-for-logging-files-label:
  .. table:: *Naming conventions for logging file*

   +-----+--------------------------------------------+-------------------+
   |Type |Directory                                   |File               |
   +=====+============================================+===================+
   |debug|/data/<tenant>/RUN/<package>/<function>/debs|debs_<pid>_<ts>.log|
   +-----+--------------------------------------------+-------------------+
   |error|/data/<tenant>/RUN/<package>/<function>/errs|errs_<pid>_<ts>.log|
   +-----+--------------------------------------------+-------------------+
   |info |/data/<tenant>/RUN/<package>/<function>/logs|info_<pid>_<ts>.log|
   +-----+--------------------------------------------+-------------------+
   |log  |/data/<tenant>/RUN/<package>/<function>/logs|logs_<pid>_<ts>.log|
   +-----+--------------------------------------------+-------------------+

  .. Naming examples-of-logging-files-label:
  .. table:: *Naming examples of logging file*

   +-----+-------------------------------+------------------------+
   |Type |Directory                      |File                    |
   +=====+===============================+========================+
   |debug|/data/umh/RUN/umh_otec/srr/debs|debs_9470_1737118199.log|
   +-----+-------------------------------+------------------------+
   |error|/data/umh/RUN/umh_otec/srr/errs|errs_9470_1737118199.log|
   +-----+-------------------------------+------------------------+
   |info |/data/umh/RUN/umh_otec/srr/logs|info_9470_1737118199.log|
   +-----+-------------------------------+------------------------+
   |log  |/data/umh/RUN/umh_otec/srr/logs|logs_9470_1737118199.log|
   +-----+-------------------------------+------------------------+

Package files
*************

Classification
==============

The Files of Package ``ka_uts_obj`` could be classified into the follwing file types:

#. *Special files*
#. *Dunder modules*
#. *Package modules*

Special files
=============

  .. Special-file-label:
  .. table:: **Special-file**

   +--------+--------+---------------------------------------------------+
   |Name    |Type    |Description                                        |
   +========+========+===================================================+
   |py.typed|Type    |The py.typed file is a marker file used in Python  |
   |        |checking|packages to indicate that the package supports type|
   |        |marker  |checking. This file is a part of the PEP 561       |
   |        |file    |standard, which provides a standardized way to     |
   |        |        |package and distribute type information in Python. |
   +--------+--------+---------------------------------------------------+

Dunder Modules
==============


  .. Dunder-modules-label:
  .. table:: *Dunder-Modules*

   +-----------------------------------------------------------------------------+
   |Dunder Module (Module with leading and trailing double underscores)          |
   +--------------+---------+----------------------------------------------------+
   |Name          |Type     |Description                                         |
   +==============+=========+====================================================+
   |__init__.py   |Package  |Module with no Statements; the module is used to    |
   |              |directory|mark the directory it contains as a package. A dummy| 
   |              |marker   |Module enforces explicit imports and thus clear     |
   |              |file     |namespace use and call them with the dot notation.  |
   +--------------+---------+----------------------------------------------------+
   |__version__.py|Version  |The module consist of Assignment Statements for     |
   |              |file     |system Variables of Versioning                      |
   +--------------+---------+----------------------------------------------------+

Package Modules
===============

The Modules of Package ``ka_uts_obj`` could be classified in the following module types:

#. *Base objects Modules*
#. *Complex objects Modules*
#. *File Modules*
#. *Path Modules*

Base objects Modules
********************

The Base objects Modules of Package ``ka_uts_obj`` are used for the management
of base objects like byte-objects, , num-obj́ects or objects.
The Base objects modules type contains the following modules.

  .. Base-objects-modules-label:
  .. table:: *Base objects Modules*

   +-------+------+-----------------+
   |Name   |Type  |Description      |
   +=======+======+=================+
   |byte.py|TyByte|Byte Manipulation|
   +-------+------+-----------------+
   |num.py |TyNum |Number Management|
   +-------+------+-----------------+
   |obj.py |TyObj |Object Management|
   +-------+------+-----------------+

byte.py (Base objects Module)
=============================

Classes
-------

The Base object Module ``byte.py`` contains the single static class ``Byte``;

byte.py Class: Byte
-------------------

The static Class ``Byte`` contains the subsequent methods

Methods
^^^^^^^

  .. Methods-of-static-class-Byte-label:
  .. table:: *Methods of static class Byte*

   +--------------+-------------------------------------+
   |Name          |Description                          |
   +==============+=====================================+
   |replace_by_dic|replace dictionary-keys found in byte|
   |              |string with corresponding values     |
   +--------------+-------------------------------------+

Byte Method: replace_by_dic
"""""""""""""""""""""""""""

  .. Parameter-of-Byte-method-replace_by_dic-label:
  .. table:: *Parameter of Byte method replace_by_dic*

   +-----------+-------+-------------------------------------------+
   |Name       |Type   |Description                                |
   +===========+=======+===========================================+
   |byte_string|TyBytes|Byte string                                |
   +-----------+-------+-------------------------------------------+
   |dic_replace|TyDic  |Dictionary with replacement keys and values| 
   +-----------+-------+-------------------------------------------+

Complex objects modules
***********************

The Complex objects module type of Package ``ka_uts_obj`` consist of the single module ``poa.py``.

poa.py
======

The Module ``poa.py`` is used to manage Pairs of arrays;

Classes
-------

The Module ``oia.py`` contains contains the single static class ``PoA``.

poa.py Class: PoA
-----------------

The static Class ``PoA`` contains the subsequent methods

PoA Methods
^^^^^^^^^^^ 

Overview
""""""""

  .. Methods-of-static-class-PoA-label:
  .. table:: *Methods of static class PoA*

   +-----------+---------------------------------------------------------+
   |Name       |Description                                              |
   +===========+=========================================================+
   |yield_items|yield items for the given pair of objects and the object.|
   |           |Every item consist of the following elements:            |
   |           +---------------------------------------------------------+
   |           |1. element of the first given array                      |  
   |           |2. element of the second given array                     |
   |           |3. the given object                                      |
   +-----------+---------------------------------------------------------+

PoA Method: yield_items
"""""""""""""""""""""""

  .. Parameter-of-PoA-method-yield_items-label:
  .. table:: *Parameter of PoA method yield_items*

   +----------+--------------+
   |Name|Type |Description   |
   +====+=====+==============+
   |poa |TyPoA|Pair of Arrays|
   +----+-----+--------------+
   |obj |TyAny|Object        | 
   +----+-----+--------------+

File modules
************

The ``File modules`` type of Package ``ka_uts_obj`` consist of the single module ``file.py``.

file.py
=======

The File module ``file.py`` is used for the management of file objects;
it contains the single class ``File``.

file.py Class: File
-------------------

The static Class ``File`` contains the subsequent methods

File Methods
^^^^^^^^^^^^

Overview
""""""""

  .. Methods-of-static-class-File-label:
  .. table:: *Methods of static class File*

   +--------------------+----------------------------------------------------------+
   |Name                |Description                                               |
   +====================+==========================================================+
   |count               |count number of paths that match path_pattern.            |
   +--------------------+----------------------------------------------------------+
   |ex_get_aod_using_fnc|execute get array of dictionaries using the function.     |
   +--------------------+----------------------------------------------------------+
   |ex_get_aod          |execute get array of dictionaries.                        |
   +--------------------+----------------------------------------------------------+
   |ex_get_dod_using_fnc|execute get dictionary of dictionaries using the function.|
   +--------------------+----------------------------------------------------------+
   |ex_get_dod          |execute get dictionary of dictionaries.                   |
   +--------------------+----------------------------------------------------------+
   |get_aod             |get array of dictionaries.                                |
   +--------------------+----------------------------------------------------------+
   |get_dic             |get array of dictionaries and return the first element.   |
   +--------------------+----------------------------------------------------------+
   |get_dod             |get dictionary of dictionaries.                           |
   +--------------------+----------------------------------------------------------+
   |get_paths           |yield paths which match given path pattern.               |
   +--------------------+----------------------------------------------------------+
   |get_latest          |get latest file path that match given path pattern.       |
   +--------------------+----------------------------------------------------------+
   |io                  |apply io function to given path and object.               |
   +--------------------+----------------------------------------------------------+

File Method: count
""""""""""""""""""

Parameter
.........

  .. Parameter-of-File-method-put_aod-label:
  .. table:: *Parameter of File method put_aod*

   +------------+------+------------+
   |Name        |Type  |Description |
   +============+======+============+
   |path_pattern|TyPath|path_pattern|
   +------------+------+------------+

Return Value
............

  .. Return-value-of-File-method-count-label:
  .. table:: *Return value of File method count*

   +----+-----+---------------+
   |Name|Type |Description    |
   +====+=====+===============+
   |    |TyInt|Number pf paths|
   +----+-----+---------------+

File Method: ex_get_aod_using_fnc
"""""""""""""""""""""""""""""""""

Parameter
.........

  .. Parameter-of-File-method-ex_get_aod_using_fnc-label:
  .. table:: *Parameter of File method ex_get_aod_using_fnc*

   +------+----------+-----------------+
   |Name  |Type      |Description      |
   +======+==========+=================+
   |path  |TyPath    |Path             |
   +------+----------+-----------------+
   |fnc   |TyCallable|Object function  |
   +------+----------+-----------------+
   |kwargs|TyDic     |keyword arguments|
   +------+----------+-----------------+

Return Value
............


  .. Return-value-of-File-method-ex_get_aod_using_fnc-label:
  .. table:: *Return value of File method ex_get_aod_using_fnc*

   +----+-----+----------------------+
   |Name|Type |Description           |
   +====+=====+======================+
   |    |TyAoD|Array of Dictionariesy|
   +----+-----+----------------------+

File Method: ex_get_aod
"""""""""""""""""""""""

Parameter
.........

  .. Parameter-of-File-method-ex_get_aod-label:
  .. table:: *Parameter of File method ex_get_aod*

   +------+------+-----------------+
   |Name  |Type  |Description      |
   +======+======+=================+
   |path  |TyPath|Path             |
   +------+------+-----------------+
   |kwargs|TyDic |keyword arguments|
   +------+------+-----------------+

Return Value
............


  .. Return-value-of-IocWPep-method-get-label:
  .. table:: *Return value of IocWbPe method get*

   +----+-----+---------------------+
   |Name|Type |Description          |
   +====+=====+=====================+
   |    |TyAoD|Array of Dictionaries|
   +----+-----+---------------------+

File Method: ex_get_dod_using_fnc
"""""""""""""""""""""""""""""""""

Parameter
.........

  .. Parameter-of-File-method-ex_get_dod_using_fnc-label:
  .. table:: *Parameter of File method ex_get_dod_using_fnc*

   +------+----------+-----------------+
   |Name  |Type      |Description      |
   +======+==========+=================+
   |path  |TyPath    |Path             |
   +------+----------+-----------------+
   |fnc   |TyCallable|Object function  |
   +------+----------+-----------------+
   |key   |TyAny     |Keyword          |
   +------+----------+-----------------+
   |kwargs|TyDic     |Keyword arguments|
   +------+----------+-----------------+

Return Value
............

  .. Return-value-of-File-method-ex_get_dod_using_fnc-label:
  .. table:: *Return value of File method ex_get_dod_using_fnc*

   +----+-----+--------------------------+
   |Name|Type |Description               |
   +====+=====+==========================+
   |    |TyDoD|Dictionary of dictionaries|
   +----+-----+--------------------------+

File Method: ex_get_dod
"""""""""""""""""""""""

Parameter
.........

  .. Parameter-of-File-method-ex_get_dod-label:
  .. table:: *Parameter of File method ex_get_dod*

   +------+------+-----------------+
   |Name  |Type  |Description      |
   +======+======+=================+
   |path  |TyPath|Path             |
   +------+------+-----------------+
   |key   |TyAny |Keyword          |
   +------+------+-----------------+
   |kwargs|TyDic |Keyword arguments|
   +------+------+-----------------+

Return Values
.............

  .. Return-value-of-File-method-ex_get_dod-label:
  .. table:: *Return value of File method ex_get_dod*

   +----+-----+--------------------------+
   |Name|Type |Description               |
   +====+=====+==========================+
   |    |TyDoD|Dictionary of dictionaries|
   +----+-----+--------------------------+

File Method: get_aod
""""""""""""""""""""

Parameter
.........

  .. Parameter-of-File-method-get_aod-label:
  .. table:: *Parameter of File method get_aod*

   +------+----------+-----------------+
   |Name  |Type      |Description      |
   +======+==========+=================+
   |cls   |class     |current class    |
   +------+----------+-----------------+
   |path  |TyPath    |Path             |
   +------+----------+-----------------+
   |fnc   |TyCallable|Object function  |
   +------+----------+-----------------+
   |kwargs|TyDic     |keyword arguments|
   +------+----------+-----------------+

Return Value
............

  .. Return-value-of-File-method-get_aod-label:
  .. table:: *Return value of File method get_aod*

   +----+-----+---------------------+
   |Name|Type |Description          |
   +====+=====+=====================+
   |    |TyDic|Array of Dictionaries|
   +----+-----+---------------------+

File Method: get_dic
""""""""""""""""""""

Parameter
.........

  .. Parameter-of-File-method-get_dic-label:
  .. table:: *Parameter of File method get_dic*

   +------+----------+-----------------+
   |Name  |Type      |Description      |
   +======+==========+=================+
   |cls   |class     |current class    |
   +------+----------+-----------------+
   |path  |TyPath    |Path             |
   +------+----------+-----------------+
   |fnc   |TnCallable|Object function  |
   +------+----------+-----------------+
   |key   |TyStr     |Keyword          |
   +------+----------+-----------------+
   |kwargs|TyDic     |keyword arguments|
   +------+----------+-----------------+

Return Value
............

  .. Return-value-of-File-method-get_dic-label:
  .. table:: *Return value of File method get_dic*

   +----+------+--------------------------+
   |Name|Type  |Description               |
   +====+======+==========================+
   |    |TyDoD |Dictionary of Dictionaries|
   +----+------+--------------------------+

File Method: get_dod
""""""""""""""""""""

Parameter
.........

  .. Parameter-of-File-method-get_dod-label:
  .. table:: *Parameter of Byte method get_dod*

   +------+----------+-----------------+
   |Name  |Type      |Description      |
   +======+==========+=================+
   |obj   |TyAny     |Object           |
   +------+----------+-----------------+
   |path  |TyPath    |Path             |
   +------+----------+-----------------+
   |fnc   |TnCallable|Object function  |
   +------+----------+-----------------+
   |key   |TyStr     |IO function      |
   +------+----------+-----------------+
   |kwargs|TyDic     |keyword arguments|
   +------+----------+-----------------+

Return Value
............

  .. Return-value-of-File-method-get_dod-label:
  .. table:: *Return value of File method get_dod*

   +----+------+--------------------------+
   |Name|Type  |Description               |
   +====+======+==========================+
   |    |TyDoD |Dictionary of Dictionaries|
   +----+------+--------------------------+

File Method: get_latest
"""""""""""""""""""""""

Parameter
.........

  .. Parameter-of-File-method-get_latest-label:
  .. table:: *Parameter of File method get_latest*

   +------------+-----+------------+
   |Name        |Type |Description |
   +============+=====+============+
   |path_pattern|TyStr|Path pattern|
   +------------+-----+------------+

Return Value
............

  .. Return-value-of-File-method-get_latest-label:
  .. table:: *Return value of File method get_latest*

   +----+------+-----------+
   |Name|Type  |Description|
   +====+======+===========+
   |    |TyPath|Path       |
   +----+------+-----------+

File Method: get_paths
""""""""""""""""""""""

Parameter
.........

  .. Parameter-of-File-method-get_paths-label:
  .. table:: *Parameter of File method get_paths*

   +------------+------+-------+----------------+
   |Name        |Type  |Default|Description     |
   +============+======+=======+================+
   |path_pattern|TyPath|       |Path pattern    |
   +------------+------+-------+----------------+
   |sw_recursive|TyBool|None   |Recursive switch|
   +------------+------+-------+----------------+

Return Value
............

  .. Parameter-of-File-method-get_paths-label:
  .. table:: *Parameter of File method get_paths*

   +----+-----+-----------+
   |Name|Type |Description|
   +====+=====+===========+
   |    |TyIoS|yield path |
   +----+-----+-----------+

File Method: io
"""""""""""""""

Parameter
.........

  .. Parameter-of-File-method-io-label:
  .. table:: *Parameter of File method io*

   +----+----------+---------------+
   |Name|Type      |Description    |
   +====+==========+===============+
   |obj |TyObj     |Object         |
   +----+----------+---------------+
   |path|TnPath    |Path           |
   +----+----------+---------------+
   |fnc |TnCallable|Object function|
   +----+----------+---------------+

Path modules
************

The ``Path modules`` type of Package ``ka_uts_obj`` consist of the following modules.

  .. Path-Modules-label:
  .. table:: *Path Modules*

   +-------+------+---------------+
   |Name   |Type  |Description    |
   +=======+======+===============+
   |path.py|TyPath|Path management|
   +-------+------+---------------+

path.py
=======

The module ``path.py`` is used for the management of path objects.

path.py Classes
---------------

The module ``path.py`` contains the single class ``Path``.

path.py Class: Path
-------------------

The static Class ``Path`` contains the subsequent methods

Path Methods
^^^^^^^^^^^^

Overview
""""""""

  .. Methods-of-static-class-Path-label:
  .. table:: *Methods of static class Path*

   +-----------------------------+---------------------------------------------------+
   |Name                         |Description                                        |
   +=============================+===================================================+
   |verify                       |Verify path                                        |
   +-----------------------------+---------------------------------------------------+
   |edit_path                    |put array of _keys found in                        |
   +-----------------------------+---------------------------------------------------+
   |mkdir                        |make directory of directory path                   |
   +-----------------------------+---------------------------------------------------+
   |mkdir_from_path              |make directory of the path, if it's a directory    |
   +-----------------------------+---------------------------------------------------+
   |sh_basename                  |show basename of the path                          |
   +-----------------------------+---------------------------------------------------+
   |sh_components                |split the path into components and show the        |
   |                             |joined components between start- and end-index     |
   +-----------------------------+---------------------------------------------------+
   |sh_component_using_field_name|split the given path into components and show the  |
   |                             |component identified by an index; the index is get |
   |                             |from the given dictionary with the given field name|
   +-----------------------------+---------------------------------------------------+
   |sh_fnc_name_using_pathlib    |extract function name from path with pathlib       |
   +-----------------------------+---------------------------------------------------+
   |sh_fnc_name_using_os_path    |extract function name from path with os.path       |
   +-----------------------------+---------------------------------------------------+
   |sh_last_component            |show last component of path                        |
   +-----------------------------+---------------------------------------------------+
   |sh_path_using_pathnm         |show basename of the path                          |
   +-----------------------------+---------------------------------------------------+
   |sh_path_using_d_path         |replace keys in path by dictionary values          |
   +-----------------------------+---------------------------------------------------+
   |sh_path_using_d_datetype     |show path using path function selected by the given|
   |                             |date type dictionary                               |
   +-----------------------------+---------------------------------------------------+
   |sh_path                      |show path                                          |
   +-----------------------------+---------------------------------------------------+
   |sh_path_first                |show first component of the given path             |
   +-----------------------------+---------------------------------------------------+
   |sh_path_last                 |show last component of the given path              |
   +-----------------------------+---------------------------------------------------+
   |sh_path_now                  |replace now variable in the path by the now date   |
   +-----------------------------+---------------------------------------------------+
   |split_to_array               |split normalized path to array                     |
   +-----------------------------+---------------------------------------------------+

Appendix
********

.. contents:: **Table of Content**
