.. doctest docs/specs/excerpts.rst
.. _welfare.specs.excerpts:

==========================================
Usage of database excerpts in Lino Welfare
==========================================

.. doctest init:

    >>> import lino
    >>> lino.startup('lino_welfare.projects.gerd.settings.doctests')
    >>> from lino.api.doctest import *


.. contents::
   :local:
   :depth: 2


Configuring excerpts
====================

See also :ref:`lino.admin.printing`.

Here is a more complete list of excerpt types:

>>> rt.show(excerpts.ExcerptTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
============================================================= ======== =============== =========================== ===================== ============================= ================================
 Modell                                                        Primär   Bescheinigend   Bezeichnung                 Druckmethode          Vorlage                       Textkörper-Vorlage
------------------------------------------------------------- -------- --------------- --------------------------- --------------------- ----------------------------- --------------------------------
 `aids.IncomeConfirmation (Einkommensbescheinigung) <…>`__     Ja       Ja              Einkommensbescheinigung                           Default.odt                   certificate.body.html
 `aids.RefundConfirmation (Kostenübernahmeschein) <…>`__       Ja       Ja              Kostenübernahmeschein                             Default.odt                   certificate.body.html
 `aids.SimpleConfirmation (Einfache Bescheinigung) <…>`__      Ja       Ja              Einfache Bescheinigung                            Default.odt                   certificate.body.html
 `art61.Contract (Art.61-Konvention) <…>`__                    Ja       Ja              Art.61-Konvention                                                               contract.body.html
 `cal.Guest (Anwesenheit) <…>`__                               Ja       Nein            Anwesenheitsbescheinigung                         Default.odt                   presence_certificate.body.html
 `cbss.IdentifyPersonRequest (IdentifyPerson-Anfrage) <…>`__   Ja       Ja              IdentifyPerson-Anfrage
 `cbss.ManageAccessRequest (ManageAccess-Anfrage) <…>`__       Ja       Ja              ManageAccess-Anfrage
 `cbss.RetrieveTIGroupsRequest (Tx25-Anfrage) <…>`__           Ja       Ja              Tx25-Anfrage
 `contacts.Partner (Partner) <…>`__                            Nein     Nein            Zahlungserinnerung          WeasyPdfBuildMethod   payment_reminder.weasy.html
 `contacts.Person (Person) <…>`__                              Nein     Nein            Nutzungsbestimmungen        AppyPdfBuildMethod    TermsConditions.odt
 `debts.Budget (Budget) <…>`__                                 Ja       Ja              Finanzielle Situation
 `esf.ClientSummary (ESF Summary) <…>`__                       Ja       Ja              Training report             WeasyPdfBuildMethod
 `finan.BankStatement (Kontoauszug) <…>`__                     Ja       Ja              Kontoauszug
 `finan.JournalEntry (Diverse Buchung) <…>`__                  Ja       Ja              Diverse Buchung
 `finan.PaymentOrder (Zahlungsauftrag) <…>`__                  Ja       Ja              Zahlungsauftrag
 `isip.Contract (VSE) <…>`__                                   Ja       Ja              VSE
 `jobs.Contract (Art.60§7-Konvention) <…>`__                   Ja       Ja              Art.60§7-Konvention
 `pcsw.Client (Klient) <…>`__                                  Ja       Nein            Aktenblatt                                        file_sheet.odt
 `pcsw.Client (Klient) <…>`__                                  Nein     Nein            Aktionsplan                                       Default.odt                   pac.body.html
 `pcsw.Client (Klient) <…>`__                                  Nein     Nein            Curriculum vitae            AppyRtfBuildMethod    cv.odt
 `pcsw.Client (Klient) <…>`__                                  Nein     Nein            eID-Inhalt                                        eid-content.odt
============================================================= ======== =============== =========================== ===================== ============================= ================================
<BLANKLINE>


Demo excerpts
=============

Here is a list of all demo excerpts.

>>> rt.show(excerpts.AllExcerpts, language="en", column_names="id excerpt_type owner project company language")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ======================== =========================================================== ============================= ================================ ==========
 ID   Excerpt Type             Controlled by                                               Client                        Recipient (Organization)         Language
---- ------------------------ ----------------------------------------------------------- ----------------------------- -------------------------------- ----------
 77   Action plan              `AUSDEMWALD Alfons (116) <…>`__                             AUSDEMWALD Alfons (116)                                        de
 76   eID sheet                `AUSDEMWALD Alfons (116) <…>`__                             AUSDEMWALD Alfons (116)                                        de
 75   File sheet               `AUSDEMWALD Alfons (116) <…>`__                             AUSDEMWALD Alfons (116)                                        de
 74   Curriculum vitae         `AUSDEMWALD Alfons (116) <…>`__                             AUSDEMWALD Alfons (116)                                        de
 73   Presence certificate     `Presence #1 (22.05.2014) <…>`__                            AUSDEMWALD Alfons (116)                                        de
 72   Payment reminder         `Belgisches Rotes Kreuz <…>`__                                                                                             de
 71   Art60§7 job supplyment   `Art60§7 job supplyment#16 (Denis DENON) <…>`__             DENON Denis (180*)            R-Cycle Sperrgutsortierzentrum   de
 70   Art60§7 job supplyment   `Art60§7 job supplyment#15 (Denis DENON) <…>`__             DENON Denis (180*)            BISA                             de
 ...
 14   Art61 job supplyment     `Art61 job supplyment#2 (Josef JONAS) <…>`__                JONAS Josef (139)                                              de
 13   Art61 job supplyment     `Art61 job supplyment#1 (Daniel EMONTS) <…>`__              EMONTS Daniel (128)                                            de
 12   Terms & conditions       `Mr Albert ADAM <…>`__                                                                                                     de
 11   Simple confirmation      `Clothes bank/22/05/2014/240/19 <…>`__                      FRISCH Paul (240)             Belgisches Rotes Kreuz           de
 10   Simple confirmation      `Clothes bank/01/06/2014/159/16 <…>`__                      RADERMACHER Guido (159)                                        de
 9    Simple confirmation      `Food bank/31/05/2014/155/13 <…>`__                         RADERMACHER Christian (155)                                    en
 8    Simple confirmation      `Heating costs/30/05/2014/152/10 <…>`__                     EMONTS-GAST Erna (152)                                         fr
 7    Simple confirmation      `Furniture/29/05/2014/146/7 <…>`__                          MALMENDIER Marc (146)                                          de
 6    Refund confirmation      `DMH/28/05/2014/142/7 <…>`__                                LAMBERTZ Guido (142)                                           de
 5    Refund confirmation      `AMK/27/05/2014/139/1 <…>`__                                JONAS Josef (139)                                              fr
 4    Simple confirmation      `Erstattung/25/05/2014/130/1 <…>`__                         FAYMONVILLE Luc (130*)                                         de
 3    Income confirmation      `Feste Beihilfe/24/05/2014/128/58 <…>`__                    EMONTS Daniel (128)                                            de
 2    Income confirmation      `Ausländerbeihilfe/08/08/2013/116/2 <…>`__                  AUSDEMWALD Alfons (116)                                        de
 1    Income confirmation      `EiEi/29/09/2012/116/1 <…>`__                               AUSDEMWALD Alfons (116)                                        de
==== ======================== =========================================================== ============================= ================================ ==========
<BLANKLINE>






As for the default language of an excerpt: the recipient overrides the
owner.

The above list no longer shows well how the language of an excerpt
depends on the recipient and the client.  That would need some more
excerpts.  Excerpt 88 (the only example) is in *French* because the
recipient (BISA) speaks French and although the owner (Charlotte)
speaks *German*:

>>> print(contacts.Partner.objects.get(id=196).language)
fr
>>> print(contacts.Partner.objects.get(id=118).language)
de


The default template for excerpts
==================================

.. xfile:: excerpts/Default.odt

This template should be customized locally to contain the :term:`site
operator`'s layout.


The template inserts the recipient address using this appy.pod code::

    do text
    from html(this.get_address_html(5, **{'class':"Recipient"})

This code is inserted as a command in some paragraph whose content in
the template can be anything since it will be replaced by the computed
text.

>>> obj = aids.SimpleConfirmation.objects.get(pk=19)
>>> print(obj.get_address_html(5, **{'class':"Recipient"}))
<p class="Recipient">Belgisches Rotes Kreuz<br/>Hillstraße 1<br/>4700 Eupen</p>

That paragraph should also contain another comment::

    do text if this.excerpt_type.print_recipient

There should of course be a paragraph style "Recipient" with proper
margins and spacing set.
