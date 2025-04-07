.. include:: /../docs/shared/include/defs.rst

============
Fakturierung
============

Zu gegebenen Zeitpunkten wird die Automatikfakturierung gestartet. Eventuell
auch einzelne Klienten oder Zahler separat. Die Rechnungen werden von Lino
ausgedruckt und persönlich ausgehändigt oder per Post verschickt.  In die
Buchhaltung werden sie manuell übertragen.


.. contents::
   :depth: 1
   :local:


Anweisungen
===========

- Zunächst prüfen, ob alle Einsätze korrekt in Lino erfasst sind.

- Wähle :menuselection:`Verkauf --> Rechnungen erstellen` und fülle alle Felder
  wie folgt aus:

    - Autor : wer als Autor der erstellten Rechnungen vermerkt sein wird. NB Dies erscheint nicht auf den Rechnungen selber.

    - Fakturierungsbereich : in welchem Journal die Rechnungen erstellt werden sollen
    - Heute : auf welches Datum die Rechnungen datiert werden sollen
    - Fakturierbare bis : bis zu welchem Datum fakturiert werden soll.
    - Partner : wenn nicht leer, dann nur Rechnungen an diesen Empfänger generieren
    - Auftrag : wenn nicht leer, dann nur Rechnung für diesen Auftrag erstellen.

- Klicke auf den gelben Blitz (|lightning|), um Vorschläge generieren zu lassen.
  Am Bildschirm siehst du nun, welche Rechnungen Lino vorschlägt.

- Dann mit |money| das Generieren der Rechnungen starten.

Tipps und Tricks
================

Lino fakturiert immer alle stattgefundenen Termine eines Auftrags (die noch
nicht fakturiert sind).

Falls ein Termin nicht fakturiert werden soll:

- Den Termin löschen
- Status auf "Abgesagt" (⚕) oder "Verpasst" (☉) setzen

Falls nötig könnten wir einen globalen Parameter definieren "Termine vor diesem
Datum nicht fakturieren"


Manuelle Verkaufsrechnungen
===========================

Abgesehen von den automatisch erstellten Rechnungen kannst Du jederzeit auch
manuell Verkaufsrechnungen erstellen und ausdrucken. Manuelle VKR stehen
üblicherweise in einem eigenen Journal, um sie nicht mit den automatisch
erstellten VKR zu vermischen.

Um eine neue VKR zu erfassen, wähle im Hauptmenü :menuselection:` Buchhaltung
--> Verkauf --> (gewünschtes Journal)` und klicke dann auf |insert| um eine
neue Rechnung einzufügen.

