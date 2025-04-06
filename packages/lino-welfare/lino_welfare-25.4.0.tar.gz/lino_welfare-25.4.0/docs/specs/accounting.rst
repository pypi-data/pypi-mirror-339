.. doctest docs/specs/accounting.rst

.. _welfare.specs.accounting:

===========================
Accounting for Lino Welfare
===========================

.. doctest init:

    >>> import lino
    >>> lino.startup('lino_welfare.projects.gerd.settings.doctests')
    >>> from etgen.html import E
    >>> from lino.api.doctest import *
    >>> from lino.api import rt


This document describes the functionalities for registering and
keeping track of social aid expenses, including client-related
refunding of certain costs, disbursements of regular monthly social
aid and communication with the bank in both directions.

These will partly turn Lino Welfare into an accounting package.
Actually it produces a *subledger*, i.e. manages only *a part of* a
complete accounting system.

A first prototype was developed between May 2015 and April 2016 as
ticket :ticket:`143` ("Nebenbuchhaltung Sozialhilfeausgaben") and
related tickets. The code examples may contain German texts for
practical reasons to facilitate analysis.

This document extends the following specifications:

- :ref:`cosi.specs.accounting`
- :ref:`cosi.specs.accounting`

This document is base for the following specifications:

- :doc:`vatless`
- :doc:`finan`.



.. contents::
   :depth: 1
   :local:

Implementation notes
====================

This project integrates several plugins into Lino Welfare which are
also used by :ref:`cosi`:

- :mod:`lino_welfare.modlib.accounting` is a thin extension of
  :mod:`lino_xl.lib.accounting`,
- :mod:`lino_xl.lib.vatless` is for VAT-less invoices (mostly
  incoming invoices)
- :mod:`lino_xl.lib.finan` is for "financial vouchers", i.e. bank
  statements, payment orders, journal entries.
  :mod:`lino_welfare.modlib.finan` extends this and adds a voucher
  type called "Disbursement orders". A disbursement order is similar
  to a payment order, but only used internally.


Some shortcuts:

>>> Journal = rt.models.accounting.Journal
>>> Journals = rt.models.accounting.Journals



Partner versus Project
======================

Accounting in Lino Welfare is special because every transaction
usually has *two* external partners: (1) the "beneficiary" or "client"
to which this transaction must be assigned and (2) the actual
recipient (or sender) of the payment.

The :attr:`project_model <lino_xl.lib.accounting.Plugin.project_model>`
of the accounting plugin is `contacts.Client`, which means that every
ledger movement can additionally point to a *client* as the "project".

The client of a transaction can be somebody else than the partner.

The following models are called "client related"
(:class:`lino_xl.lib.accounting.mixins.ProjectRelated` (don't mix that
up with :class:`lino.mixins.ProjectRelated`), i.e. can point to a
client:

>>> from lino_xl.lib.accounting.mixins import ProjectRelated
>>> # from lino.mixins import ProjectRelated
>>> for m in rt.models_by_base(ProjectRelated):
...     print(m)
<class 'lino_xl.lib.accounting.models.Movement'>
<class 'lino_xl.lib.finan.models.BankStatementItem'>
<class 'lino_xl.lib.finan.models.JournalEntry'>
<class 'lino_xl.lib.finan.models.JournalEntryItem'>
<class 'lino_xl.lib.finan.models.PaymentOrderItem'>
<class 'lino_xl.lib.vatless.models.AccountInvoice'>
<class 'lino_xl.lib.vatless.models.InvoiceItem'>


.. _wilfried:

The "accountant" user type
=============================

A demo user with the fictive name *Wilfried Willems* has the user
user_type of an accountant
(:class:`lino_welfare.modlib.welfare.roles.LedgerUser`).

>>> p = rt.login('wilfried').get_user().user_type
>>> print(p)
500 (Buchhalter)

Accountants have no direct contact with clients and probably won't use
the calendar.  But for the first prototype they get :class:`OfficeUser
<lino.modlib.office.roles.OfficeUser>` functionality so they can
decide themselves whether they want it.

>>> from lino.modlib.office.roles import OfficeUser
>>> p.has_required_roles([OfficeUser])
True

Here is the main menu for accountants:

>>> show_menu('wilfried', language="de")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Meine Benachrichtigungen, Meine Auszüge, Meine ablaufenden Upload-Dateien, Meine Upload-Dateien, Mein E-Mail-Ausgang, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine unbestätigten Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten, Meine überfälligen Termine
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- Buchhaltung :
  - Rechnungseingänge : Rechnungseingänge (REG), Sammelrechnungen (SREG)
  - Ausgabeanweisungen : Ausgabeanweisungen (AAW)
  - Zahlungsaufträge : KBC Zahlungsaufträge (ZKBC)
- Berichte :
  - Buchhaltung : Schuldner, Gläubiger
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - ÖSHZ : Hilfearten, Kategorien
- Explorer :
  - Kontakte : Partner
  - ÖSHZ : Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - Buchhaltung : Rechnungen
  - SEPA : Bankkonten, Importierte  Bankkonten, Kontoauszüge, Transaktionen
- Site : Info


General accounts ("budgetary articles")
=======================================

Belgian public instances use so-called budgetary articles (`Articles budgétaires
<http://www.pouvoirslocaux.irisnet.be/fr/theme/finances/docfin/la-structure-dun-article-budgetaire>`_
in French, "Haushaltsartikel" in German) for classifying their monetary
transactions.  These budgetary articles are in public sector accounting exactly
what general accounts are in private sector accounting.  It seems BTW that the
usage of the term "budgetary articles" is being replaced by the term "accounts".

The main difference is that they are structured differently.  The demo database
currently has a mixture of "PCMN style" and "public sector style" references
because Lino Welfare doesn't use full accounting reports
(:mod:`lino_xl.lib.sheets`).

>>> rt.show(accounting.Accounts)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
======================================================== ================= =============== =============
 Beschreibung                                             Braucht Partner   Auszugleichen   Referenz
-------------------------------------------------------- ----------------- --------------- -------------
 **   1000 Net income (loss)**                            Ja                Ja              1000
 **   4000 Kunden**                                       Ja                Ja              4000
 **   4100 Lieferanten**                                  Ja                Ja              4100
 **   4200 Angestellte**                                  Ja                Ja              4200
 **   4300 Offene Zahlungsaufträge**                      Ja                Ja              4300
 **   4450 Auszuführende Ausgabeanweisungen**             Ja                Ja              4450
 **   4500 Steuerämter**                                  Ja                Ja              4500
 **   4510 Geschuldete Mehrwertsteuer**                   Nein              Nein            4510
 **   4513 Deklarierte Mehrwertsteuer**                   Nein              Nein            4513
 **   4520 Abziehbare Mehrwertsteuer**                    Nein              Nein            4520
 **   4530 Rückzahlbare Mehrwertsteuer**                  Nein              Nein            4530
 **   4800 Internal clearings**                           Ja                Ja              4800
 **   4810 Gewährte Hilfen**                              Ja                Ja              4810
 **   4900 Wartekonto**                                   Ja                Ja              4900
 **   5500 BestBank**                                     Nein              Nein            5500
 **   5700 Kasse**                                        Nein              Nein            5700
 **   6010 Einkäufe von Dienstleistungen**                Nein              Nein            6010
 **   6020 Investierungskäufe**                           Nein              Nein            6020
 **   6040 Wareneinkäufe**                                Nein              Nein            6040
 **   6300 Löhne und Gehälter**                           Nein              Nein            6300
 **   6900 Net income**                                   Nein              Nein            6900
 **   7000 Verkauf**                                      Nein              Nein            7000
 **         820/333/01 Vorschuss auf Vergütungen o.ä.**   Nein              Nein            820/333/01
 **         821/333/01 Vorschuss auf Pensionen**          Nein              Nein            821/333/01
 **         822/333/01 Vorsch. Entsch. Arbeitsunfälle**   Nein              Nein            822/333/01
 **         823/333/01 Vor. Kranken- u. Invalidengeld**   Nein              Nein            823/333/01
 **         825/333/01 Vorschuss auf Familienzulage**     Nein              Nein            825/333/01
 **         826/333/01 Vorschuss auf Arbeitslosengeld**   Nein              Nein            826/333/01
 **         827/333/01 Vorschuss auf Behindertenzulag**   Nein              Nein            827/333/01
 **         832/330/01 Allgemeine Beihilfen**             Nein              Nein            832/330/01
 **         832/330/02 Gesundheitsbeihilfe**              Nein              Nein            832/330/02
 **         832/330/03 Heizkosten- u. Energiebeihilfe**   Nein              Nein            832/330/03
 **          832/330/03F Fonds Gas und Elektrizität**     Nein              Nein            832/330/03F
 **         832/330/04 Mietkaution**                      Nein              Nein            832/330/04
 **         832/333/22 Mietbeihilfe**                     Nein              Nein            832/333/22
 **          832/3331/01 Eingliederungseinkommen**        Nein              Nein            832/3331/01
 **         832/334/27 Sozialhilfe**                      Nein              Nein            832/334/27
 **          832/3343/21 Beihilfe für Ausländer**         Nein              Nein            832/3343/21
 **         P82/000/00 Einn. Dritter: Weiterleitung**     Nein              Nein            P82/000/00
 **         P83/000/00 Unber. erh. Beträge + Erstatt.**   Nein              Nein            P83/000/00
 **         P87/000/00 Abhebung von pers. Guthaben**      Nein              Nein            P87/000/00
======================================================== ================= =============== =============
<BLANKLINE>


Vouchers
========

A **voucher** (German *Beleg*) is a document which serves as legal
proof for a transaction. A transaction is a set of accounting
**movements** whose debit equals to their credit.

Lino Welfare uses the following **voucher types**:

>>> rt.show(accounting.VoucherTypes)
=================================== ====== ================================================= =====================================================
 Wert                                name   Text                                              Modell
----------------------------------- ------ ------------------------------------------------- -----------------------------------------------------
 finan.BankStatementsByJournal              Kontoauszug (finan.BankStatementsByJournal)       <class 'lino_xl.lib.finan.models.BankStatement'>
 finan.DisbursementOrdersByJournal          Ausgabeanweisungen                                <class 'lino_xl.lib.finan.models.PaymentOrder'>
 finan.JournalEntriesByJournal              Diverse Buchung (finan.JournalEntriesByJournal)   <class 'lino_xl.lib.finan.models.JournalEntry'>
 finan.PaymentOrdersByJournal               Zahlungsauftrag (finan.PaymentOrdersByJournal)    <class 'lino_xl.lib.finan.models.PaymentOrder'>
 vatless.InvoicesByJournal                  Rechnungen                                        <class 'lino_xl.lib.vatless.models.AccountInvoice'>
 vatless.ProjectInvoicesByJournal           Project invoices                                  <class 'lino_xl.lib.vatless.models.AccountInvoice'>
=================================== ====== ================================================= =====================================================
<BLANKLINE>

.. before sorting them:
   =================================== ====== =================================================
    Wert                                name   Text
   ----------------------------------- ------ -------------------------------------------------
    vatless.InvoicesByJournal                  Rechnungen
    vatless.ProjectInvoicesByJournal           Project invoices
    finan.JournalEntriesByJournal              Diverse Buchung (finan.JournalEntriesByJournal)
    finan.PaymentOrdersByJournal               Zahlungsauftrag (finan.PaymentOrdersByJournal)
    finan.BankStatementsByJournal              Kontoauszug (finan.BankStatementsByJournal)
    finan.DisbursementOrdersByJournal          Ausgabeanweisungen
   =================================== ====== =================================================
   <BLANKLINE>


Invoices are partner-related vouchers (often we simply say **partner
voucher**). That is, you select one partner per voucher. Every
partner-related voucher points to to one and only one partner.

The other voucher types (Bank statements etc) are called **financial
vouchers**. Financial vouchers have their individual *entries*
partner-related, so the vouchers themselves are *not* related to a
single partner.

There are two types of invoice: those with only one project (client)
and those with more than one projects.

More about voucher types in
:class:`lino_xl.lib.accounting.choicelists.VoucherTypes`.

Journals
========

A :class:`Journal <lino_xl.lib.edger.models.Journal>` is a sequence
of numbered vouchers. All vouchers of a given journal are of same
type, but there may be more than one journal per voucher type.  The
demo database currently has the following journals defined:

>>> rt.show(Journals, column_names="ref name voucher_type journal_group")
========== ====================== ================================================ ====================
 Referenz   Bezeichnung            Belegart                                         Journalgruppe
---------- ---------------------- ------------------------------------------------ --------------------
 REG        Rechnungseingänge      Project invoices                                 Rechnungseingänge
 SREG       Sammelrechnungen       Rechnungen                                       Rechnungseingänge
 AAW        Ausgabeanweisungen     Ausgabeanweisungen                               Ausgabeanweisungen
 ZKBC       KBC Zahlungsaufträge   Zahlungsauftrag (finan.PaymentOrdersByJournal)   Zahlungsaufträge
========== ====================== ================================================ ====================
<BLANKLINE>

A default Lino Welfare has the following **journal groups**.

>>> rt.show(accounting.JournalGroups)
====== ====== ======================
 Wert   name   Text
------ ------ ----------------------
 10     bst    Bestellungen Einkauf
 20     reg    Rechnungseingänge
 30     ffo    Forderungen
 40     anw    Ausgabeanweisungen
 50     zau    Zahlungsaufträge
====== ====== ======================
<BLANKLINE>


The state of a voucher
=======================


>>> rt.show(accounting.VoucherStates)
====== ============ ============= ============
 Wert   name         Text          Editierbar
------ ------------ ------------- ------------
 10     draft        Entwurf       Ja
 20     registered   Registriert   Nein
 30     sent         Versendet     Nein
 40     cancelled    Storniert     Nein
====== ============ ============= ============
<BLANKLINE>

.. technical:

    The `VoucherStates` choicelist is used by two fields: one database
    field and one parameter field.

    >>> len(accounting.VoucherStates._fields)
    4
    >>> for f in accounting.VoucherStates._fields:
    ...     print(f)
    <lino.core.choicelists.ChoiceListField: state>
    accounting.Declaration.state
    finan.FinancialVoucher.state
    vatless.AccountInvoice.state

    >>> obj = vatless.AccountInvoice.objects.get(id=1)
    >>> ar = rt.login("robin").spawn(vatless.Invoices)
    >>> print(tostring(ar.get_data_value(obj, 'workflow_buttons')))
    <span><b>Registriert</b> → [Entwurf]</span>


Movements
=========

Users can consult the movements of a given general account.

>>> obj = accounting.Account.get_by_ref('820/333/01')
>>> print(str(obj))
(820/333/01) Vorschuss auf Vergütungen o.ä.

>>> rt.show(accounting.MovementsByAccount, obj)
========== ===================== ================================================================ ============ ======== =======
 Valuta     Beleg                 Beschreibung                                                     Debit        Kredit   Match
---------- --------------------- ---------------------------------------------------------------- ------------ -------- -------
 22.05.14   `REG 1/2014 <…>`__    `AS Express Post <…>`__ / `AUSDEMWALD Alfons (116) <…>`__        10,00
 03.03.14   `SREG 6/2014 <…>`__   `Niederau Eupen AG <…>`__ / `AUSDEMWALD Alfons (116) <…>`__      25,00
 03.03.14   `SREG 6/2014 <…>`__   `Niederau Eupen AG <…>`__ / `COLLARD Charlotte (118) <…>`__      149,95
 03.03.14   `SREG 6/2014 <…>`__   `Niederau Eupen AG <…>`__ / `DOBBELSTEIN Dorothée (124) <…>`__   125,33
 03.03.14   `SREG 6/2014 <…>`__   `Niederau Eupen AG <…>`__ / `EVERS Eberhart (127) <…>`__         10,00
 03.03.14   `SREG 6/2014 <…>`__   `Niederau Eupen AG <…>`__ / `EMONTS Daniel (128) <…>`__          12,50
                                  **Saldo 332.78 (6 Bewegungen)**                                  **332,78**
========== ===================== ================================================================ ============ ======== =======
<BLANKLINE>
