.. doctest docs/specs/db.rst
.. _presto.specs.db:

=================================
Database structure of Lino Presto
=================================

This document describes the database structure.

.. contents::
  :local:


.. include:: /../docs/shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_presto.projects.presto1.settings.doctests')
>>> from lino.api.doctest import *


>>> analyzer.show_db_overview()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
45 plugins: lino, about, jinja, react, printing, system, users, office, xl, countries, contacts, uploads, contenttypes, gfks, cal, orders, periods, weasyprint, accounting, products, memo, linod, checkdata, excerpts, vat, trading, dashboard, calview, clients, households, addresses, phones, humanlinks, topics, healthcare, invoicing, sepa, notes, appypod, export_excel, tinymce, help, presto, staticfiles, sessions.
83 models:
=========================== ============================ ========= =======
 Name                        Default table                #fields   #rows
--------------------------- ---------------------------- --------- -------
 accounting.Account          accounting.Accounts          18        21
 accounting.Journal          accounting.Journals          27        8
 accounting.LedgerInfo       accounting.LedgerInfoTable   2         0
 accounting.MatchRule        accounting.MatchRules        3         0
 accounting.Movement         accounting.Movements         11        0
 accounting.PaymentTerm      accounting.PaymentTerms      11        8
 accounting.Voucher          accounting.AllVouchers       9         114
 addresses.Address           addresses.Addresses          16        145
 cal.Calendar                cal.Calendars                6         1
 cal.EntryRepeater           cal.EntryRepeaterTable       17        0
 cal.Event                   cal.Events                   26        1206
 cal.EventPolicy             cal.EventPolicies            20        6
 cal.EventType               cal.EventTypes               24        8
 cal.Guest                   cal.Guests                   6         1204
 cal.GuestRole               cal.GuestRoles               5         2
 cal.RecurrentEvent          cal.RecurrentEvents          22        16
 cal.RemoteCalendar          cal.RemoteCalendars          7         0
 cal.Room                    cal.Rooms                    13        6
 cal.Subscription            cal.Subscriptions            4         0
 cal.Task                    cal.Tasks                    17        6
 calview.DailyPlannerRow     calview.DailyPlannerRows     7         2
 checkdata.Message           checkdata.Messages           6         329
 clients.ClientContact       clients.ClientContacts       7         0
 clients.ClientContactType   clients.ClientContactTypes   5         5
 contacts.Company            contacts.Companies           30        31
 contacts.CompanyType        contacts.CompanyTypes        7         16
 contacts.Membership         contacts.Memberships         4         30
 contacts.Partner            contacts.Partners            28        151
 contacts.Person             contacts.Persons             35        106
 contacts.Role               contacts.Roles               4         4
 contacts.RoleType           contacts.RoleTypes           5         5
 contacts.Worker             contacts.Workers             38        9
 contenttypes.ContentType    gfks.ContentTypes            3         83
 countries.Country           countries.Countries          6         10
 countries.Place             countries.Places             9         80
 dashboard.Widget            dashboard.Widgets            5         0
 excerpts.Excerpt            excerpts.Excerpts            12        0
 excerpts.ExcerptType        excerpts.ExcerptTypes        17        7
 healthcare.Plan             healthcare.Plans             4         5
 healthcare.Rule             healthcare.Rules             6         0
 healthcare.Situation        healthcare.Situations        6         0
 households.Household        households.Households        30        14
 households.Member           households.Members           14        57
 households.Type             households.Types             4         6
 humanlinks.Link             humanlinks.Links             4         56
 invoicing.FollowUpRule      invoicing.FollowUpRules      5         2
 invoicing.Item              invoicing.Items              10        0
 invoicing.Plan              invoicing.Plans              8         1
 invoicing.SalesRule         invoicing.SalesRules         3         17
 invoicing.Tariff            invoicing.Tariffs            8         2
 invoicing.Task              invoicing.Tasks              29        1
 linod.SystemTask            linod.SystemTasks            25        2
 memo.Mention                memo.Mentions                5         0
 notes.EventType             notes.EventTypes             8         1
 notes.Note                  notes.Notes                  17        100
 notes.NoteType              notes.NoteTypes              11        3
 orders.Enrolment            orders.Enrolments            5         136
 orders.Order                orders.Orders                36        114
 orders.OrderItem            orders.OrderItems            7         114
 periods.StoredPeriod        periods.StoredPeriods        7         63
 periods.StoredYear          periods.StoredYears          5         11
 phones.ContactDetail        phones.ContactDetails        8         15
 presto.Client               presto.Clients               43        65
 presto.LifeMode             presto.LifeModes             4         6
 products.Category           products.Categories          15        2
 products.PriceRule          products.PriceRules          5         12
 products.Product            products.Products            20        9
 sepa.Account                sepa.Accounts                6         16
 sessions.Session            users.Sessions               3         ...
 system.SiteConfig           system.SiteConfigs           11        1
 tinymce.TextFieldTemplate   None                         5         2
 topics.Tag                  topics.Tags                  4         0
 topics.Topic                topics.Topics                4         3
 trading.InvoiceItem         trading.InvoiceItems         15        0
 trading.PaperType           trading.PaperTypes           5         3
 trading.VatProductInvoice   trading.Invoices             28        0
 uploads.Upload              uploads.Uploads              20        12
 uploads.UploadType          uploads.UploadTypes          10        11
 uploads.Volume              uploads.Volumes              4         1
 users.Authority             users.Authorities            3         0
 users.User                  users.AllUsers               21        4
 vat.InvoiceItem             vat.InvoiceItemTable         9         0
 vat.VatAccountInvoice       vat.Invoices                 21        0
=========================== ============================ ========= =======
<BLANKLINE>
