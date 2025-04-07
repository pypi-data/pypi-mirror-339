.. doctest dedocs/basics/tour.rst
.. include:: /../docs/shared/include/defs.rst
.. _presto.de.tour:

======================
Eine Besichtigungstour
======================

.. contents::
  :local:

Anmeldung
=========

Wir melden uns an als Rolf. Der ist Systemverwalter und darf deshalb alles. Wer
es lieber in Französisch hat, wählt Romain.


Klient erstellen
================

- :menuselection:`Kontakte --> Klienten`

- Dubletten vermeiden: vorher suchen, ob der Klient nicht schon existiert.

- Auf |insert| klicken, um das Dialogfenster "Einfügen" zu öffnen.

- Nach Bestätigung des Dialogfensters erstellt Lino den Datensatz und zeigt den
  neuen  Klient im Detail an.

- Das Layout des Detail-Fensters (welche Reiter, und welche Elemente wo
  angezeigt werden) ist ein Vorschlag, der leicht anpassbar ist und bei dem der
  Kunde mitreden sollte (was am einfachsten direkt auf den Produktionsdaten
  geht).

Auftragsarten konfigurieren
===========================

- Wir haben eine Liste der Journale (Auftragsarten) und eine Liste der Teams.

  Siehe :menuselection:`Konfigurierung --> Buchhaltung --> Journale`
  und :menuselection:`Konfigurierung --> Kalender --> Teams`

  Ein Team kann ggf. für mehrere Auftragsjournale zuständig sein.

- Pro Team haben wir eine Liste der Mitarbeiter, die für Aufträge in Frage kommen.
  Ein Arbeiter kann ggf. in mehreren Teams sein.
  Die Mitglieder eines Teams kann man entweder vom Team aus oder vom Arbeiter aus verwalten.


Auftrag erfassen
================

- `Klient erstellen`_

- Auftrag erstellen:

  - vom Klienten aus:

     - Reiter "Fakturierung", Panel "Aufträge"
     - Doppelklick auf der letzten leeren Zeile dieser Tabelle
     - Journal auswählen (Garten, Umzüge, Haushaltshilfe...) und ggf. Erfassungsdatum anpassen
     - :kbd:`Ctrl-S`

  - vom Hauptmenü aus:

     - :menuselection:`Aufträge --> (Auftragsjournal)`
     - In der Toolbar auf |insert| klicken
     - Klient auswählen, Erfassungsdatum, :kbd:`Ctrl-S`

- Weitere `Details eines Auftrags erfassen`_

- ggf. Auftragsbedingungen für den Kunden und Auftragsblatt für die Arbeiter
  ausdrucken

Details eines Auftrags erfassen
===============================

- ggf. Rechnungsempfänger angeben

- ggf. Beschreibung der Arbeiten

- Den oder die Arbeiter/innen erfassen. Die hier erfassten Arbeiter kommen bei
  allen *neu erstellten* Einsätzen in die Anwesenheitsliste, die jedoch pro
  Einsatz auch verändert werden kann.

- Fahrtkosten eintragen in "Kosten pro Einsatz". Hier können außer
  Fahrtkosten auch z.B. Verbrauchsprodukte angegeben werden.

  Die hier angegebenen Kosten werden für jeden stattgefundenen Termin zusätzlich
  zur Arbeitszeit fakturiert. Hier ist bisher nicht geplant, dass man diese
  Mengen pro Einsatz nochmal anpassen kann.


Übersicht Kalenderansichten
===========================

Es gibt zwei "Kalenderansichten" (in denen man pro Tag, Woche oder pro Monat
navigieren kann) und daneben kann man die Termine und Einsätze von vielen
Stellen aus einsehen.

Über :menuselection:`Kalender --> Kalender` kann man eine
Kalenderansicht mit Schwerpunkt "Tagesplanung" öffnen.
Über :menuselection:`Kalender --> Mitarbeiterplaner` kann man eine
Kalenderansicht mit Schwerpunkt "Mitarbeiter" öffnen.

In beiden Ansichten kann man auch Filter setzen: z.B. nur ein bestimmtes Team.

Die Termine eines bestimmten Auftrags kann man im Detail des Auftrags (Reiter
"Kalender") sehen.

Die Termine eines bestimmten Klienten (für alle Aufträge dieses Klienten,
sowie unfakturierte Termine) kann man im Detail des Klienten (Reiter
"Kalendereinträge") sehen.

Die Termine eines bestimmten Arbeiters kann man im Detail des Arbeiters (Reiter
"Anwesenheiten") sehen.

Die Termine eines bestimmten Teams kann man im Detail des Teams
(Panel "Kalendereinträge") sehen.

Daneben gibt es noch weitere Kalenderansichten. Zum Beispiel "Überfällig
Termine" sind Termine, die älter als eine Woche sind und bei denen man noch
nicht bestätigt hat, ob sie stattgefunden haben oder nicht. Manche dieser
Ansichten können vielleicht raus, und manche fehlen vielleicht noch.

Der Zustand eines Auftrags
==========================

Ein Auftrag ist immer in einem der folgenden **Zustände**:

  Wartet / Aktiv / Dringend / Erledigt / Storniert

Im Dashboard können die Aufträge entsprechend ihres Zustands aufgelistet werden.

NB Diese Zustände habe ich dem Lastenheft entnommen. Kann sein, dass noch
Zustände hinzu kommen oder welche wegfallen.


Ersatzsuche
===========

Ersatzsuche versteht sich pro Anwesenheit und ist unabhängig vom Zustand des
Auftrags und des Termins.

Fallbeispiel : Ein Arbeiter sagt an, dass er an einem bestimmten Tag fehlen wird
und deshalb bei einem geplanten Einsatz ersetzt werden muss.

- Finde den Termin, um den es geht (über den Arbeiter oder über den Auftrag).

- Im Panel "Anwesenheiten" steht der Arbeiter.

- In der Kolonne "Workflow" gibt es verschiedene Aktionen:
  Wenn du noch nicht weißt, welcher Arbeiter ihn ersetzen wird, dann klicke auf :guilabel:`⚕`.
  Ansonsten klicke auf "Ersatz suchen", wähle den Arbeiter aus und bestätige das Dialogfenster.

- Arbeiter, die auf :guilabel:`⚕` gesetzt wurden, erscheinen automatisch im
  Dashboard unter "Einsätze auf Ersatzsuche" bis auch hier auf "Ersatz suchen"
  geklickt wurde.


Einsatz nachträglich erfassen
=============================

Erfassung eines einfachen einmaligen Einsatzes ausgehend von der händisch
ausgefüllten Rechnung:

- Auf den Auftrag gehen

- Termin erfassen:

  - einzelne Termine mit |insert| im Panel "Termine" im Reiter "Kalender"

  - Siehe auch `Auftrag mit regelmäßigen Terminen`_

  - Beachte, dass der oder die im Auftrag erfassten Arbeiter automatisch in den
    **Anwesenheiten** des Termins stehen.

  - Beachte das Feld **Workflow** : jeder Termin steht zunächst im Status "Vorschlag" bzw.
    "Geplant", und man muss auf :guilabel:`☑` klicken, damit er in den Zustand
    "Stattgefunden" wechselt. Ansonsten erstellt Lino keine Rechnung.

- :kbd:`Escape` um auf den Auftrag zurück zu springen.

- Auf |basket| klicken um einen **Fakturierungsplan** für diesen Auftrag zu
  starten. Ein Fakturierungsplan ist, wenn ein Benutzer plant, eine Serie
  on Rechnungen erstellen zu lassen.

  Lino zeigt nun genau einen Vorschlag an, weil es nur einen Termin gibt.

- Vergleiche den von Lino vorgeschlagenen Betrag der Rechnung mit der händisch
  erstellten Rechnung.  Falls ein Unterschied ist: entweder :kbd:`Escape` und den
  Auftrag überprüfen oder Rechnung trotzdem erstellen lassen und dann manuell
  bearbeiten.

- Im Fakturierungsplan auf |money| klicken, um die vorgeschlagenen
  Rechnungen zu generieren.

- Wenn eine Rechnung generiert wurde, steht im betreffenden Vorschlag nicht
  mehr ein |money|, sondern die anklickbare Nummer der erstellten Rechnung.  Auf
  diese Nummer kann man klicken, um die Rechnung im Detail anzuzeigen.

Rechnung manuell bearbeiten
===========================

Man kann eine erstellte Rechnung jederzeit manuell bearbeiten:

- Die Rechnung im Detail anzeigen (z.B. über den Fakturierungsplan, oder über
  :menuselection:`Verkauf --> (Journal)` und dann Doppelklick auf der
  gewünschten Rechnung).

- Im Feld :guilabel:`Workflow` auf "Entwurf" klicken falls die Rechnung auf
  "Registriert" steht.

- Inhalt bearbeiten

- Im Feld :guilabel:`Workflow` auf "Registriert" klicken, um sie wieder zu
  registrieren.

Auftrag mit regelmäßigen Terminen
=================================

Lino kann Terminvorschläge automatisch generieren. Dabei wird pro Klient ein
Auftrag erstellt, in dem die Wiederholungsregeln festgehalten werden (gewünschte
Wochentage und Uhrzeiten, Wiederholungsrate, Anzahl Einsätze und/oder Enddatum,
...).  Lino generiert daraufhin Terminvorschläge. Jeder einzelne Termin kann
manuell verändert werden.  Die Terminvorschläge müssen in Lino bestätigt werden,
wenn sie stattgefunden haben.

- Gehe auf den Auftrag und aktiviere den Reiter "Kalender"

- Fülle die Felder aus, die die Kriterien definieren zum Erstellen der Terminserie:

  - "Beginnt am", "Beginnt um" und "Endet um" : wann der erste Einsatz stattfinden soll
  - "Enddatum" sollte immer frei sein ausser bei Terminen, die mehrere Tage dauern
  - "Wiederholung" und "... alle"

  - "Anzahl Termine" und "Termine generieren bis" : normalerweise wird nur
    eines dieser beiden Felder ausgefüllt.  Lino hört auf, wenn die erste der
    beiden Grenzen erreicht ist. Falls beide Felder leer sind, wird ein
    konfigurierbarer Höchstwert angenommen
    (:menuselection:`Konfigurierung --> System --> Site-Parameter`).

  - Wenn **kein** Wochentag angekreuzt ist, gilt der Wochentag nicht als Kriterium

- Klicke auf |lightning| und beobachte das Panel Kalendereinträge

Den Button |lightning| kannst du so oft betätigen wie du willst (und nach jeder
Änderung in den Kriterien musst du dies selber tun). Lino verändert nur
Terminvorschläge, die noch nicht manuell bearbeitet wurden.

Der Button :guilabel:`☷` dient dazu, die Anwesenheitslisten der erstellten
Terminvorschläge zu aktualisieren. Also wenn du
einen Arbeiter im Auftrag auswechselst, nachdem du schon auf |lightning|
geklickt hattest, möchtest du wahrscheinlich auch auf :guilabel:`☷` klicken.
Auch hier werden natürlich nur Termine aktualisiert, die noch nicht
stattgefunden haben


Rechnungen an die ÖSHZ
======================

Rechnungen an die ÖSHZ werden auf Basis der erfassten Termine erstellt,
unabhängig der tatsächlich an den Kunden fakturierten Dienstleistungen.
Nullrechnungen sind also nicht nötig. Wohl aber ist ein Auftrag nötig, denn
sonst hat Lino ja keine Ahnung, wer der Klient ist.

Der Rechnungsinhalt könnte automatisch von Lino generiert werden.

Momentan gilt die pragmatischse Vorgehensweise, dass man pro Gemeinde pro
Quartal folgendes macht:

- In das Journal gehen (z.B. :menuselection:`Buchhaltung -->
  Gemeinderechnungen`)

- |insert| um eine neue Rechnung zu erstellen. Als Partner die
  Gemeindeverwaltung (das ÖSHZ) auswählen.

- Papierart muss sein "Dienstleistungsbericht" (das kann man schon in den
  Stammdaten der Gemeinde eintragen).

- **Fakturierbare von / bis** aufüllen

- Leere Rechnung ausdrucken (auf den Button `printer` klicken).

  Der Dienstleistungsbericht zeigt automatisch alle Klienten, die im gleichen
  Ort wie die Verwaltung oder einem untergeordneten Ort wohnen. Siehe
  :menuselection:`Konfigurierung --> Orte --> Orte`, Kolonne "Teil von".

- Eventuell die tatsächlich fakturierten Zahlen manuell eingeben.

Beispiele
=========

Hier einige Tests auf den Demo-Daten.

>>> from lino import startup
>>> startup('lino_presto.projects.presto1.settings.doctests')
>>> from lino.api.doctest import *

Liste der Teams:

>>> show_menu_path(cal.AllRooms)
Konfigurierung --> Kalender --> Teams

>>> rt.show(cal.AllRooms, column_names="name event_type")
================ ================== ================== =====================
 Bezeichnung      Bezeichnung (fr)   Bezeichnung (en)   Kalendereintragsart
---------------- ------------------ ------------------ ---------------------
 Garten           Garten             Garden             Außenarbeiten
 Umzüge           Umzüge             Moves              Außenarbeiten
 Renovierung      Renovierung        Renovation         Innenarbeiten
 Haushaltshilfe   Haushaltshilfe     Home help          Innenarbeiten
 Heimpflege       Heimpflege         Home care          Innenarbeiten
 Büro             Bureau             Office             Büroarbeiten
================ ================== ================== =====================
<BLANKLINE>

>>> rt.show(accounting.Journals, column_names="ref name room voucher_type")
================ ====================== ====================== ================== ================ ============================================
 Referenz         Bezeichnung            Bezeichnung (fr)       Bezeichnung (en)   Team             Belegart
---------------- ---------------------- ---------------------- ------------------ ---------------- --------------------------------------------
 SLS              Verkaufsrechnungen     Factures vente         Sales invoices                      Verkaufsrechnung (sales.InvoicesByJournal)
 MAN              Händische Rechnungen   Händische Rechnungen   Manual invoices                     Verkaufsrechnung (sales.InvoicesByJournal)
 Garten           Garten                                                           Garten           Auftrag (orders.OrdersByJournal)
 Umzüge           Umzüge                                                           Umzüge           Auftrag (orders.OrdersByJournal)
 Renovierung      Renovierung                                                      Renovierung      Auftrag (orders.OrdersByJournal)
 Haushaltshilfe   Haushaltshilfe                                                   Haushaltshilfe   Auftrag (orders.OrdersByJournal)
 Heimpflege       Heimpflege                                                       Heimpflege       Auftrag (orders.OrdersByJournal)
 Büro             Büro                                                             Büro             Auftrag (orders.OrdersByJournal)
================ ====================== ====================== ================== ================ ============================================
<BLANKLINE>

>>> rt.show(orders.OrderStates)
====== ============ =========== ============
 Wert   name         Text        Editierbar
------ ------------ ----------- ------------
 10     draft        Wartet      Ja
 20     active       Aktiv       Ja
 30     urgent       Dringend    Ja
 40     registered   Erledigt    Nein
 50     cancelled    Storniert   Nein
====== ============ =========== ============
<BLANKLINE>


Screencasts
===========
