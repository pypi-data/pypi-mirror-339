##########
ka_uts_dic
##########

Overview
********

.. start short_desc

**Dictionary 'Utilities'**

.. end short_desc

Installation
************

.. start installation

Package ``ka_uts_dic`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_dic

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_dic

.. end installation

Package logging
***************

Standard or user specific Package logging of the package **ka_uts_arr** is defined
in the static logging class **Log_** of Base module log\_.py of the Communication
Package **ka_uts_com**.
The default Logging configuration is defined by the yaml files **log.std.yml**
or **log.usr.yml** in the data directory of the Communication package.
The Logging configuration could be overriden by yaml files with the same names in the
data directory of the application package **ka_uts_arr**.
Logging defines log file paths for the following log message types: .

#. *error*
#. *warning*
#. *info*
#. *log*
#. *debug*

  .. Naming-conventions-for-logging-files-label:
  .. table:: *Naming conventions for logging file*

   +-------+--------------------------------------------+-------------------+
   |Type   |Directory                                   |File               |
   +=======+============================================+===================+
   |error  |/data/<tenant>/RUN/<package>/<function>/errs|errs_<pid>_<ts>.log|
   +-------+--------------------------------------------+-------------------+
   |warning|/data/<tenant>/RUN/<package>/<function>/errs|wrns_<pid>_<ts>.log|
   +-------+--------------------------------------------+-------------------+
   |info   |/data/<tenant>/RUN/<package>/<function>/logs|infs_<pid>_<ts>.log|
   +-------+--------------------------------------------+-------------------+
   |log    |/data/<tenant>/RUN/<package>/<function>/logs|logs_<pid>_<ts>.log|
   +-------+--------------------------------------------+-------------------+
   |debug  |/data/<tenant>/RUN/<package>/<function>/debs|debs_<pid>_<ts>.log|
   +-------+--------------------------------------------+-------------------+

  .. Example-of-Naming-conventions-for-logging-files-label:
  .. table:: *Example of Naming conventions for logging files*

   +-------+-------------------------------+------------------------+
   |Type   |Directory                      |File                    |
   +=======+===============================+========================+
   |error  |/data/umh/RUN/otec_xls_srr/errs|errs_9470_1737118199.log|
   +-------+-------------------------------+------------------------+
   |warning|/data/umh/RUN/otec_xls_srr/errs|wrns_9470_1737118199.log|
   +-------+-------------------------------+------------------------+
   |info   |/data/umh/RUN/otec_xls_srr/logs|infs_9470_1737118199.log|
   +-------+-------------------------------+------------------------+
   |log    |/data/umh/RUN/otec_xls_srr/logs|logs_9470_1737118199.log|
   +-------+-------------------------------+------------------------+
   |debug  |/data/umh/RUN/otec_xls_srr/debs|debs_9470_1737118199.log|
   +-------+-------------------------------+------------------------+

Package files
*************

Classification
==============

The Files of Package ``ka_uts_dic`` could be classified into the follwing file types:

#. *Special files*
#. *Dunder modules*
#. *Package modules*

Special files
*************

  .. Special-python-specific-files-elabel:
  .. table:: **Special python specific files**

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

   +--------------+---------+----------------------------------------------------+
   |Name          |Type     |Description                                         |
   +==============+=========+====================================================+
   |__init__.py   |Package  |The module is used to execute initialisation code or|
   |              |directory|mark the directory it contains as a package. The    | 
   |              |marker   |Module enforces explicit imports and thus clear     |
   |              |file     |namespace use and call them with the dot notation.  |
   +--------------+---------+----------------------------------------------------+
   |__version__.py|Version  |The module consist of Assignment Statements for     |
   |              |file     |system Variables used in Versioning.                |
   +--------------+---------+----------------------------------------------------+

Package Modules
***************

Classification
==============

The Modules of Package ``ka_uts_dic`` could be classified into the following module types:

#. **Module for Dictionaries**
#. **Modules for Dictionaries of Dictionaries**
#. **Modules for Dictionaries of Arrays**
#. **Modules for Dictionaries of Objects**

Modules for Dictionaries
************************

  .. Management-Modules-for-Dictionary-label:
  .. table:: *Management Modules for Dictionary*

   +------+------------------------+
   |Name  |Description             |
   +======+========================+
   |dic.py|Management of Dictionary|
   +------+------------------------+

Module: dic.py
==============

Classes
-------

The Module ``dic.py`` contains the followinga static classes:

   +----+--------------------------+
   |Name|Description               |
   +====+==========================+
   |Arr |Management of Arrays      |
   +----+--------------------------+
   |Dic |Management of Dictionaries|
   +----+--------------------------+

Class: Arr
----------

The static Class ``Arr`` is used to manage Arrays used for flattening of dictionaries;
it contains the subsequent methods.

Arr Methods
^^^^^^^^^^^

  .. Arr-Methods-label:
  .. table:: *Arr Methods*

   +---------------------+------------------------------------------------------+
   |Name                 |Description                                           |
   +=====================+======================================================+
   |flatten_merge_to_aod |Type-dependent flattening of array elements to arrays |
   |                     |of dictionaries and merging of these arrays.          |
   +---------------------+------------------------------------------------------+
   |flattenx_keys        |show last key or concatinate keys with separator of   |
   |                     |flatten-dictionary if concatination is requested      |
   |                     |by given switch defined in flatten-dictionary.        |
   +---------------------+------------------------------------------------------+
   |flattenx_merge_to_aod|Type-dependent extended flattening of array elements  |
   |                     |to arrays of dictionaries and merging of these arrays.|
   +---------------------+------------------------------------------------------+

Class: Dic
----------

The static Class ``Dic`` is used to manage Dictionaries;
The Methods of Class ``Dic`` could be classified into the following method types:

#. *Miscellenous Methods*
#. *Flatten Methods*
#. *Set Methods*
#. *Get / Show Methods*
#. *Split Methods*
#. *Yield Methods*

Miscellenous Methods
^^^^^^^^^^^^^^^^^^^^

  .. Miscellenous-Methods-of-class-Dic-label:
  .. table:: *Miscellenous Methods of class Dic*

   +------------------------+----------------------------------------------------------+
   |Name                    |Description                                               |
   +========================+==========================================================+
   |add_counter_to_values   |Apply the function "add_counter_with key" to the last key |
   |                        |of the key list and the Dictionary localized by that key. |
   +------------------------+----------------------------------------------------------+
   |add_counter_to_value    |Initialize the unintialized counter with 1 and add it to  |
   |                        |the Dictionary value of the key.                          |
   +------------------------+----------------------------------------------------------+
   |append_to_values        |Apply the function "append with key" to the last key of   |
   |                        |the key list amd the Dictionary localized by that key.    |
   +------------------------+----------------------------------------------------------+
   |append_to_value         |Initialize the unintialized counter with 1 and add it to  |
   |                        |the Dictionary value of the key.                          |
   +------------------------+----------------------------------------------------------+
   |change_keys_by_keyfilter|Change the keys of the Dictionary by the values of the    |
   |                        |keyfilter Dictionary with the same keys.                  |
   +------------------------+----------------------------------------------------------+
   |copy                    |Copy the value for keys from source to target dictionary. |
   +------------------------+----------------------------------------------------------+
   |extend_values           |Appply the function "extend_by_key" to the last key of the|
   |                        |key list and the dictionary localized by that key.        |
   +------------------------+----------------------------------------------------------+
   |extend_value            |Add the item with the key as element to the dictionary if |
   |                        |the key is undefined in the dictionary. Extend the element|
   |                        |value with the value if both supports the extend function.|
   +------------------------+----------------------------------------------------------+
   |increment_values        |Appply the function "increment_by_key" to the last key of |
   |                        |the key list and the Dictionary localized by that key.    |
   +------------------------+----------------------------------------------------------+
   |increment_value         |Increment the value of the key if it is defined in the    |
   |                        |Dictionary, otherwise assign the item to the key          |
   +------------------------+----------------------------------------------------------+
   |is_not                  |Return False if the key is defined in the Dictionary and  |
   |                        |the key value if not empty, othewise returm True.         |
   +------------------------+----------------------------------------------------------+
   |locate                  |Return the value of the key reached by looping thru the   |
   |                        |nested Dictionary with the keys from the key list until   |
   |                        |the value is None or the last key is reached.             |
   +------------------------+----------------------------------------------------------+
   |locate_last_value       |Apply the locate function for the key list which contains |
   |                        |all items except the last one.                            |
   +------------------------+----------------------------------------------------------+
   |lstrip_keys             |Remove the first string found in the Dictionary keys.     |
   +------------------------+----------------------------------------------------------+
   |merge                   |Merge two Dictionaries.                                   |
   +------------------------+----------------------------------------------------------+
   |new                     |create a new dictionary from keys and values.             |
   +------------------------+----------------------------------------------------------+
   |normalize_value         |Replace every Dictionary value by the first list element  |
   |                        |of the value if it is a list with only one element.       |
   +------------------------+----------------------------------------------------------+
   |nvl                     |Return the Dictionary if it is not None otherwise return  |
   |                        |the empty Dictionary "{}".                                |
   +------------------------+----------------------------------------------------------+
   |rename_key_using_kwargs |Rename old Dictionary key with new one get from kwargs.   |
   +------------------------+----------------------------------------------------------+
   |replace_string_in_keys  |Replace old string contained in keys with new one.        |
   +------------------------+----------------------------------------------------------+
   |rename_key              |Rename old Dictionary key with new one.                   |
   +------------------------+----------------------------------------------------------+
   |round_values            |Round values selected by keys,                            |
   +------------------------+----------------------------------------------------------+
   |to_aod                  |Convert dictionary to array of dictionaries.              |
   +------------------------+----------------------------------------------------------+


Flatten Methods
^^^^^^^^^^^^^^^

  .. Flatten-Methods-of-class-Dic-label:
  .. table:: *Flatten Methods of class Dic*

   +------------------+-------------------------------------------------------------------+
   |Name              |Description                                                        |
   +==================+===================================================================+
   |flatten_to_aod    |Flatten dictionary to array of dictionaries                        |
   +------------------+-------------------------------------------------------------------+
   |flatten_using_d2p |Flatten dictionary nded flattening of array elements               |
   +------------------+-------------------------------------------------------------------+
   |flatten           |Flatten dictionary                                                 |
   +------------------+-------------------------------------------------------------------+
   |flattenx_to_aod   |Flatten dictionary in array of dictionaries in extended mode.      |
   +------------------+-------------------------------------------------------------------+
   |flattenx_using_d2p|Type-dependent extended flattening of array elements               |
   +------------------+-------------------------------------------------------------------+
   |flattenx          |Flatten dictionary in extended mode                                |
   +------------------+-------------------------------------------------------------------+

Get / Show Methods
^^^^^^^^^^^^^^^^^^

  .. Get-Show-Methods-of-class-Dic-label:
  .. table:: *Get Show Methods class Dic*

   +-------------------+-------------------------------------------------------------------+
   |Name               |Description                                                        |
   +===================+===================================================================+
   |get                |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |get_yn_value       |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_dic             |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_d_filter        |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_d_index_d_values|Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_d_vals_d_cols   |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_prefixed        |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_keys            |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |show_sorted_keys   |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_value           |Show value of dictionary element selected by keys                  |
   +-------------------+-------------------------------------------------------------------+
   |sh_values          |Convert the dictionary into an array by using a key filter.        |
   |                   |The array elements are the values of all dictionary elements       |
   |                   |where the key is the given single key or where the key is contained|
   |                   |in the key list.                                                   |
   +-------------------+-------------------------------------------------------------------+
   |sh_value2keys      |Convert the dictionary to a new dictionary by using the values as  |
   |                   |new keys and all keys mapped to the same value as new value.       |
   +-------------------+-------------------------------------------------------------------+

Set Methods
^^^^^^^^^^^

  .. Set-Methods-of-class-Dic-label:
  .. table:: *Set Methods of class Dic*

   +-----------------------------------------+-------------------------------------------------------------------+
   |Name                                     |Description                                                        |
   +=========================================+===================================================================+
   |set                                      |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_kv_not_none                          |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_by_keys                              |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_by_key_pair                          |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_if_none                              |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_by_div                               |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_divide                               |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_first_tgt_with_src_using_d_tgt2src   |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_format_value                         |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_multiply_with_factor                 |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_tgt_with_src                         |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_tgt_with_src_using_doaod_tgt2src     |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_nonempty_tgt_with_src_using_d_tgt2src|                                                                   |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_tgt_with_src_using_d_src2tgt         |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+
   |set_tgt_with_src_using_d_tgt2src         |Type-dependent extended flattening of array elements               |
   +-----------------------------------------+-------------------------------------------------------------------+

Split Methods
^^^^^^^^^^^^^

  .. Split-Methods-of-class-Dic-label:
  .. table:: *Split Methods of class Dic*

   +----------------------+----------------------------------------------------------------------------+
   |Name                  |Description                                                                 |
   +======================+============================================================================+
   |split_by_value_endwith|Split the dictionary into a tuple of dictionaries using the the condition   |
   |                      |"the element value ends with the given value".                              |
   |                      |The first tuple element is the dictionary of all dictionary                 |
   |                      |elements whose value ends with the given value; the second one is           |
   |                      |the dictionary of the other elements.                                       |
   +----------------------+----------------------------------------------------------------------------+
   |split_by_value        |Split the dictionary into a tuple of dictionaries using the given value. The|
   |                      |first tuple element is the dictionary of all elements whose value is equal  |
   |                      |to the given value; the second one is the dictionary of the other elements. |
   +----------------------+----------------------------------------------------------------------------+
   |split_by_value_is_int |Split the dictionary into a tuple of dictionaries using the condition       |
   |                      |"the element value is of type integer". The first tuple element is the      |
   |                      |dictionary of all elements whose value is of type integer; the second one is| 
   |                      |the dictionary of the other elements.                                       |
   +----------------------+----------------------------------------------------------------------------+

Yield Methods
^^^^^^^^^^^^^

  .. Yield-Methods-of-class-Dic-label:
  .. table:: *Yield Methods of class Dic*

   +---------------------------+----------------------------------------------------------------------------+
   |Name                       |Description                                                                 |
   +===========================+============================================================================+
   |yield_values_with_keyfilter|Yield the values of all elements which are selected by the given key filter.|
   +---------------------------+----------------------------------------------------------------------------+

Modules for Dictionaries of Dictionaries
****************************************

  .. Modules-for-Dictionary-of-Dictionaries-label:
  .. table:: *Modules for Dictionary of Dictionaries*

   +------+-------------------------------------------------------+
   |Name  |Description                                            |
   +======+=======================================================+
   |dod.py|Management of Dictionary of Dictionaries.              |
   +------+-------------------------------------------------------+
   |d2v.py|Management of 2-dimensional Dictionary of Dictionaries.|
   |      |A 2 dimensional Dictionary of Dictionaries contains    |
   |      |dictionaries of Dictionaries as values.                |
   +------+-------------------------------------------------------+
   |d3v.py|Management of 3-dimensional Dictionary of Dictionaries.|
   |      |A 3 dimensional Dictionary of Dictionaries contains    |
   |      |Dictionaries of Dictionaries of Dictionaries as values.|
   +------+-------------------------------------------------------+

Modules for Dictionaries of Arrays
**********************************

  .. Modules-for-Dictionaryies-of-Arrays-label:
  .. table:: *Modules for Dictionaries of Arrays*

   +--------+---------------------------------------------------+
   |Name    |Description                                        |
   +========+===================================================+
   |doaod.py|Management of Dictionary of Arrays of Dictionaries.|
   +--------+---------------------------------------------------+
   |doa.py  |Management of Dictionary of Arrays.                |
   +--------+---------------------------------------------------+

Module doaod.py
===============

Classes
-------

The Module ``doaoa.py`` contains the static class ``DoAoD``:

Class DoAoD
-----------

The static Class ``DoAoD`` is used to manage ``Dictionary of Arrays of Dictionaries``;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoAoD-label:
  .. table:: *Methods-of-class-DoAoD*

   +------------------+-------------------------------------------------------+
   |Name              |Description                                            |
   +==================+=======================================================+
   |dic_value_is_empty|Check if all keys of the given Dictionary of Arrays of |
   |                  |Dictionaries are found in any Dictionary of the Array  |
   |                  |of Dictionaries and the value for the key is not empty.|
   +------------------+-------------------------------------------------------+
   |sh_aod_unique     |Convert Dictionary of Array of Dictionaries to unique  |
   |                  |Array of Dictionaries.                                 |
   +------------------+-------------------------------------------------------+
   |sh_aod            |Convert Dictionary of Array of Dictionaries to Array   |
   |                  |of Dictionaries.                                       |
   +------------------+-------------------------------------------------------+
   |sh_unique         |Convert Dictionary of Array of Dictionaries to         |
   |                  |Dictionaries of unique Array of Dictionaries.          |
   +------------------+-------------------------------------------------------+
   |union_by_keys     |Convert filtered Dictionary of Arrays of Dictionaries  |
   |                  |by keys to an Array of distinct Dictionaries           |
   +------------------+-------------------------------------------------------+
   |union             |Convert Dictionary of Arrays of Dictionaries to an     |
   |                  |Array of distinct Dictionaries                         |
   +------------------+-------------------------------------------------------+

Module doa.py
=============

Classes
-------

The Module ``doa.py`` contains the static classes ``DoA``:

Class DoA
---------

The static Class ``DoA`` is used to manage Arrays used for the flattening of dictionaries;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoA-label:
  .. table:: *Methods of class DoA*

   +-------------+------------------------------------------------------+
   |Name         |Description                                           |
   +=============+======================================================+
   |apply        |                                                      |
   +-------------+------------------------------------------------------+
   |append       |                                                      |
   +-------------+------------------------------------------------------+
   |append_by_key|                                                      |
   +-------------+------------------------------------------------------+
   |append_unique|                                                      |
   +-------------+------------------------------------------------------+
   |extend       |                                                      |
   +-------------+------------------------------------------------------+
   |set          |                                                      |
   +-------------+------------------------------------------------------+
   |sh_d_pddf    |                                                      |
   +-------------+------------------------------------------------------+
   |sh_union     |                                                      |
   +-------------+------------------------------------------------------+

Modules for Dictionaries of Dictionaries
**************************+++++++*******

  .. Modules-for-Dictionaries-of-Dictionaries-label:
  .. table:: *Modules for Dictionaries of Dictionaries*

   +--------+---------------------------------------------------------+
   |Name    |Description                                              |
   +========+=========================================================+
   |dodoa.py|Management of Dictionary of Dictionaries of Arrays.      |
   +--------+---------------------------------------------------------+
   |dodod.py|Management of Dictionary of Dictionaries of Dictionaries.|
   +--------+---------------------------------------------------------+
   |dod.py  |Management of Dictionary of Dictionaries.                |
   +--------+---------------------------------------------------------+

Module dodoa.py
===============

Classes
-------

The Module ``dodoa.py`` contains the static class ``DoDoA``:

Class DoDoA
-----------

The static Class ``DoDoA`` is used to manage Dictionary of Dictionaries of Arrays;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoDoA-label:
  .. table:: *Methods of class DoDoA*

   +-------------+------------------------------------------------------+
   |Name         |Description                                           |
   +=============+======================================================+
   |append       |                                                      |
   +-------------+------------------------------------------------------+
   |sh_union     |                                                      |
   +-------------+------------------------------------------------------+

Module dodod.py
===============

Classes
-------

The Module ``dodod.py`` contains the static Class ``DoDoD``:

Class DoDoD
-----------

The static Class ``DoDoD`` is used to manage Dictionary of Dictionaries of Dictionaries;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoDoD-label:
  .. table:: *Methods of class DoDoD*

   +------------+------------------------------------------------------+
   |Name        |Description                                           |
   +============+======================================================+
   |set         |                                                      |
   +------------+------------------------------------------------------+
   |yield_values|                                                      |
   +------------+------------------------------------------------------+

Module: dod.py
==============

Classes
-------

The Module ``dod.py`` contains the static Class ``DoD``:


Class DoD
---------

The static Class ``DoD`` is used to manage ``Dictionary of Dictionaries``;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of_class-DoD-label:
  .. table:: *DoD Methods*

   +---------------+-------------------------------------------------------+
   |Name           |Description                                            |
   +===============+=======================================================+
   |nvl            |Return the Dictionary of Dictionaries if it is not None|
   |               |otherwise return the empty Dictionary "{}".            |
   +---------------+-------------------------------------------------------+
   |replace_keys   |Recurse through the Dictionary while building a new one|
   |               |with new keys and old values; the old keys are         |
   |               |translated to new ones by the keys Dictionary.         |
   +---------------+-------------------------------------------------------+
   |yield_values   |                                                       |
   +---------------+-------------------------------------------------------+

Module: dodows.py
=================

Classes
-------

The Module ``dodows.py`` contains the static Class ``DoDoWs``:

Class: DoDoWs
-------------

The static Class ``DoDoWs`` is used to manage ``Dictionary of Dictionaries of Worksheets``;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoDoWs-label:
  .. table:: *Methods of class DoDoWs*

   +--------------+------------------------------------------------------------------+
   |Name          |Description                                                       |
   +==============+==================================================================+
   |write_workbook|Write a workbook using a Dictionary of Dictionaries of worksheets.|
   +--------------+------------------------------------------------------------------+

Modules for Dictionaries of Ojects
**********************************

Modules
=======

The Module Type ``Modules for Dictionaries of Objects`` contains the following Modules:

  .. Management-Modules-for-Dictionaries-of-Ojects-label:
  .. table:: *Management Modules for Dictionaries of Ojects*

   +------+------------------------------------+
   |Name  |Description                         |
   +======+====================================+
   |doo.py|Management of Dictionary of Objects.|
   +------+------------------------------------+

Module doo.py
=============

Classes
-------

The Module ``doo.py`` contains the static Classes ``DoO``.


Class DoO
---------

The static Class ``DoO`` is used to manage ``Dictionary of Objects``;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoO-label:
  .. table:: *Methods of class DoO*

   +------------+---------------------------------------------------------------+
   |Name        |Description                                                    |
   +============+===============================================================+
   |replace_keys|Replace the keys of the given Dictionary by the values found in|
   |            |the given keys Dictionary if the values are not Dictionaries;  |
   |            |otherwise the function is called with these values.            |
   +------------+---------------------------------------------------------------+

Modules for Dictionaries of Dataframes
**************************************

Modules
=======

The Module Type ``Modules for Dictionaries of Dataframes`` contains the following Modules:

  .. Management Modules for Dictionary of Dataframes-label:
  .. table:: *Management Modules for Dictionary of Dataframes*

   +---------+----------------------------------------------+
   |Name     |Description                                   |
   +=========+==============================================+
   |dopddf.py|Management of Dictionary of Panda Dataframes. |
   +---------+----------------------------------------------+
   |dopldf.py|Management of Dictionary of Polars Dataframes.|
   +---------+----------------------------------------------+

Classes
-------

The Module ``dopddf.py`` contains the static Class ``DoPdDf``.


Class DoPdDf
------------

The static Class ``DoPdDf`` is used to manage ``Dictionaries of Panda Dataframes``;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoPdDf-label:
  .. table:: *Methodsc of class DoPdDf*

   +----------------------+-----------------------------------------------------+
   |Name                  |Description                                          |
   +======================+=====================================================+
   |set_ix_drop_key_filter|Apply Function set_ix_drop_col_filter to all Panda   |
   |                      |Dataframe values of given Dictionary.                |
   +----------------------+-----------------------------------------------------+
   |to_doaod              |Replace NaN values of Panda Dataframe values of given|
   |                      |Dictionary and convert them to Array of Dictionaries.|
   +----------------------+-----------------------------------------------------+

Module dopldf.py
=================

Classes
-------

The Module ``dopldf.py`` contains the static Classes ``DoPlDf``:


Class DoPlDf
------------

The static Class ``DoPlDf`` is used to manage ``Dictionary of Polars Dataframes``;
it contains the subsequent Methods.

Methods
^^^^^^^

  .. Methods-of-class-DoPlDf-label:
  .. table:: *Methods of class DoPlDf*

   +--------+------------------------------------------------------+
   |Name    |Description                                           |
   +========+======================================================+
   |to_doaod|Replace NaN values of Polars Dataframe values of given|
   |        |Dictionary and convert them to Array of Dictionaries. |
   +--------+------------------------------------------------------+

Appendix
********

.. contents:: **Table of Content**
