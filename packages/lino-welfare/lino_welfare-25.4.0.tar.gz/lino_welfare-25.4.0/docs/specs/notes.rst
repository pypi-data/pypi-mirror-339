.. doctest docs/specs/notes.rst
.. _welfare.specs.notes:

=============
Notes
=============

.. contents::
   :local:
   :depth: 2

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *
>>> translation.activate("en")


Permalink to the detail of a note type
======================================

>>> url = '/api/notes/NoteTypes/1?fmt=detail'
>>> test_client.force_login(rt.login('rolf').user)
>>> res = test_client.get(url, REMOTE_USER='rolf')
>>> print(res.status_code)
200

We test whether a normal HTML response arrived:

>> print(res.content)  #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<!DOCTYPE html ...
Lino.notes.NoteTypes.detail.run(null,{ "record_id": "1", "base_params": {  } })
...</body>
</html>


The first meeting
=================

We can use the :meth:`lino_welfare.modlib.pcsw.Client.get_first_meeting`
method for getting the last note about a given client and of given
type.

>>> from django.utils.translation import gettext_lazy as _
>>> flt = dd.str2kw("name", _("First meeting"))
>>> fm = rt.models.notes.NoteType.objects.get(**flt)
>>> ses = rt.login('rolf')
>>> ses.show(notes.NotesByType, fm, column_names="id project")
===== ==========================================
 ID    Klient
----- ------------------------------------------
 26    ERNST Berta (125)
 37    EVERTZ Bernd (126*)
 48    AUSDEMWALD Alfons (116)
 59    BASTIAENSEN Laurent (117)
 70    COLLARD Charlotte (118)
 81    CHANTRAINE Marc (120*)
 92    DERICUM Daniel (121)
 103   DEMEULENAERE Dorothée (122)
 114   DOBBELSTEIN-DEMEULENAERE Dorothée (123*)
 16    JEANÉMART Jérôme (181)
 17    VANDENMEULENBOS Marie-Louise (174)
 14    DUBOIS Robin (179)
 15    LAHM Lisa (176)
 13    DENON Denis (180*)
 12    JEANÉMART Jérôme (181)
 11    KASENNOVA Tatjana (213)
===== ==========================================
<BLANKLINE>


Client 125 has a first meeting, while client 124 doesn't:

>>> rt.models.pcsw.Client.objects.get(pk=125).get_first_meeting()
Note #26 ('Ereignis/Notiz #26')
>>> rt.models.pcsw.Client.objects.get(pk=124).get_first_meeting()

The first meeting is also printed on a :term:`debts mediation budget`.
See :ref:`welfare.specs.debts.first_meeting`.


Change notifications
====================

>>> ses = rt.login('robin')
>>> from lino.core.diff import ChangeWatcher
>>> obj = notes.Note.objects.get(id=26)
>>> print(obj.get_change_body(ses, None))  #doctest: +NORMALIZE_WHITESPACE
<div><p>Robin Rood hat <a href="…">Ereignis/Notiz #26</a> erstellt<p>Betreff:
Get acquaintaned<br>Klient: [client 125]</p></p>.</div>

>>> cw = ChangeWatcher(obj)
>>> obj.subject = "foo"
>>> obj.date = i2d(20240228)
>>> print(obj.get_change_body(ses, cw))  #doctest: +NORMALIZE_WHITESPACE
<div><p>Robin Rood hat <a href="…">Ereignis/Notiz #26</a> bearbeitet:</p><ul><li><b>Datum</b> : 2013-04-25 --&gt; 2024-02-28</li><li><b>Betreff</b> : Get acquaintaned --&gt; foo</li></ul><p>Betreff: foo<br>Klient: [client 125]</p></div>
