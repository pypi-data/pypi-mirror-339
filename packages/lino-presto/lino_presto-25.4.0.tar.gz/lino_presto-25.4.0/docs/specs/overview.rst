.. doctest docs/specs/overview.rst
.. include:: /../docs/shared/include/defs.rst

.. _lino.tested.presto:
.. _presto.specs.overview:

========
Overview
========

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_presto.projects.presto1.settings.doctests')
>>> from lino.api.doctest import *


Some vocabulary
===============

================ ================================
English          German
================ ================================
Furniture        Möbel
Used furniture   Gebrauchtmöbel
Renovation       Renovierungsarbeiten
Bicycle studio   Fahrradwerkstatt
Furniture store  Möbellager
Garden services  Gartenarbeiten
Home help        Haushaltshilfe
Small repair     Kleinreparaturen im Haushalt
Laundry service  Wäschedienst (Waschbären)
Transport        Transport
Moving           Umzüge
Delivery note    Lieferschein
================ ================================


- Managed as contracts : Garden contracts, Home help
- Managed as delivery notes  : Bicycle, Transport, Small repair, Moving, Furniture store, Renovation


Complexity factors
==================

>>> print(analyzer.show_complexity_factors())
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
- 45 plugins
- 83 models
- 4 user types
- 312 views
- 29 dialog actions
<BLANKLINE>




Don't read me
=============

>>> show_choicelists()
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
=============================== ======== ================= =============================== ================================== ==================================
 name                            #items   preferred_width   en                              de                                 fr
------------------------------- -------- ----------------- ------------------------------- ---------------------------------- ----------------------------------
 about.DateFormats               4        8                 Date formats                    Date formats                       Date formats
 about.TimeZones                 1        4                 Time zones                      Zeitzonen                          Time zones
 accounting.CommonAccounts       21       23                Common accounts                 Gemeinkonten                       Comptes communs
 accounting.DC                   2        6                 Booking directions              Buchungsrichtungen                 Directions d'imputation
 accounting.JournalGroups        7        26                Journal groups                  Journalgruppen                     Groupes de journaux
 accounting.TradeTypes           6        19                Trade types                     Handelsarten                       Types de commerce
 accounting.VoucherStates        4        10                Voucher states                  Belegzustände                      Voucher states
 accounting.VoucherTypes         4        41                Voucher types                   Belegarten                         Types de pièce
 addresses.AddressTypes          6        18                Address types                   Adressenarten                      Types d'adresses
 addresses.DataSources           2        16                Data sources                    Datenquellen                       Sources de données
 cal.EntryStates                 5        10                Entry states                    Kalendereintrag-Zustände           Entry states
 cal.EventEvents                 2        8                 Observed events                 Beobachtungskriterien              Évènements observés
 cal.GuestStates                 3        17                Presence states                 Anwesenheits-Zustände              Presence states
 cal.NotifyBeforeUnits           4        7                 Notify Units                    Notify Units                       Notify Units
 cal.PlannerColumns              5        10                Planner columns                 Tagesplanerkolonnen                Colonnes planificateur
 cal.ReservationStates           0        4                 States                          Zustände                           États
 cal.TaskStates                  5        9                 Task states                     Aufgaben-Zustände                  Task states
 cal.YearMonths                  12       9                 None                            None                               None
 calview.Planners                2        15                None                            None                               None
 checkdata.Checkers              17       90                Data checkers                   Datentests                         Tests de données
 clients.ClientEvents            3        8                 Observed events                 Beobachtungskriterien              Évènements observés
 clients.ClientStates            3        8                 Client states                   Bearbeitungszustände Klienten      Etats bénéficiaires
 clients.KnownContactTypes       2        5                 Known contact types             Standard-Klientenkontaktarten      Types de contact connus
 contacts.CivilStates            7        18                Civil states                    Zivilstände                        Etats civils
 contacts.PartnerEvents          1        18                Observed events                 Beobachtungskriterien              Évènements observés
 countries.PlaceTypes            23       14                None                            None                               None
 excerpts.Shortcuts              0        4                 Excerpt shortcuts               Excerpt shortcuts                  Excerpt shortcuts
 healthcare.Tariffs              3        6                 Healthcare tariffs              Krankenkassen-Tarife               Healthcare tariffs
 households.MemberDependencies   3        16                Household Member Dependencies   Haushaltsmitgliedsabhängigkeiten   Dépendances de membres de ménage
 households.MemberRoles          9        17                Household member roles          Haushaltsmitgliedsrollen           Rôles de membres de ménage
 humanlinks.LinkTypes            13       33                Parency types                   Verwandschaftsarten                Types de parenté
 invoicing.Periodicities         4        9                 Subscription periodicities      Abonnementperiodizitäten           Subscription periodicities
 linod.LogLevels                 5        8                 Logging levels                  Logging levels                     Logging levels
 linod.Procedures                3        25                Background procedures           Background procedures              Background procedures
 notes.SpecialTypes              0        4                 Special note types              Sondernotizarten                   Special note types
 orders.OrderStates              5        10                Voucher states                  Belegzustände                      Voucher states
 periods.PeriodStates            2        6                 States                          Zustände                           États
 periods.PeriodTypes             4        9                 Period types                    Period types                       Period types
 phones.ContactDetailTypes       6        7                 Contact detail types            Kontaktangabenarten                Contact detail types
 presto.IncomeCategories         4        4                 Income categories               Einkommenskategorien               Income categories
 printing.BuildMethods           10       20                None                            None                               None
 products.BarcodeDrivers         2        4                 Barcode drivers                 Barcode drivers                    Barcode drivers
 products.DeliveryUnits          13       13                Delivery units                  Liefereinheiten                    Unités de livraison
 products.PriceFactors           1        15                Price factors                   Price factors                      Price factors
 products.ProductTypes           2        9                 Product types                   Product types                      Product types
 system.DisplayColors            26       10                Display colors                  Display colors                     Display colors
 system.DurationUnits            7        7                 None                            None                               None
 system.Genders                  3        9                 Genders                         Geschlechter                       Sexes
 system.PeriodEvents             3        9                 Observed events                 Beobachtungskriterien              Évènements observés
 system.Recurrences              11       18                Recurrences                     Wiederholungen                     Récurrences
 system.Weekdays                 7        9                 None                            None                               None
 system.YesNo                    2        12                Yes or no                       Ja oder Nein                       Oui ou non
 uploads.Shortcuts               3        20                Upload shortcuts                Upload shortcuts                   Upload shortcuts
 uploads.UploadAreas             1        7                 Upload areas                    Upload-Bereiche                    Domaines de téléchargement
 users.UserTypes                 4        19                User types                      Benutzerarten                      Types d'utilisateur
 vat.DeclarationFieldsBase       0        4                 Declaration fields              Declaration fields                 Declaration fields
 vat.VatAreas                    3        13                VAT areas                       MWSt-Zonen                         Zones TVA
 vat.VatClasses                  8        25                VAT classes                     MwSt.-Klassen                      Classes TVA
 vat.VatColumns                  0        4                 VAT columns                     MWSt-Kolonnen                      VAT columns
 vat.VatRegimes                  1        6                 VAT regimes                     MwSt.-Regimes                      VAT regimes
 vat.VatRules                    1        38                VAT rules                       MwSt-Regeln                        VAT rules
 xl.Priorities                   5        8                 Priorities                      Prioritäten                        Priorités
=============================== ======== ================= =============================== ================================== ==================================
<BLANKLINE>


>>> rt.show(printing.BuildMethods)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
============ ============ ======================
 value        name         text
------------ ------------ ----------------------
 appydoc      appydoc      AppyDocBuildMethod
 appyodt      appyodt      AppyOdtBuildMethod
 appypdf      appypdf      AppyPdfBuildMethod
 appyrtf      appyrtf      AppyRtfBuildMethod
 latex        latex        LatexBuildMethod
 pub          pub          PublisherBuildMethod
 rtf          rtf          RtfBuildMethod
 weasy2html   weasy2html   WeasyHtmlBuildMethod
 weasy2pdf    weasy2pdf    WeasyPdfBuildMethod
 xml          xml          XmlBuildMethod
============ ============ ======================
<BLANKLINE>
