.. doctest docs/specs/menu.rst
.. include:: /../docs/shared/include/defs.rst

.. _presto.specs.menu:

========
The menu
========

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_presto.projects.presto1.settings.doctests')
>>> from lino.api.doctest import *

Dependencies
============

>>> dd.plugins.invoicing
<lino_xl.lib.invoicing.Plugin lino_xl.lib.invoicing(needs ['lino_xl.lib.trading'])>

>>> dd.plugins.trading
<lino_xl.lib.trading.Plugin lino_presto.lib.trading(needs ['lino.modlib.memo', 'lino_xl.lib.products', 'lino_xl.lib.vat'])>

>>> dd.plugins.products
<lino_xl.lib.products.Plugin lino_presto.lib.products(needs ['lino_xl.lib.xl'])>

>>> dd.plugins.orders
<lino_presto.lib.orders.Plugin lino_presto.lib.orders(needs ['lino_xl.lib.cal'])>

>>> show_menu('rolf')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Arbeiter, Organisationen, Personen, Haushalte, Klienten
- Büro : Meine ablaufenden Upload-Dateien, Meine Upload-Dateien, Meine Auszüge
- Kalender : Meine Termine, Überfällige Termine, Meine unbestätigten Termine, Meine überfälligen Termine, Meine Aufgaben, Einsätze auf Ersatzsuche, Kalender, Mitarbeiterplaner
- Aufträge : Wartende Aufträge, Aktive Aufträge, Dringende Aufträge, -, Garden (Garden), Moves (Moves), Renovation (Renovation), Home help (Home help), Home care (Home care), Office (Office)
- Verkauf : Verkaufsrechnungen (SLS), Händische Rechnungen (MAN), Mein Fakturationsplan
- Konfigurierung :
  - System : Benutzer, Site-Konfiguration, System tasks
  - Kontakte : Rechtsformen, Funktionen, Klientenkontaktarten, Haushaltsarten, Themen, Krankenkassen, Krankenkassen-Regeln, Lebensweisen
  - Büro : Dateibibliotheken, Upload-Arten, Notizarten, Ereignisarten, Auszugsarten
  - Kalender : Kalenderliste, Teams, Regelmäßige Ereignisse, Gastrollen, Kalendereintragsarten, Wiederholungsregeln, Externe Kalender, Tagesplanerzeilen
  - Buchhaltung : Konten, Journale, Zahlungsbedingungen, Geschäftsjahre, Buchungsperioden
  - Produkte : Dienstleistungen, Möbel, Produktkategorien, Preisregeln
  - Verkauf : Papierarten, Pauschalen, Folgeregeln, Fakturierungsaufgaben
  - Orte : Länder, Orte
- Explorer :
  - System : Vollmachten, Benutzerarten, Benutzerrollen, All dashboard widgets, Datenbankmodelle, Background procedures, Datentests, Datenproblemmeldungen
  - Kontakte : Kontaktpersonen, Partner, Klientenkontakte, Standard-Klientenkontaktarten, Haushaltsmitgliedsrollen, Mitglieder, Adressenarten, Adressen, Kontaktangabenarten, Kontaktangaben, Verwandtschaftsbeziehungen, Verwandschaftsarten, Tags, Krankenkassen-Tarife, Krankenkassen-Situationen, Klienten
  - Büro : Upload-Dateien, Upload-Bereiche, Erwähnungen, Auszüge
  - Kalender : Kalendereinträge, Aufgaben, Anwesenheiten, Abonnements, Kalendereintrag-Zustände, Anwesenheits-Zustände, Aufgaben-Zustände, Tagesplanerkolonnen, Display colors
  - Aufträge : Aufträge, Einschreibungen
  - Buchhaltung : Gemeinkonten, Begleichungsregeln, Belege, Belegarten, Bewegungen, Handelsarten, Journalgruppen
  - Produkte : Price factors
  - Verkauf : Verkaufsrechnungen, Sales invoice items, Fakturationspläne, Verkaufsregeln
  - SEPA : Bankkonten
  - MwSt. : MWSt-Zonen, MwSt.-Regimes, MwSt.-Klassen, MWSt-Kolonnen, Rechnungen, MwSt-Regeln
- Site : Info, Benutzersitzungen
