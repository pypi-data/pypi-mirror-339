##########
ka_uts_dfr
##########

Overview
********

.. start short_desc

**Dataframe 'Utilities'**

.. end short_desc

Installation
************

.. start installation

Package ``ka_uts_dfr`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_dfr

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_dfr

.. end installation

This requires that the ``readme`` extra is installed:

.. code-block:: shell

	$ python -m pip install ka_uts_dfr[readme]

Package logging
***************

Standard or user specific Package logging of the package **ka_uts_arr** is defined 
in the static logging class **Log_** of Base module log\_.py of the Communication
Package **ka_uts_com**.
The default Logging configuration is defined by the yaml files **log.standard.yml**
or **log.personal.yml** in the data directory of the Communication package.
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
   |     +--------------------------------------------+-------------------+
   |error|/data/<tenant>/RUN/<package>/<function>/errs|errs_<pid>_<ts>.log|
   |     +--------------------------------------------+-------------------+
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
   |log  |/data/umh/RUN/umh_otec/srr/logs|logs_9470_1737118199.log|
   +-----+-------------------------------+------------------------+

Package files
*************

Classification
==============

The Files of Package ``ka_uts_dfr`` could be classified into the follwing file types:

#. *Special python specific files*
#. *Dunder modules*
#. *Package modules*

Special python specific files
************+****************

  .. Special-python-specific-files-elabel:
  .. table:: **Special python specific files**

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
**************

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
***************

Classification
==============

The Modules of Package ``ka_uts_dfr`` could be classified into the following module classes:

#. *Modules for pandas dataframe*
#. *Modules for polars dataframe*

Modules for Pandas Dataframe    
****************************

  .. Modules-for-pandas-dataframe-label:
  .. table:: *Modules for Pandas Dataframe*

   +-------+----------------+
   |Name   |Type            |
   +=======+================+
   |pddf.py|Pandas Dataframe|
   +-------+----------------+

pddf.py
=======

The Module ``pddf.py`` contains a single static classes ``PdDf``.

pddf.py Class: PdDf
-------------------

The static Class ``PdDf`` is used to manage Pandas Dataframes;
it contains the subsequent methods.

PdDf Methods
^^^^^^^^^^^^

  .. Methods-of-static-class-PdDf-label:
  .. table:: *Methods of static class PdDf*

   +----------------------+--------------------------------------------------+
   |Name                  |Description                                       |
   +======================+==================================================+
   |sh_d_aod              |show dictionary of array of dictionaries.         |
   +----------------------+--------------------------------------------------+
   |sh_d_pddf             |show dictionary of pandas dataframes.             |
   +----------------------+--------------------------------------------------+
   |pivot_table           |create pandas dataframe pivot table.              |
   |                      |The pivot rules are defined by a pivot dictionary.|
   +----------------------+--------------------------------------------------+
   |filter                |Filter pandas dataframe.                          |
   |                      |The filteris defined by filter dictionary         |
   +----------------------+--------------------------------------------------+
   |set_ix_drop_col_filter|set index and drop column filter                  |
   +----------------------+--------------------------------------------------+
   |format-leading_zeros  |format pandas dataframe columns with leading zeros|         
   +----------------------+--------------------------------------------------+
   |format-as-date        |format pandas dataframe columns as date           |
   +----------------------+--------------------------------------------------+

PdDf Method: sh_d_aod
^^^^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PdDf-method-sh_d_aod-label:
  .. table:: **Parameter of PdDf method sh_d_aod**

   +----+------+-----------------+
   |Name|Type  |Description      |
   +====+======+=================+
   |df  |TyPdDf|Pandas Datafame  |
   +----+------+-----------------+
   |key |str   |Keyword arguments|
   +----+------+-----------------+

Return Value
............

  .. Return-Value-of-PdDf-method-sh_d_aod-label:
  .. table:: **Return Value of PdDf method sh_d_aod**

   +-----+--------+-----------------------------------+
   |Name |Type    |Description                        |
   +=====+========+===================================+
   |d_aod|TyDoAoD |dictionary of array of dictionaries|
   +-----+--------+-----------------------------------+

PdDf Method: sh_d_pddf
^^^^^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PdDf-method-sh_d_pddf-label:
  .. table:: **Parameter of PdDf method sh_d_pddf**

   +----+------+-----------------+
   |Name|Type  |Description      |
   +====+======+=================+
   |cls |class |current class    |
   +----+------+-----------------+
   |df  |TyPdDf|Pandas Datafame  |
   +----+------+-----------------+
   |key |str   |keyword arguments|
   +----+------+-----------------+

Return Value
............

  .. Return-Value-of-PdDf-method-sh_d_pddf-label:
  .. table:: **Return Value of PdDf method sh_d_pddf**

   +----+--------+-------------------------------+
   |Name|Type    |Description                    |
   +====+========+===============================+
   |d_df|TyDoPdDf|dictionary of pandas dataframes|
   +----+--------+-------------------------------+
   
PdDf Method: pivot_table
^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PdDf-method-pivot_table-label:
  .. table:: **Parameter of PdDf method pivot_table**

   +----+------+---------------------------------+
   |Name|Type  |Description                      |
   +====+======+=================================+
   |cls |class |current class                    |
   +----+------+---------------------------------+
   |df  |TyPdDf|pandas datafame                  |
   +----+------+---------------------------------+
   |d_pv|TyDic |pivot table definition dictionary|
   +----+------+---------------------------------+

Return Value
............

  .. Return-Value-of-PdDf-method-pivot_table-label:
  .. table:: *Return Value of PdDf method pivot_table*

   +----+------+----------------------------+
   |Name|Type  |Description                 |
   +====+======+============================+
   |dfpv|TyPdDf|pandas dataframe pivot table|
   +----+------+----------------------------+

PdDf Method: filter
^^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PdDf-method-filter-label:
  .. table:: **Parameter of PdDf method filter**

   +--------+------+----------------------------+
   |Name    |Type  |Description                 |
   +========+======+============================+
   |cls     |class |current class               |
   +--------+------+----------------------------+
   |df      |TyPdDf|pandas datafame             |
   +--------+------+----------------------------+
   |d_filter|TyDic |filter definition dictionary|
   +--------+------++---------------------------+
   |relation|TyStr |filter relation             |
   +--------+------+----------------------------+

Return Value
............

  .. Return-Value-of-PdDf-method-filter-label:
  .. table:: **Return Value of PdDf method filter**

   +------+------+------------------------+
   |Name  |Type  |Description             |
   +======+======+========================+
   |df_new|TyPdDf|filtered pandas datafame|
   +------+------+------------------------+

PdDf Method: set_ix_drop_col_filter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PdDf-method-set_ix_drop_col_filter-label:
  .. table:: *Parameter of PdDf method set_ix_drop_col_filter*

   +--------+------+----------------------------+
   |Name    |Type  |Description                 |
   +========+======+============================+
   |cls     |class |current class               |
   +--------+------+----------------------------+
   |df      |TyPdDf|pandas datafame             |
   +--------+------+----------------------------+
   |d_filter|TyDic |filter definition dictionary|
   +--------+------+----------------------------+
   |relation|str   |filter relation             |
   +--------+------+----------------------------+

Return Value
.............

  .. Return-Value-of-PdDf-method-set_ix_drop_col_filter-label:
  .. table:: *Return Value of PdDf method set_ix_drop_col_filter*

   +------+------+------------------------+
   |Name  |Type  |Description             |
   +======+======+========================+
   |df_new|TyPdDf|filtered pandas datafame|
   +------+------+------------------------+

PdDf Module: format_leading_zeros
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PdDf-method-format_leading_zeros-label:
  .. table:: **Parameter of PdDf method format_leading_zeros**

   +--------+------+----------------------------+
   |Name    |Type  |Description                 |
   +========+======+============================+
   |cls     |class |current class               |
   +--------+------+----------------------------+
   |df      |TyPdDf|pandas datafame             |
   +--------+------+----------------------------+
   |d_filter|TyDic |filter definition dictionary|
   +--------+------+----------------------------+
   |relation|str   |filter relation             |
   +--------+------+----------------------------+

Return Value
.............

  .. Return-Value-of-PdDf-method-format_leading_zeros-label:
  .. table:: **Return Value of PdDf method format_leading_zeros**

   +------+------+------------------------+
   |Name  |Type  |Description             |
   +======+======+========================+
   |df_new|TyPdDf|filtered pandas datafame|
   +------+------+------------------------+

PdDf Method: format_as_date
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PdDf-method-format_as_date-label:
  .. table:: **Parameter of PdDf method format_as_date**

   +--------+------+----------------------------+
   |Name    |Type  |Description                 |
   +========+======+============================+
   |cls     |class |current class               |
   +--------+------+----------------------------+
   |df      |TyPdDf|pandas datafame             |
   +--------+------+----------------------------+
   |d_filter|TyDic |filter definition dictionary|
   +--------+------+----------------------------+
   |relation|str   |filter relation             |
   +--------+------+----------------------------+

Return Value
............

  .. Return Values-of-PdDf-method-format_as_date-label:
  .. table:: **Return Values of PdDf methodR ormat_as_date**

   +------+------+------------------------+
   |Name  |Type  |Description             |
   +======+======+========================+
   |df_new|TyPdDf|filtered pandas datafame|
   +------+------+------------------------+

Modules for Polars Dataframe    
****************************

  .. Modules-for-polars-dataframe-label:
  .. table:: *Modules for Polars Dataframe*

   +---------------------+------------------------------------+
   |Module               |Classes                             |
   +-----+---------------+----+------+------------------------+
   |Name|Type            |Name|Type  |Description             |
   +====+================+====+======+========================+
   |pldf|Polars Dataframe|PdDf|Static|Manage Polars Dataframes|
   +----+----------------+----+------+------------------------+

pldf.py
=======

The Module ``pldf`` contains a single static class ``PLDF``.

PlDf
----

The static Class ``PlDf`` contains the subsequent methods.

PlDf Methods
^^^^^^^^^^^^

  .. pldf-methods-label:
  .. table:: *pldf Methods*

   +------------+------------------------------------------------------------+
   |Name        |Description                                                 |
   +============+============================================================+
   |filter      |Filter polars dataframe using the given statement.          |
   +------------+------------------------------------------------------------+
   |pivot       |Create polars dataframe pivot table.                        |
   |            |The pivot rules are defined by the given pivot dictionary.  |
   +------------+------------------------------------------------------------+
   |pivot_filter|Filter polars dataframe using the given statement and       |
   |            |create polars dataframe pivot table from filtered dataframe.|
   |            |The pivot rules are defined by the given pivot dictionary.  |
   +------------+------------------------------------------------------------+
   |to_aod      |create pandas dataframe pivot table.                        |
   |            |The pivot rules are defined by pivot dictionary             |
   +------------+------------------------------------------------------------+
   |to_doa      |create pandas dataframe pivot table.                        |
   |            |The pivot rules are defined by pivot dictionary             |
   +------------+------------------------------------------------------------+

PlDf Method: filter
^^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PlDf-method-filter-label:
  .. table:: *Parameter of PlDf method filter*

   +----+------+----------------+
   |Name|Type  |Description     |
   +====+======+================+
   |cls |class |current class   |
   +----+------+----------------+
   |df  |TyPdDf|polars datafame |
   +----+------+----------------+
   |stmt|TyStmt|filter statement|
   +----+------+----------------+

Return Value
............

  .. Return-Value-of-PlDf-method-filter-label:
  .. table:: *Return Value of PlDf method filter*

   +------+------+------------------------+
   |Name  |Type  |Description             |
   +======+======+========================+
   |df_new|TyPlDf|filtered polars datafame|
   +------+------+------------------------+

PlDf Method: pivot
^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PlDf-method-pivot-label:
  .. table:: *Parameter of P.Df method pivot*

   +----+------+---------------------------------+
   |Name|Type  |Description                      |
   +====+======+=================================+
   |cls |class |current class                    |
   +----+------+---------------------------------+
   |df  |TyPlDf|polars datafame                  |
   +----+------+---------------------------------+
   |d_pv|TyDic |pivot table definition dictionary|
   +----+------+---------------------------------+

Return Value
............

  .. Return-Value-of-PdDf-method-pivot_label:
  .. table:: *Return value of PdDf method pivot*

   +----+------+----------------------------+
   |Name|Type  |Description                 |
   +====+======+============================+
   |dfpv|TyPlDf|polars dataframe pivot table|
   +----+------+----------------------------+

PlDf Method: pivot_filter
^^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PdDf-method-pivot_filter-label:
  .. table:: *Parameter of PdDf method pivot_filter*

   +----+------+---------------------------------+
   |Name|Type  |Description                      |
   +====+======+=================================+
   |cls |class |current class                    |
   +----+------+---------------------------------+
   |df  |TyPlDf|polars datafame                  |
   +----+------+---------------------------------+
   |d_pv|TyDic |pivot table definition dictionary|
   +----+------+---------------------------------+
   |stmt|TyStmt|filter statement                 |
   +----+------+---------------------------------+

Return Value
............

  .. Return-Value-of-PlDf-method-pivot_filter-label:
  .. table:: *Return value of PlDf method pivot_gilter*

   +----+------+----------------------------+
   |Name|Type  |Description                 |
   +====+======+============================+
   |dfpv|TyPlDf|polars dataframe pivot table|
   +----+------+----------------------------+

PlDf Method: to_aod
^^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PdDf-method-to_aod-label:
  .. table:: *Parameter of PdDf method to_aod*

   +----+------+---------------+
   |Name|Type  |Description    |
   +====+======+===============+
   |df  |TyPlDf|polars datafame|
   +----+------+---------------+

Return Value
............

  .. Return-Value-of-PlDf-method-to_aod-label:
  .. table:: *Return value of PlDf method to_aod*

   +----+-----+---------------------+
   |Name|Type |Description          |
   +====+=====+=====================+
   |aod |TyAoD|Array of Dictionaries|
   +----+-----+---------------------+

PlDf Method: to_doa 
^^^^^^^^^^^^^^^^^^^

Parameter
.........

  .. Parameter-of-PdDf-method-to_doa-label:
  .. table:: *Parameter of PdDf method to_doa*

   +----+------+---------------+
   |Name|Type  |Description    |
   +====+======+===============+
   |df  |TyPlDf|polars datafame|
   +----+------+---------------+

Return Value
............

  .. Return-Value-of-PlDf-method-to_doa-label:
  .. table:: *Return value of PlDf method to_doa*

   +----+-----+--------------------+
   |Name|Type |Description         |
   +====+=====+====================+
   |doa |TyDoA|Dictionary of Arrays|
   +----+-----+--------------------+

Appendix
========

.. contents:: **Table of Content**
