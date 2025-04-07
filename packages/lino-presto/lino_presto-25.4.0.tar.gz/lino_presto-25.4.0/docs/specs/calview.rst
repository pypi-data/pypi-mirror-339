.. doctest docs/specs/calview.rst
.. include:: /../docs/shared/include/defs.rst

.. _presto.specs.calview:

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


>>> url = "/api/contacts/WeeklySlave?dm=grid&fmt=json&limit=99999&mk=0&rp=weak-key-8&start=0&ul=en&wt=t"
>>> test_client.force_login(rt.login('robin').user)
>>> res = test_client.get(url, REMOTE_USER='robin')
>>> print(res.status_code)
200
>>> result = json.loads(res.content.decode('utf-8'))
>>> print(result['param_values'])
{'event_type': None, 'event_typeHidden': None, 'navigation_panel': None, 'project': None, 'projectHidden': None, 'project__municipality': None, 'project__municipalityHidden': None, 'room': None, 'roomHidden': None, 'state': None, 'stateHidden': None}

>>> today = rt.models.calview.Day(0)
>>> today
<Day(0=2017-03-12)>
>>> str(today)
'Sunday, 12 March 2017'

>>> rt.show(contacts.WeeklySlave, today, max_width=20)
+---------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
| Worker              | Monday               | Tuesday              | Wednesday            | Thursday             | Friday               | Saturday             | Sunday               |
+=====================+======================+======================+======================+======================+======================+======================+======================+
| `All workers <…>`__ | **6**                | **7**                | **8**                | **9**                | **10**               | **11**               | ****12****           |
+---------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
| Mr Ahmed **⎙**      |                      | ` 08:00 EMONTS       | ` 13:00 FAYMONVILLE  | ` 08:00 RADERMACHER  | ` 08:00 JANSEN       |                      | ` 08:00 MEIER Marie- |
|                     |                      | Daniel (127) Eupen   | Luc (129) Eupen Home | Daniela (155) Raeren | Jérémy (135) Eupen   |                      | Louise (148) Eupen   |
|                     |                      | Renovation 14/2017   | care 15/2017         | Einsatz 2            | Deployment 1         |                      | Einsatz 1            |
|                     |                      | <…>`__Craftsmen :    | <…>`__Home care :    | <…>`__` 13:00        | <…>`__Office work :  |                      | <…>`__` 13:00        |
|                     |                      | 1:00                 | 3:00                 | RADERMECKER Rik      | 1:00                 |                      | LAMBERTZ Guido (141) |
|                     |                      |                      |                      | (172) Amsterdam      |                      |                      | Eupen Deployment 1   |
|                     |                      |                      |                      | Einsatz 2            |                      |                      | <…>`__Craftsmen :    |
|                     |                      |                      |                      | <…>`__Craftsmen :    |                      |                      | 4:00                 |
|                     |                      |                      |                      | 1:00Home care : 3:00 |                      |                      |                      |
+---------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
| Mrs Beata **⎙**     | ` 09:00 EVERS        | ` 09:00 EVERS        | ` 09:00 EVERS        | ` 09:00 CHARLIER     | ` 09:00 EVERS        | ` 09:00 EVERS        | ` 09:00 EVERS        |
|                     | Eberhart (126) Eupen | Eberhart (126) Eupen | Eberhart (126) Eupen | Ulrike (118) Eupen   | Eberhart (126) Eupen | Eberhart (126) Eupen | Eberhart (126) Eupen |
|                     | Deployment 8         | Deployment 9         | Deployment 10        | Einsatz 3            | Deployment 12        | Deployment 13        | Deployment 14        |
|                     | <…>`__` 09:00 EMONTS | <…>`__` 09:00 EMONTS | <…>`__` 09:00 EMONTS | <…>`__` 09:00 EVERS  | <…>`__` 09:00 EMONTS | <…>`__` 09:00 ARENS  | <…>`__` 09:00 EMONTS |
|                     | Erich (149) Raeren   | Erich (149) Raeren   | Erich (149) Raeren   | Eberhart (126) Eupen | Erich (149) Raeren   | Andreas (112) Eupen  | Erich (149) Raeren   |
|                     | Deployment 1         | Deployment 2         | Deployment 3         | Deployment 11        | Deployment 5         | Einsatz 2            | Deployment 7         |
|                     | <…>`__Home care :    | <…>`__` 14:00        | <…>`__Home care :    | <…>`__` 09:00 EMONTS | <…>`__` 09:00        | <…>`__` 09:00 EMONTS | <…>`__` 14:00 DENON  |
|                     | 1:00                 | GERNEGROSS Germaine  | 1:00                 | Erich (149) Raeren   | JEANÉMART Jérôme     | Erich (149) Raeren   | Denis (179) Paris    |
|                     |                      | (130) Eupen          |                      | Deployment 4         | (180) Paris Garden   | Deployment 6         | Einsatz 2            |
|                     |                      | Deployment 1         |                      | <…>`__Outside work : | 17/2017  <…>`__Home  | <…>`__` 14:00        | <…>`__Home care :    |
|                     |                      | <…>`__Home care :    |                      | 0:30Home care : 1:00 | care : 1:00Outside   | LASCHET Laura (142)  | 1:00Craftsmen : 4:00 |
|                     |                      | 1:00Office work :    |                      |                      | work : 0:30          | Eupen Renovation     |                      |
|                     |                      | 4:00                 |                      |                      |                      | 18/2017  <…>`__Home  |                      |
|                     |                      |                      |                      |                      |                      | care : 1:00Outside   |                      |
|                     |                      |                      |                      |                      |                      | work : 0:30Craftsmen |                      |
|                     |                      |                      |                      |                      |                      | : 4:00               |                      |
+---------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
| Mr Conrad **⎙**     | ` 11:00 EMONTS-GAST  | ` 14:00 GERNEGROSS   |                      | ` 11:00 JOHNEN       |                      | ` 11:00 EVERTZ Bernd | ` 11:00 RADERMACHER  |
|                     | Erna (151) Raeren    | Germaine (130) Eupen |                      | Johann (137) Eupen   |                      | (125) Eupen Einsatz  | Alfons (152) Raeren  |
|                     | Einsatz 1            | Deployment 1         |                      | Deployment 1         |                      | 3  <…>`__` 14:00     | Home care 19/2017    |
|                     | <…>`__Home care :    | <…>`__Office work :  |                      | <…>`__Craftsmen :    |                      | LASCHET Laura (142)  | <…>`__` 14:00 DENON  |
|                     | 2:00                 | 4:00                 |                      | 2:00                 |                      | Eupen Renovation     | Denis (179) Paris    |
|                     |                      |                      |                      |                      |                      | 18/2017  <…>`__Home  | Einsatz 2            |
|                     |                      |                      |                      |                      |                      | care : 2:00Craftsmen | <…>`__Home care :    |
|                     |                      |                      |                      |                      |                      | : 4:00               | 2:00Craftsmen : 4:00 |
+---------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
| Mr Dennis **⎙**     | ` 08:00 MEIER Marie- | ` 08:00 JANSEN       | ` 08:00 MEIER Marie- | ` 08:00 MEIER Marie- | ` 08:00 MEIER Marie- | ` 08:00 MEIER Marie- | ` 08:00 MEIER Marie- |
|                     | Louise (148) Eupen   | Jérémy (135) Eupen   | Louise (148) Eupen   | Louise (148) Eupen   | Louise (148) Eupen   | Louise (148) Eupen   | Louise (148) Eupen   |
|                     | Deployment 5         | Einsatz 2            | Deployment 7         | Deployment 8         | Deployment 9         | Deployment 10        | Deployment 11        |
|                     | <…>`__` 08:00        | <…>`__` 08:00 MEIER  | <…>`__` 08:00        | <…>`__` 13:00 JONAS  | <…>`__` 08:00        | <…>`__` 08:00        | <…>`__` 08:00        |
|                     | DERICUM Daniel (120) | Marie-Louise (148)   | GROTECLAES Gregory   | Josef (138) Eupen    | LAZARUS Line (143)   | LAZARUS Line (143)   | LAZARUS Line (143)   |
|                     | Eupen Deployment 1   | Eupen Deployment 6   | (131) Eupen Einsatz  | Einsatz 1            | Eupen Deployment 1   | Eupen Deployment 2   | Eupen Deployment 3   |
|                     | <…>`__Home care :    | <…>`__` 13:00        | 1  <…>`__Home care : | <…>`__Home care :    | <…>`__Home care :    | <…>`__` 13:00        | <…>`__Home care :    |
|                     | 2:00                 | LAMBERTZ Guido (141) | 1:00Outside work :   | 1:00Craftsmen : 3:00 | 2:00                 | RADERMACHER Berta    | 2:00                 |
|                     |                      | Eupen Einsatz 2      | 1:00                 |                      |                      | (153) Raeren         |                      |
|                     |                      | <…>`__` 13:00        |                      |                      |                      | Deployment 1         |                      |
|                     |                      | EMONTSPOOL Erwin     |                      |                      |                      | <…>`__Home care :    |                      |
|                     |                      | (150) Raeren         |                      |                      |                      | 2:00Office work :    |                      |
|                     |                      | Deployment 1         |                      |                      |                      | 3:00                 |                      |
|                     |                      | <…>`__Outside work : |                      |                      |                      |                      |                      |
|                     |                      | 1:00Home care :      |                      |                      |                      |                      |                      |
|                     |                      | 1:00Craftsmen :      |                      |                      |                      |                      |                      |
|                     |                      | 3:00Office work :    |                      |                      |                      |                      |                      |
|                     |                      | 3:00                 |                      |                      |                      |                      |                      |
+---------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
| Mrs Evelyne **⎙**   | ` 09:00 DOBBELSTEIN  | ` 14:00 DENON Denis  | ` 14:00 DENON Denis  | ` 09:00 MIESSEN      | ` 09:00 LEFFIN       | ` 14:00 DENON Denis  | ` 14:00 DENON Denis  |
|                     | Dorothée (123) Eupen | (179) Paris          | (179) Paris          | Michael (147) Eupen  | Josefine (144) Eupen | (179) Paris          | (179) Paris          |
|                     | Home care 13/2017    | Deployment 12        | Deployment 13        | Einsatz 2            | Einsatz 1            | Deployment 16        | Deployment 17        |
|                     | <…>`__` 14:00 DENON  | <…>`__` 14:00 BRECHT | <…>`__` 14:00 BRECHT | <…>`__` 09:00        | <…>`__` 14:00 DENON  | <…>`__` 14:00 BRECHT | <…>`__` 14:00 BRECHT |
|                     | Denis (179) Paris    | Bernd (176) Aachen   | Bernd (176) Aachen   | HILGERS Henri (133)  | Denis (179) Paris    | Bernd (176) Aachen   | Bernd (176) Aachen   |
|                     | Deployment 11        | Deployment 3         | Deployment 4         | Eupen Deployment 1   | Deployment 15        | Deployment 7         | Deployment 8         |
|                     | <…>`__` 14:00 BRECHT | <…>`__Home care :    | <…>`__` 14:00 ENGELS | <…>`__` 14:00 DENON  | <…>`__` 14:00        | <…>`__Home care :    | <…>`__Home care :    |
|                     | Bernd (176) Aachen   | 8:00                 | Edgar (128) Eupen    | Denis (179) Paris    | RADERMACHER Hans     | 8:00                 | 8:00                 |
|                     | Deployment 2         |                      | Garden 15/2017       | Deployment 14        | (159) Raeren Einsatz |                      |                      |
|                     | <…>`__Home care :    |                      | <…>`__Home care :    | <…>`__` 14:00 BRECHT | 2  <…>`__` 14:00     |                      |                      |
|                     | 8:30                 |                      | 8:00Outside work :   | Bernd (176) Aachen   | BRECHT Bernd (176)   |                      |                      |
|                     |                      |                      | 4:00                 | Deployment 5         | Aachen Deployment 6  |                      |                      |
|                     |                      |                      |                      | <…>`__Home care :    | <…>`__` 14:00        |                      |                      |
|                     |                      |                      |                      | 8:30Craftsmen : 0:30 | JOUSTEN Jan (139)    |                      |                      |
|                     |                      |                      |                      |                      | Eupen Deployment 1   |                      |                      |
|                     |                      |                      |                      |                      | <…>`__Home care :    |                      |                      |
|                     |                      |                      |                      |                      | 12:30Outside work :  |                      |                      |
|                     |                      |                      |                      |                      | 4:00                 |                      |                      |
+---------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
| Mr Fred **⎙**       | ` 11:00 DOBBELSTEIN- | ` 14:00 DENON Denis  | ` 14:00 DENON Denis  | ` 11:00 HILGERS      | ` 14:00 DENON Denis  | ` 11:00 VAN VEEN     | ` 14:00 DENON Denis  |
|                     | DEMEULENAERE         | (179) Paris          | (179) Paris          | Hildegard (132)      | (179) Paris          | Vincent (165) Raeren | (179) Paris          |
|                     | Dorothée (122) Eupen | Deployment 12        | Deployment 13        | Eupen Renovation     | Deployment 15        | Einsatz 2            | Deployment 17        |
|                     | Deployment 1         | <…>`__` 14:00 BRECHT | <…>`__` 14:00 BRECHT | 16/2017              | <…>`__` 14:00        | <…>`__` 11:00        | <…>`__` 14:00 BRECHT |
|                     | <…>`__` 14:00 DENON  | Bernd (176) Aachen   | Bernd (176) Aachen   | <…>`__` 14:00 DENON  | RADERMACHER Hans     | MALMENDIER Marc      | Bernd (176) Aachen   |
|                     | Denis (179) Paris    | Deployment 3         | Deployment 4         | Denis (179) Paris    | (159) Raeren Einsatz | (145) Eupen          | Deployment 8         |
|                     | Deployment 11        | <…>`__Home care :    | <…>`__` 14:00 ENGELS | Deployment 14        | 2  <…>`__` 14:00     | Deployment 1         | <…>`__Home care :    |
|                     | <…>`__` 14:00 BRECHT | 8:00                 | Edgar (128) Eupen    | <…>`__` 14:00 BRECHT | BRECHT Bernd (176)   | <…>`__` 14:00 DENON  | 8:00                 |
|                     | Bernd (176) Aachen   |                      | Garden 15/2017       | Bernd (176) Aachen   | Aachen Deployment 6  | Denis (179) Paris    |                      |
|                     | Deployment 2         |                      | <…>`__Home care :    | Deployment 5         | <…>`__` 14:00        | Deployment 16        |                      |
|                     | <…>`__Office work :  |                      | 8:00Outside work :   | <…>`__Craftsmen :    | JOUSTEN Jan (139)    | <…>`__` 14:00 BRECHT |                      |
|                     | 2:00Home care : 8:00 |                      | 4:00                 | 2:00Home care : 8:00 | Eupen Deployment 1   | Bernd (176) Aachen   |                      |
|                     |                      |                      |                      |                      | <…>`__Home care :    | Deployment 7         |                      |
|                     |                      |                      |                      |                      | 12:00Outside work :  | <…>`__Craftsmen :    |                      |
|                     |                      |                      |                      |                      | 4:00                 | 2:00Office work :    |                      |
|                     |                      |                      |                      |                      |                      | 2:00Home care : 8:00 |                      |
+---------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
| Mr Garry **⎙**      | ` 13:00 JONAS Josef  | ` 13:00 JONAS Josef  | ` 08:00 ERNST Berta  | ` 08:00 DERICUM      | ` 08:00 KAIVERS Karl | ` 13:00 JONAS Josef  | ` 08:00 CHANTRAINE   |
|                     | (138) Eupen          | (138) Eupen          | (124) Eupen          | Daniel (120) Eupen   | (140) Eupen Home     | (138) Eupen          | Marc (119) Eupen     |
|                     | Deployment 7         | Deployment 8         | Deployment 1         | Einsatz 3            | care 17/2017         | Deployment 12        | Einsatz 2            |
|                     | <…>`__Home care :    | <…>`__` 13:00 DUBOIS | <…>`__` 13:00 JONAS  | <…>`__` 13:00 JONAS  | <…>`__` 13:00        | <…>`__` 13:00 INGELS | <…>`__` 13:00 JONAS  |
|                     | 3:00                 | Robin (178) Paris    | Josef (138) Eupen    | Josef (138) Eupen    | EMONTSPOOL Erwin     | Irene (134) Eupen    | Josef (138) Eupen    |
|                     |                      | Einsatz 1            | Deployment 9         | Deployment 10        | (150) Raeren Einsatz | Deployment 3         | Deployment 13        |
|                     |                      | <…>`__Home care :    | <…>`__Craftsmen :    | <…>`__` 13:00 INGELS | 3  <…>`__` 13:00     | <…>`__Home care :    | <…>`__` 13:00 INGELS |
|                     |                      | 3:00Outside work :   | 1:00Home care : 3:00 | Irene (134) Eupen    | JONAS Josef (138)    | 6:00                 | Irene (134) Eupen    |
|                     |                      | 3:00                 |                      | Deployment 1         | Eupen Deployment 11  |                      | Deployment 4         |
|                     |                      |                      |                      | <…>`__Home care :    | <…>`__` 13:00 INGELS |                      | <…>`__` 13:00        |
|                     |                      |                      |                      | 7:00                 | Irene (134) Eupen    |                      | MARTELAER Mark (171) |
|                     |                      |                      |                      |                      | Deployment 2         |                      | Amsterdam Garden     |
|                     |                      |                      |                      |                      | <…>`__Home care :    |                      | 19/2017  <…>`__Home  |
|                     |                      |                      |                      |                      | 7:00Outside work :   |                      | care : 7:00Outside   |
|                     |                      |                      |                      |                      | 3:00                 |                      | work : 3:00          |
+---------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
| Mrs Helen **⎙**     | ` 09:00 CHARLIER     |                      | ` 09:00 EVERS        | ` 14:00 JACOBS       | ` 09:00 KELLER Karl  |                      | ` 14:00 JOUSTEN Jan  |
|                     | Ulrike (118) Eupen   |                      | Eberhart (126) Eupen | Jacqueline (136)     | (177) Aachen         |                      | (139) Eupen Einsatz  |
|                     | Deployment 1         |                      | Einsatz 1            | Eupen Einsatz 1      | Deployment 1         |                      | 3  <…>`__` 14:00     |
|                     | <…>`__Office work :  |                      | <…>`__` 14:00        | <…>`__Home care :    | <…>`__Office work :  |                      | MEESSEN Melissa      |
|                     | 0:30                 |                      | EIERSCHAL Emil (174) | 4:00                 | 0:30                 |                      | (146) Eupen          |
|                     |                      |                      | Aachen Deployment 1  |                      |                      |                      | Deployment 1         |
|                     |                      |                      | <…>`__Craftsmen :    |                      |                      |                      | <…>`__Home care :    |
|                     |                      |                      | 4:30                 |                      |                      |                      | 4:00Craftsmen : 4:00 |
+---------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
| Mrs Maria **⎙**     | ` 11:00 RADERMACHER  | ` 11:00 MALMENDIER   | ` 11:00 RADERMACHER  | ` 11:00 RADERMACHER  | ` 11:00 RADERMACHER  | ` 11:00 RADERMACHER  | ` 11:00 RADERMACHER  |
|                     | Jean (162) Raeren    | Marc (145) Eupen     | Jean (162) Raeren    | Jean (162) Raeren    | Jean (162) Raeren    | Jean (162) Raeren    | Jean (162) Raeren    |
|                     | Deployment 5         | Einsatz 2            | Deployment 7         | Deployment 8         | Deployment 9         | Deployment 10        | Deployment 11        |
|                     | <…>`__` 11:00        | <…>`__` 11:00        | <…>`__` 14:00        | <…>`__` 11:00 EVERTZ | <…>`__Home care :    | <…>`__` 11:00 LAHM   | <…>`__` 14:00        |
|                     | COLLARD Charlotte    | RADERMACHER Jean     | EIERSCHAL Emil (174) | Bernd (125) Eupen    | 2:00                 | Lisa (175) Aachen    | JOUSTEN Jan (139)    |
|                     | (117) Eupen Garden   | (162) Raeren         | Aachen Deployment 1  | Deployment 1         |                      | Einsatz 1            | Eupen Einsatz 3      |
|                     | 13/2017  <…>`__Home  | Deployment 6         | <…>`__Home care :    | <…>`__` 14:00 JACOBS |                      | <…>`__Home care :    | <…>`__` 14:00        |
|                     | care : 2:00Outside   | <…>`__Outside work : | 2:00Craftsmen : 4:00 | Jacqueline (136)     |                      | 2:00Outside work :   | MEESSEN Melissa      |
|                     | work : 2:00          | 2:00Home care : 2:00 |                      | Eupen Einsatz 1      |                      | 2:00                 | (146) Eupen          |
|                     |                      |                      |                      | <…>`__Home care :    |                      |                      | Deployment 1         |
|                     |                      |                      |                      | 8:00                 |                      |                      | <…>`__Home care :    |
|                     |                      |                      |                      |                      |                      |                      | 6:00Craftsmen : 4:00 |
+---------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
<BLANKLINE>
