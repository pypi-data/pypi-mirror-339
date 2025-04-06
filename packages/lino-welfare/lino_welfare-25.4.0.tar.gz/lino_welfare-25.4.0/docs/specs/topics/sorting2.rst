.. doctest docs/specs/topics/sorting2.rst

.. _welfare.specs.topics.sorting2:

=================
About sorting (2)
=================


.. contents::
   :depth: 2
   :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.mathieu.settings.demo')
>>> from lino.api.doctest import *

This to verify whether sorting works as expected.

>>> for o in contacts.Company.objects.all():
...    print("{o.id} {o.name}".format(o=o))  #doctest: +REPORT_UDIFF
100 Belgisches Rotes Kreuz
101 Rumma & Ko OÜ
102 Bäckerei Ausdemwald
103 Bäckerei Mießen
104 Bäckerei Schmitz
105 Garage Mergelsberg
106 Donderweer BV
107 Van Achter NV
108 Hans Flott & Co
109 Bernd Brechts Bücherladen
110 Reinhards Baumschule
111 Moulin Rouge
112 Auto École Verte
187 ÖSHZ Kettenis
188 BISA
189 R-Cycle Sperrgutsortierzentrum
190 Die neue Alternative V.o.G.
191 Pro Aktiv V.o.G.
192 Werkstatt Cardijn V.o.G.
193 Behindertenstätten Eupen
194 Beschützende Werkstätte Eupen
195 Alliance Nationale des Mutualités Chrétiennes
196 Mutualité Chrétienne de Verviers - Eupen
197 Union Nationale des Mutualités Neutres
198 Mutualia - Mutualité Neutre
199 Solidaris - Mutualité socialiste et syndicale de la province de Liège
200 Apotheke Reul
201 Apotheke Schunck
202 Pharmacies Populaires de Verviers
203 Bosten-Bocken A
204 Brüll Christine
205 Brocal Catherine
206 Bourseaux Alexandre
207 Baguette Stéphanie
208 Demarteau Bernadette
209 Schmitz Marc
210 Cashback sprl
211 Money Wizard AS
214 Arbeitsamt der D.G.
220 Pro Aktiv Unterstadt
221 Pro Aktiv Noereth
222 Pro Aktiv Nispert

>>> for o in contacts.Person.objects.all():
...    print("{o.id} {o.last_name}, {o.first_name}".format(o=o))
... #doctest: +REPORT_UDIFF
249 Adam, Albert
253 Adam, Ilja
258 Adam, Noémie
259 Adam, Odette
260 Adam, Pascale
184 Allmanns, Alicia
115 Altenberg, Hans
113 Arens, Andreas
114 Arens, Annette
116 Ausdemwald, Alfons
117 Bastiaensen, Laurent
170 Bodard, Bernard
250 Braun, Bruno
254 Braun, Jan
255 Braun, Kevin
256 Braun, Lars
257 Braun, Monique
177 Brecht, Bernd
217 Castou, Carmen
120 Chantraine, Marc
119 Charlier, Ulrike
118 Collard, Charlotte
122 Demeulenaere, Dorothée
180 Denon, Denis
121 Dericum, Daniel
124 Dobbelstein, Dorothée
123 Dobbelstein-Demeulenaere, Dorothée
240 Drosson, Dora
179 Dubois, Robin
171 Dupont, Jean
175 Eierschal, Emil
235 Einzig, Paula
128 Emonts, Daniel
150 Emonts, Erich
152 Emonts-Gast, Erna
151 Emontspool, Erwin
129 Engels, Edgar
125 Ernst, Berta
127 Evers, Eberhart
126 Evertz, Bernd
251 Evrard, Eveline
130 Faymonville, Luc
252 Freisen, Françoise
233 Frisch, Alice
234 Frisch, Bernd
239 Frisch, Clara
241 Frisch, Dennis
229 Frisch, Hubert
244 Frisch, Irma
232 Frisch, Ludwig
243 Frisch, Melba
231 Frisch, Paul
236 Frisch, Peter
238 Frisch, Philippe
230 Frogemuth, Gaby
212 Gerkens, Gerd
131 Gernegroß, Germaine
132 Groteclaes, Gregory
134 Hilgers, Henri
133 Hilgers, Hildegard
183 Huppertz, Hubert
135 Ingels, Irene
137 Jacobs, Jacqueline
136 Jansen, Jérémy
181 Jeanémart, Jérôme
138 Johnen, Johann
139 Jonas, Josef
140 Jousten, Jan
186 Jousten, Judith
141 Kaivers, Karl
213 Kasennova, Tatjana
178 Keller, Karl
219 Kimmel, Killian
176 Lahm, Lisa
142 Lambertz, Guido
143 Laschet, Laura
144 Lazarus, Line
145 Leffin, Josefine
242 Loslever, Laura
146 Malmendier, Marc
172 Martelaer, Mark
147 Meessen, Melissa
149 Meier, Marie-Louise
148 Mießen, Michael
182 Mélard, Mélanie
153 Radermacher, Alfons
154 Radermacher, Berta
155 Radermacher, Christian
156 Radermacher, Daniela
157 Radermacher, Edgard
158 Radermacher, Fritz
159 Radermacher, Guido
160 Radermacher, Hans
161 Radermacher, Hedi
162 Radermacher, Inge
163 Radermacher, Jean
173 Radermecker, Rik
185 Thelen, Theresia
174 Vandenmeulenbos, Marie-Louise
218 Waldmann, Walter
215 Waldmann, Waltraud
216 Wehnicht, Werner
237 Zweith, Petra
165 da Vinci, David
164 di Rupo, Didier
166 van Veen, Vincent
169 Ärgerlich, Erna
167 Õunapuu, Õie
168 Östges, Otto

>>> for o in pcsw.Client.objects.all():
...    print("{o.id} {o.last_name}, {o.first_name}".format(o=o))
116 Ausdemwald, Alfons
117 Bastiaensen, Laurent
118 Collard, Charlotte
120 Chantraine, Marc
121 Dericum, Daniel
122 Demeulenaere, Dorothée
123 Dobbelstein-Demeulenaere, Dorothée
124 Dobbelstein, Dorothée
125 Ernst, Berta
126 Evertz, Bernd
127 Evers, Eberhart
128 Emonts, Daniel
129 Engels, Edgar
130 Faymonville, Luc
131 Gernegroß, Germaine
132 Groteclaes, Gregory
133 Hilgers, Hildegard
134 Hilgers, Henri
135 Ingels, Irene
136 Jansen, Jérémy
137 Jacobs, Jacqueline
138 Johnen, Johann
139 Jonas, Josef
140 Jousten, Jan
141 Kaivers, Karl
142 Lambertz, Guido
143 Laschet, Laura
144 Lazarus, Line
145 Leffin, Josefine
146 Malmendier, Marc
147 Meessen, Melissa
149 Meier, Marie-Louise
150 Emonts, Erich
151 Emontspool, Erwin
152 Emonts-Gast, Erna
153 Radermacher, Alfons
154 Radermacher, Berta
155 Radermacher, Christian
156 Radermacher, Daniela
157 Radermacher, Edgard
158 Radermacher, Fritz
159 Radermacher, Guido
160 Radermacher, Hans
161 Radermacher, Hedi
162 Radermacher, Inge
164 di Rupo, Didier
165 da Vinci, David
166 van Veen, Vincent
167 Õunapuu, Õie
168 Östges, Otto
172 Martelaer, Mark
173 Radermecker, Rik
174 Vandenmeulenbos, Marie-Louise
175 Eierschal, Emil
176 Lahm, Lisa
177 Brecht, Bernd
178 Keller, Karl
179 Dubois, Robin
180 Denon, Denis
181 Jeanémart, Jérôme
213 Kasennova, Tatjana
231 Frisch, Paul
250 Braun, Bruno


>>> for o in coachings.Coaching.objects.all():
...    print("{o.id} {o}".format(o=o))
1 alicia / Ausdemwald A
2 hubert / Ausdemwald A
3 melanie / Ausdemwald A
4 caroline / Ausdemwald A
5 hubert / Collard C
6 melanie / Collard C
7 hubert / Dobbelstein-Demeulenaere D
8 melanie / Dobbelstein D
9 alicia / Evertz B
10 hubert / Evers E
11 melanie / Evers E
12 caroline / Evers E
13 hubert / Emonts D
14 melanie / Emonts D
15 hubert / Emonts D
16 melanie / Engels E
17 alicia / Engels E
18 hubert / Engels E
19 melanie / Engels E
20 caroline / Faymonville L
21 hubert / Faymonville L
22 melanie / Groteclaes G
23 hubert / Hilgers H
24 melanie / Hilgers H
25 alicia / Hilgers H
26 hubert / Jacobs J
27 melanie / Jacobs J
28 caroline / Jacobs J
29 hubert / Johnen J
30 melanie / Johnen J
31 hubert / Jonas J
32 melanie / Jonas J
33 alicia / Jonas J
34 hubert / Jonas J
35 melanie / Kaivers K
36 caroline / Kaivers K
37 hubert / Lambertz G
38 melanie / Lazarus L
39 hubert / Lazarus L
40 melanie / Lazarus L
41 alicia / Leffin J
42 hubert / Malmendier M
43 melanie / Malmendier M
44 caroline / Malmendier M
45 hubert / Meessen M
46 melanie / Meessen M
47 hubert / Meessen M
48 melanie / Meessen M
49 alicia / Emonts-Gast E
50 hubert / Emonts-Gast E
51 melanie / Radermacher A
52 caroline / Radermacher C
53 hubert / Radermacher C
54 melanie / Radermacher C
55 hubert / Radermacher E
56 melanie / Radermacher E
57 alicia / Radermacher E
58 hubert / Radermacher F
59 melanie / Radermacher G
60 caroline / Radermacher G
61 hubert / Radermacher G
62 melanie / Radermacher G
63 hubert / Radermacher H
64 melanie / Radermacher H
65 alicia / da Vinci D
66 hubert / van Veen V
67 melanie / van Veen V
68 caroline / van Veen V
69 hubert / Õunapuu Õ
70 melanie / Õunapuu Õ
71 hubert / Östges O
72 melanie / Östges O
73 alicia / Östges O
74 hubert / Radermecker R
75 melanie / Radermecker R
76 caroline / Radermecker R
77 hubert / Radermecker R
78 melanie / Brecht B
79 hubert / Brecht B
80 melanie / Keller K
81 alicia / Dubois R
82 hubert / Dubois R
83 melanie / Dubois R
84 caroline / Denon D
85 hubert / Denon D
86 melanie / Denon D
87 hubert / Jeanémart J
88 melanie / Jeanémart J
89 alicia / Jeanémart J
90 hubert / Jeanémart J

>>> for o in cv.ObstacleType.objects.all():
...    print("{o.id} {o}".format(o=o))
1 Alcohol
2 Santé
3 Dettes
4 Problèmes familiers

>>> for o in cv.Obstacle.objects.all():
...    print("{o.id} {o.person} {o.type}".format(o=o))
1 M. Josef JONAS Alcohol
2 M. Karl KAIVERS Santé
3 M. Guido LAMBERTZ Dettes
4 Mme Line LAZARUS Problèmes familiers
5 M. Marc MALMENDIER Alcohol
6 M. Josef JONAS Santé
7 M. Karl KAIVERS Dettes
8 M. Guido LAMBERTZ Problèmes familiers
9 Mme Line LAZARUS Alcohol
10 M. Marc MALMENDIER Santé
11 M. Josef JONAS Dettes
12 M. Karl KAIVERS Problèmes familiers
13 M. Guido LAMBERTZ Alcohol
14 Mme Line LAZARUS Santé
15 M. Marc MALMENDIER Dettes
16 M. Josef JONAS Problèmes familiers
17 M. Karl KAIVERS Alcohol
18 M. Guido LAMBERTZ Santé
19 Mme Line LAZARUS Dettes
20 M. Marc MALMENDIER Problèmes familiers


>>> for o in courses.Course.objects.all():
...    print("{o.id} {o}".format(o=o))
1 Cuisine (12/05/2014)
2 Créativité (12/05/2014)
3 Notre premier bébé (12/05/2014)
4 Mathématiques (12/05/2014)
5 Français (12/05/2014)
6 Activons-nous! (12/05/2014)
7 Intervention psycho-sociale (03/11/2013)

>>> for o in courses.Enrolment.objects.all():
...    print("{o.id} {o}".format(o=o))
1 Cuisine (12/05/2014) / AUSDEMWALD Alfons (116)
2 Créativité (12/05/2014) / BASTIAENSEN Laurent (117)
3 Notre premier bébé (12/05/2014) / COLLARD Charlotte (118)
4 Mathématiques (12/05/2014) / CHANTRAINE Marc (120*)
5 Français (12/05/2014) / DERICUM Daniel (121)
6 Activons-nous! (12/05/2014) / DEMEULENAERE Dorothée (122)
7 Intervention psycho-sociale (03/11/2013) / DOBBELSTEIN-DEMEULENAERE Dorothée (123*)
8 Cuisine (12/05/2014) / DOBBELSTEIN Dorothée (124)
9 Créativité (12/05/2014) / ERNST Berta (125)
10 Notre premier bébé (12/05/2014) / EVERTZ Bernd (126*)
11 Mathématiques (12/05/2014) / EVERS Eberhart (127)
12 Français (12/05/2014) / EMONTS Daniel (128)
13 Activons-nous! (12/05/2014) / ENGELS Edgar (129)
14 Intervention psycho-sociale (03/11/2013) / FAYMONVILLE Luc (130*)
15 Cuisine (12/05/2014) / GERNEGROSS Germaine (131)
16 Créativité (12/05/2014) / GROTECLAES Gregory (132)
17 Notre premier bébé (12/05/2014) / HILGERS Hildegard (133)
18 Mathématiques (12/05/2014) / HILGERS Henri (134)
19 Français (12/05/2014) / INGELS Irene (135)
20 Activons-nous! (12/05/2014) / JANSEN Jérémy (136)
21 Cuisine (12/05/2014) / JACOBS Jacqueline (137)
22 Créativité (12/05/2014) / JOHNEN Johann (138*)
23 Notre premier bébé (12/05/2014) / JONAS Josef (139)
24 Mathématiques (12/05/2014) / JOUSTEN Jan (140*)
25 Français (12/05/2014) / KAIVERS Karl (141)
26 Activons-nous! (12/05/2014) / LAMBERTZ Guido (142)
27 Cuisine (12/05/2014) / LASCHET Laura (143)
28 Créativité (12/05/2014) / LAZARUS Line (144)
29 Notre premier bébé (12/05/2014) / LEFFIN Josefine (145*)
30 Mathématiques (12/05/2014) / MALMENDIER Marc (146)
31 Français (12/05/2014) / MEESSEN Melissa (147)
32 Activons-nous! (12/05/2014) / MEIER Marie-Louise (149)
33 Cuisine (12/05/2014) / EMONTS Erich (150*)
34 Créativité (12/05/2014) / EMONTSPOOL Erwin (151)
35 Notre premier bébé (12/05/2014) / EMONTS-GAST Erna (152)
36 Mathématiques (12/05/2014) / RADERMACHER Alfons (153)
37 Français (12/05/2014) / RADERMACHER Berta (154)
38 Cuisine (12/05/2014) / RADERMACHER Christian (155)
39 Créativité (12/05/2014) / RADERMACHER Daniela (156)
40 Notre premier bébé (12/05/2014) / RADERMACHER Edgard (157)
41 Mathématiques (12/05/2014) / RADERMACHER Fritz (158*)
42 Français (12/05/2014) / RADERMACHER Guido (159)
43 Cuisine (12/05/2014) / RADERMACHER Hans (160*)
44 Créativité (12/05/2014) / RADERMACHER Hedi (161)
45 Notre premier bébé (12/05/2014) / RADERMACHER Inge (162)
46 Mathématiques (12/05/2014) / DI RUPO Didier (164)
47 Français (12/05/2014) / DA VINCI David (165)
48 Cuisine (12/05/2014) / VAN VEEN Vincent (166)
49 Créativité (12/05/2014) / ÕUNAPUU Õie (167*)
50 Notre premier bébé (12/05/2014) / ÖSTGES Otto (168)
51 Mathématiques (12/05/2014) / MARTELAER Mark (172)
52 Français (12/05/2014) / RADERMECKER Rik (173)
53 Cuisine (12/05/2014) / VANDENMEULENBOS Marie-Louise (174)
54 Créativité (12/05/2014) / EIERSCHAL Emil (175)
55 Notre premier bébé (12/05/2014) / LAHM Lisa (176)
56 Mathématiques (12/05/2014) / BRECHT Bernd (177)
57 Français (12/05/2014) / KELLER Karl (178)
58 Cuisine (12/05/2014) / DUBOIS Robin (179)
59 Créativité (12/05/2014) / DENON Denis (180*)
60 Notre premier bébé (12/05/2014) / JEANÉMART Jérôme (181)
61 Mathématiques (12/05/2014) / KASENNOVA Tatjana (213)
62 Français (12/05/2014) / AUSDEMWALD Alfons (116)
63 Cuisine (12/05/2014) / BASTIAENSEN Laurent (117)
64 Créativité (12/05/2014) / COLLARD Charlotte (118)
65 Notre premier bébé (12/05/2014) / CHANTRAINE Marc (120*)
66 Mathématiques (12/05/2014) / DERICUM Daniel (121)
67 Français (12/05/2014) / DEMEULENAERE Dorothée (122)
68 Cuisine (12/05/2014) / DOBBELSTEIN-DEMEULENAERE Dorothée (123*)
69 Créativité (12/05/2014) / DOBBELSTEIN Dorothée (124)
70 Notre premier bébé (12/05/2014) / ERNST Berta (125)
71 Mathématiques (12/05/2014) / EVERTZ Bernd (126*)
72 Français (12/05/2014) / EVERS Eberhart (127)
73 Cuisine (12/05/2014) / EMONTS Daniel (128)
74 Créativité (12/05/2014) / ENGELS Edgar (129)
75 Notre premier bébé (12/05/2014) / FAYMONVILLE Luc (130*)
76 Mathématiques (12/05/2014) / GERNEGROSS Germaine (131)
77 Français (12/05/2014) / GROTECLAES Gregory (132)
78 Cuisine (12/05/2014) / HILGERS Hildegard (133)
79 Créativité (12/05/2014) / HILGERS Henri (134)
80 Notre premier bébé (12/05/2014) / INGELS Irene (135)
81 Mathématiques (12/05/2014) / JANSEN Jérémy (136)
82 Français (12/05/2014) / JACOBS Jacqueline (137)
83 Cuisine (12/05/2014) / JOHNEN Johann (138*)
84 Créativité (12/05/2014) / JONAS Josef (139)
85 Notre premier bébé (12/05/2014) / JOUSTEN Jan (140*)
86 Mathématiques (12/05/2014) / KAIVERS Karl (141)
87 Français (12/05/2014) / LAMBERTZ Guido (142)
88 Créativité (12/05/2014) / LASCHET Laura (143)
89 Notre premier bébé (12/05/2014) / LAZARUS Line (144)
90 Mathématiques (12/05/2014) / LEFFIN Josefine (145*)
91 Français (12/05/2014) / MALMENDIER Marc (146)
92 Cuisine (12/05/2014) / MEESSEN Melissa (147)
93 Créativité (12/05/2014) / MEIER Marie-Louise (149)
94 Notre premier bébé (12/05/2014) / EMONTS Erich (150*)
95 Mathématiques (12/05/2014) / EMONTSPOOL Erwin (151)
96 Français (12/05/2014) / EMONTS-GAST Erna (152)
97 Cuisine (12/05/2014) / RADERMACHER Alfons (153)
98 Créativité (12/05/2014) / RADERMACHER Berta (154)
99 Notre premier bébé (12/05/2014) / RADERMACHER Christian (155)
100 Mathématiques (12/05/2014) / RADERMACHER Daniela (156)

>>> for o in immersion.ContractType.objects.all():
...    print("{o.id} {o}".format(o=o))
3 MISIP
1 Mise en situation interne
2 Stage d'immersion

>>> for o in immersion.Goal.objects.all():
...    print("{o.id} {o}".format(o=o))
3 Avoir une expérience de travail
2 Confirmer un projet professionel
1 Découvrir un métier
4 Démontrer des compétences

>>> for o in polls.Question.objects.all():
...    print("{o.id} {o}".format(o=o))
1 Pour commencer ma recherche d'emploi, je dois
31 1) Cherchez-vous du travail actuellement?
2 1) Avoir une farde de recherche d’emploi organisée
32 2) Avez-vous un CV à jour?
3 2) Réaliser mon curriculum vitae
33 3) Est-ce que vous vous présentez régulièrement au FOREM?
4 3) Savoir faire une lettre de motivation adaptée au poste de travail visé
34 4) Est-ce que vous consultez les petites annonces?
5 4) Respecter les modalités de candidature
35 5) Demande à l’entourage?
6 5) Me créer une boite e-mail appropriée à la recherche d’emploi
36 6) Candidature spontanée?
7 6) Créer mon compte sur le site de Forem
37 7) Antécédents judiciaires?
8 7) Mettre mon curriculum vitae sur le site du Forem
38 Temps de travail acceptés
9 8) Connaître les aides à l’embauche qui me concernent
10 9) Etre préparé à l’entretien d’embauche ou téléphonique
11 Est-ce que je sais...
12 1) Utiliser le site du Forem pour consulter les offres d’emploi
13 2) Décoder une offre d’emploi
14 3) Adapter mon curriculum vitae par rapport à une offre ou pour une candidature spontanée
15 4) Réaliser une lettre de motivation suite à une offre d’emploi
16 5) Adapter une lettre de motivation par rapport à l’offre d’emploi
17 6) Réaliser une lettre de motivation spontanée
18 7) Utiliser le fax pour envoyer mes candidatures
19 8) Utiliser ma boite e-mail pour envoyer mes candidatures
20 9) Mettre mon curriculum vitae en ligne sur des sites d’entreprise
21 10) Compléter en ligne les formulaires de candidature
22 11) M’inscrire aux agences intérim via Internet
23 12) M’inscrire auprès d’agence de recrutement via Internet
24 13) Utiliser Internet pour faire des recherches sur une entreprise
25 14) Préparer un entretien d’embauche (questions, argumentation du C.V.,…)
26 15) Utiliser Internet pour gérer ma mobilité (transport en commun ou itinéraire voiture)
27 16) Utiliser la photocopieuse (ex : copie de lettre de motivation que j’envoie par courrier)
28 17) Utiliser le téléphone pour poser ma candidature
29 18) Utiliser le téléphone pour relancer ma candidature
30 19) Trouver et imprimer les formulaires de demandes d’aides à l’embauche se trouvant sur le site de l’ONEm

>>> for o in cal.GuestRole.objects.all():
...    print("{o.id} {o}".format(o=o))
1 Collègue
2 Visiteur
3 Président
4 Greffier

>>> for o in cal.EventType.objects.all():
...    print("{o.id} {o}".format(o=o))
1 Absences
2 Jours fériés
3 Réunion
4 Interne
5 Internal meetings with client
6 Évaluation
7 Consultations avec le bénéficiaire
8 Réunions externes avec le bénéficiaire
9 Informational meetings
10 Réunions interne
11 Réunions externe
12 Privé
13 Atelier

..
  >> for o in polls.AnswerChoice.objects.all():
  ..    print("{o.id} {o}".format(o=o))

>>> for o in isip.ContractEnding.objects.all():
...    print("{o.id} {o}".format(o=o))
1 Normal
2 Alcohol
3 Santé
4 Force majeure
