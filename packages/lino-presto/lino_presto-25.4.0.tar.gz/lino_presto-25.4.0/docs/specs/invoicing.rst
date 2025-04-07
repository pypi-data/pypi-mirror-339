.. doctest docs/specs/invoicing.rst
.. include:: /../docs/shared/include/defs.rst

.. _presto.specs.invoicing:

=========
Invoicing
=========

.. currentmodule:: lino_presto.lib.invoicing

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_presto.projects.presto1.settings.doctests')
>>> from lino.api.doctest import *

>>> with translation.override("en"):
...     print(dd.plugins.invoicing.verbose_name)
Invoicing


.. class:: Plan

    An extended invoicing plan.

    .. attribute:: order

        If this field is nonempty, select only enrolments of that
        given order.

.. class:: StartInvoicingForOrder

    Start an invoicing plan for this order.

    This action is installed onto the :class:`orders.Order
    <lino_xl.lib.orders.Order>` model as `start_invoicing`.
