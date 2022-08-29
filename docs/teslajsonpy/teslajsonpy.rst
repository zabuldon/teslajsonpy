===============
``teslajsonpy``
===============

.. automodule:: teslajsonpy

   .. contents::
      :local:


Submodules
==========

.. toctree::

   teslajsonpy.__version__
   teslajsonpy.car
   teslajsonpy.connection
   teslajsonpy.const
   teslajsonpy.controller
   teslajsonpy.energy
   teslajsonpy.exceptions
   teslajsonpy.teslaproxy

.. currentmodule:: teslajsonpy


Classes
=======

- :py:class:`TeslaCar`:
  Class to handle car attributes and methods.

- :py:class:`Connection`:
  Connection to Tesla Motors API.

- :py:class:`Controller`:
  Controller for connections to Tesla Motors API.

- :py:class:`Energy`:
  Class to handle energy site attributes and methods.

- :py:class:`TeslaProxy`:
  Class to handle proxy login connections to Alexa.


.. autoclass:: TeslaCar
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: TeslaCar
      :parts: 1

.. autoclass:: Connection
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Connection
      :parts: 1

.. autoclass:: Controller
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Controller
      :parts: 1

.. autoclass:: Energy
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Energy
      :parts: 1

.. autoclass:: TeslaProxy
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: TeslaProxy
      :parts: 1


Exceptions
==========

- :py:exc:`TeslaException`:
  Class of Tesla API exceptions.

- :py:exc:`UnknownPresetMode`:
  Class of exceptions for Unknown Preset.

- :py:exc:`HomelinkError`:
  Class of exceptions for Homelink Error.

- :py:exc:`RetryLimitError`:
  Class of exceptions for hitting retry limits.

- :py:exc:`IncompleteCredentials`:
  Class of exceptions for incomplete credentials.


.. autoexception:: TeslaException

   .. rubric:: Inheritance
   .. inheritance-diagram:: TeslaException
      :parts: 1

.. autoexception:: UnknownPresetMode

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnknownPresetMode
      :parts: 1

.. autoexception:: HomelinkError

   .. rubric:: Inheritance
   .. inheritance-diagram:: HomelinkError
      :parts: 1

.. autoexception:: RetryLimitError

   .. rubric:: Inheritance
   .. inheritance-diagram:: RetryLimitError
      :parts: 1

.. autoexception:: IncompleteCredentials

   .. rubric:: Inheritance
   .. inheritance-diagram:: IncompleteCredentials
      :parts: 1


Variables
=========

- :py:data:`__version__`

.. autodata:: __version__
   :annotation:

   .. code-block:: text

      '2.4.0'
