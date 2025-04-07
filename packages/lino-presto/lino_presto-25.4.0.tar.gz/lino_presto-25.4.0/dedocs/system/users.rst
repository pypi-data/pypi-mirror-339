.. doctest dedocs/system/users.rst
.. include:: /../docs/shared/include/defs.rst

==================
Benutzerverwaltung
==================

Um die Liste der Benutzer und ihrer Zugriffsrechte zu sehen und zu verwalten,
wähle im Menü :menuselection:`Konfigurierung --> System --> Benutzer`.

Um einen **neuen Benutzer** anzulegen, klicke in der Werkzeugleiste auf |insert|.

Der **Benutzername** ist der Name, mit dem der Benutzer sich anmeldet. Lino
stellt keine besonderen Bedingungen an den Benutzernamen.  Üblich sind
kleinbuchstaben und ein Punkt zum Trennen von Vor- und Nachname.  Für einen
Benutzer Max Mustermann zum Beispiel wären Benutzernamen denkbar:
``max.mustermann``, ``m.mustermann``, ``mm``, ``max``.

Man kann den Benutzernamen eines bestehenden Benutzers ändern. Falls der
Benutzer gerade in Lino arbeitet, würde er wohl Fehlermeldungen kriegen und
sich neu anmelden müssen.

Man kann den Benutzernamen eines bestehenden Benutzers auf leer setzen und dann
kann dieser Benutzer sich nicht mehr anmelden.

Die **Benutzerart** entscheidet über die Zugriffsrechte des
Benutzers.  Wenn das Feld leer ist kann der Benutzer sich nicht
anmelden.  Es gibt folgende Benutzerarten:

- Sekretariat
- Verwalter (kann neue Benutzer anlegen, Zugriffsrechte und Passwörter ändern)
- Arbeiter (kann seine Dienstleistungen erfassen)



Das **ID** ist die interne Benutzernummer und das, was einen Benutzer
identifiziert.

Einen **Benutzer löschen** kann man nur, wenn es keine Datenobjekte in der
Datenbank gibt, die auf diese Benutzernummer verweisen.
  
Alle anderen Felder können die Benutzer auch selber ändern.
Siehe :doc:`/basics/settings`.

Der Systemverwalter kann bei jedem Benutzer auf den Button mit dem Asterisk (✱)
klicken und dessen Passwort ändern.


