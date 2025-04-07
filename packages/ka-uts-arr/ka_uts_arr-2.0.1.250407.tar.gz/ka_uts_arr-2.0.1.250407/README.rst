##########
ka_uts_arr
##########

Overview
********

.. start short_desc

**Array Utilities**

.. end short_desc

Installation
************

.. start installation

Package ``ka_uts_array`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_arr

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_arr

.. end installation

Package logging
***************

Standard or user specific Package logging of the package **ka_uts_arr** is defined 
in the static logging class **Log_** of Base module log\_.py of the Communication
Package **ka_uts_com**.
The default Logging configuration is defined by the yaml files **log.std.yml**
or **log.usr.yml** in the data directory **ka_uts_com/data** of the Communication package.
The Logging configuration could be overriden by yaml files with the same names in the
data directory **ka_uts_arr/data** of the application package **ka_uts_arr**.

Logging defines log file paths for the following log message types: .

#. *error*
#. *warning*
#. *info*
#. *log*
#. *debug*

  .. Naming-conventions-for-logging-files-label:
  .. table:: *Naming conventions for logging file*

   +-----+--------------------------------------------+-------------------+
   |Type |Directory                                   |File               |
   +=====+============================================+===================+
   |error|/data/<tenant>/RUN/<package>/<function>/errs|errs_<pid>_<ts>.log|
   +-----+--------------------------------------------+-------------------+
   |info |/data/<tenant>/RUN/<package>/<function>/logs|info_<pid>_<ts>.log|
   +-----+--------------------------------------------+-------------------+
   |log  |/data/<tenant>/RUN/<package>/<function>/logs|logs_<pid>_<ts>.log|
   +-----+--------------------------------------------+-------------------+
   |debug|/data/<tenant>/RUN/<package>/<function>/debs|debs_<pid>_<ts>.log|
   +-----+--------------------------------------------+-------------------+

  .. Naming examples-of-logging-files-label:
  .. table:: *Naming examples of logging file*

   +-----+-------------------------------+------------------------+
   |Type |Directory                      |File                    |
   +=====+===============================+========================+
   |error|/data/umh/RUN/umh_otec/srr/errs|errs_9470_1737118199.log|
   +-----+-------------------------------+------------------------+
   |info |/data/umh/RUN/umh_otec/srr/logs|info_9470_1737118199.log|
   +-----+-------------------------------+------------------------+
   |log  |/data/umh/RUN/umh_otec/srr/logs|logs_9470_1737118199.log|
   +-----+-------------------------------+------------------------+
   |debug|/data/umh/RUN/umh_otec/srr/debs|debs_9470_1737118199.log|
   +-----+-------------------------------+------------------------+

Package files
*************

Classification
==============

The Files of Package ``ka_uts_arr`` could be classified into the follwing file types:

#. *Special files*
#. *Dunder modules*
#. *Package modules*

Special files
=============

  .. Special-file-label:
  .. table:: **Special-file**

   +--------+--------+-------------------------------------------------------------+
   |Name    |Type    |Description                                                  |
   +========+========+=============================================================+
   |py.typed|Type    |The py.typed file is a marker file used in Python packages to|
   |        |checking|indicate that the package supports type checking. This is a  |
   |        |marker  |part of the PEP 561 standard, which provides a standardized  |
   |        |file    |way to package and distribute type information in Python.    |
   +--------+--------+-------------------------------------------------------------+

Dunder Modules
==============

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
===============

Overview
--------

The Modules of Package ``ka_uts_arr`` could be classified into the follwing module types:

#. *Module for Arrays*
#. *Module for Arrays of Arrays*
#. *Modules for Arrays of Dictionaries*
#. *Modules for arrays of basic objects*

Modules for array of dictionaries
*********************************

  .. Modules-for-array-of-data-structures-label:
  .. table:: **Modules-for-array-of-data-structures**

   +--------+-----------------------------------+
   |Name    |Description                        |
   +========+===================================+
   |aoa.py  |Array of arrays                    |
   +--------+-----------------------------------+

Module: aoa.py
==============

Classes
-------

The Module ``aoa.py`` contains the single static class ``AoA``;

aoa.py Class: AoA
-----------------

The static Class ``AoA`` contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-AoA-label:
  .. table:: *Methods of class AoA*

   +-----------------+-----------------------------------------+
   |Name             |Short description                        |
   +=================+=========================================+
   |concatinate      |Concatinate all arrays of array of arrays|
   +-----------------+-----------------------------------------+
   |csv_writerows    |Write array of arrays to csv file        |
   +-----------------+-----------------------------------------+
   |nvl              |Replace empty array of arrays            |
   +-----------------+-----------------------------------------+
   |to_aod           |Convert array of arrays to array of      |
   |                 |dictionaries using an array of keys      |
   +-----------------+-----------------------------------------+
   |to_arr_from_2cols|Convert array of arrays to array using   |
   |                 |a 2-dimensional index array              |
   +-----------------+-----------------------------------------+
   |to_doa_from_2cols|Convert array of arrays to dictionary of |
   |                 |arrays using a 2-dimensionl index array  |
   +-----------------+-----------------------------------------+
   |to_dic_from_2cols|Convert array of arrays to dictionary by |
   |                 |using a 2-dimensional index array        |
   +-----------------+-----------------------------------------+

Method: concatinate
^^^^^^^^^^^^^^^^^^^

Description
...........

Concatinate all arrays of array of arrays.

Parameter
.........

  .. Parameter-of-method-concatinate-label:
  .. table:: **Parameter of method concatinate**

   +-------+-----+-------+---------------+
   |Name   |Type |Default|Description    |
   +=======+=====+=======+===============+
   |aoa    |TyAoA|       |Array of arrays|
   +-------+-----+-------+---------------+

Return Value
............

  .. Return-Value-method-concatinate-label:
  .. table:: **Return Value of method concatinate**

   +-------+-----+-----------+
   |Name   |Type |Description|
   +=======+=====+===========+
   |arr_new|TyArr|new array  |
   +-------+-----+-----------+

Method: csv_writerows
^^^^^^^^^^^^^^^^^^^^^

Description
...........

Write Array of Arrays to Csv file defined by the path string 
using the function "writerows" of module "csv".

Parameter
.........

  .. Parameter-of-method-csv_writerows-label:
  .. table:: **Parameter of method csv_writerows**

   +------+------+-------+----------------+
   |Name  |Type  |Default|Description     |
   +======+======+=======+================+
   |aoa   |TyAoA |       |Array of arrays |
   +------+------+-------+----------------+
   |path  |TyPath|       |Path string     |
   +------+------+-------+----------------+
   |kwargs|TyDic |       |Keyword aruments|
   +------+------+-------+----------------+

Return Value
............

  .. Return-Value-of-method-csv_writerows-label:
  .. table:: **Parameter/Return Value of method csv_writerows**

   +------+------+----------------+
   |Name  |Type  |Description     |
   +======+======+================+
   |      |None  |                |
   +------+------+----------------+

method: nvl
^^^^^^^^^^^

Description
...........

Return the empty array if the Array of Arrays is None.

Parameter
.........

  .. Parameter-of-method-nvl-label:
  .. table:: *Parameter of method nvl*

   +-------+-----+-------+-------------------+
   |Name   |Type |Default|Description        |
   +=======+=====+=======+===================+
   |aoa    |TyAoA|       |Array of arrays    |
   +-------+-----+-------+-------------------+

Return Value
............

  .. Return-Value-of-method-nvl-label:
  .. table:: *Return Value of method nvl*

   +-------+-----+-------------------+
   |Name   |Type |Description        |
   +=======+=====+===================+
   |aoa_new|TyAoA|new Array of arrays|
   +-------+-----+-------------------+

Method: to_aod
^^^^^^^^^^^^^^

Description
...........

Convert array of arrays to array of Dictionaries.

Parameter
.........

  .. Parameter-of-method-to_aod-label:
  .. table:: **Parameter of method to_aod**

   +----+-----+-------+---------------+
   |Name|Type |Default|Description    |
   +====+=====+=======+===============+
   |aoa |TyAoA|       |Array of arrays|
   +----+-----+-------+---------------+
   |keys|TyArr|       |Array of keys  |
   +----+-----+-------+---------------+

Return Value
............

  .. Return-Value-of-method-to_aod-label:
  .. table:: **Return Value of method to_aod**

   +----+-----+---------------------+
   |Name|Type |Description          |
   +====+=====+=====================+
   |aod |TyAoD|array of dictionaries|
   +----+-----+---------------------+

method: to_arr_from_2cols
^^^^^^^^^^^^^^^^^^^^^^^^^

Description
...........

Convert Array of Arrays to unique array with distinct elements by
selecting 2 columns of each Array as elements of the new array using a
2-dimensional index-array.

Parameter
.........

  .. Parameter-of-method-to_arr_from_2cols-label:
  .. table:: **Parameter of method to_arr_from_2cols**

   +----+-----+-------+----------------+
   |Name|Type |Default|Description     |
   +====+=====+=======+================+
   |aoa |TyAoA|       |Array of arrays |
   +----+-----+-------+----------------+
   |a_ix|TyAoI|       |Array of integer|
   +----+-----+-------+----------------+

Return Value
............

  .. Return-Value-of-method-to_arr_from_2cols-label:
  .. table:: **Return Value of method to_arr_from_2cols**

   +----+-----+-------------------+
   |Name|Type |Description        |
   +====+=====+===================+
   |arr |TyArr|Array              |
   +----+-----+-------------------+

method: to_doa_from_2cols
^^^^^^^^^^^^^^^^^^^^^^^^^

Description
...........

Convert array of arrays to dictionary of unique arrays (array with distinct elements)

#. Select 2 columns of each array as key-, value-candidates of the new dictionary
   using a 2-dimensional index-array. 

#. If the new key exists then 
   the new value extends the key value as unique array, 
   
# otherwise
   the new value is assigned as unique array to the key.

Parameter
.........

  .. Parameter-of-method-to_doa_from_2cols-label:
  .. table:: **Parameter of method to_doa_from_2cols**

   +----+-----+-------+----------------+
   |Name|Type |Default|Description     |
   +====+=====+=======+================+
   |aoa |TyAoA|       |Array of arrays |
   +----+-----+-------+----------------+
   |a_ix|TyAoI|       |Array of integer|
   +----+-----+-------+----------------+

Return Value
............

  .. Return-Value-of-method-to_doa_from_2cols-label:
  .. table:: **Return Value of method to_doa_from_2cols**

   +----+-----+-------------------+
   |Name|Type |Description        |
   +====+=====+===================+
   |doa |TyDoA|Dictionry of arrays|
   +----+-----+-------------------+

Method: to_dic_from_2cols
^^^^^^^^^^^^^^^^^^^^^^^^^

Description
...........

Convert array of arrays to dictionary by selecting 2 columns of each array as
key-, value-candidates of the new dictionary if the key is not none using a
2-dimensional index-array.

Parameter
.........

  .. Parameter-of-method-to_dic_from_2cols-label:
  .. table:: **Parameter of method to_dic_from_2cols**

   +----+-----+-------+----------------+
   |Name|Type |Default|Description     |
   +====+=====+=======+================+
   |aoa |TyAoA|       |Array of arrays |
   +----+-----+-------+----------------+
   |a_ix|TyAoI|       |Array of integer|
   +----+-----+-------+----------------+

Return Value
............

  .. Return-Value-of-method-to_dic_from_2cols-label:
  .. table:: **Return Value of method to_dic_from_2cols**

   +----+-----+-----------+
   |Name|Type |Description|
   +====+=====+===========+
   |dic |TyDic|Dictionary |
   +----+-----+-----------+

Modules for array of dictionaries
*********************************

  .. Modules-for-array-of-data-structures-label:
  .. table:: **Modules-for-array-of-data-structures**

   +--------+-----------------------------------+
   |Name    |Description                        |
   +========+===================================+
   |aod2p.py|Array of 2-dimensional dictionaries|
   +--------+-----------------------------------+
   |aod.py  |Array of dictionaries              |
   +--------+-----------------------------------+

aod.py
======

The Module ``aod.py`` contains the single static class ``AoD``;

aod.py class: AoD
-----------------

Methods
^^^^^^^

  .. AoD-methods-label:
  .. table:: *AoD-methods*

   +------------------------------------+----------------------------------------------+
   |Name                                |Short description                             |
   +====================================+==============================================+
   |add                                 |Add object to array of dictionaries.          |
   +------------------------------------+----------------------------------------------+
   |apply_function                      |Apply function to array of dictionaries       |
   +------------------------------------+----------------------------------------------+
   |csv_dictwriterows                   |Write array of dictionaries to csv file       |
   |                                    |with function dictwriterows.                  |
   +------------------------------------+----------------------------------------------+
   |dic_found_with_empty_value          |Return True or raise an exception if the arr. |
   |                                    |of dicts. contains a dict. with empty value   |
   |                                    |and the execption switch is True.             |
   +------------------------------------+----------------------------------------------+
   |extend_if_not_empty                 |Extend array of dicts. with non empty dict.   |
   +------------------------------------+----------------------------------------------+
   |join_aod                            |Join elements of array of dicts.              |
   +------------------------------------+----------------------------------------------+
   |merge_dic                           |Merge elements of array of dicts.             |
   +------------------------------------+----------------------------------------------+
   |nvl                                 |Replace empty array of dicts.                 |
   +------------------------------------+----------------------------------------------+
   |pd_to_csv                           |Write array of dicts. to csv file with pandas.|
   +------------------------------------+----------------------------------------------+
   |pl_to_csv                           |Write array of dicts. to csv file with polars.|
   +------------------------------------+----------------------------------------------+
   |put                                 |Write transformed array of dicts. to a csv    |
   |                                    |file with a selected I/O function.            |
   +------------------------------------+----------------------------------------------+
   |sh_doaod_split_by_value_is_not_empty|Converted array of dicts. to array of arrays  |
   |                                    |dict. by using conditional split              |
   +------------------------------------+----------------------------------------------+
   |sh_dod                              |Convert array of dicts. to dict. of dicts.    |
   +------------------------------------+----------------------------------------------+
   |sh_key_value_found                  |Show True if an element exists in the array of|
   |                                    |dicts. which contains the key, value pair     |
   +------------------------------------+----------------------------------------------+
   |sh_unique                           |Deduplicate arr.  of dicts.                   |
   +------------------------------------+----------------------------------------------+
   |split_by_value_is_not_empty         |Split arr. of dicts. by the condition "the    |
   |                                    |given key value is not empty".                |
   +------------------------------------+----------------------------------------------+
   |to_aoa                              |Convert array of dictionaries to array of     |
   |                                    |arrays controlled by key- and value-switch.   |
   +------------------------------------+----------------------------------------------+
   |to_aoa of_keys_values               |Convert arr. of dicts. to arr. of arrays usin |
   |                                    |keys of any dict. and values of all dict.     |
   +------------------------------------+----------------------------------------------+
   |to_aoa of_values                    |Convert arr. of dicts. to arr. of arrays      |
   |                                    |using values of all dict.                     |
   +------------------------------------+----------------------------------------------+
   |to_aoa of_key_values                |Convert array of dicts. to array using dict.  |
   |                                    |values with given key.                        |
   +------------------------------------+----------------------------------------------+
   |to_doaod_by_key                     |Convert array of dics. to dict. of arrays of  |
   |                                    |dicts. using a key.                           |
   +------------------------------------+----------------------------------------------+
   |to_dic_by_key                       |Convert array of dicts. to dict. of dicts     |
   |                                    |using a key                                   |
   +------------------------------------+----------------------------------------------+
   |to_dic_by_lc_keys                   |Convert array of dicts. to dict. of arrays    |
   |                                    |using 2 lowercase keys.                       |
   +------------------------------------+----------------------------------------------+
   |to_unique_by_key                    |Convert array of dicts. to array of dicts by  |
   +------------------------------------+----------------------------------------------+
   |sh_unique                           |by selecting dictionaries with ke.            |
   +------------------------------------+----------------------------------------------+
   |write_xlsx_wb                       |Write array of dicts. to xlsx workbook.       |
   +------------------------------------+----------------------------------------------+

AoD method: add
^^^^^^^^^^^^^^^

Description
...........

Add object to array of dictionaries.

#. If the objects is a dictionary:

   * the object is appended to the array of dictionaries
  
#. If the objects is an array of dictionaries:

   * the object extends the array of dictionaries

Parameter
.........

  .. Parameter-of-AoD-method-add-label:
  .. table:: **Parameter of AoD method add**

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |Array of dictionaries|
   +----+-----+-------+---------------------+
   |obj |TyAny|       |Object               |
   +----+-----+-------+---------------------+

Return Value
............

  .. Return-Value-of-AoD-method-add-label:
  .. table:: **Return Value of AoD method add**

   +----+----+---------------------+
   |Name|Type|Description          |
   +====+====+=====================+
   |    |None|                     |
   +----+----+---------------------+

AoD method: apply_function
^^^^^^^^^^^^^^^^^^^^^^^^^^

Description
...........

Create a new array of dictionaries by applying the function to each element
element of the array of dictionaries.

Parameter
.........

  .. Parameter-of-AoD-method-apply_function-label:
  .. table:: **Parameter of AoD method apply_function**

   +------+-------+-------+---------------------+
   |Name  |Type   |Default|Description          |
   +======+=======+=======+=====================+
   |aod   |TyAoD  |       |Array of dictionaries|
   +------+-------+-------+---------------------+
   |fnc   |TN_Call|       |Object               |
   +------+-------+-------+---------------------+
   |kwargs|TN_Dic |       |Keyword arguments    |
   +------+-------+-------+---------------------+

Return Value
............

  .. Return-Value-of-AoD-method-apply_function-label:
  .. table:: **Return Value of AoD method apply_function**

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyAoD|new array of dictionaries|
   +-------+-----+-------------------------+

AoD method: csv_dictwriterows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^          

Description
...........

Write given array of dictionaries (1.argument) to a csv file with the given path
name (2.argument) using the function "dictwriter" of the builtin path module "csv"

Parameter
.........

  .. Parameter-of-AoD-method-csc_dictwriterows-label:
  .. table:: **Parameter of AoD method csc_dictwriterows**

   +----+------+-------+---------------------+
   |Name|Type  |Default|Description          |
   +====+======+=======+=====================+
   |aod |TyAoD |       |Array of dictionaries|
   +----+------+-------+---------------------+
   |path|TyPath|       |Path                 |
   +----+------+-------+---------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-csc_dictwriterows-label:
  .. table:: **Return Value of AoD method csc_dictwriterows**

   +----+------+---------------------+
   |Name|Type  |Description          |
   +====+======+=====================+
   |    |None  |                     |
   +----+------+---------------------+
   
AoD method: dic_found_with_empty_value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
   
Description
...........

#. Set the switch sw_found to True if a dictionary with an empty value for the key is found
   in the given array of dictionaries (1.argument). 

#. If the Argument "sw_raise" is True and the switch "sw_found" is True, then an Exception is raised,
   otherwise the value of "sw_found" is returned.                  

Parameter
.........

  .. Parameter-of-AoD-method-dic_found_with_empty_value-label:
  .. table:: **Parameter of AoD method dic_found_with_empty_value**

   +--------+------+-------+---------------------+
   |Name    |Type  |Default|Description          |
   +========+======+=======+=====================+
   |aod     |TyAoD |       |array of dictionaries|
   +--------+------+-------+---------------------+
   |key     |TyStr |       |Key                  |
   +--------+------+-------+---------------------+
   |sw_raise|TyBool|False  |                     |
   +--------+------+-------+---------------------+

Return Value
............

  .. Return-Value-of-AoD-method-dic_found_with_empty_value-label:
  .. table:: **Return Value of AoD method dic_found_with_empty_value**

   +--------+------+----------------------------+
   |Name    |Type  |Description                 |
   +========+======+============================+
   |sw_found|TyBool|key is found in a dictionary|
   +--------+------+----------------------------+
   
AoD method: extend_if_not_empty
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Description
...........

#. Apply the given function (4.argument) to the value of the given dictionary (2.argument) for
   the key (3.argument).

#. The result is used to extend the given array of dictionaries (1.argument).

Parameter
.........

  .. Parameter-of-AoD-method-extend_if_not_empty-label:
  .. table:: **Parameter of AoD method extend_if_not_empty**

   +--------+------+-------+---------------------+
   |Name    |Type  |Default|Description          |
   +========+======+=======+=====================+
   |aod     |TyAoD |       |Array of dictionaries|
   +--------+------+-------+---------------------+
   |dic     |TyDic |       |Dictionary           |
   +--------+------+-------+---------------------+
   |key     |TN_Any|       |Key                  |
   +--------+------+-------+---------------------+
   |function|TyCall|       |Function             |
   +--------+------+-------+---------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-extend_if_not_empty-label:
  .. table:: **Return Value of AoD method extend_if_not_empty**

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyAoD|New array of dictionaries|
   +-------+-----+-------------------------+
   
AoD method: join_aod
^^^^^^^^^^^^^^^^^^^^
  
Description
...........

join 2 arrays of dictionaries

Parameter
.........

  .. Parameter-of-AoD-method-join_aod-label:
  .. table:: **Parameter of AoD method join_aod**

   +----+-----+-------+----------------------------+
   |Name|Type |Default|Description                 |
   +====+=====+=======+============================+
   |aod0|TyAoD|       |First array of dictionaries |
   +----+-----+-------+----------------------------+
   |aod1|TyAoD|       |Second array of dictionaries|
   +----+-----+-------+----------------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-join_aod-label:
  .. table:: **Return Value of AoD method join_aod**

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyAoD|New array of dictionaries|
   +-------+-----+-------------------------+
   
AoD method: merge_dic
^^^^^^^^^^^^^^^^^^^^^
   
Description
...........

Merge array of dictionaries (1.argument) with the dictionary (2.argument).

#. Each element of the new array of dictionaries is created by merging an element
   of the given array of dictionaries with the given dictionary.
   
Parameter
.........

  .. Parameter-of-AoD-method-merge_dic-label:
  .. table:: **Parameter of AoD method merge_dic**

   +----+------+-------+---------------------+
   |Name|Type  |Default|Description          |
   +====+======+=======+=====================+
   |aod |TN_AoD|       |Array of dictionaries|
   +----+------+-------+---------------------+
   |dic |TN_Dic|       |Dictionary           |
   +----+------+-------+---------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-merge_dic-label:
  .. table:: **Return Value of AoD method merge_dic**

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyAoD|New array of dictionaries|
   +-------+-----+-------------------------+
   
AoD method: nvl
^^^^^^^^^^^^^^^
   
Description
...........

Replace a none value of the first argument with the emty array. 

Parameter
.........

  .. Parameter-of-AoD-method-nvl-label:
  .. table:: **Parameter of AoD method nvl**

   +----+------+-------+---------------------+
   |Name|Type  |Default|Description          |
   +====+======+=======+=====================+
   |aod |TN_AoD|       |Array of dictionaries|
   +----+------+-------+---------------------+
   
Return Value
.............

  .. Return-Value-of-AoD-method-nvl-label:
  .. table:: **Return Value of AoD method nvl**

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyArr|New array of dictionaries|
   +-------+-----+-------------------------+
   
AoD method: pd_to_csv
^^^^^^^^^^^^^^^^^^^^^
   
Description
...........

#. Convert the given array of dictionaries (1.argument) to a panda dataframe using the panda function "from_dict".

#. Write the result to a csv file with the given path name (2.argument using the panda function "to_csv".

Parameter
.........

  .. Parameter-of-AoD-method-pd_to_csv-label:
  .. table:: **Parameter of AoD method pd_to_csv**

   +------+------+-------+---------------------+
   |Name  |Type  |Default|Description          |
   +======+======+=======+=====================+
   |aod   |TyAoD |       |Array of dictionaries|
   +------+------+-------+---------------------+
   |path  |TyPath|       |Csv file psth        |
   +------+------+-------+---------------------+
   |fnc_pd|TyCall|       |Panda function       |
   +------+------+-------+---------------------+
   
AoD method: pl_to_csv
^^^^^^^^^^^^^^^^^^^^^
   
Description
...........

#. Convert the given array of dictionaries (1.argument) to a panda dataframe with the panda function "from_dict". 

#. Convert the result to a polars dataframe using the polars function "to_pandas".
  
#. Apply the given function (3. argument) to the polars dataframe.
  
#. Write the result to a csv file with the given name (2.argument) using the polars function "to_csv".

Parameter
.........

  .. Parameter-of-AoD-method-pl_to_csv-label:
  .. table:: **Parameter of AoD method pl_to_csv**

   +------+------+-------+---------------------+
   |Name  |Type  |Default|Description          |
   +======+======+=======+=====================+
   |aod   |TyAoD |       |Array of dictionaries|
   +------+------+-------+---------------------+
   |path  |TyPath|       |Csv file path        |
   +------+------+-------+---------------------+
   |fnc_pd|TyCall|       |Polars function      |
   +------+------+-------+---------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-pl_to_csv-label:
  .. table:: **Return Value of AoD method pl_to_csv**

   +----+----+---------------------+
   |Name|Type|Description          |
   +====+====+=====================+
   |    |None|                     |
   +----+----+---------------------+
   
AoD method: put
^^^^^^^^^^^^^^^
   
Description
...........

#. Transform array of dictionaries (1.argument) with a transformer function (3.argument)

#. If the I/O function is defined for the given dataframe type (4.argument).

   #. write result to a csv file with the given path name (2.argument).

Parameter
.........

  .. Parameter-of-AoD-method-put-label:
  .. table:: **Parameter of AoD method put**

   +-------+------+-------+---------------------+
   |Name   |Type  |Default|Description          |
   +=======+======+=======+=====================+
   |aod    |TyAoD |       |Array of dictionaries|
   +-------+------+-------+---------------------+
   |path   |TyPath|       |Csv file path        |
   +-------+------+-------+---------------------+
   |fnc_aod|TyAoD |       |AoD function         |
   +-------+------+-------+---------------------+
   |df_type|TyStr |       |Dataframe type       |
   +-------+------+-------+---------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-put-label:
  .. table:: **Return Value of AoD method put**

   +----+----+--------------------+
   |Name|Type|Description         |
   +====+====+====================+
   |    |None|                    |
   +----+----+--------------------+
   
AoD method: sh_doaod_split_by_value_is_not_empty
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Description
...........

#. Create 2-dimensional dict. of array of dictionaries from given array of dict. (1.argument)
and key (2.argument) to split the array of dictionaries into 2 array of dictionaries by
the two conditions

   #. "the key is contained in the dictionary and the value empty".

   #. "the key is contained in the dictionary and the value is not empty".

#. The first array of dictionaries is created by the condition and is assigned to 
   the new dictionary of array of dictionaries using the given key (3.argument).

#. The second array of dictionaries is created by the negation of the condition 
   and is assigned to the new dictionary of array of dictionaries using the given
   key (4.argument).

Parameter
.........

  .. Parameter-of-AoD-method-join_aod-label:
  .. table:: **Parameter of AoD method join_aod**

   +-----+-----+-------+--------------------------------------+
   |Name |Type |Default|Description                           |
   +=====+=====+=======+======================================+
   |aod  |TyAoD|       |Array of dictionaries                 |
   +-----+-----+-------+--------------------------------------+
   |key  |Any  |       |Key                                   |
   +-----+-----+-------+--------------------------------------+
   |key_n|Any  |       |key of the array of dictionaries      |
   |     |     |       |wich satisfies the condition.         |
   +-----+-----+-------+--------------------------------------+
   |key_y|Any  |       |key of the array of dictionaries which|
   |     |     |       |does not satisfies the condition.     |
   +-----+-----+-------+--------------------------------------+
   
  .. Return-Value-of-AoD-method-join_aod-label:
  .. table:: **Return Value of AoD method join_aod**

   +-----+-------+-----------------------------------+
   |Name |Type   |Description                        |
   +=====+=======+===================================+
   |doaod|TyDoAoD|Dictionary of array of dictionaries|
   +-----+-------+-----------------------------------+
   
AoD method: sh_dod
^^^^^^^^^^^^^^^^^^
   
Description
...........

Create dictionary of dicionaries from the array of dictionaries (1.argument) and the key (2.argument).       

Parameter
.........

  .. Parameter-of-AoD-method-sh_dod-label:
  .. table:: **Parameter of AoD method sh_dod**

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |Array of dictionaries|
   +----+-----+-------+---------------------+
   |key |Any  |       |Key                  |
   +----+-----+-------+---------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-sh_dod-label:
  .. table:: **Return Value of AoD method sh_dod**

   +----+-----+--------------------------+
   |Name|Type |Description               |
   +====+=====+==========================+
   |dod |TyDoD|Dictionary of dictionaries|
   +----+-----+--------------------------+
   
AoD method: sh_unique
^^^^^^^^^^^^^^^^^^^^^

Description
...........

Deduplicate array of dictionaries (1.argument).
   
Parameter
.........

  .. Parameter-of-AoD-method-join_aod-label:
  .. table:: **Parameter of AoD method join_aod**

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |Array of dictionaries|
   +----+-----+-------+---------------------+
   |key |Any  |       |Key                  |
   +----+-----+-------+---------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-join_aod-label:
  .. table:: **Return Value of AoD method join_aod**

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyAoD|New array of dictionaties|
   +-------+-----+-------------------------+
   
AoD method: split_by_value_is_not_empty
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^      
   
Description
...........

Split the given array of dictionary into 2 arrays of dictionary by the condition 
"the key is contained in the dictionary and the value is not empty"

Parameter
.........

  .. Parameter-of-AoD-method-split_by_value_is_not_empty-label:
  .. table:: **Parameter of AoD method split_by_value_is_not_empty**

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |array of dictionaries|
   +----+-----+-------+---------------------+
   |key |Any. |       |Key                  |
   +----+-----+-------+---------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-split_by_value_is_not_empty-label:
  .. table:: **Return Value of AoD method split_by_value_is_not_empty**

   +--------------+--------+---------------------------------+
   |Name          |Type    |Description                      |
   +==============+========+=================================+
   |(aod_n, aod_y)|Ty2ToAoD|Tuple of 2 arrays of dictionaries|
   +--------------+--------+---------------------------------+
   
AoD method: sw_key_value_found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Description
...........

Set the condition to True if:

* the key is contained in a dictionary of the array of dictionaries and

* the key value is not empty"

Parameter
.........

  .. Parameter-of-AoD-method-sw_key_value_found-label:
  .. table:: **Parameter/Return Value of AoD method sw_key_value_found**

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |Array of dictionaries|
   +----+-----+-------+---------------------+
   |key |Any  |       |Key                  |
   +----+-----+-------+---------------------+
   
Return Value
............

  .. Parameter-of-AoD-method-sw_key_value_found-label:
  .. table:: **Parameter/Return Value of AoD method sw_key_value_found**

   +----+------+-------+--------------------------------+
   |Name|Type  |Default|Description                     |
   +====+======+=======+================================+
   |sw  |TyBool|       |key is contained in a dictionary|
   |    |      |       |of the array of dictionaries    |
   +----+------+-------+--------------------------------+
   
AoD method: to_aoa
^^^^^^^^^^^^^^^^^^
   
Description
...........

Create array of arrays from given array of dictionaries (1.argument).

#. If switch sw_keys (2.argument) is True:

   Create the first element of the array of arrays as the list of dict. keys of the
   first elements of the array of dictionaries.

#. If the switch sw_values (3. argument) is True:

   Create the other elemens of the array of dictionries as list of dict. values of the
   elements of the array of dictionaries.

Parameter
.........

  .. Parameter-of-AoD-method-to_aoa-label:
  .. table:: **Parameter of AoD method to_aoa**

   +---------+------+-------+---------------------+
   |Name     |Type  |Default|Description          |
   +=========+======+=======+=====================+
   |aod      |TyAoD |       |array of dictionaries|
   +---------+------+-------+---------------------+
   |sw_keys  |TyBool|       |keys switch          |
   +---------+------+-------+---------------------+
   |sw_values|TyBool|       |values switch        |
   +---------+------+-------+---------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-to_aoa-label:
  .. table:: **Return Value of AoD method to_aoa**

   +----+-----+---------------+
   |Name|Type |Description    |
   +====+=====+===============+
   |aoa |TyAoA|array of arrays|
   +----+-----+---------------+
   
Aod method: to_aoa of_key_values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Description
...........

Convert the given array of dictionary (1.argument) into an array of arrays.
#. Create first element of the new array of arrays as the keys-list of the first dictionary.
#. Create other elements as the values-lists of the dictionaries of the array of dictionaries.

Parameter
.........

  .. Parameter-of-AoD-method-to_aoa_of_key_values-label:
  .. table:: **Parameter of AoD method to_aoa_of_key_values**

   +----+-----+--------+---------------------+
   |Name|Type |Default |Description          |
   +====+=====+========+=====================+
   |aod |TyAoD|        |Array of dictionaries|
   +----+-----+--------+---------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-to_aoa_of_key_values-label:
  .. table:: **Return Value of AoD method to_aoa_of_key_values**

   +----+-----+---------------+
   |Name|Type |Description    |
   +====+=====+===============+
   |aoa |TyAoA|Array of arrays|
   +----+-----+---------------+
   
AoD method: to_aoa_of_values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  
Description
...........

Convert the given array of dictionaries (1.argument) into an array of arrays.
The elements of the new array of arrays are the values-lists of the dictionaries
of the array of dictionaries.

Parameter
.........

  .. Parameter-of-AoD-method-to_aoa_of_values-label:
  .. table:: **Parameter of AoD method to_aoa_of_values**

   +----+-----+--------+---------------------+
   |Name|Type |Default |Description          |
   +====+=====+========+=====================+
   |aod |TyAoD|        |Array of dictionaries|
   +----+-----+--------+---------------------+
   
  .. Return-Value-of-AoD-method-to_aoa_of_values-label:
  .. table:: **Return Value of AoD method to_aoa_of_values**

   +----+-----+--------+---------------+
   |Name|Type |Default |Description    |
   +====+=====+========+===============+
   |aoa |TyAoA|        |Array of arrays|
   +----+-----+--------+---------------+
   
AoD method: to_arr of_key_values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Description
...........

Convert the given array of dictionaries (1.argument) to an array. The elements of the new
array are the selected values of each dictionary of the array of dictionaries with the 
given key (2.argument).

Parameter
.........

  .. Parameter-of-AoD-method-to_arr_of_key_values-label:
  .. table:: **Parameter of AoD method to_arr_of_key_values**

   +----+-----+--------+---------------------+
   |Name|Type |Default |Description          |
   +====+=====+========+=====================+
   |aod |TyAoD|        |Array of dictionaries|
   +----+-----+--------+---------------------+
   |key |Any  |        |Key                  |
   +----+-----+--------+---------------------+
   
  .. Return-Value-of-AoD-method-to_arr_of_key_values-label:
  .. table:: **Return Value of AoD method to_arr_of_key_values**

   +----+-----+-----------+
   |Name|Type |Description|
   +====+=====+===========+
   |arr |TyAoD|New array  |
   +----+-----+-----------+
   
AoD method: to_doaod_by_key
^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Parameter
.........

  .. Parameter-of-AoD-method-to_doaod_by_key-label:
  .. table:: **Parameter of AoD method to_doaod_by_key**

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |Array of dictionaries|
   +----+-----+-------+---------------------+
   |key |Any  |       |Key                  |
   +----+-----+-------+---------------------+
   
  .. Return-Value-of-AoD-method-to_doaod_by_key-label:
  .. table:: **Return Value of AoD method to_doaod_by_key**

   +-----+-----+-----------------------------------+
   |Name |Type |Description                        |
   +=====+=====+===================================+
   |doaod|TyAoD|Dictionary of array of dictionaries|
   +-----+-----+-----------------------------------+
   
AoD method: to_dod_by_key
^^^^^^^^^^^^^^^^^^^^^^^^^
   
Parameter
.........

  .. Parameter-of-AoD-method-to_dod_by_key-label:
  .. table:: **Parameter of AoD method to_dod_by_key**

   +----+-----+-------+-------------+
   |Name|Type |Default|Description  |
   +====+=====+=======+=============+
   |aod |TyAoD|       |             |
   +----+-----+-------+-------------+
   |key |Any  |       |             |
   +----+-----+-------+-------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-to_dod_by_key-label:
  .. table:: **Return Value of AoD method to_dod_by_key**

   +----+-----+-------------+
   |Name|Type |Description  |
   +====+=====+=============+
   |dic |TyDic|             |
   +----+-----+-------------+
   
   
AoD method: to_doa_by_lc_keys
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Parameter
.........

  .. Parameter-of-AoD-method-to_doa_by_lc_keys-label:
  .. table:: **Parameter of AoD method to_doa_by_lc_keys**

   +----+-----+-------+-------------+
   |Name|Type |Default|Description  |
   +====+=====+=======+=============+
   |aod |TyAoD|       |             |
   +----+-----+-------+-------------+
   |key |Any  |       |             |
   +----+-----+-------+-------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-to_doa_by_lc_keys-label:
  .. table:: **Return Value of AoD method to_doa_by_lc_keys**

   +----+-----+-------------+
   |Name|Type |Description  |
   +====+=====+=============+
   |doa |TyDoA|             |
   +----+-----+-------------+
   
AoD method: to_unique_by_key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Parameter
.........

  .. Parameter-of-AoD-method-to_unique_by_key-label:
  .. table:: **Parameter of AoD method to_unique_by_key**

   +----+-----+-------+-------------+
   |Name|Type |Default|Description  |
   +====+=====+=======+=============+
   |aod |TyAoD|       |             |
   +----+-----+-------+-------------+
   |key |Any  |       |             |
   +----+-----+-------+-------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-to_unique_by_key-label:
  .. table:: **Return Value of AoD method to_unique_by_key**

   +-------+-----+-------+-------------+
   |Name   |Type |Default|Description  |
   +=======+=====+=======+=============+
   |aod_new|TyAoD|       |             |
   +-------+-----+-------+-------------+
   
AoD method: write_xlsx_wb
^^^^^^^^^^^^^^^^^^^^^^^^^
   
Parameter
.........

  .. Parameter-of-AoD-method-write_xlsx_wb-label:
  .. table:: **Parameter of AoD method write_xlsx_wb**

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |array of dictionaries|
   +----+-----+-------+---------------------+
   
Return Value
............

  .. Return-Value-of-AoD-method-write_xlsx_wb-label:
  .. table:: **Return Value of AoD method write_xlsx_wb**

   +----+-----+-----------+
   |Name|Type |Description|
   +====+=====+===========+
   |    |None |           |
   +----+-----+-----------+
   
Modules for array of basic objects
**********************************

  .. Modules-for-arrays-of-basic-objects-label:
  .. table:: **Modules for arrays of basic objects**

   +---------+----------------+
   |Name     |Description     |
   +=========+================+
   |aoo.py   |Array of objects|
   +---------+----------------+
   |aopath.py|Array of paths  |
   +---------+----------------+
   |aos.py   |Array of strings|
   +---------+----------------+

Array Module: aoo.py
********************

Classes
=======

The Module ``aoo.py`` contains the single static class ``AoO``;

Static class: AoO
-----------------

AoO methods
^^^^^^^^^^^

  .. AoO-methods-label:
  .. table:: *AoO methods*

   +---------+------------------------+
   |Name     |short Description       |
   +=========+========================+
   |to_unique|Concatinate array arrays|
   +---------+------------------------+

AoO method: to_unique
^^^^^^^^^^^^^^^^^^^^^
   
Deduplicate array of objects

Parameter
.........

  .. Parameter-of-AoO-Method-to_unique-label:
  .. table:: **Parameter of AoO Method to_unique**

   +----+-----+----------------+
   |Name|Type |Description     |
   +====+=====+================+
   |aoo |TyAoO|Array of objects|
   +----+-----+----------------+
   
Return Value
............

  .. Return-Value-of-AoO-Method-to_unique-label:
  .. table:: **Return Value of AoO Method to_unique**

   +-------+-----+--------------------+
   |Name   |Type |Description         |
   +=======+=====+====================+
   |aoo_new|TyAoO|New array of objects|
   +-------+-----+--------------------+
   
Array Module: aopath.py
***********************

Classes
=======

The Module ``aopath.py`` contains the single static class ``AoPath``;

Class: AoPath
-------------

AoPath methods
^^^^^^^^^^^^^^

  .. AoPath-methods-label:
  .. table:: *AoPath methods*

   +--------------------------+-------------------------------------------------+
   |Name                      |short Description                                |
   +==========================+=================================================+
   |join                      |Join array of paths using the os separator       |
   +--------------------------+-------------------------------------------------+
   |sh_a_path                 |Show array of paths for path template.           |
   +--------------------------+-------------------------------------------------+
   |sh_a_path_by_tmpl         |Convert array of path template keys and kwargs   |
   |                          |to array of paths.                               |
   +--------------------------+-------------------------------------------------+
   |sh_path_tmpl              |Convert array of path templates to path template.|
   +--------------------------+-------------------------------------------------+
   |yield_path_kwargs         |yield path for path-array and kwargs.            |
   +--------------------------+-------------------------------------------------+
   |yield_path_kwargs_new     |yield path from dictionary- and path-array and   |
   |                          |modified kwargs by dictionary item               |
   +--------------------------+-------------------------------------------------+
   |yield_path_item_kwargs    |yield path from path-array, item from array and  |
   |                          |kwargs.                                          |
   +--------------------------+-------------------------------------------------+
   |yield_path_item_kwargs_new|yield path from path-array, item from array and  |
   |                          |modified kwargs by dictionary item.              |
   +--------------------------+-------------------------------------------------+

AoPath Method: join
^^^^^^^^^^^^^^^^^^^
   
#. Convert array of paths (1.argument) by striping the leading or trailing os separator.

#. join the converted array of paths.

Parameter
.........

  .. Parameter-of-AoPath-Method-to_unique-label:
  .. table:: **Parameter of AoPath Method to_unique**

   +------+--------+-------+--------------+
   |Name  |Type    |Default|Description   |
   +======+========+=======+==============+
   |aopath|TyAoPath|       |array of paths|
   +------+--------+-------+--------------+
   
Return Value
............

  .. Return-Value-of-AoPath-method-to_unique-label:
  .. table:: **Return Value of AoPath method to_unique**

   +----+------+-----------+
   |Name|Type  |Description|
   +====+======+===========+
   |path|TyPath|Path       |
   +----+------+-----------+
   
AoPath method: sh_a_path
^^^^^^^^^^^^^^^^^^^^^^^^

Convert path template to array of paths using glob function of module glob.py.

Parameter
.........

  .. Parameter-of-AoPath-method-sh_a_path-label:
  .. table:: **Parameter of AoPath method sh_a_path**

   +----+------+-------+-----------+
   |Name|Type  |Default|Description|
   +====+======+=======+===========+
   |path|TyPath|       |Path       |
   +----+------+-------+-----------+
   
Return Value
............

  .. Return-Value-of-AoPath-method-sh_a_path-label:
  .. table:: **Return Value of AoPath-method sh_a_path**

   +------+--------+--------------+
   |Name  |Type    |Description   |
   +======+========+==============+
   |a_path|TyAoPath|Array of paths|
   +------+--------+--------------+
   
AoPath method: sh_a_path_by_tmpl
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
#. Select array of path templates from keyword arguments (1.arguments) using the parameter

   * array of path template keys (1.argument);

#. join the array of path templates with the os separator

#. convert the created final path template to an array of paths.

Parameter
.........

  .. Parameter-of-AoPath-Method-sh_a_path_by_tmpl-label:
  .. table:: **Parameter of AoPath Method sh_a_path_by_tmpl**

   +---------------+--------+-------+---------------------------+
   |Name           |Type    |Default|Description                |
   +===============+========+=======+===========================+
   |a_path_tmpl_key|TyAoPath|       |array of path template keys|
   +---------------+--------+-------+---------------------------+
   |kwargs         |TyDic   |       |keyword arguments          |
   +---------------+--------+-------+---------------------------+
   
Return Value
............

  .. Return-Value-of-AoPath-Method-sh_a_path_by_tmpl-label:
  .. table:: **Return Value of AoPath Method sh_a_path_by_tmpl**

   +------+--------+-------+-----------+
   |Name  |Type    |Default|Description|
   +======+========+=======+===========+
   |a_path|TyAoPath|       |Path       |
   +------+--------+-------+-----------+
   
AoPath method: yield_path_kwargs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
#. Create array of paths by executing the function sh_a_path_by_tmpl with the parameter:

   * array of path template keys (2.argument).
    
#. Loop over array of paths to yield:

   #. yield path, kwargs (3. argument)

Parameter
.........

  .. Parameter-of-AoPath-Method-yield_path_kwargs-label:
  .. table:: **Parameter of AoPath Method yield_path_kwargs**

   +---------------+--------+-------+---------------------------+
   |Name           |Type    |Default|Description                |
   +===============+========+=======+===========================+
   |cls            |Tyclass |       |current class              |
   +---------------+--------+-------+---------------------------+
   |a_path_tmpl_key|TyAoPath|       |array of path template keys|
   +---------------+--------+-------+---------------------------+
   |kwargs         |TyDic   |       |keyword arguments          |
   +---------------+--------+-------+---------------------------+

Return Value
............

  .. Return-Value-of-AoPath-Method-yield_path_kwargs-label:
  .. table:: **Return Value of AoPath Method yield_path_kwargs**

   +--------------+--------+-----------+
   |Name          |Type    |Description|
   +==============+========+===========+
   |(path, kwargs)|TyAoPath|Path       |
   +--------------+--------+-----------+
   
AoPath method: yield_path_kwargs_new
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Synopsis
........

sh_a_path_by_tmpl(a_path_tmpl_key, kwargs)


Description
...........

#. Create array of directories by executing the function sh_a_path_by_tmpl with the arguments:

   * array of directory template keys (2.argument).

#. Loop over array of directories to:

   #. create kwargs_new by executing ths given function sh_kwargs_new (4. argument) with the arguments:

      * directory, given kwargs (5. argument) 

   #. create array of paths by executing the function sh_a_oath_by_tmpl with the arguments:

      * given array of path template keys (3. argument), kwargs_new

#. Loop over array of paths within the outer loop to:

   #. yield path, kwargs_new

Parameter
.........

  .. Parameter-of-AoPath-Method-yield_path_kwargs-new-label:
  .. table:: **Parameter of AoPath Method yield_path_kwarg-news**

   +---------------+--------+-------+-----------------------------------+
   |Name           |Type    |Default|Description                        |
   +===============+========+=======+===================================+
   |cls            |Tyclass |       |Current class                      |
   +---------------+--------+-------+-----------------------------------+
   |a_dir_tmpl_key |TyAoPath|       |Array of path template keys        |
   +---------------+--------+-------+-----------------------------------+
   |a_path_tmpl_key|TyAoPath|       |Array of path template keys        |
   +---------------+--------+-------+-----------------------------------+
   |sh_kwargs_new  |TyAoPath|       |Show new keyword arguments function|
   +---------------+--------+-------+-----------------------------------+
   |kwargs         |TyDic   |       |Keyword arguments                  |
   +---------------+--------+-------+-----------------------------------+
   
Return Value
............

  .. Return-Value-of-AoPath-Method-yield_path_kwargs-new-label:
  .. table:: **Return Value of AoPath Method yield_path_kwarg-news**

   +------------------+--------+---------------------------+
   |Name              |Type    |Description                |
   +==================+========+===========================+
   |(path, kwargs_new)|TyAoPath|Path, new keyword arguments|
   +------------------+--------+---------------------------+
   
AoPath method: yield_path_item_kwargs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
#. Create array of paths by executing the function sh_a_path_by_tmpl with the arguments:

   * array of path template keys (2.argument).

#. Create array of items by selecting the value in the directory kwargs (4. argument) for
   the kwargs key (3. argument)

#. Loop over array of path and array of items to:

   #. yield path, item, kwargs (4. argument)

Parameter
.........

  .. Parameter-of-AoPath-Method-yield_path_item_kwargs-label:
  .. table:: **Parameter of AoPath Method yield_path_item_kwargs**

   +---------------+--------+-------+---------------------------+
   |Name           |Type    |Default|Description                |
   +===============+========+=======+===========================+
   |cls            |Tyclass |       |current class              |
   +---------------+--------+-------+---------------------------+
   |a_path_tmpl_key|TyAoPath|       |array of path template keys|
   +---------------+--------+-------+---------------------------+
   |a_arr_key      |TyAoPath|       |array of path template keys|
   +---------------+--------+-------+---------------------------+
   |kwargs         |TyDic   |       |keyword arguments          |
   +---------------+--------+-------+---------------------------+
   
Return Value
............

  .. Return Value-of-AoPath-Method-yield_path_item_kwargs-label:
  .. table:: **Return Value of AoPath Method yield_path_item_kwargs**

   +--------------------+--------+-----------------------------+
   |Name                |Type    |Description                  |
   +====================+========+=============================+
   |(path, item, kwargs)|TyAoPath|Path, Item, keyword arguments|
   +--------------------+--------+-----------------------------+
   
AoPath method: yield_path_item_kwargs_new
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
#. Create array of directories by executing the function sh_a_path_by_tmpl with the parameter:

   * a_dir_tmpl_key (2.argument).

#. Create  array of items by selecting the value in the directory kwargs (4. argument) for
   the key arr_key (3. argument)

#. Loop over the array of directories to:

   #. create kwargs_new by executing ths function sh_kwargs_new (4. argument) with the arguments:

      * directory, given kwargs (5. argument) 

   #. create array of paths by executing the function sh_a_oath_by_tmpl with the arguments:

      * given array of path template keys (3. argument), kwargs_new

   #. Loop over array of path and array of items within the outer loop to:

      #. yield path, item, kwargs_new

Parameter
.........

  .. Parameter-of-AoPath-Method-yield_path_item_kwargs_new-label:
  .. table:: **Parameter of AoPath Method yield_path_item_kwargs_new**

   +---------------+--------+-------+-----------------------------------+
   |Name           |Type    |Default|Description                        |
   +===============+========+=======+===================================+
   |cls            |Tyclass |       |current class                      |
   +---------------+--------+-------+-----------------------------------+
   |a_dir_tmpl_key |TyAoPath|       |array of path template keys        |
   +---------------+--------+-------+-----------------------------------+
   |a_path_tmpl_key|TyAoPath|       |array of path template keys        |
   +---------------+--------+-------+-----------------------------------+
   |sh_kwargs_new  |TyAoPath|       |show new keyword arguments function|
   +---------------+--------+-------+-----------------------------------+
   |kwargs         |TyDic   |       |keyword arguments                  |
   +---------------+--------+-------+-----------------------------------+
   
Return Value
............

  .. Return-Value-of-AoPath-Method-yield_path_item_kwargs_new-label:
  .. table:: *Return Value of AoPath Method yield_path_item_kwargs_new**

   +------------------------+--------+---------------------------------+
   |Name                    |Type    |Description                      |
   +========================+========+=================================+
   |(path, item, kwargs_new)|TyAoPath|Path, Item, new keyword arguments|
   +------------------------+--------+---------------------------------+
   
Array Module: aos.py
********************

Classes
=======

The Module ``aos.py`` contains the single static class ``AoS``;

Static class: AoS
-----------------

AoS Methods
^^^^^^^^^^^

  .. AoS-methods-label:
  .. table:: *AoS methods*

   +-------------------------+------------------------------------------+
   |Name                     |short Description                         |
   +=========================+==========================================+
   |nvl                      |Replace empty array of strings            |
   +-------------------------+------------------------------------------+
   |sh_a_date                |Convert array of strings to array of dates|
   +-------------------------+------------------------------------------+
   |to_lower                 |Convert array of strings to array of      |
   |                         |lowered strings.                          |
   +-------------------------+------------------------------------------+
   |to_unique                |Deduplicate array of arrays               |
   +-------------------------+------------------------------------------+
   |to_unique_lower          |Convert array of strings to deduplicted   |
   |                         |array of lowered strings.                 |
   +-------------------------+------------------------------------------+
   |to_unique_lower_invariant|Convert array of arrays to array of arrays|
   +-------------------------+------------------------------------------+

AoS method: to_unique
^^^^^^^^^^^^^^^^^^^^^
   
Parameter
.........

  .. Parameter-of-AoS-Method-to_unique-label:
  .. table:: **Parameter of AoS Method to_unique**

   +----+-----+-------+----------------+
   |Name|Type |Default|Description     |
   +====+=====+=======+================+
   |aoo |TyAoO|       |array of objects|
   +----+-----+-------+----------------+

Return Value
............

  .. Return Value-of-AoS-Method-to_unique-label:
  .. table:: **Return Value of AoS Method to_unique**

   +-------+-----+--------------------+
   |Name   |Type |Description         |
   +=======+=====+====================+
   |aoo_new|TyAoO|new array of objects|
   +-------+-----+--------------------+

General Array Module
********************

  .. General-Array-Module-label:
  .. table:: **General Array Module**

   +------+-----------------+
   |Name  |Short description|
   +======+=================+
   |arr.py|Array            |
   +------+-----------------+

Classes
=======

The Module ``arr.py`` contains the single static class ``Arr``;

arr.py class: Arr
-----------------

Arr Methods
^^^^^^^^^^^

  .. Arr-methods-label:
  .. table:: *Arr methods*

   +-----------------------+---------------------------------------------------+
   |Name                   |Short description                                  |
   +=======================+===================================================+
   |append                 |Append item to the array                           |
   +-----------------------+---------------------------------------------------+
   |append_unique          |Append item to the array if the item is not in the |
   |                       |array.                                             |
   +-----------------------+---------------------------------------------------+
   |apply_function         |Apply function with the keyword arguments to all   |
   |                       |non empty array elements.                          |
   +-----------------------+---------------------------------------------------+
   |apply_replace          |Replace source by target to all array elements.    |
   +-----------------------+---------------------------------------------------+
   |apply_str              |Apply function str to all non empty array elements.|
   +-----------------------+---------------------------------------------------+
   |encode                 |Join array elements with blank separator and encode|
   |                       |result string.                                     |
   +-----------------------+---------------------------------------------------+
   |ex_intersection        |Intersection of first array with second array      |
   +-----------------------+---------------------------------------------------+
   |extend                 |Extend first array with second array               |
   +-----------------------+---------------------------------------------------+
   |get_key_value          |Get next array item value without line feed for the|
   |                       |given index or the given default value if the item |
   |                       |value is identical to the given value without line |
   |                       |feeds.                                             |
   +-----------------------+---------------------------------------------------+
   |get_item               |Extend array of dicts. with non empty dict.        |
   +-----------------------+---------------------------------------------------+
   |get_text               |Extend array of dicts. with non empty dict.        |
   +-----------------------+---------------------------------------------------+
   |get_text_spli          |Extend array of dicts. with non empty dict.        |
   +-----------------------+---------------------------------------------------+
   |intersection           |Extend array of dicts. with non empty dict.        |
   +-----------------------+---------------------------------------------------+
   |is_empty               |Extend array of dicts. with non empty dict.        |
   +-----------------------+---------------------------------------------------+
   |is_not_empty           |Extend array of dicts. with non empty dict.        |
   +-----------------------+---------------------------------------------------+
   |join_not_none          |Extend array of dicts. with non empty dict.        |
   +-----------------------+---------------------------------------------------+
   |length                 |Extend array of dicts. with non empty dict.        |
   +-----------------------+---------------------------------------------------+
   |merge                  |Extend array of dicts. with non empty dict.        |
   +-----------------------+---------------------------------------------------+
   |sh_dic_from_keys_values|Extend array of dicts. with non empty dict.        |
   +-----------------------+---------------------------------------------------+
   |sh_dic_zip             |Join elements of array of dicts.                   |
   +-----------------------+---------------------------------------------------+
   |sh_item                |Show True if an element exists in the array of     |
   +-----------------------+---------------------------------------------------+
   |sh_item_if             |Show True if an element exists in the array of     |
   +-----------------------+---------------------------------------------------+
   |sh_item_lower          |Show True if an element exists in the array of     |
   +-----------------------+---------------------------------------------------+
   |sh_item_str            |Show True if an element exists in the array of     |
   +-----------------------+---------------------------------------------------+
   |sh_item0               |Deduplicate arr.  of dicts.                        |
   +-----------------------+---------------------------------------------------+
   |sh_item0_if            |Deduplicate arr.  of dicts.                        |
   +-----------------------+---------------------------------------------------+
   |sh_subarray            |Deduplicate arr.  of dicts.                        |
   +-----------------------+---------------------------------------------------+
   |to_dic                 |Show arr. of arrays created from arr. of dict.     |
   |                       |by using any key- and all value-arrays             |
   +-----------------------+---------------------------------------------------+
   |yield_items            |Convert array of dictionaries to array of          |
   |                       |arrays controlled by key- and value-switch.        |
   +-----------------------+---------------------------------------------------+

Appendix
********

.. contents:: **Table of Content**
