Introduction
============

Basic Usage
-----------

Importing
^^^^^^^^^

  >>> from khayyam import *

This will imports
:py:class:`khayyam.JalaliDate`,
:py:class:`khayyam.JalaliDatetime`,
:py:class:`khayyam.Timezone`,
:py:class:`khayyam.TehranTimezone`,
:py:obj:`khayyam.MINYEAR`,
:py:obj:`khayyam.MAXYEAR`,
:py:obj:`khayyam.SATURDAY`,
:py:obj:`khayyam.SUNDAY`,
:py:obj:`khayyam.MONDAY`,
:py:obj:`khayyam.THURSDAY`,
:py:obj:`khayyam.WEDNESDAY`,
:py:obj:`khayyam.TUESDAY`,
:py:obj:`khayyam.FRIDAY`

Or

  >>> from khayyam import JalaliDatetime, TehranTimezone

And:


  >>> print(JalaliDatetime)
  <class 'khayyam.jalali_datetime.JalaliDatetime'>


Instantiating
^^^^^^^^^^^^^

Simply you can instantiate :py:class:`khayyam.JalaliDate`
and :py:class:`khayyam.JalaliDatetime` classes just like the other regular python classes.


.. doctest::

  >>> JalaliDate(1345)
  khayyam.JalaliDate(1345, 1, 1, Doshanbeh)

  >>> JalaliDate(427, 2, 28) # Khayyam's birthday
  khayyam.JalaliDate(427, 2, 28, Panjshanbeh)

  >>> JalaliDate(1345, 12, 30) # doctest: +SKIP
  ValueError: .... # So, it's not a leap year!

  >>> JalaliDate(1346, 12, 30) # A leap year.
  khayyam.JalaliDate(1346, 12, 30, Chaharshanbeh)

  >>> JalaliDatetime(JalaliDate(1345, 1, 1))
  khayyam.JalaliDatetime(1345, 1, 1, 0, 0, 0, 0, Doshanbeh)

  >>> from datetime import datetime
  >>> JalaliDatetime(datetime(1982, 9, 6))
  khayyam.JalaliDatetime(1361, 6, 15, 0, 0, 0, 0, Doshanbeh)

  >>> JalaliDatetime()
  khayyam.JalaliDatetime(1, 1, 1, 0, 0, 0, 0, Jomeh)

Interesting! the calendar starting by friday.

Adjusting microseconds:

  >>> JalaliDatetime(989, 3, 25, 10, 43, 23, 345453)
  khayyam.JalaliDatetime(989, 3, 25, 10, 43, 23, 345453, Seshanbeh)


Current date and time
^^^^^^^^^^^^^^^^^^^^^

.. doctest::

  >>> JalaliDatetime.now() # doctest: +SKIP
  khayyam.JalaliDatetime(1394, 4, 30, 20, 49, 55, 205834, Seshanbeh)

  >>> print(JalaliDatetime.now())) # doctest: +SKIP
  1394-04-30 20:56:20.991585


DST aware

.. doctest::

  >>> print(JalaliDatetime.now(TehranTimezone())) # doctest: +SKIP
  1394-04-30 19:59:12.935506+04:30

  >>> print(JalaliDatetime.now(TehranTimezone()) - timedelta(days=6*30)) # doctest: +SKIP
  1393-11-02 20:01:11.663719+03:30

As you see, the DST offset in the second statement is `+3:30`. so
the :py:class:`khayyam.TehranTimezone` is supporting `daylight saving time` properly.

Today

.. doctest::

  >>> JalaliDate.today() # doctest: +SKIP
  khayyam.JalaliDate(1394, 4, 30, Seshanbeh)

  >>> print(JalaliDate.today()) # doctest: +SKIP
  1394-4-30

  >>> print(JalaliDate.today().strftime('%A %d %B %Y')) # doctest: +SKIP
  چهارشنبه 31 تیر 1394

  >>> print(JalaliDate(1394, 5, 1).strftime('%A %D %B %N'))
  پنجشنبه ۱ مرداد ۱۳۹۴



Right-to-left
^^^^^^^^^^^^^

Additionally, if right to left text rendering is not supported by your terminal emulator::

  ﻅ.ﺏ 05:45:40 1394 ﺩاﺩﺮﻣ 01 ﻪﺒﻨﺸﺠﻨﭘ

You can install the rtl package:

.. code-block:: console

  $ pip install rtl

And then use it to reshape and change direction of the text

.. doctest::

  >>> from rtl import rtl
  >>> print(rtl(JalaliDatetime(1394, 5, 1, 17, 45, 40).strftime('%C'))) # doctest: +SKIP
  پنجشنبه 01 مرداد 1394 05:45:40 ب.ظ


rprint() function
^^^^^^^^^^^^^^^^^

If you are using python2 its good to import new print function:

  >>> from __future__ import print_function

Extending your practice environment by defining a handy print function for RTL:

.. doctest::

  >>> def rprint(s):
  ...     print(rtl(s))

  >>> rprint(JalaliDatetime(1394, 5, 1, 17, 45, 40).strftime('%C')) # doctest: +SKIP
  پنجشنبه 01 مرداد 1394 05:45:40 ب.ظ


Formatting & Parsing
--------------------

All Supported format directives are listed here: :doc:`/directives`.

All formatting behaviours are driven from :ref:`strftime-strptime-behavior`.

To format locale's date & time:

  >>> from khayyam import JalaliDatetime
  >>> dt = JalaliDatetime(1394, 4, 31, 17, 45, 40)
  >>> time_string = dt.strftime('%C')
  >>> print(time_string)
  چهارشنبه ۳۱ تیر ۱۳۹۴ ۰۵:۴۵:۴۰ ب.ظ


And parsing it again to a :py:class:`khayyam.JalaliDatetime` instance:

  >>> JalaliDatetime.strptime(time_string, '%C')
  khayyam.JalaliDatetime(1394, 4, 31, 17, 45, 40, 0, Chaharshanbeh)


You may use `%f` and or `%z` formatting directives to represent
microseconds and timezone info in your formatting or parsing pattern.

So, to reach accurate serialization, you could include those two
directive alongside time and date directives in your pattern. for example:

  >>> from datetime import timedelta
  >>> from khayyam import Timezone
  >>> tz = Timezone(timedelta(seconds=60*210)) # +3:30 Tehran
  >>> now_string = JalaliDatetime(1394, 4, 31, 14, 10, 21, 452958, tz).strftime('%Y-%m-%d %H:%M:%S.%f %z')
  >>> print(now_string)
  1394-04-31 14:10:21.452958 +03:30

Parse it back to the :py:class:`khayyam.JalaliDatetime` instance:

  >>> now = JalaliDatetime.strptime(now_string, '%Y-%m-%d %H:%M:%S.%f %z')
  >>> now
  khayyam.JalaliDatetime(1394, 4, 31, 14, 10, 21, 452958, tzinfo=+03:30, Chaharshanbeh)


Try some formatting and parsing directives:

.. doctest::

  >>> now = JalaliDatetime(1394, 4, 31)
  >>> print(now.strftime('%a %d %B %y'))
  چ 31 تیر 94

  >>> print(now.strftime('%A %d %b %Y'))
  چهارشنبه 31 تی 1394

  >>> from khayyam import TehranTimezone
  >>> print(now.astimezone(TehranTimezone()).strftime('%A %d %B %Y %Z'))
  چهارشنبه 31 تیر 1394 Iran/Tehran

Converting
----------

Converting to gregorian calendar, python's native
:py:class:`datetime.date` and :py:class:`datetime.datetime`:

.. doctest::

  >>> from datetime import date, datetime
  >>> from khayyam import JalaliDate, JalaliDatetime, TehranTimezone

  >>> JalaliDate(1394, 4, 31).todate()
  datetime.date(2015, 7, 22)

  >>> now = JalaliDatetime(1394, 4, 31, 15, 38, 6, 37269)
  >>> now.todate()
  datetime.date(2015, 7, 22)

  >>> now.todatetime()
  datetime.datetime(2015, 7, 22, 15, 38, 6, 37269)


And vise-versa:

.. doctest::

  >>> JalaliDatetime(datetime(2015, 7, 22, 14, 47, 9, 821830))
  khayyam.JalaliDatetime(1394, 4, 31, 14, 47, 9, 821830, Chaharshanbeh)

  >>> JalaliDatetime(datetime(2015, 7, 22, 14, 47, 9, 821830, TehranTimezone()))
  khayyam.JalaliDatetime(1394, 4, 31, 14, 47, 9, 821830, tzinfo=+03:30 dst:60, Chaharshanbeh)

  >>> JalaliDate(date(2015, 7, 22))
  khayyam.JalaliDate(1394, 4, 31, Chaharshanbeh)


Arithmetics & Operators
-----------------------

Addition and subtraction:

.. doctest::

  >>> from datetime import timedelta
  >>> from khayyam import JalaliDate, JalaliDatetime
  >>> now = JalaliDatetime(1394, 4, 31, 16, 17, 31, 374398)
  >>> now
  khayyam.JalaliDatetime(1394, 4, 31, 16, 17, 31, 374398, Chaharshanbeh)

  >>> now + timedelta(days=1)
  khayyam.JalaliDatetime(1394, 5, 1, 16, 17, 31, 374398, Panjshanbeh)

  >>> now + timedelta(seconds=3600)
  khayyam.JalaliDatetime(1394, 4, 31, 17, 17, 31, 374398, Chaharshanbeh)

  >>> now - timedelta(seconds=3600)
  khayyam.JalaliDatetime(1394, 4, 31, 15, 17, 31, 374398, Chaharshanbeh)

  >>> yesterday = now - timedelta(1)
  >>> yesterday
  khayyam.JalaliDatetime(1394, 4, 30, 16, 17, 31, 374398, Seshanbeh)

  >>> now - yesterday
  datetime.timedelta(1)

  >>> JalaliDatetime.now() - now # doctest: +SKIP
  datetime.timedelta(0, 478, 328833) # 478 seconds taken to writing this section


Supported operators:

* :py:meth:`khayyam.JalaliDate.__add__`
* :py:meth:`khayyam.JalaliDate.__sub__`



Comparison
----------

Just like the :py:mod:`datetime`, all comparison operators are overridden:

* :py:meth:`khayyam.JalaliDate.__lt__`
* :py:meth:`khayyam.JalaliDate.__le__`
* :py:meth:`khayyam.JalaliDate.__hash__`
* :py:meth:`khayyam.JalaliDate.__eq__`
* :py:meth:`khayyam.JalaliDate.__ne__`
* :py:meth:`khayyam.JalaliDate.__gt__`
* :py:meth:`khayyam.JalaliDate.__ge__`

So:

.. doctest::

  >>> now > yesterday
  True

  >>> now != yesterday
  True

  >>> now.todate() == yesterday.todate()
  False
