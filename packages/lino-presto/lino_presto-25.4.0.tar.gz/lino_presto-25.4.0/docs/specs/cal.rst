.. doctest docs/specs/cal.rst
.. include:: /../docs/shared/include/defs.rst

.. _presto.specs.cal:

=============================
The Calendar plugin in Presto
=============================

Presto extends the standard :mod:`lino_xl.lib.cal` plugin
:mod:`lino_presto.lib.cal`.

.. contents::
  :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_presto.projects.presto1.settings.doctests')
>>> from lino.api.doctest import *


Workflow
========

Presto uses the :mod:`lino_xl.lib.cal.workflows.voga` workflow, but with some
customizations:

- Add a calendar entry state "missed" (which means that the
  *client* missed the appointment).
- Don't refuse to mark an entry as "took place"
  when a guest (a worker) is still "invited".


>>> rt.show(cal.EntryStates)
======= ============ ============ ============= ============= ======== ============= =========
 value   name         text         Button text   Fill guests   Stable   Transparent   No auto
------- ------------ ------------ ------------- ------------- -------- ------------- ---------
 10      suggested    Suggested    ?             Yes           No       No            No
 20      draft        Scheduled    ☐             Yes           No       No            No
 50      took_place   Took place   ☑             No            Yes      No            No
 60      missed       Missed       ☉             No            Yes      No            Yes
 70      cancelled    Called off   ⚕             No            Yes      Yes           Yes
======= ============ ============ ============= ============= ======== ============= =========
<BLANKLINE>


Don't refuse to mark an entry as "took place" when a guest (a worker) is still
"invited". The internal name of the default guest state is "invited", but that's
only the internal name, the verbose name is "Present".   Saying that a
deployment took place, in Presto means that you confirm that all invited workers
were present.

>>> rt.show(cal.GuestStates)
======= ========= ============ =================== =============
 value   name      Afterwards   text                Button text
------- --------- ------------ ------------------- -------------
 10      invited   No           Present             ☑
 50      needs     Yes          Needs replacement   ⚕
 60      found     No           Found replacement   ☉
======= ========= ============ =================== =============
<BLANKLINE>


Replacement planning
====================

A worker announces that they need replacement for a deployment in the future.
You find the calendar entry, and in the :class:`GuestsByEntry` slave table,
Workflow column, change the presence state from "planned" to "needs replacement"

At any moment you can see the :class:`GuestsNeedingReplacement` table, which
shows all presences needing replacement.

>>> rt.login("robin").show(cal.GuestsNeedingReplacement)
============ ============ ============= ======================================================== ====================================================== ========
 Start date   Start time   Worker        Calendar entry                                           Workflow                                               Remark
------------ ------------ ------------- -------------------------------------------------------- ------------------------------------------------------ --------
 16/03/2017   14:00:00     Mrs Helen     `JACOBS Jacqueline (136) Eupen Einsatz 2  <…>`__         **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 21/03/2017   11:00:00     Mrs Maria     `MALMENDIER Marc (145) Eupen Einsatz 4  <…>`__           **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 23/03/2017   13:00:00     Mr Ahmed      `RADERMECKER Rik (172) Amsterdam Einsatz 4  <…>`__       **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 15/04/2017   11:00:00     Mrs Maria     `LAHM Lisa (175) Aachen Einsatz 6  <…>`__                **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 06/05/2017   11:00:00     Mr Conrad     `EVERTZ Bernd (125) Eupen Einsatz 11  <…>`__             **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 30/05/2017   11:00:00     Mr Conrad     `EMONTS-GAST Erna (151) Raeren Einsatz 13  <…>`__        **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 26/06/2017   11:00:00     Mrs Maria     `HILGERS Hildegard (132) Eupen Deployment 5  <…>`__      **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 22/07/2017   08:00:00     Mr Garry      `DERICUM Daniel (120) Eupen Einsatz 22  <…>`__           **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 29/07/2017   09:00:00     Mrs Evelyne   `MIESSEN Michael (147) Eupen Einsatz 22  <…>`__          **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 16/08/2017   08:00:00     Mr Garry      `CHANTRAINE Marc (119) Eupen Einsatz 24  <…>`__          **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 19/08/2017   09:00:00     Mrs Evelyne   `LEFFIN Josefine (144) Eupen Einsatz 24  <…>`__          **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 23/08/2017   14:00:00     Mrs Helen     `JOUSTEN Jan (139) Eupen Einsatz 26  <…>`__              **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 09/09/2017   11:00:00     Mrs Maria     `EVERTZ Bernd (125) Eupen Deployment 7  <…>`__           **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 09/09/2017   14:00:00     Mrs Helen     `JACOBS Jacqueline (136) Eupen Einsatz 27  <…>`__        **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 26/04/2018   08:00:00     Mr Dennis     `EMONTS Daniel (127) Eupen Deployment 15  <…>`__         **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 03/06/2018   09:00:00     Mrs Beata     `RADERMACHER Edgard (156) Raeren Deployment 16  <…>`__   **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 06/07/2018   08:00:00     Mr Dennis     `DERICUM Daniel (120) Eupen Deployment 17  <…>`__        **⚕ Needs replacement** → [Find replacement] [☑] [☉]
 13/08/2018   09:00:00     Mrs Beata     `MIESSEN Michael (147) Eupen Deployment 18  <…>`__       **⚕ Needs replacement** → [Find replacement] [☑] [☉]
============ ============ ============= ======================================================== ====================================================== ========
<BLANKLINE>

When this table is not empty, it causes a welcome message "You have 3 items in
Needing replacement".

In the workflow column you can click on "Find replacement" to specify another
worker who is going to replace the originally planned worker.


Teams
=====

A team is a group of workers responsible for a given activity.

The team of an order is defined by its journal. You can have a same team for
different journals, but you cannot have several teams for one journal.

Lino Presto injects a field :attr:`lino_xl.lib.accounting.Journal.room`.

.. class:: Room

    .. attribute:: event_type
    .. attribute:: guest_role
    .. attribute:: invoicing_area

>>> print(rt.models.cal.Room._meta.verbose_name)
Team

>>> rt.show(cal.Rooms, language="en")
============= ================== ================== =====================
 Designation   Designation (de)   Designation (fr)   Calendar entry type
------------- ------------------ ------------------ ---------------------
 Garden        Garten             Garden             Outside work
 Moves         Umzüge             Moves              Craftsmen
 Renovation    Renovierung        Renovation         Craftsmen
 Home help     Haushaltshilfe     Home help          Home care
 Home care     Heimpflege         Home care          Home care
 Office        Büro               Bureau             Office work
============= ================== ================== =====================
<BLANKLINE>

In Lino Presto we have *two* planners:

>>> rt.show(calview.Planners)
========== ========== ================= ===================== ===================== ====================
 value      name       text              Monthly view          Weekly view           Daily view
---------- ---------- ----------------- --------------------- --------------------- --------------------
 default    default    Calendar          calview.MonthlyView   calview.WeeklyView    calview.DailyView
 contacts   contacts   Workers planner                         contacts.WeeklyView   contacts.DailyView
========== ========== ================= ===================== ===================== ====================
<BLANKLINE>


Presto contacts :

.. inheritance-diagram::
    lino_presto.lib.contacts.models.DailyView
    lino_presto.lib.contacts.models.WeeklyView
    :parts: 1
    :top-classes: lino.core.actors.Actor

Don't read
==========

>>> contacts.WeeklyView.planner
<calview.Planners.contacts:contacts>

>>> contacts.DailyView.planner is contacts.WeeklyView.planner
True

>>> calview.WeeklyView.planner
<calview.Planners.default:default>

>>> for a in contacts.WeeklyView.collect_extra_actions():
...     print(repr(a))
<lino.core.actions.WrappedAction contacts_DailyView_detail ('Detail')>
<lino.core.actions.WrappedAction contacts_WeeklyView_detail ('Detail')>

>>> a = contacts.WeeklyView.detail_action.action
>>> ut = rt.login("robin").get_user().user_type
>>> for ba in contacts.WeeklyView.get_toolbar_actions(a, ut):
...     print(ba.action.button_text, ba.action.label)
Daily Detail
Weekly Detail
