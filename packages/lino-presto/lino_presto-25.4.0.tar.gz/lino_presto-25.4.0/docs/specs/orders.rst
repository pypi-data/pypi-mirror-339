.. doctest docs/specs/orders.rst
.. include:: /../docs/shared/include/defs.rst

.. _presto.specs.orders:

=========
Orders
=========

Orders in Presto are implemented using the :mod:`lino_xl.lib.orders`
plugin.

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_presto.projects.presto1.settings.doctests')
>>> from lino.api.doctest import *

>>> with translation.override("en"):
...     print(dd.plugins.orders.verbose_name)
Orders

>>> rt.show(accounting.JournalGroups, language="en")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
======= =========== ============================
 value   name        text
------- ----------- ----------------------------
 05      orders      Orders
 10      sales       Sales
 20      purchases   Purchases
 30      wages       Wages
 40      financial   Financial
 50      vat         VAT
 60      misc        Miscellaneous transactions
======= =========== ============================


>>> rt.show(orders.Orders, language="en")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
============ ========================================= ======== ===============
 Start date   Client                                    Remark   Workflow
------------ ----------------------------------------- -------- ---------------
 13/03/2017   MIESSEN Michael (147)                              **Active**
 12/03/2017   MEESSEN Melissa (146)                              **Cancelled**
 12/03/2017   LAMBERTZ Guido (141)                               **Done**
 12/03/2017   MARTELAER Mark (171)                               **Done**
 12/03/2017   RADERMACHER Alfons (152)                           **Urgent**
 ...
 24/02/2017   DOBBELSTEIN-DEMEULENAERE Dorothée (122)            **Urgent**
 24/02/2017   EMONTS Erich (149)                                 **Active**
 23/02/2017   DEMEULENAERE Dorothée (121)                        **Done**
 23/02/2017   EMONTS-GAST Erna (151)                             **Urgent**
 23/02/2017   CHARLIER Ulrike (118)                              **Active**
 23/02/2017   DOBBELSTEIN Dorothée (123)                         **Active**
 22/02/2017   BRECHT Bernd (176)                                 **Cancelled**
 22/02/2017   DENON Denis (179)                                  **Cancelled**
 22/02/2017   BASTIAENSEN Laurent (116)                          **Done**
 22/02/2017   ALTENBERG Hans (114)                               **Waiting**
 22/02/2017   CHANTRAINE Marc (119)                              **Waiting**
 22/02/2017   DERICUM Daniel (120)                               **Waiting**
 21/02/2017   AUSDEMWALD Alfons (115)                            **Urgent**
 21/02/2017   ARENS Andreas (112)                                **Active**
============ ========================================= ======== ===============
<BLANKLINE>



>>> rt.show(orders.OrderStates, language="en")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
======= ============ =========== ==========
 value   name         text        Editable
------- ------------ ----------- ----------
 10      draft        Waiting     Yes
 20      active       Active      Yes
 30      urgent       Urgent      Yes
 40      registered   Done        No
 50      cancelled    Cancelled   No
======= ============ =========== ==========
<BLANKLINE>

>>> rt.show(accounting.VoucherTypes, language="en")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF -SKIP
=========================== ====== =========================================== ========================================================
 value                       name   text                                        Model
--------------------------- ------ ------------------------------------------- --------------------------------------------------------
 orders.OrdersByJournal             Order (orders.OrdersByJournal)              <class 'lino_presto.lib.orders.models.Order'>
 orders.TraOrdersByJournal          Order (orders.TraOrdersByJournal)           <class 'lino_presto.lib.orders.models.Order'>
 trading.InvoicesByJournal          Sales invoice (trading.InvoicesByJournal)   <class 'lino_xl.lib.trading.models.VatProductInvoice'>
 vat.InvoicesByJournal              Invoice (vat.InvoicesByJournal)             <class 'lino_xl.lib.vat.models.VatAccountInvoice'>
=========================== ====== =========================================== ========================================================
<BLANKLINE>

>>> accounting.VoucherTypes.get_for_model(orders.Order)

>>> rt.login('robin').show(orders.WaitingOrders)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
============ =========================== ============================ ==================================================== ================= ================================ =============
 Date         Client                      Order                        Workflow                                             Author            When                             Times
------------ --------------------------- ---------------------------- ---------------------------------------------------- ----------------- -------------------------------- -------------
 21/02/2017   ALTENBERG Hans (114)        `Garden 1/2017 <…>`__        **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Martha            On Wednesday, 22 February 2017   08:00-09:00
 21/02/2017   CHANTRAINE Marc (119)       `Office 1/2017 <…>`__        **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Romain Raffault   Every day                        08:00-09:00
 22/02/2017   DERICUM Daniel (120)        `Home care 2/2017 <…>`__     **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Rolf Rompen       Every week                       08:00-09:00
 23/02/2017   EMONTS Daniel (127)         `Home help 3/2017 <…>`__     **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Robin Rood        Every month                      08:00-09:00
 24/02/2017   ERNST Berta (124)           `Renovation 4/2017 <…>`__    **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Martha            On Saturday, 25 February 2017    08:00-09:00
 25/02/2017   GROTECLAES Gregory (131)    `Moves 5/2017 <…>`__         **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Romain Raffault   Every day                        08:00-09:00
 26/02/2017   JANSEN Jérémy (135)         `Garden 6/2017 <…>`__        **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Rolf Rompen       Every week                       08:00-09:00
 26/02/2017   KAIVERS Karl (140)          `Office 6/2017 <…>`__        **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Robin Rood        Every month                      08:00-09:00
 27/02/2017   LAZARUS Line (143)          `Home care 7/2017 <…>`__     **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Martha            On Tuesday, 28 February 2017     08:00-09:00
 28/02/2017   MEIER Marie-Louise (148)    `Home help 8/2017 <…>`__     **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Romain Raffault   Every day                        08:00-09:00
 01/03/2017   RADERMACHER Daniela (155)   `Renovation 9/2017 <…>`__    **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Rolf Rompen       Every week                       08:00-09:00
 02/03/2017   RADERMACHER Hedi (160)      `Moves 10/2017 <…>`__        **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Robin Rood        Every month                      08:00-09:00
 03/03/2017   DA VINCI David (164)        `Garden 11/2017 <…>`__       **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Martha            On Saturday, 4 March 2017        08:00-09:00
 03/03/2017   ALTENBERG Hans (114)        `Office 11/2017 <…>`__       **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Romain Raffault   Every day                        08:00-09:00
 04/03/2017   CHANTRAINE Marc (119)       `Home care 12/2017 <…>`__    **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Rolf Rompen       Every week                       08:00-09:00
 05/03/2017   DERICUM Daniel (120)        `Home help 13/2017 <…>`__    **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Robin Rood        Every month                      08:00-09:00
 06/03/2017   EMONTS Daniel (127)         `Renovation 14/2017 <…>`__   **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Martha            On Tuesday, 7 March 2017         08:00-09:00
 07/03/2017   ERNST Berta (124)           `Moves 15/2017 <…>`__        **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Romain Raffault   Every day                        08:00-09:00
 08/03/2017   GROTECLAES Gregory (131)    `Garden 16/2017 <…>`__       **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Rolf Rompen       Every week                       08:00-09:00
 08/03/2017   JANSEN Jérémy (135)         `Office 16/2017 <…>`__       **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Robin Rood        Every month                      08:00-09:00
 09/03/2017   KAIVERS Karl (140)          `Home care 17/2017 <…>`__    **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Martha            On Friday, 10 March 2017         08:00-09:00
 10/03/2017   LAZARUS Line (143)          `Home help 18/2017 <…>`__    **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Romain Raffault   Every day                        08:00-09:00
 11/03/2017   MEIER Marie-Louise (148)    `Renovation 19/2017 <…>`__   **Waiting** → [Active] [Urgent] [Done] [Cancelled]   Rolf Rompen       Every week                       08:00-09:00
============ =========================== ============================ ==================================================== ================= ================================ =============
<BLANKLINE>
