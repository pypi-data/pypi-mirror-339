.. doctest docs/specs/uploads.rst
.. _presto.specs.uploads:

=======================================
Uploads with expiration date management
=======================================

.. currentmodule:: lino_xl.lib.uploads

In Lino Presto we use the :mod:`lino_xl.lib.uploads` plugin to manage
certificates that were considered for assigning the price category of a client.
These documents are issued by other institutions. When registering a new order,
the office worker usually checks whether the category is still correct based on
the expiry date of the relevant uploaded documents.  They have an upload
shortcut "tariff certificate"


.. contents::
  :local:

.. include:: /../docs/shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_presto.projects.presto1.settings.doctests')
>>> from lino.api.doctest import *

Here are the default values for the :class:`MyExpiringUploads` table:

>>> dd.plugins.uploads.expiring_start
0
>>> dd.plugins.uploads.expiring_end
365

The demo_coach is the user who uploaded all demo uploads.

>>> dd.plugins.clients.demo_coach
'martha'

>>> rt.show(rt.models.uploads.Shortcuts)
==================================== ==================== ======================
 value                                name                 text
------------------------------------ -------------------- ----------------------
 accounting.Voucher.source_document   source_document      Source document
 presto.Client.id_document            id_document          Identifying document
 presto.Client.income_certificate     income_certificate   Income certificate
==================================== ==================== ======================
<BLANKLINE>
