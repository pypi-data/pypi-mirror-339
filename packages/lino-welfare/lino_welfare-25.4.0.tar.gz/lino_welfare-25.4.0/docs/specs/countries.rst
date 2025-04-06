.. doctest docs/specs/countries.rst
.. _welfare.specs.countries:

===============================================
The :mod:`lino_xl.lib.statbel.countries` plugin
===============================================

.. contents::
   :local:
   :depth: 1


.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *
>>> from django.db.models import Q

>>> dd.plugins.countries
<lino_xl.lib.statbel.countries.Plugin lino_xl.lib.statbel.countries(needs ['lino.modlib.office', 'lino_xl.lib.xl'])>

>>> dd.plugins.countries.extends_models
['Country', 'Place']

Refugee statuses and former country
===================================

The demo database comes with 224 known countries, but some of them are not real
countries because they actually represent for example a *refugee status* or a
*former country*.

Lino knows them because their :attr:`actual_country
<lino.modlib.statbel.countries.models.Country.actual_country>` field
points to another (the "real") country.

>>> countries.Country.objects.all().count()
224
>>> countries.Country.objects.filter(actual_country__isnull=True).count()
220
>>> countries.Country.objects.filter(actual_country__isnull=False).count()
4

>>> rt.show(countries.Countries,
...     filter=Q(actual_country__isnull=False),
...     column_names="isocode name inscode actual_country actual_country__isocode")
========== ============================================ ========== ================ ==========
 ISO-Code   Bezeichnung                                  INS code   Actual country   ISO-Code
---------- -------------------------------------------- ---------- ---------------- ----------
 BYAA       Byelorussian SSR Soviet Socialist Republic              Belarus          BY
 DDDE       German Democratic Republic                   170        Deutschland      DE
 DEDE       German Federal Republic                      103        Deutschland      DE
 SUHH       USSR, Union of Soviet Socialist Republics               Russland         RU
========== ============================================ ========== ================ ==========
<BLANKLINE>


The following database fields refer to a country:

>>> for m, f in rt.models.countries.Country._lino_ddh.fklist:
...     print ("{} {}".format(dd.full_model_name(m), f.name))
addresses.Address country
contacts.Partner country
countries.Country actual_country
countries.Place country
cv.Experience country
cv.Study country
cv.Training country
pcsw.Client birth_country
pcsw.Client nationality


>>> kw = dict()
>>> fields = 'count rows'
>>> demo_get(
...    'rolf', 'choices/addresses/Address/country', fields, 220, **kw)
>>> demo_get(
...    'rolf', 'choices/contacts/Partners/country', fields, 220, **kw)
>>> demo_get(
...    'rolf', 'choices/pcsw/Clients/country', fields, 220, **kw)
>>> demo_get(
...    'rolf', 'choices/countries/Countries/actual_country', fields, 220, **kw)

>>> demo_get(
...    'rolf', 'choices/cv/Training/country', fields, 220, **kw)

The following fields have the full list, including fake countries)

>>> demo_get(
...    'rolf', 'choices/pcsw/Clients/nationality', fields, 224, **kw)

>>> demo_get(
...    'rolf', 'choices/countries/Places/country', fields, 224, **kw)
