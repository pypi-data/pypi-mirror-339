.. doctest dedocs/basics/concepts.rst
.. include:: /../docs/shared/include/defs.rst
.. _presto.de.concepts:

============================
Wortschatz und Grundbegriffe
============================

.. contents::
  :local:

Hauptbildschirm
===============

Im Hauptbildschirm haben wir das **Hauptmenü**, die sogenannten
**Schnellverbindungen**, eventuelle **Willkommensnachrichten** und dann das
**Dashboard**, d.h. eine Serie von Tabellen mit diversen Daten. Das Dashboard
ist konfigurierbar pro Benutzer.

.. Die Menüs "Buchhaltung" und "Berichte" kommen wahrscheinlich noch raus, weil
   Presto voraussichtlich nur VKR generiert und diese dann in einer externe
   Buchhaltung verarbeitet werden.  Es wäre kein technischer Aufwand, die
   Buchhaltung mal kurz auszuprobieren (dazu müsste ich lediglich noch
   :mod:`lino_xl.lib.finan` und :mod:`lino_xl.lib.bevats`  aktivieren)

Kontakte
========

Als **Partner** bezeichnen wir allgemein jede Einzelperson oder Gruppe, die als
Geschäftspartner, Rechnungsempfänger, Klient, Arbeiter oder sonstiger Kontakt
fungieren kann. Jeder Partner kann unterschiedliche Rollen oder gar parallele
Rollen je nach Auftragstyp oder Finalität einer Dienstleistung haben.

Die Datenbankstruktur unterscheidet fünf Partnerarten: **Personen**,
**Klienten**, **Arbeiter**, **Haushalte** und **Organisationen**. Klienten und
Arbeiter sind eigentlch eine Unterart von Personen. Ein Klient oder Arbeiter
ist immer auch eine Person.  Eine gleiche physische Person kann theoretisch
zugleich Kontaktperson einer Firma, Arbeiter und auch Klient sein.
Der Unterschied zwischen Person, Arbeiter und Klient ist also lediglich
**Ansichtssache** und man kann von einer Ansicht zur anderen wechseln ("Ansicht
als Person, Arbeiter [❌], Klient [❌]").

Jede Person kann **Kontaktperson** für eine oder mehrere Organisationen sein
und kann dort jeweils eine **Funktion** ausüben.

Pro Partner können mehrere **Adressen** hinterlegt werden. Eine davon sollte
als **primär** markiert sein (nur diese Adresse wird tatsächlich benutzt).
Mögliche Adressenarten können definiert werden (z.B. "Referenzadresse" oder
"Wohnsitz"). Auf "Adressen verwalten" klicken, um diese Adressen zu bearbeiten.

Idem für **Kontaktangaben** (Telefon, GSM und E-Mail).

Die **Einkommenskategorie** eines Klienten bestimmt den Tarif, der für Arbeiten
fakturiert wird.  Siehe Fakturierung_.

Haushaltszusammensetzung und familiäre Beziehungen
==================================================

Damit die Suche und die familiäre Einschätzung einfacher ersichtlich wird,
können für jeden Klienten auch deren Haushaltszusammensetzungen und familiäre
Beziehungen erfasst werden.

Ein **Haushalt** ist eine informale Gruppe von Personen, die zusammen wohnen.
Eine Person kann im Laufe der Zeit mehreren Haushalten als **Mitglied** angehören.
Ein Haushalt sollte als **primär** markiert sein.  Die
**Haushaltszusammensetzung** zeigt alle Mitglieder des primären Haushalts.

**Familiäre Beziehungen** sind Beziehungen von Person zu Person, die unabhängig
von der Wohnung existieren.

- Beispiel : :menuselection:`Kontakte --> Personen` und nach *Hubert Frisch*
  suchen.  Dennis Frisch Beziehungen anschauen und Mitgliedschaften korrigieren:
  Dennis ist *Pflegekind* (nicht Kind) in zwei Haushalten.

Kalenderverwaltung
==================

Ein **Kalendereintrag** ist, wenn zu einem bestimmten Zeipunkt (Datum und
Uhrzeit Beginn und Ende) etwas stattfindet, das in unserem Kalender erwähnt
werden soll.

Ein **Termin** ist ein Kalendereintrag, den ein bestimmter
Mitarbeiter mit einem bestimmten Klienten verabredet hat. Zum Beispiel sind
Urlaubstage oder Feiertage zwar Kalendereinträge, aber keine Termine.

Ein **Einsatz** ist ein Termin im Rahmen eines Auftrags (siehe Einsätze_).
Man kann in Lino auch Termine verwalten, die keine Einsätze sind, also nicht mit
einem Auftrag verknüpft sind (z.B. interne Besprechungen, Urlaubstage, sonstige
Termine der Mitarbeiter, ...).

Der **Autor** eines Kalendereintrags ist der administrative Mitarbeiter, der den
Kalendereintrag erstellt hat (manuell oder automatisch). Generell kann man für
jeden Kalendereintrag **Anwesenheiten** erfassen (Gruppenkalender, Versammlungen
oder Veranstaltungen planen...).


Aufträge
========

Ein **Auftrag** ist, wenn man eine Serie von *Einsätzen* plant, bei denen eine
Serie von *Arbeitern* eine bestimmte Aufgabe für einen bestimmten *Klienten*
verrichtet. Die Serie von Arbeitern beschränkt sich oft auf einen einzigen
Arbeiter. Die Serie von Einsätzen kann sich auf einen einzigen Einsatz
beschränken.

Ein Auftrag muss immer einem *Klienten* zugewiesen sein und kann optional einen
anderen *Partner* als Rechnungsempfänger haben.

Jeder einzelne Einsatz hat eine Liste der anwesenden Arbeiter, die prinzipiell
immer die Gleiche (im Auftrag konfigurierte) ist, die sich unter Umständen
jedoch von Mal zu Mal ändern kann.  Siehe auch "Ersatzsuche".

Im Auftrag können neben den vorgesehenen Arbeitern auch Fahrtkosten
und sonstige planbare Nebenkosten erfasst werden, die pro Einsatz fakturiert
werden.

Aufträge sind in **Journale** gruppiert. Ein Journal ist eine Serie von
chronologisch geordneten und durchlaufend nummerierten Dokumenten.

Um die verschiedenen **Tätigkeitsbereiche** des Betriebs zu differenzieren, kann
der Systemverwalter **Teams** konfigurieren.  Menü
:menuselection:`Konfigurierung --> Kalender --> Teams`.

Pro Journal kann man definieren, welches Team für die Aufträge in diesem Journal
zuständig ist. Ein Team kann für mehrere Journale zugleich zuständig sein.   Was
man nicht sagen kann: "für dieses Journal ist mal dieses und mal jenes Team
zuständig".


Einsätze
========

Ein **Einsatz** ist ein Termin im Rahmen eines Auftrags, d.h. ein
Kalendereintrag, der mit einem Auftrag verknüpft ist.

Bei einem Einsatz ist normalerweise ein Arbeiter **anwesend**.
Gegebenenfalls auch mehrere Arbeiter (z.B. Umzüge, Haushaltshilfe).
Gegebenenfalls auch niemand (z.B. in einem stornierten Einsatz).

Die bei einem Einsatz anwesenden Arbeiter stehen im Panel "Anwesenheiten" und
werden dort automatisch auf Basis des Auftrags eingetragen.

Der Einsatz gilt als Grundlage für die Fakturierung. Ohne Einsatz keine
Rechnung. Ob ein Einsatz bereits fakturiert ist, kann man im Detail dieses
Einsatzes (Reiter "Mehr") sehen. Dort stehen sowohl Dienstleistungen als auch
Nebenkosten,

Aufgaben
========

Eine Aufgabe ist eine Notiz über etwas, das erledigt werden muss. Und zwar
normalerweise von einer bestimmten Person für ein bestimmtes Datum.   Eventuell
auch einem bestimmten Auftrag zugeordnet


Fakturierung
============

Für **punktuelle Arbeiten** füllt der Arbeiter oder die Mannschaft nach jedem
Einsatz eine handgeschriebene Rechnung aus und gibt sie dem Kunden. Die
Durchschläge der Rechnungen (= Arbeitsberichte) werden im Büro gesammelt. Jeder
Einsatz wird ausgehend von dieser Rechnung erfasst. Diese Einsätze brauchen
nicht in Lino geplant zu werden. Dies betrifft die meisten Arbeitsbereiche
(Garten, Umzug, ....)

In der Praxis können auch die bisher punktuellen Einsätze schon in Lino geplant
werden.  In diesem Fall muss nach dem Einsatz allerdings die Rechnung vom
Auftrag aus erstellt werden.

Für **regelmäßige Dienstleistungen**
wird die Terminplanung in Lino gemacht.
Hier muss vorher jeder einzelne Einsatz bestätigt werden.
Dies betrifft momentan die Arbeiten im Bereich
*Haushaltshilfe*.

Lino Presto bietet ein angepasstes System, um die Preise der Fakturierung zu
ermitteln. Dabei wird die **Einkommenskategorie** des Klienten und die **Art der
Arbeit** berücksichtigt. Siehe :menuselection:`Konfigurierung --> Produkte -->
Preisregeln` und :menuselection:`Konfigurierung --> Produkte -->
Dienstleistungen`.

Jedes Team unterliegt einem **Fakturationsbereich**.
Diese können konfiguriert werden unter
:menuselection:`Konfigurierung --> Verkauf --> Fakturationsbereiche`.


Dokumente drucken
=================

Auf den Button |print|  `printer` klicken.  Lino öffnet dann das druckbare PDF-Dokument
in einem neuen Browserfenster. Beim ersten Mal muss der Browser gesagt
bekommen, dass Lino neue Popup-Fenster öffnen darf.

Inhalt und Layout der gedruckten Dokumente sind noch zu besprechen.

Grund der Anfrage
=================

Pro Klient kann ein **Grund der Anfrage** (oder mehrere) angegeben werden im
Panel **Interessen** (im Reiter "Klient").  Die **Themen**, für die sich ein
Klient interessieren kann, sind konfigurierbar unter
:menuselection:`Konfigurierung --> Themen --> Themen`. Falls nötig können diese
Bezeichnungen und/oder ihre Einordnung geändert werden.

Bin nicht sicher, wozu diese Information gebraucht wird.

Dienstleistungen ohne Auftrag
=============================

Zum Beispiel reine Lagerbesichtungen sind Dienstleistungen, die nicht an den
Kunden fakturiert werden, wohl aber ans ÖSHZ.

Hierfür muss ein Auftrag erstellt und der *Termin* als *Einsatz* erfasst werden,
damit Lino "weiß", dass die Zeit ans ÖSHZ fakturiert werden soll.

Ist noch nicht definitiv.
