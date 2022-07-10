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
   teslajsonpy.connection
   teslajsonpy.const
   teslajsonpy.controller
   teslajsonpy.exceptions
   teslajsonpy.homeassistant
   teslajsonpy.teslaproxy

.. currentmodule:: teslajsonpy


Classes
=======

- :py:class:`Connection`:
  Connection to Tesla Motors API.

- :py:class:`Controller`:
  Controller for connections to Tesla Motors API.

- :py:class:`TeslaProxy`:
  Class to handle proxy login connections to Alexa.

- :py:class:`Battery`:
  Home-Assistant battery class for a Tesla VehicleDevice.

- :py:class:`Range`:
  Home-Assistant class of the battery range for a Tesla VehicleDevice.

- :py:class:`ChargerConnectionSensor`:
  Home-assistant charger connection class for Tesla vehicles.

- :py:class:`ChargingSensor`:
  Home-Assistant charging sensor class for a Tesla VehicleDevice.

- :py:class:`OnlineSensor`:
  Home-Assistant Online sensor class for a Tesla VehicleDevice.

- :py:class:`ParkingSensor`:
  Home-assistant parking brake class for Tesla vehicles.

- :py:class:`UpdateSensor`:
  Home-Assistant update sensor class for a Tesla VehicleDevice.

- :py:class:`ChargerSwitch`:
  Home-Assistant class for the charger of a Tesla VehicleDevice.

- :py:class:`RangeSwitch`:
  Home-Assistant class for setting range limit for charger.

- :py:class:`Climate`:
  Home-assistant class of HVAC for Tesla vehicles.

- :py:class:`TempSensor`:
  Home-assistant class of temperature sensors for Tesla vehicles.

- :py:class:`GPS`:
  Home-assistant class for GPS of Tesla vehicles.

- :py:class:`Odometer`:
  Home-assistant class for odometer of Tesla vehicles.

- :py:class:`Lock`:
  Home-assistant lock class for Tesla vehicles.

- :py:class:`SentryModeSwitch`:
  Home-Assistant class for sentry mode of Tesla vehicles.

- :py:class:`Horn`:
  Home-Assistant class for horn of Tesla vehicles.

- :py:class:`FlashLights`:
  Home-Assistant class for flash lights of Tesla vehicles.

- :py:class:`TriggerHomelink`:
  Home-Assistant class for trigger homelink of Tesla vehicles.

- :py:class:`TrunkLock`:
  Home-Assistant rear trunk lock for a Tesla VehicleDevice.

- :py:class:`FrunkLock`:
  Home-Assistant front trunk (frunk) lock for a Tesla VehicleDevice.


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

.. autoclass:: TeslaProxy
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: TeslaProxy
      :parts: 1

.. autoclass:: Battery
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Battery
      :parts: 1

.. autoclass:: Range
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Range
      :parts: 1

.. autoclass:: ChargerConnectionSensor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ChargerConnectionSensor
      :parts: 1

.. autoclass:: ChargingSensor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ChargingSensor
      :parts: 1

.. autoclass:: OnlineSensor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OnlineSensor
      :parts: 1

.. autoclass:: ParkingSensor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ParkingSensor
      :parts: 1

.. autoclass:: UpdateSensor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UpdateSensor
      :parts: 1

.. autoclass:: ChargerSwitch
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ChargerSwitch
      :parts: 1

.. autoclass:: RangeSwitch
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: RangeSwitch
      :parts: 1

.. autoclass:: Climate
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Climate
      :parts: 1

.. autoclass:: TempSensor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: TempSensor
      :parts: 1

.. autoclass:: GPS
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GPS
      :parts: 1

.. autoclass:: Odometer
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Odometer
      :parts: 1

.. autoclass:: Lock
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Lock
      :parts: 1

.. autoclass:: SentryModeSwitch
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: SentryModeSwitch
      :parts: 1

.. autoclass:: Horn
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Horn
      :parts: 1

.. autoclass:: FlashLights
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FlashLights
      :parts: 1

.. autoclass:: TriggerHomelink
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: TriggerHomelink
      :parts: 1

.. autoclass:: TrunkLock
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: TrunkLock
      :parts: 1

.. autoclass:: FrunkLock
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FrunkLock
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

      '2.3.0'
