"""Translation tables for VMQTG V5: VI / EN / FR.

Keyed by SITEMAP id ("A", "B1", "B3.4", ...), or by content slug path
("tham-quan", "ve-di-tich/lich-su/thoi-ly", ...).

Vietnamese is the canonical text in build.py; here we store EN+FR.
Missing translations fall back to Vietnamese in JS.
"""

# ── UI strings (header, footer, sidebar, breadcrumb, search) ─────────────────
UI = {
    "site_name":    {"en":"Temple of Literature",                 "fr":"Temple de la Littérature"},
    "site_sub":     {"en":"Special National Heritage Site",       "fr":"Site du patrimoine national spécial"},
    "buy_ticket":   {"en":"Tickets",                              "fr":"Billets"},
    "buy_ticket_arrow": {"en":"Buy ticket →",                     "fr":"Acheter →"},
    "home":         {"en":"Home",                                 "fr":"Accueil"},
    "in_section":   {"en":"In this section",                      "fr":"Dans cette section"},
    "discover":     {"en":"Discover the Temple of Literature",    "fr":"Découvrez le Temple de la Littérature"},
    "search_ph":    {"en":"Search the site…",                     "fr":"Rechercher…"},
    "search_no":    {"en":"No results",                           "fr":"Aucun résultat"},
    "lang_vi":      {"en":"VI",  "fr":"VI"},
    "lang_en":      {"en":"EN",  "fr":"EN"},
    "lang_fr":      {"en":"FR",  "fr":"FR"},
    "hours":        {"en":"Opening hours",   "fr":"Heures d'ouverture"},
    "address":      {"en":"Address",         "fr":"Adresse"},
    "phone":        {"en":"Phone",           "fr":"Téléphone"},
    "price":        {"en":"Ticket",          "fr":"Tarif"},
    "price_val_adult": {"en":"30,000 VND / adult", "fr":"30 000 VND / adulte"},
    "addr_short":   {"en":"58 Quoc Tu Giam, Dong Da, Hanoi",
                     "fr":"58 Quoc Tu Giam, Dong Da, Hanoï"},
    "hero_title":   {"en":"Temple of Literature – Imperial Academy",
                     "fr":"Temple de la Littérature – Académie Impériale"},
    "hero_sub":     {"en":"Special National Heritage · First university of Vietnam · 82 Doctoral Stelae — UNESCO Memory of the World",
                     "fr":"Patrimoine national · Première université du Vietnam · 82 stèles doctorales — Mémoire du monde UNESCO"},
    "footer_brand": {"en":"Temple of Literature – Imperial Academy",
                     "fr":"Temple de la Littérature – Académie Impériale"},
    "footer_addr":  {"en":"58 Quoc Tu Giam St., Van Mieu Ward<br>Dong Da District, Hanoi<br>Phone: 024.3747.1322<br>Email: vanmieuqtg@hanoi.gov.vn",
                     "fr":"58 rue Quoc Tu Giam, Quartier Van Mieu<br>District de Dong Da, Hanoï<br>Tél : 024.3747.1322<br>Courriel : vanmieuqtg@hanoi.gov.vn"},
    "footer_copy":  {"en":"© Centre for Cultural and Scientific Activities of the Temple of Literature",
                     "fr":"© Centre des activités culturelles et scientifiques du Temple de la Littérature"},
    "count_items":  {"en":"items", "fr":"éléments"},
    "count_a":      {"en":"Tickets · Hours · Directions",
                     "fr":"Billets · Horaires · Accès"},
    "count_b":      {"en":"6 sections", "fr":"6 sections"},
    "count_c":      {"en":"3 sections", "fr":"3 sections"},
    "count_d":      {"en":"7 sections", "fr":"7 sections"},
    "count_e":      {"en":"6 sections", "fr":"6 sections"},
    "page_a_title": {"en":"Visitor information",
                     "fr":"Informations pratiques"},
    "page_a_sub":   {"en":"Tickets, hours, rules, directions and on-site amenities.",
                     "fr":"Billets, horaires, règlement, accès et services sur place."},
    "updating":     {"en":"Detail content is being prepared. Please contact Communications Office: 024.3747.1322.",
                     "fr":"Contenu en cours de préparation. Veuillez contacter le service Communication : 024.3747.1322."},
    "detail_about": {"en":"Detail page for", "fr":"Fiche détaillée pour"},
    "in_group":     {"en":"in", "fr":"dans"},
}

# ── Section / group / item labels — keyed by id ──────────────────────────────
LABELS = {
    "A":     {"en":"Visit",              "fr":"Visite"},
    "B":     {"en":"About the site",     "fr":"À propos du site"},
    "C":     {"en":"Exhibitions",        "fr":"Expositions"},
    "D":     {"en":"Activities",         "fr":"Activités"},
    "E":     {"en":"Services",           "fr":"Services"},

    # B groups
    "B1": {"en":"History",                "fr":"Histoire"},
    "B2": {"en":"Site sectors",           "fr":"Secteurs du site"},
    "B3": {"en":"Architecture",           "fr":"Architecture"},
    "B4": {"en":"Eminent figures",        "fr":"Personnages éminents"},
    "B5": {"en":"Statues of worship",     "fr":"Statues vénérées"},
    "B6": {"en":"Library",                "fr":"Bibliothèque"},

    # B1 items
    "B1.1": {"en":"Lý dynasty",     "fr":"Dynastie Lý"},
    "B1.2": {"en":"Trần dynasty",   "fr":"Dynastie Trần"},
    "B1.3": {"en":"Lê dynasty",     "fr":"Dynastie Lê"},
    "B1.4": {"en":"Nguyễn dynasty", "fr":"Dynastie Nguyễn"},

    # B2
    "B2.1": {"en":"Inner sanctuary", "fr":"Enceinte intérieure"},
    "B2.2": {"en":"Giám Garden",     "fr":"Jardin Giám"},
    "B2.3": {"en":"Văn Lake",        "fr":"Lac Văn"},

    # B3
    "B3.1":  {"en":"Hạ Mã steles",            "fr":"Stèles Hạ Mã"},
    "B3.2":  {"en":"Văn Miếu Gate",           "fr":"Porte Văn Miếu"},
    "B3.3":  {"en":"Đại Trung Gate",          "fr":"Porte Đại Trung"},
    "B3.4":  {"en":"Khuê Văn Pavilion",       "fr":"Pavillon Khuê Văn"},
    "B3.5":  {"en":"Stelae shelters",         "fr":"Abris des stèles"},
    "B3.6":  {"en":"Đại Thành Gate",          "fr":"Porte Đại Thành"},
    "B3.7":  {"en":"Ceremonial hall",         "fr":"Salle des cérémonies"},
    "B3.8":  {"en":"Thái Học Gate",           "fr":"Porte Thái Học"},
    "B3.9":  {"en":"Thái Học hall",           "fr":"Salle Thái Học"},
    "B3.10": {"en":"Bell and drum towers",    "fr":"Tours de la cloche et du tambour"},
    "B3.11": {"en":"Octagonal pavilion",      "fr":"Pavillon octogonal"},
    "B3.12": {"en":"Phương Đình",             "fr":"Phương Đình"},

    # B4
    "B4.1": {"en":"Emperor Lý Thánh Tông",   "fr":"Empereur Lý Thánh Tông"},
    "B4.2": {"en":"Emperor Lý Nhân Tông",    "fr":"Empereur Lý Nhân Tông"},
    "B4.3": {"en":"Emperor Lê Thánh Tông",   "fr":"Empereur Lê Thánh Tông"},
    "B4.5": {"en":"Master Chu Văn An",       "fr":"Maître Chu Văn An"},
    "B4.6": {"en":"Doctoral laureates",      "fr":"Lauréats doctoraux"},

    # B5
    "B5.1": {"en":"Confucius",  "fr":"Confucius"},
    "B5.2": {"en":"Yan Hui",    "fr":"Yan Hui"},
    "B5.3": {"en":"Zisi",       "fr":"Zisi"},
    "B5.4": {"en":"Zengzi",     "fr":"Zengzi"},
    "B5.5": {"en":"Mencius",    "fr":"Mencius"},

    # B6
    "B6.1": {"en":"Photo library", "fr":"Photothèque"},
    "B6.2": {"en":"Video",         "fr":"Vidéos"},

    # C
    "C1": {"en":"Permanent exhibitions",  "fr":"Expositions permanentes"},
    "C2": {"en":"Themed exhibitions",     "fr":"Expositions thématiques"},
    "C3": {"en":"Special exhibitions",    "fr":"Expositions spéciales"},
    "C1.1": {"en":"Imperial Academy – Vietnam's first national school",
             "fr":"Académie Impériale – Première école nationale du Vietnam"},
    "C1.2": {"en":"The source of learning",
             "fr":"À la source du savoir"},
    "C1.3": {"en":"Stone history",
             "fr":"L'histoire gravée dans la pierre"},

    # D
    "D1": {"en":"Events",                       "fr":"Événements"},
    "D2": {"en":"Heritage education",           "fr":"Éducation au patrimoine"},
    "D3": {"en":"Hands-on experiences",         "fr":"Expériences pratiques"},
    "D4": {"en":"Cultural & artistic events",   "fr":"Événements culturels et artistiques"},
    "D5": {"en":"Conferences & talks",          "fr":"Conférences et tables rondes"},
    "D6": {"en":"Diplomatic delegations",       "fr":"Délégations diplomatiques"},
    "D7": {"en":"Workshops",                    "fr":"Ateliers"},
    "D1.1": {"en":"Upcoming events",  "fr":"Événements à venir"},
    "D1.2": {"en":"Current events",   "fr":"Événements en cours"},

    # E
    "E1": {"en":"Night tour",            "fr":"Visite nocturne"},
    "E2": {"en":"Audio guide",           "fr":"Audioguide"},
    "E3": {"en":"Live guide",            "fr":"Guide sur place"},
    "E4": {"en":"Souvenirs",             "fr":"Souvenirs"},
    "E5": {"en":"Calligraphy experience","fr":"Calligraphie"},
    "E6": {"en":"Refreshments",          "fr":"Rafraîchissements"},
}

# ── Sub-text (descriptions shown on hub cards / page headers) ────────────────
SUBS = {
    "A": {"en":"Tickets, hours, rules, directions and amenities.",
          "fr":"Billets, horaires, règlement, accès et services."},
    "B": {"en":"History, sectors, architecture, figures, statues and library.",
          "fr":"Histoire, secteurs, architecture, personnages, statues et bibliothèque."},
    "C": {"en":"Permanent and themed displays plus special exhibitions.",
          "fr":"Expositions permanentes, thématiques et spéciales."},
    "D": {"en":"Events, heritage education, cultural experiences and workshops.",
          "fr":"Événements, éducation, expériences culturelles et ateliers."},
    "E": {"en":"Night tour, guides, souvenirs and on-site services.",
          "fr":"Visite nocturne, guides, souvenirs et services sur place."},

    "B1": {"en":"Foundation and growth across the dynasties.",
           "fr":"Fondation et évolution à travers les dynasties."},
    "B2": {"en":"The three main sectors of the site.",
           "fr":"Les trois secteurs principaux du site."},
    "B3": {"en":"Twelve emblematic structures within the complex.",
           "fr":"Douze ouvrages emblématiques du complexe."},
    "B4": {"en":"Emperors, scholars and laureates.",
           "fr":"Empereurs, lettrés et lauréats."},
    "B5": {"en":"Confucius, the Four Sages and the Confucian masters.",
           "fr":"Confucius, les Quatre Sages et les maîtres confucéens."},
    "B6": {"en":"Photo and video archives of the site.",
           "fr":"Archives photographiques et vidéo du site."},

    "C1": {"en":"Three permanent displays in the Thái Học sector.",
           "fr":"Trois expositions permanentes dans le secteur Thái Học."},
    "C2": {"en":"Themes that change throughout the year.",
           "fr":"Thèmes renouvelés tout au long de l'année."},
    "C3": {"en":"Partner exhibitions and special events.",
           "fr":"Expositions partenaires et événements spéciaux."},

    "D1": {"en":"Cultural events and festival schedule.",
           "fr":"Programme des événements culturels et fêtes."},
    "D2": {"en":"Programmes for pupils from kindergarten to high school.",
           "fr":"Programmes pour élèves de maternelle au lycée."},
    "D3": {"en":"Calligraphy, stelae rubbing and folk games.",
           "fr":"Calligraphie, estampage de stèles et jeux populaires."},
    "D4": {"en":"Traditional music, ca trù and arts performances.",
           "fr":"Musique traditionnelle, ca trù et arts de la scène."},
    "D5": {"en":"Academic talks on heritage, history and education.",
           "fr":"Conférences sur le patrimoine, l'histoire et l'éducation."},
    "D6": {"en":"Reception of diplomatic delegations and international guests.",
           "fr":"Accueil des délégations diplomatiques et invités internationaux."},
    "D7": {"en":"Creative, calligraphy and heritage workshops.",
           "fr":"Ateliers créatifs, calligraphie et patrimoine."},

    "E1": {"en":"The site at night, lit by artistic lighting.",
           "fr":"Le site la nuit, sous une mise en lumière artistique."},
    "E2": {"en":"Audio guide in 8 languages.",
           "fr":"Audioguide en 8 langues."},
    "E3": {"en":"Live guides in Vietnamese, English, French, Chinese.",
           "fr":"Guides en vietnamien, anglais, français, chinois."},
    "E4": {"en":"Books, prints and traditional handcrafts.",
           "fr":"Livres, estampes et artisanat traditionnel."},
    "E5": {"en":"Try Vietnamese calligraphy on site.",
           "fr":"Essayez la calligraphie vietnamienne sur place."},
    "E6": {"en":"Refreshment kiosks within the grounds.",
           "fr":"Kiosques de boissons dans l'enceinte."},
}

# ── Long content translations (slug-keyed). Best-effort, concise. ────────────
CONTENT = {
    "tham-quan": {
        "en": """
<h2>Opening hours</h2>
<table class="info-table">
  <tr><th>Summer (Apr – Oct)</th><td>07:30 – 18:00 (daily)</td></tr>
  <tr><th>Winter (Nov – Mar)</th><td>08:00 – 17:00 (daily)</td></tr>
  <tr><th>Ticket counter</th><td>Closes 30 minutes before site closing</td></tr>
</table>
<h2>Ticket prices</h2>
<div class="price-table">
  <div class="price-row"><div class="price-cat"><p>Adult (16+)</p></div><p class="price-val">30,000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Pupils & students (with ID)</p></div><p class="price-val">15,000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Senior (60+)</p></div><p class="price-val">15,000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Children under 15</p></div><p class="price-val">Free</p></div>
</div>
<h2>Getting there</h2>
<table class="info-table">
  <tr><th>Address</th><td>58 Quoc Tu Giam St., Van Mieu Ward, Dong Da District, Hanoi</td></tr>
  <tr><th>Bus</th><td>Lines 02, 23, 38 — stop at Văn Miếu</td></tr>
  <tr><th>Parking</th><td>Cars: Văn Miếu street · Motorbikes/bicycles: Vườn Giám</td></tr>
</table>
<h2>Visitor rules</h2>
<ol>
  <li>Visitors must purchase and present a valid ticket.</li>
  <li>Protect the site and keep it clean. Do not touch, write or draw on artefacts, stelae or buildings. Do not step on lawns, pick flowers or break branches.</li>
  <li>Comply with fire-safety regulations. Smoking is prohibited on site.</li>
  <li>Wear respectful attire when entering shrines. Maintain quiet in sacred areas.</li>
  <li>Superstitious practices, gambling and fraud are strictly forbidden.</li>
  <li>Visitors are legally responsible for any damage they cause.</li>
  <li>Security may end the visit of any rule-breaker.</li>
  <li>Feedback: 024.3747.1322 / 024.3211.5793.</li>
</ol>
<h2>On-site amenities</h2>
<ul>
  <li>Car park (Văn Miếu street) and motorbike/bicycle park (Vườn Giám)</li>
  <li>Café and refreshment kiosks within the grounds</li>
  <li>Souvenir shop near the exit</li>
  <li>Free Wi-Fi, benches, public restrooms</li>
</ul>
""",
        "fr": """
<h2>Heures d'ouverture</h2>
<table class="info-table">
  <tr><th>Été (avr. – oct.)</th><td>07h30 – 18h00 (tous les jours)</td></tr>
  <tr><th>Hiver (nov. – mars)</th><td>08h00 – 17h00 (tous les jours)</td></tr>
  <tr><th>Billetterie</th><td>Ferme 30 min avant la fermeture du site</td></tr>
</table>
<h2>Tarifs</h2>
<div class="price-table">
  <div class="price-row"><div class="price-cat"><p>Adulte (16 ans et +)</p></div><p class="price-val">30 000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Élèves & étudiants (carte)</p></div><p class="price-val">15 000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Senior (60 ans et +)</p></div><p class="price-val">15 000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Enfants -15 ans</p></div><p class="price-val">Gratuit</p></div>
</div>
<h2>Accès</h2>
<table class="info-table">
  <tr><th>Adresse</th><td>58 rue Quoc Tu Giam, Quartier Van Mieu, District Dong Da, Hanoï</td></tr>
  <tr><th>Bus</th><td>Lignes 02, 23, 38 — arrêt Văn Miếu</td></tr>
  <tr><th>Parking</th><td>Voitures : rue Văn Miếu · Motos/vélos : Vườn Giám</td></tr>
</table>
<h2>Règlement de visite</h2>
<ol>
  <li>Les visiteurs doivent acheter et présenter un billet valide.</li>
  <li>Protégez le site et gardez-le propre. Ne touchez pas, n'écrivez pas et ne dessinez pas sur les œuvres, les stèles ni les bâtiments.</li>
  <li>Respectez les consignes de sécurité incendie. Il est interdit de fumer.</li>
  <li>Tenue correcte exigée dans les lieux de culte. Restez silencieux dans les espaces sacrés.</li>
  <li>Les pratiques superstitieuses, les jeux d'argent et la fraude sont interdits.</li>
  <li>Les visiteurs sont responsables des dommages causés.</li>
  <li>La sécurité peut mettre fin à la visite en cas de manquement.</li>
  <li>Contact : 024.3747.1322 / 024.3211.5793.</li>
</ol>
<h2>Services sur place</h2>
<ul>
  <li>Parking voitures (rue Văn Miếu) et motos/vélos (Vườn Giám)</li>
  <li>Café et kiosques de boissons dans l'enceinte</li>
  <li>Boutique de souvenirs à la sortie</li>
  <li>Wi-Fi gratuit, bancs, toilettes publiques</li>
</ul>
""",
    },

    # ── B1. History ──────────────────────────────────────────────────────────
    "ve-di-tich/lich-su/thoi-ly": {
        "en": """
<p>The Temple of Literature was founded under King Lý Thánh Tông in the year Canh Tuất, second year of the Thần Vũ era (1070), as a place of worship for Confucius, the Duke of Zhou and the Four Sages. This marked the beginning of formal Confucian education in Đại Việt.</p>
<h2>Key events</h2>
<ul>
  <li><strong>1070</strong> — King Lý Thánh Tông establishes the Temple of Literature</li>
  <li><strong>1076</strong> — King Lý Nhân Tông founds the Imperial Academy — Vietnam's first university</li>
  <li><strong>1156</strong> — King Lý Anh Tông restores the Temple, dedicating it solely to Confucius</li>
</ul>
<p>The Imperial Academy was initially reserved for princes and the nobility. In 1253, King Trần Thái Tông opened it to talented commoners as well.</p>
""",
        "fr": """
<p>Le Temple de la Littérature fut fondé sous le règne du roi Lý Thánh Tông, en l'an Canh Tuất, deuxième année de l'ère Thần Vũ (1070), pour honorer Confucius, le duc de Zhou et les Quatre Sages. Cet événement marque l'acte de naissance de l'enseignement confucéen officiel à Đại Việt.</p>
<h2>Événements clés</h2>
<ul>
  <li><strong>1070</strong> — Le roi Lý Thánh Tông fonde le Temple de la Littérature</li>
  <li><strong>1076</strong> — Le roi Lý Nhân Tông crée l'Académie Impériale — première université du Vietnam</li>
  <li><strong>1156</strong> — Le roi Lý Anh Tông restaure le Temple, entièrement dédié à Confucius</li>
</ul>
<p>L'Académie Impériale était initialement réservée aux princes et à la noblesse. En 1253, le roi Trần Thái Tông l'ouvrit aux roturiers talentueux.</p>
""",
    },

    "ve-di-tich/lich-su/thoi-tran": {
        "en": """
<p>During the Trần dynasty (1225–1400), the Temple of Literature and Imperial Academy continued to grow. In 1253, King Trần Thái Tông expanded the Academy, renaming it the National Academy of Learning and opening it to talented commoners.</p>
<h2>Educational reforms</h2>
<ul>
  <li><strong>1253</strong> — The Imperial Academy is renamed the National Academy; commoners admitted</li>
  <li><strong>1272</strong> — Lê Văn Hưu completes the <em>Đại Việt sử ký</em> — Vietnam's first official chronicle</li>
  <li><strong>1370</strong> — Grand Preceptor Chu Văn An is enshrined at the Temple after his death</li>
</ul>
<p>Chu Văn An — the great teacher of the Trần era — was the first Vietnamese scholar to be co-enshrined at the Temple alongside Confucius and the Four Sages.</p>
""",
        "fr": """
<p>Sous la dynastie Trần (1225–1400), le Temple de la Littérature et l'Académie Impériale poursuivirent leur essor. En 1253, le roi Trần Thái Tông agrandit l'Académie, la renomma Académie nationale du savoir et l'ouvrit aux roturiers méritants.</p>
<h2>Réformes de l'éducation</h2>
<ul>
  <li><strong>1253</strong> — Renommée Académie nationale ; admission des roturiers</li>
  <li><strong>1272</strong> — Lê Văn Hưu achève le <em>Đại Việt sử ký</em> — première chronique officielle du Vietnam</li>
  <li><strong>1370</strong> — Le Grand Précepteur Chu Văn An est consacré au Temple après sa mort</li>
</ul>
<p>Chu Văn An — grand maître de l'ère Trần — fut le premier lettré vietnamien à être co-enshrined au Temple aux côtés de Confucius et des Quatre Sages.</p>
""",
    },

    "ve-di-tich/lich-su/thoi-le": {
        "en": """
<p>After expelling the Ming occupiers (1428), the Lê dynasty officially re-established and rebuilt the Temple of Literature – Imperial Academy on a grander scale. The Lê period was the golden age of Confucian civil-service examinations in Vietnam.</p>
<h2>The 82 Doctoral Stelae</h2>
<p>From 1484, by order of King Lê Thánh Tông, the Doctoral Stelae began to be erected. Over 300 years (1484–1780), 82 stone stelae were inscribed with the names of 1,304 Doctors of Letters across 82 Palace Examinations.</p>
<h2>Key milestones</h2>
<ul>
  <li><strong>1442</strong> — First Palace Examination organised by the Lê state</li>
  <li><strong>1484</strong> — King Lê Thánh Tông orders the erection of the Doctoral Stelae</li>
  <li><strong>1645</strong> — The complex reaches near-complete form under the Later Lê</li>
  <li><strong>1780</strong> — The last Doctoral Stele is erected (Cảnh Hưng 40 examination)</li>
</ul>
""",
        "fr": """
<p>Après l'expulsion des occupants Ming (1428), la dynastie Lê reconstruisit le Temple de la Littérature – Académie Impériale à plus grande échelle. La période Lê fut l'âge d'or des examens mandarinaux confucéens au Vietnam.</p>
<h2>Les 82 stèles doctorales</h2>
<p>À partir de 1484, par décret du roi Lê Thánh Tông, les stèles doctorales commencèrent à être érigées. Sur 300 ans (1484–1780), 82 stèles de pierre furent gravées avec les noms de 1 304 docteurs à l'issue de 82 examens palatins.</p>
<h2>Jalons historiques</h2>
<ul>
  <li><strong>1442</strong> — Premier examen palatin organisé par l'État Lê</li>
  <li><strong>1484</strong> — Le roi Lê Thánh Tông ordonne l'érection des stèles doctorales</li>
  <li><strong>1645</strong> — Le complexe atteint sa forme quasi définitive sous les Lê tardifs</li>
  <li><strong>1780</strong> — Dernière stèle érigée (examen Cảnh Hưng 40)</li>
</ul>
""",
    },

    "ve-di-tich/lich-su/thoi-nguyen": {
        "en": """
<p>Under the Nguyễn dynasty (1802–1945), Thăng Long was no longer the capital. The Hanoi Imperial Academy gradually lost its educational role — the Nguyễn dynasty's own Imperial Academy was established in Huế. The Hanoi Temple of Literature became primarily a place of worship.</p>
<h2>Architectural transformations</h2>
<ul>
  <li><strong>1805</strong> — The Khuê Văn Pavilion is built under Emperor Gia Long</li>
  <li><strong>1863</strong> — Major restoration under Emperor Tự Đức</li>
  <li><strong>1947</strong> — French bombing partially destroys the old Imperial Academy buildings</li>
  <li><strong>1962</strong> — The site is classified as a National Historical and Cultural Monument</li>
  <li><strong>2010</strong> — UNESCO inscribes the 82 Doctoral Stelae on the Memory of the World Register</li>
  <li><strong>2014</strong> — Designated a Special National Heritage Site</li>
</ul>
""",
        "fr": """
<p>Sous la dynastie Nguyễn (1802–1945), Thăng Long n'était plus la capitale. L'Académie Impériale de Hanoï perdit progressivement sa vocation éducative — la nouvelle académie des Nguyễn fut établie à Huế. Le Temple de la Littérature de Hanoï devint essentiellement un lieu de culte.</p>
<h2>Transformations architecturales</h2>
<ul>
  <li><strong>1805</strong> — Construction du Pavillon Khuê Văn sous l'Empereur Gia Long</li>
  <li><strong>1863</strong> — Grande restauration sous l'Empereur Tự Đức</li>
  <li><strong>1947</strong> — Bombardements français détruisant partiellement les anciens bâtiments</li>
  <li><strong>1962</strong> — Classement en monument historique et culturel national</li>
  <li><strong>2010</strong> — L'UNESCO inscrit les 82 stèles doctorales au registre Mémoire du monde</li>
  <li><strong>2014</strong> — Classé Site du patrimoine national spécial</li>
</ul>
""",
    },

    # ── B2. Site sectors ──────────────────────────────────────────────────────
    "ve-di-tich/phan-khu/noi-tu": {
        "en": """
<p>The Inner Sanctuary is the main area of the site, running along a North–South axis from the Văn Miếu Gate to the Thái Học sector. It comprises five successive courtyards, each with its own symbolic meaning within the Confucian system.</p>
<h2>Five courtyards</h2>
<ol>
  <li>First courtyard: from the Văn Miếu Gate to the Đại Trung Gate</li>
  <li>Second courtyard: from the Đại Trung Gate to the Khuê Văn Pavilion</li>
  <li>Third courtyard: Khuê Văn Pavilion – Doctoral Stele Garden – Thiên Quang Well</li>
  <li>Fourth courtyard: Đại Thành Gate – main worship area (Ceremonial Hall and Upper Shrine)</li>
  <li>Fifth courtyard: Thái Học sector</li>
</ol>
""",
        "fr": """
<p>L'Enceinte intérieure est la zone principale du site, orientée Nord–Sud depuis la Porte Văn Miếu jusqu'au secteur Thái Học. Elle se compose de cinq cours successives, chacune dotée d'une signification symbolique propre dans le système confucéen.</p>
<h2>Les cinq cours</h2>
<ol>
  <li>Première cour : de la Porte Văn Miếu à la Porte Đại Trung</li>
  <li>Deuxième cour : de la Porte Đại Trung au Pavillon Khuê Văn</li>
  <li>Troisième cour : Pavillon Khuê Văn – Jardin des stèles – Puits Thiên Quang</li>
  <li>Quatrième cour : Porte Đại Thành – espace de culte (Salle des cérémonies et Sanctuaire supérieur)</li>
  <li>Cinquième cour : Secteur Thái Học</li>
</ol>
""",
    },

    "ve-di-tich/phan-khu/vuon-giam": {
        "en": """
<p>Vườn Giám is a tree-lined garden to the left of the Inner Sanctuary, providing an open green space and housing several ancillary structures such as the Octagonal Pavilion.</p>
<p>It also serves as the motorbike and bicycle parking area for visitors.</p>
<h2>Highlights</h2>
<ul>
  <li>Ancient trees providing year-round shade</li>
  <li>The Octagonal Pavilion — a distinctive eight-sided structure</li>
  <li>Outdoor venue for cultural events</li>
</ul>
""",
        "fr": """
<p>Le Jardin Giám est un parc arboré situé à gauche de l'Enceinte intérieure, offrant un espace vert ouvert et abritant plusieurs structures annexes comme le Pavillon octogonal.</p>
<p>Il sert également de parking pour les motos et vélos des visiteurs.</p>
<h2>À voir</h2>
<ul>
  <li>Arbres centenaires offrant de l'ombre toute l'année</li>
  <li>Le Pavillon octogonal — architecture octogonale caractéristique</li>
  <li>Espace de plein air pour des événements culturels</li>
</ul>
""",
    },

    "ve-di-tich/phan-khu/ho-van": {
        "en": """
<p>Văn Lake lies in front of the Văn Miếu Gate, separated from the Inner Sanctuary by Quốc Tử Giám Street. At its centre is Kim Châu islet, on which stands the Phán Thuỷ pavilion.</p>
<h2>Significance</h2>
<ul>
  <li>According to feng shui, Văn Lake is the mirror of wisdom reflecting the Temple of Literature</li>
  <li>Annual venue for the Poetry Festival and Calligraphy Fair during the Lunar New Year</li>
  <li>Outdoor space for cultural events</li>
</ul>
""",
        "fr": """
<p>Le Lac Văn se trouve devant la Porte Văn Miếu, séparé de l'Enceinte intérieure par la rue Quốc Tử Giám. En son centre se dresse l'îlot Kim Châu, sur lequel se trouve le pavillon Phán Thuỷ.</p>
<h2>Signification</h2>
<ul>
  <li>Selon le feng shui, le Lac Văn est le miroir de la sagesse reflétant le Temple</li>
  <li>Lieu annuel du Festival de poésie et de la Foire à la calligraphie pour le Nouvel An lunaire</li>
  <li>Espace de plein air pour des événements culturels</li>
</ul>
""",
    },

    # ── B3. Architecture ──────────────────────────────────────────────────────
    "ve-di-tich/kien-truc/bia-ha-ma": {
        "en": """
<p>The Hạ Mã steles stand on either side of the Văn Miếu Gate, bearing the Chinese characters "下馬" (Hạ Mã — Dismount). They required everyone, including the emperor and court officials, to dismount from their horses as a sign of reverence for Confucius and the Imperial Academy.</p>
<h2>Features</h2>
<ul>
  <li>Two ancient stone steles flanking the entrance gate</li>
  <li>Inscribed with the Chinese characters "Hạ Mã" — Dismount</li>
  <li>Symbol of the ethos of "venerating teachers and honouring learning"</li>
</ul>
""",
        "fr": """
<p>Les stèles Hạ Mã se dressent de part et d'autre de la Porte Văn Miếu, gravées des caractères chinois « 下馬 » (Hạ Mã — Descendre de cheval). Elles imposaient à tous — y compris l'Empereur et les mandarins — de mettre pied à terre en signe de respect envers Confucius et l'Académie Impériale.</p>
<h2>Caractéristiques</h2>
<ul>
  <li>Deux stèles de pierre antiques flanquant le portail d'entrée</li>
  <li>Inscrites des caractères « Hạ Mã » — Descendre de cheval</li>
  <li>Symbole du principe « Révérer les maîtres, honorer le savoir »</li>
</ul>
""",
    },

    "ve-di-tich/kien-truc/cong-van-mieu": {
        "en": """
<p>The Văn Miếu Gate (Văn Miếu Môn) is the main southern gate, a triple-arched tam quan with two tiers of curved roofs. Built during the Lê dynasty and restored many times over the centuries.</p>
<h2>Architectural features</h2>
<ul>
  <li>Triple-arched gateway with two tiers of curved roofs</li>
  <li>Inscribed with four Chinese characters "Văn Miếu Môn"</li>
  <li>Flanked by four tall ceremonial pillars</li>
  <li>The most recognisable symbol of the site</li>
</ul>
""",
        "fr": """
<p>La Porte Văn Miếu (Văn Miếu Môn) est le portail principal au sud, un tam quan à trois ouvertures avec deux rangées de toits incurvés. Construite sous la dynastie Lê et restaurée à de nombreuses reprises.</p>
<h2>Caractéristiques architecturales</h2>
<ul>
  <li>Triple portail à deux niveaux de toits incurvés</li>
  <li>Inscrite des quatre caractères chinois « Văn Miếu Môn »</li>
  <li>Flanquée de quatre hautes colonnes cérémonielles</li>
  <li>Symbole le plus emblématique du site</li>
</ul>
""",
    },

    "ve-di-tich/kien-truc/cong-dai-trung": {
        "en": """
<p>The Đại Trung Gate is the second gateway, separating the first and second courtyards. It has three bays with a traditional curved roof.</p>
<p>On either side are two smaller gates: Đạt Tài (Achieve Talent, on the left) and Thành Đức (Attain Virtue, on the right) — symbolising the two core qualities of the ideal Confucian gentleman.</p>
""",
        "fr": """
<p>La Porte Đại Trung est le deuxième portail, séparant la première et la deuxième cour. Elle comporte trois travées surmontées d'un toit traditionnel incurvé.</p>
<p>De chaque côté se trouvent deux portails secondaires : Đạt Tài (Atteindre le Talent, à gauche) et Thành Đức (Atteindre la Vertu, à droite) — symbolisant les deux qualités essentielles du gentleman confucéen.</p>
""",
    },

    "ve-di-tich/kien-truc/khue-van-cac": {
        "en": """
<p>The Khuê Văn Pavilion was built in 1805 under Emperor Gia Long. It is the iconic symbol of the Temple of Literature – Imperial Academy and the cultural emblem of Hanoi.</p>
<h2>Distinctive architecture</h2>
<ul>
  <li>Two-storey square pavilion with eight curved roof sections</li>
  <li>Lower storey: four square brick pillars</li>
  <li>Upper storey: four circular windows — symbolising the radiant star of literature</li>
  <li>Inscribed plaque with four Chinese characters "Khuê Văn Các"</li>
</ul>
<p>In 2012, the Khuê Văn Pavilion was chosen as the official symbol of the capital Hanoi.</p>
""",
        "fr": """
<p>Le Pavillon Khuê Văn fut construit en 1805 sous l'Empereur Gia Long. Il est le symbole iconique du Temple de la Littérature – Académie Impériale et l'emblème culturel de Hanoï.</p>
<h2>Architecture distinctive</h2>
<ul>
  <li>Pavillon carré à deux étages avec huit sections de toiture incurvée</li>
  <li>Étage inférieur : quatre piliers carrés en brique</li>
  <li>Étage supérieur : quatre fenêtres circulaires — symbolisant l'étoile rayonnante des lettres</li>
  <li>Plaque inscrite des quatre caractères chinois « Khuê Văn Các »</li>
</ul>
<p>En 2012, le Pavillon Khuê Văn a été choisi comme symbole officiel de la capitale Hanoï.</p>
""",
    },

    "ve-di-tich/kien-truc/nha-che-bia": {
        "en": """
<p>Two rows of stele shelters flank Thiên Quang Well, each housing 41 Doctoral Stelae — 82 in total. The shelters were built to protect the stelae from rain and sun, with double-tiered tiled roofs.</p>
<h2>The 82 Doctoral Stelae</h2>
<ul>
  <li>Erected from 1484 to 1780 — spanning 300 years</li>
  <li>Recording 1,304 Doctors of Letters across 82 Palace Examinations</li>
  <li>2010 — UNESCO Memory of the World inscription</li>
  <li>2015 — Designated a National Treasure</li>
</ul>
""",
        "fr": """
<p>Deux rangées d'abris pour stèles flanquent le Puits Thiên Quang, chacune abritant 41 stèles doctorales — 82 au total. Ces abris furent construits pour protéger les stèles de la pluie et du soleil, avec des toits à double rangée de tuiles.</p>
<h2>Les 82 stèles doctorales</h2>
<ul>
  <li>Érigées de 1484 à 1780 — sur 300 ans</li>
  <li>Commémorant 1 304 docteurs à travers 82 examens palatins</li>
  <li>2010 — Inscription au registre Mémoire du monde de l'UNESCO</li>
  <li>2015 — Classées Trésor national</li>
</ul>
""",
    },

    "ve-di-tich/kien-truc/cong-dai-thanh": {
        "en": """
<p>The Đại Thành Gate (Great Achievement Gate) leads into the main worship area — the Ceremonial Hall and the Upper Shrine. A triple-arched gateway with palatial curved roofs.</p>
<h2>Meaning of the name</h2>
<p>"Đại Thành" (Great Achievement) is taken from a passage by Mencius praising Confucius: "Confucius is the great synthesis" — the one who distilled the wisdom of all the Sages before him.</p>
""",
        "fr": """
<p>La Porte Đại Thành (Porte de la Grande Réalisation) mène à l'espace de culte principal — la Salle des cérémonies et le Sanctuaire supérieur. Triple portail à toits palatins incurvés.</p>
<h2>Sens du nom</h2>
<p>« Đại Thành » (Grande Réalisation) est tiré d'un passage de Mencius louant Confucius : « Confucius est la grande synthèse » — celui qui a distillé la sagesse de tous les Saints qui l'ont précédé.</p>
""",
    },

    "ve-di-tich/kien-truc/bai-duong": {
        "en": """
<p>The Ceremonial Hall (Đại Bái Đường) is the principal building in the worship complex, where rituals honouring Confucius and the Four Sages are performed. A wide nine-bay hall with yin-yang interlocking tiles.</p>
<h2>Shrine layout</h2>
<ul>
  <li>Central bay: main altar</li>
  <li>Side bays: altars for the Four Sages — Yan Hui, Zengzi, Zisi, Mencius</li>
  <li>Innermost hall: the Upper Shrine housing the statue of Confucius</li>
</ul>
""",
        "fr": """
<p>La Salle des cérémonies (Đại Bái Đường) est le bâtiment principal du complexe de culte, où se déroulent les rites en l'honneur de Confucius et des Quatre Sages. Vaste salle à neuf travées couverte de tuiles yin-yang imbriquées.</p>
<h2>Organisation du sanctuaire</h2>
<ul>
  <li>Travée centrale : autel principal</li>
  <li>Travées latérales : autels des Quatre Sages — Yan Hui, Zengzi, Zisi, Mencius</li>
  <li>Hall intérieur : le Sanctuaire supérieur abritant la statue de Confucius</li>
</ul>
""",
    },

    "ve-di-tich/kien-truc/cong-thai-hoc": {
        "en": """
<p>The Thái Học Gate leads into the Thái Học sector — the rearmost part of the site, which was the original location of the Imperial Academy.</p>
""",
        "fr": """
<p>La Porte Thái Học conduit au secteur Thái Học — la partie la plus reculée du site, qui était l'emplacement originel de l'Académie Impériale.</p>
""",
    },

    "ve-di-tich/kien-truc/thai-hoc": {
        "en": """
<p>The Thái Học sector was rebuilt in 2000 on the foundations of the old Imperial Academy. The complex includes:</p>
<ul>
  <li><strong>Front Hall (Tiền Đường)</strong> — enshrining the three kings who contributed to the Temple (Lý Thánh Tông, Lý Nhân Tông, Lê Thánh Tông) and Grand Preceptor Chu Văn An</li>
  <li><strong>Rear Hall (Hậu Đường)</strong> — permanent exhibition space</li>
  <li><strong>East and West Wings (Đông Vũ – Tây Vũ)</strong> — exhibition and event spaces</li>
</ul>
""",
        "fr": """
<p>Le secteur Thái Học a été reconstruit en 2000 sur les fondations de l'ancienne Académie Impériale. Il comprend :</p>
<ul>
  <li><strong>Salle avant (Tiền Đường)</strong> — consacrée aux trois rois bienfaiteurs du Temple (Lý Thánh Tông, Lý Nhân Tông, Lê Thánh Tông) et au Grand Précepteur Chu Văn An</li>
  <li><strong>Salle arrière (Hậu Đường)</strong> — espace d'exposition permanente</li>
  <li><strong>Ailes est et ouest (Đông Vũ – Tây Vũ)</strong> — espaces d'exposition et d'événements</li>
</ul>
""",
    },

    "ve-di-tich/kien-truc/nha-chuong-trong": {
        "en": """
<p>On either side of the second courtyard stand two symmetrical towers: the Bell Tower (left) and the Drum Tower (right). This bell-and-drum architecture is traditional in Vietnamese temples and shrines.</p>
""",
        "fr": """
<p>De part et d'autre de la deuxième cour se dressent deux tours symétriques : la Tour de la Cloche (à gauche) et la Tour du Tambour (à droite). Cette architecture cloche-tambour est traditionnelle dans les temples et sanctuaires vietnamiens.</p>
""",
    },

    "ve-di-tich/kien-truc/nha-bat-giac": {
        "en": """
<p>The Octagonal Pavilion is a distinctive eight-sided structure set within the Vườn Giám garden. Its octagonal roof and eight supporting columns create an open, airy space.</p>
""",
        "fr": """
<p>Le Pavillon octogonal est une structure à huit pans caractéristique, installée dans le Jardin Giám. Son toit octogonal et ses huit colonnes portantes créent un espace ouvert et aéré.</p>
""",
    },

    "ve-di-tich/kien-truc/phuong-dinh": {
        "en": """
<p>The Phương Đình is a small square pavilion within the site's grounds, serving as a rest point and a place to enjoy the scenery.</p>
""",
        "fr": """
<p>Le Phương Đình est un petit pavillon carré dans l'enceinte du site, servant de lieu de repos et de contemplation du paysage.</p>
""",
    },

    # ── B4. Eminent figures ───────────────────────────────────────────────────
    "ve-di-tich/danh-nhan/vua-ly-thanh-tong": {
        "en": """
<p>Lý Thánh Tông (1023–1072) was the third king of the Lý dynasty. In the year Canh Tuất (1070), he founded the Temple of Literature — laying the foundation for formal Confucian education in Đại Việt.</p>
<h2>Contributions</h2>
<ul>
  <li>Founded the Temple of Literature in 1070 — enshrining Confucius, the Duke of Zhou and the Four Sages</li>
  <li>Established the basis for formal Confucian scholarship</li>
  <li>Expanded the territory and consolidated the Đại Việt state</li>
</ul>
""",
        "fr": """
<p>Lý Thánh Tông (1023–1072) était le troisième roi de la dynastie Lý. En l'an Canh Tuất (1070), il fonda le Temple de la Littérature — posant les bases de l'éducation confucéenne officielle à Đại Việt.</p>
<h2>Contributions</h2>
<ul>
  <li>Fondation du Temple de la Littérature en 1070 — consacré à Confucius, au Duc de Zhou et aux Quatre Sages</li>
  <li>Établissement des fondements de l'érudition confucéenne officielle</li>
  <li>Expansion territoriale et consolidation de l'État Đại Việt</li>
</ul>
""",
    },

    "ve-di-tich/danh-nhan/vua-ly-nhan-tong": {
        "en": """
<p>Lý Nhân Tông (1066–1128) was the son of Lý Thánh Tông. In 1076, he founded the Imperial Academy within the Temple of Literature grounds — Vietnam's first university.</p>
<h2>Contributions</h2>
<ul>
  <li>Founded the Imperial Academy in 1076 — Vietnam's first university</li>
  <li>Introduced the Three-Round Examination in 1075 — the first royal examination to select talented officials</li>
  <li>Developed education and scholarship during the Lý dynasty</li>
</ul>
""",
        "fr": """
<p>Lý Nhân Tông (1066–1128) était le fils de Lý Thánh Tông. En 1076, il fonda l'Académie Impériale dans l'enceinte du Temple de la Littérature — première université du Vietnam.</p>
<h2>Contributions</h2>
<ul>
  <li>Fondation de l'Académie Impériale en 1076 — première université du Vietnam</li>
  <li>Instauration de l'examen en trois épreuves en 1075 — premier examen royal pour sélectionner les fonctionnaires</li>
  <li>Développement de l'éducation et de la culture savante sous la dynastie Lý</li>
</ul>
""",
    },

    "ve-di-tich/danh-nhan/vua-le-thanh-tong": {
        "en": """
<p>Lê Thánh Tông (1442–1497) was the fifth king of the Early Lê dynasty — one of the most outstanding rulers in Vietnamese history.</p>
<h2>Contributions to the Temple of Literature</h2>
<ul>
  <li>1484 — Issued the royal edict to erect Doctoral Stelae at the Temple</li>
  <li>Vigorously promoted Confucian scholarship and the examination system</li>
  <li>Promulgated the Hồng Đức Code — Vietnam's first comprehensive legal code</li>
  <li>Expanded the territory southward</li>
</ul>
""",
        "fr": """
<p>Lê Thánh Tông (1442–1497) était le cinquième roi de la première dynastie Lê — l'un des souverains les plus remarquables de l'histoire vietnamienne.</p>
<h2>Contributions au Temple de la Littérature</h2>
<ul>
  <li>1484 — Édit royal ordonnant l'érection des stèles doctorales au Temple</li>
  <li>Promotion vigoureuse de l'érudition confucéenne et du système d'examens</li>
  <li>Promulgation du Code Hồng Đức — premier code juridique complet du Vietnam</li>
  <li>Expansion territoriale vers le sud</li>
</ul>
""",
    },

    "ve-di-tich/danh-nhan/chu-van-an": {
        "en": """
<p>Chu Văn An (1292–1370) was the most eminent scholar and teacher of the Trần era, widely regarded as the "founding father" of Vietnamese education. He held the position of Grand Preceptor of the Imperial Academy, overseeing national education.</p>
<h2>Career</h2>
<ul>
  <li>Grand Preceptor of the Imperial Academy — taught the crown prince and court officials</li>
  <li>Authored the "Seven-Beheading Memorial" — petitioning for the execution of seven corrupt ministers</li>
  <li>Author of "Concise Explanation of the Four Books" — a commentary on the Confucian classics</li>
</ul>
<p>After his death, Chu Văn An was co-enshrined at the Temple of Literature alongside Confucius and the Four Sages — a rare honour for a Vietnamese person.</p>
""",
        "fr": """
<p>Chu Văn An (1292–1370) fut le plus éminent lettré et enseignant de l'ère Trần, largement considéré comme le « père fondateur » de l'éducation vietnamienne. Il occupa le poste de Grand Précepteur de l'Académie Impériale, supervisant l'éducation nationale.</p>
<h2>Carrière</h2>
<ul>
  <li>Grand Précepteur de l'Académie Impériale — enseigna au prince héritier et aux mandarins</li>
  <li>Auteur du « Mémorial des Sept Décapitations » — demandant l'exécution de sept ministres corrompus</li>
  <li>Auteur d'un commentaire concis sur les Quatre Livres confucéens</li>
</ul>
<p>Après sa mort, Chu Văn An fut consacré au Temple de la Littérature aux côtés de Confucius et des Quatre Sages — un honneur rare pour un Vietnamien.</p>
""",
    },

    "ve-di-tich/danh-nhan/khoa-bang": {
        "en": """
<p>Over 300 years (1442–1779), 1,304 Doctors of Letters who passed 82 Palace Examinations had their names inscribed on 82 stone stelae in the Stele Garden. This is an invaluable heritage of the human capital and intellectual culture of Đại Việt.</p>
<h2>Notable laureates</h2>
<ul>
  <li><strong>Nguyễn Trãi</strong> — passed the Thai Hoc Sinh examination in 1400; national hero and great cultural figure</li>
  <li><strong>Lê Quý Đôn</strong> — Doctor of Letters 1752; greatest polymath of the 18th century</li>
  <li><strong>Nguyễn Bỉnh Khiêm</strong> — First Laureate 1535; the prophetic sage known as Trạng Trình</li>
  <li><strong>Ngô Sĩ Liên</strong> — Doctor of Letters 1442; compiler of the <em>Complete Annals of Đại Việt</em></li>
</ul>
<h2>Distinguished scholarly clans</h2>
<ul>
  <li>Nguyễn Quán Nho clan (Thanh Hoá)</li>
  <li>Phan Huy clan (Hà Tĩnh)</li>
  <li>Ngô Thì clan (Hanoi)</li>
</ul>
""",
        "fr": """
<p>Sur 300 ans (1442–1779), 1 304 docteurs ayant réussi 82 examens palatins ont vu leurs noms gravés sur 82 stèles de pierre dans le Jardin des stèles. C'est un patrimoine inestimable du capital humain et de la culture intellectuelle de Đại Việt.</p>
<h2>Lauréats notables</h2>
<ul>
  <li><strong>Nguyễn Trãi</strong> — Reçu à l'examen Thai Hoc Sinh en 1400 ; héros national et grande figure culturelle</li>
  <li><strong>Lê Quý Đôn</strong> — Docteur en 1752 ; plus grand érudit du XVIIIe siècle</li>
  <li><strong>Nguyễn Bỉnh Khiêm</strong> — Premier lauréat en 1535 ; le sage prophète Trạng Trình</li>
  <li><strong>Ngô Sĩ Liên</strong> — Docteur en 1442 ; compilateur des <em>Annales complètes de Đại Việt</em></li>
</ul>
<h2>Clans lettrés illustres</h2>
<ul>
  <li>Clan Nguyễn Quán Nho (Thanh Hoá)</li>
  <li>Clan Phan Huy (Hà Tĩnh)</li>
  <li>Clan Ngô Thì (Hanoï)</li>
</ul>
""",
    },

    # ── B5. Statues ───────────────────────────────────────────────────────────
    "ve-di-tich/tuong-tho/khong-tu": {
        "en": """
<p>Confucius (孔子, 551–479 BC) was the greatest thinker and educator of ancient China — founder of Confucianism. The statue of Confucius occupies the central position of the Upper Shrine in the Đại Thành complex.</p>
<h2>Position at the Temple of Literature</h2>
<ul>
  <li>Statue placed in the Upper Shrine (Đại Thành Điện) — the central position</li>
  <li>Principal object of worship at the Temple since 1070</li>
  <li>The Confucius Ritual (Tế Khổng) is held annually in Spring and Autumn</li>
</ul>
""",
        "fr": """
<p>Confucius (孔子, 551–479 av. J.-C.) était le plus grand penseur et éducateur de la Chine antique — fondateur du confucianisme. La statue de Confucius occupe la position centrale du Sanctuaire supérieur dans le complexe Đại Thành.</p>
<h2>Position au Temple de la Littérature</h2>
<ul>
  <li>Statue placée dans le Sanctuaire supérieur (Đại Thành Điện) — position centrale</li>
  <li>Objet principal de culte au Temple depuis 1070</li>
  <li>Le Rituel de Confucius (Tế Khổng) est célébré chaque année au printemps et en automne</li>
</ul>
""",
    },

    "ve-di-tich/tuong-tho/nhan-tu": {
        "en": """
<p>Yan Hui (顔子) — courtesy name Ziyuan — was Confucius's most gifted disciple. He is honoured as the Restored Sage, one of the Four Sages enshrined alongside Confucius.</p>
<p>Yan Hui was renowned for his love of learning and simple lifestyle. Confucius praised him: "How admirable Hui is!" (Hiền tài thay, Hồi vậy!)</p>
""",
        "fr": """
<p>Yan Hui (顔子) — nom de courtoisie Ziyuan — était le disciple le plus doué de Confucius. Il est honoré sous le titre de Sage Restauré, l'un des Quatre Sages consacrés aux côtés de Confucius.</p>
<p>Yan Hui était réputé pour son amour de l'apprentissage et sa vie simple. Confucius le loua : « Comme Hui est admirable ! »</p>
""",
    },

    "ve-di-tich/tuong-tho/tu-tu": {
        "en": """
<p>Zisi (子思, 483–402 BC) — given name Kongji — was the grandson of Confucius and a disciple of Zengzi. He is honoured as the Transmitting Sage, one of the Four Sages.</p>
<p>Zisi is the author of the <em>Doctrine of the Mean</em> (中庸) — one of the Four Books of Confucianism.</p>
""",
        "fr": """
<p>Zisi (子思, 483–402 av. J.-C.) — nom de naissance Kongji — était le petit-fils de Confucius et disciple de Zengzi. Il est honoré sous le titre de Sage Transmetteur, l'un des Quatre Sages.</p>
<p>Zisi est l'auteur de <em>La Doctrine du Milieu</em> (中庸) — l'un des Quatre Livres du confucianisme.</p>
""",
    },

    "ve-di-tich/tuong-tho/tang-tu": {
        "en": """
<p>Zengzi (曾子, 505–435 BC) — given name Zeng Shen — was one of Confucius's younger and most gifted disciples. He is honoured as the Exemplary Sage, one of the Four Sages.</p>
<p>Zengzi is the author of the <em>Great Learning</em> (大學) — one of the Four Books of Confucianism. He was also the teacher of Zisi, Confucius's grandson.</p>
""",
        "fr": """
<p>Zengzi (曾子, 505–435 av. J.-C.) — nom de naissance Zeng Shen — était l'un des disciples les plus jeunes et les plus talentueux de Confucius. Il est honoré sous le titre de Sage Exemplaire, l'un des Quatre Sages.</p>
<p>Zengzi est l'auteur de <em>La Grande Étude</em> (大學) — l'un des Quatre Livres du confucianisme. Il fut également le maître de Zisi, petit-fils de Confucius.</p>
""",
    },

    "ve-di-tich/tuong-tho/manh-tu": {
        "en": """
<p>Mencius (孟子, 372–289 BC) — given name Meng Ke — was one of the greatest thinkers of Confucianism, living about 100 years after Confucius. He is honoured as the Second Sage — the highest position after Confucius himself.</p>
<p>Mencius is the author of the <em>Mencius</em> — one of the Four Books. He developed the doctrine of "inherent goodness" — the idea that human nature is fundamentally benevolent.</p>
""",
        "fr": """
<p>Mencius (孟子, 372–289 av. J.-C.) — nom de naissance Meng Ke — fut l'un des plus grands penseurs du confucianisme, vivant environ 100 ans après Confucius. Il est honoré sous le titre de Second Sage — la position la plus haute après Confucius lui-même.</p>
<p>Mencius est l'auteur du <em>Mencius</em> — l'un des Quatre Livres. Il développa la doctrine de « la bonté innée » — l'idée que la nature humaine est fondamentalement bienveillante.</p>
""",
    },

    # ── B6. Library ───────────────────────────────────────────────────────────
    "ve-di-tich/thu-vien/thu-vien-anh": {
        "en": """
<p>A documentary photo collection of the Temple of Literature – Imperial Academy across the ages, including historical archive photos, architectural photography and images from cultural events at the site.</p>
<div class="gallery">
  <div class="gallery-item"><img src="../../../assets/images/lich-su/hero.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/lich-su/ho-van.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/lich-su/bia.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/lich-su/nha-bia.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/kien-truc/cong-dai-thanh.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/kien-truc/cong-dai-trung.jpg" alt="" loading="lazy"></div>
</div>
""",
        "fr": """
<p>Collection de photos documentaires sur le Temple de la Littérature – Académie Impériale à travers les âges, comprenant des archives historiques, des photographies architecturales et des images d'événements culturels sur le site.</p>
<div class="gallery">
  <div class="gallery-item"><img src="../../../assets/images/lich-su/hero.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/lich-su/ho-van.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/lich-su/bia.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/lich-su/nha-bia.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/kien-truc/cong-dai-thanh.jpg" alt="" loading="lazy"></div>
  <div class="gallery-item"><img src="../../../assets/images/kien-truc/cong-dai-trung.jpg" alt="" loading="lazy"></div>
</div>
""",
    },

    "ve-di-tich/thu-vien/video": {
        "en": """
<p>Video archive of the Temple of Literature – Imperial Academy: historical documentaries, introductory films and television programmes about the heritage site.</p>
<div class="note">Contact the Communications Department for archival materials for research, education or media use.</div>
<h2>Video topics</h2>
<ul>
  <li>Documentary "Temple of Literature – Over 950 Years" (2020)</li>
  <li>Short film "82 Doctoral Stelae — UNESCO Memory of the World" (2018)</li>
  <li>Virtual tour of the Temple of Literature – Imperial Academy (2022)</li>
  <li>Series on architecture and decorative arts</li>
</ul>
""",
        "fr": """
<p>Archives vidéo du Temple de la Littérature – Académie Impériale : documentaires historiques, films de présentation et émissions télévisées sur le patrimoine.</p>
<div class="note">Contactez le Département Communication pour les documents d'archives à des fins de recherche, d'éducation ou médias.</div>
<h2>Thèmes vidéo</h2>
<ul>
  <li>Documentaire « Temple de la Littérature – Plus de 950 ans » (2020)</li>
  <li>Court-métrage « 82 stèles doctorales — Mémoire du monde UNESCO » (2018)</li>
  <li>Visite virtuelle du Temple de la Littérature – Académie Impériale (2022)</li>
  <li>Série sur l'architecture et les arts décoratifs</li>
</ul>
""",
    },

    # ── C. Exhibitions ────────────────────────────────────────────────────────
    "trung-bay-trien-lam/co-dinh/truong-quoc-hoc": {
        "en": """
<p>The exhibition "Imperial Academy – Vietnam's First National School" presents the history, development and role of the Imperial Academy in Vietnamese education during the feudal era.</p>
<h2>Exhibition content</h2>
<ul>
  <li>History of the Imperial Academy's establishment (1076 – present)</li>
  <li>Organisational structure and governance</li>
  <li>Curriculum across different periods</li>
  <li>Notable figures of the Imperial Academy</li>
</ul>
""",
        "fr": """
<p>L'exposition « Académie Impériale – Première école nationale du Vietnam » présente l'histoire, le développement et le rôle de l'Académie Impériale dans l'éducation vietnamienne à l'époque féodale.</p>
<h2>Contenu de l'exposition</h2>
<ul>
  <li>Histoire de la fondation de l'Académie Impériale (1076 – aujourd'hui)</li>
  <li>Structure organisationnelle et gouvernance</li>
  <li>Programme d'études à travers les différentes périodes</li>
  <li>Personnages notables de l'Académie Impériale</li>
</ul>
""",
    },

    "trung-bay-trien-lam/co-dinh/khoi-nguon-dao-hoc": {
        "en": """
<p>The exhibition "At the Source of Learning" focuses on the Vietnamese Confucian system — from the philosophy of Confucius to representative generations of Vietnamese disciples.</p>
<h2>Exhibition content</h2>
<ul>
  <li>Confucian thought and philosophy</li>
  <li>Ritual and ceremonial systems</li>
  <li>Classical works and textbooks</li>
  <li>The four scholarly treasures (brush, ink, inkstone, paper) through the ages</li>
</ul>
""",
        "fr": """
<p>L'exposition « À la source du savoir » se concentre sur le système confucéen vietnamien — de la philosophie de Confucius aux générations représentatives de disciples vietnamiens.</p>
<h2>Contenu de l'exposition</h2>
<ul>
  <li>Pensée et philosophie confucéennes</li>
  <li>Systèmes rituels et cérémoniels</li>
  <li>Œuvres classiques et manuels scolaires</li>
  <li>Les quatre trésors du lettré (pinceau, encre, pierre à encre, papier) à travers les âges</li>
</ul>
""",
    },

    "trung-bay-trien-lam/co-dinh/su-da-luu-danh": {
        "en": """
<p>The exhibition "History Etched in Stone" presents the system of 82 Doctoral Stelae — the UNESCO Memory of the World inscribed in 2010.</p>
<h2>Exhibition content</h2>
<ul>
  <li>History of the erection of Doctoral Stelae (1484–1780)</li>
  <li>Original rubbings and artistic reproductions</li>
  <li>The content and significance of the stele inscriptions</li>
  <li>Conservation and promotion of the documentary heritage</li>
</ul>
""",
        "fr": """
<p>L'exposition « L'histoire gravée dans la pierre » présente le système des 82 stèles doctorales — inscrites au registre Mémoire du monde de l'UNESCO en 2010.</p>
<h2>Contenu de l'exposition</h2>
<ul>
  <li>Histoire de l'érection des stèles doctorales (1484–1780)</li>
  <li>Estampages originaux et reproductions artistiques</li>
  <li>Contenu et signification des inscriptions sur les stèles</li>
  <li>Conservation et valorisation du patrimoine documentaire</li>
</ul>
""",
    },

    # ── D. Activities ─────────────────────────────────────────────────────────
    "cac-hoat-dong/giao-duc-di-san": {
        "en": """
<p>Heritage education programmes for pupils from kindergarten to high school — helping children experience and understand the cultural heritage of the nation.</p>
<h2>Programmes by school level</h2>
<ul>
  <li><strong>Kindergarten (age 3–5)</strong> — Guided visit, storytelling, drawing and colouring</li>
  <li><strong>Primary school grades 1–3</strong> — Folk games, handwriting practice</li>
  <li><strong>Primary school grades 4–6</strong> — Doctoral Stelae study, stele-rubbing practice</li>
  <li><strong>Lower and upper secondary (grades 7–12)</strong> — In-depth research, student symposia</li>
</ul>
<table class="info-table">
  <tr><th>Contact</th><td>0369.087.468 (Education &amp; Communications Dept.)</td></tr>
  <tr><th>Book ahead</th><td>Minimum 3 days in advance</td></tr>
  <tr><th>Minimum group</th><td>15 pupils</td></tr>
</table>
""",
        "fr": """
<p>Programmes d'éducation au patrimoine pour les élèves de la maternelle au lycée — pour aider les enfants à vivre et comprendre le patrimoine culturel de la nation.</p>
<h2>Programmes par niveau scolaire</h2>
<ul>
  <li><strong>Maternelle (3–5 ans)</strong> — Visite guidée, contes, dessin et coloriage</li>
  <li><strong>Primaire niveaux 1–3</strong> — Jeux populaires, pratique de l'écriture</li>
  <li><strong>Primaire niveaux 4–6</strong> — Étude des stèles doctorales, estampage</li>
  <li><strong>Collège et lycée (niveaux 7–12)</strong> — Recherche approfondie, symposiums étudiants</li>
</ul>
<table class="info-table">
  <tr><th>Contact</th><td>0369.087.468 (Département Éducation &amp; Communication)</td></tr>
  <tr><th>Réservation</th><td>Minimum 3 jours à l'avance</td></tr>
  <tr><th>Groupe minimum</th><td>15 élèves</td></tr>
</table>
""",
    },

    "cac-hoat-dong/trai-nghiem": {
        "en": """
<p>Hands-on activities for visitors and study groups.</p>
<h2>Main activities</h2>
<ul>
  <li>Doctoral Stele rubbing experience</li>
  <li>Vietnamese and Chinese calligraphy</li>
  <li>Traditional folk games</li>
  <li>Themed guided tours</li>
  <li>Exploration of Confucian rituals</li>
</ul>
""",
        "fr": """
<p>Activités pratiques pour les visiteurs et les groupes scolaires.</p>
<h2>Activités principales</h2>
<ul>
  <li>Estampage des stèles doctorales</li>
  <li>Calligraphie vietnamienne et chinoise</li>
  <li>Jeux populaires traditionnels</li>
  <li>Visites guidées thématiques</li>
  <li>Découverte des rites confucéens</li>
</ul>
""",
    },

    "cac-hoat-dong/van-hoa-nghe-thuat": {
        "en": """
<p>Cultural and arts programmes at the Temple of Literature — bringing traditional Vietnamese performing arts to the public.</p>
<h2>Art forms</h2>
<ul>
  <li>Traditional music — ca trù, chầu văn, quan họ</li>
  <li>Imperial court dance</li>
  <li>Xẩm and chèo folk theatre</li>
  <li>Áo dài fashion performance</li>
</ul>
""",
        "fr": """
<p>Programmes culturels et artistiques au Temple de la Littérature — pour présenter les arts de la scène traditionnels vietnamiens au grand public.</p>
<h2>Formes artistiques</h2>
<ul>
  <li>Musique traditionnelle — ca trù, chầu văn, quan họ</li>
  <li>Danse de cour impériale</li>
  <li>Théâtre populaire xẩm et chèo</li>
  <li>Défilé de mode áo dài</li>
</ul>
""",
    },

    "cac-hoat-dong/hoi-thao": {
        "en": """
<p>Academic conferences and round-table talks at the Temple of Literature – Imperial Academy on heritage, history and education.</p>
<h2>Topics</h2>
<ul>
  <li>Preservation and promotion of Sino-Nôm heritage</li>
  <li>History of Confucian civil-service examinations in Vietnam</li>
  <li>Doctoral Stelae and the value of documentary world heritage</li>
  <li>Heritage education in schools</li>
  <li>Heritage tourism and sustainable development</li>
</ul>
""",
        "fr": """
<p>Conférences académiques et tables rondes au Temple de la Littérature – Académie Impériale sur le patrimoine, l'histoire et l'éducation.</p>
<h2>Thèmes</h2>
<ul>
  <li>Préservation et valorisation du patrimoine sino-nôm</li>
  <li>Histoire des examens mandarinaux confucéens au Vietnam</li>
  <li>Stèles doctorales et valeur du patrimoine documentaire mondial</li>
  <li>Éducation au patrimoine à l'école</li>
  <li>Tourisme patrimonial et développement durable</li>
</ul>
""",
    },

    "cac-hoat-dong/doan-ngoai-giao": {
        "en": """
<p>The Temple of Literature – Imperial Academy is an important destination for diplomatic delegations and foreign leaders visiting Vietnam.</p>
<h2>Reception services</h2>
<ul>
  <li>Guided tour with professional multilingual guides</li>
  <li>Welcome ceremony in traditional style</li>
  <li>Special cultural gift sets</li>
  <li>Coordination with diplomatic agencies</li>
</ul>
""",
        "fr": """
<p>Le Temple de la Littérature – Académie Impériale est une destination importante pour les délégations diplomatiques et les dirigeants étrangers en visite au Vietnam.</p>
<h2>Services d'accueil</h2>
<ul>
  <li>Visite guidée avec des guides multilingues professionnels</li>
  <li>Cérémonie d'accueil de style traditionnel</li>
  <li>Coffrets cadeaux culturels spéciaux</li>
  <li>Coordination avec les agences diplomatiques</li>
</ul>
""",
    },

    "cac-hoat-dong/workshop": {
        "en": """
<p>Creative and cultural experience workshops at the Temple of Literature.</p>
<h2>Featured workshops</h2>
<ul>
  <li>Sino-Nôm calligraphy workshop</li>
  <li>Doctoral Stele rubbing workshop</li>
  <li>Traditional brush-making workshop</li>
  <li>Confucian bookbinding workshop</li>
  <li>Paper-cutting art workshop</li>
</ul>
<table class="info-table">
  <tr><th>Open to</th><td>All ages (varies by workshop)</td></tr>
  <tr><th>Book ahead</th><td>Minimum 5 days in advance</td></tr>
</table>
""",
        "fr": """
<p>Ateliers créatifs et d'expérience culturelle au Temple de la Littérature.</p>
<h2>Ateliers phares</h2>
<ul>
  <li>Atelier de calligraphie sino-nôm</li>
  <li>Atelier d'estampage de stèles doctorales</li>
  <li>Atelier de fabrication de pinceaux traditionnels</li>
  <li>Atelier de reliure confucéenne</li>
  <li>Atelier d'art du découpage de papier</li>
</ul>
<table class="info-table">
  <tr><th>Ouvert à</th><td>Tous les âges (selon l'atelier)</td></tr>
  <tr><th>Réservation</th><td>Minimum 5 jours à l'avance</td></tr>
</table>
""",
    },

    "cac-hoat-dong/su-kien/sap-dien-ra": {
        "en": """
<p>Schedule of upcoming events at the Temple of Literature – Imperial Academy.</p>
<div class="note">The events calendar is updated monthly. Contact 024.3747.1322 for details.</div>
<h2>Annual events</h2>
<ul>
  <li><strong>Lunar New Year (Tết)</strong> — Inaugural brushstroke ceremony, Confucius incense offering, Spring Calligraphy Fair</li>
  <li><strong>Fifteenth of the First Lunar Month</strong> — Vietnam Poetry Day, poetry gathering at the Khuê Văn Pavilion</li>
  <li><strong>September</strong> — Autumn Confucius Ritual</li>
  <li><strong>23 November</strong> — Vietnam Cultural Heritage Day</li>
</ul>
""",
        "fr": """
<p>Calendrier des prochains événements au Temple de la Littérature – Académie Impériale.</p>
<div class="note">Le calendrier est mis à jour chaque mois. Contactez le 024.3747.1322 pour plus d'informations.</div>
<h2>Événements annuels</h2>
<ul>
  <li><strong>Nouvel An lunaire (Tết)</strong> — Cérémonie du premier pinceau, offrande d'encens à Confucius, Foire à la calligraphie de printemps</li>
  <li><strong>15e jour du premier mois lunaire</strong> — Journée nationale de la poésie, rencontre poétique au Pavillon Khuê Văn</li>
  <li><strong>Septembre</strong> — Rituel automnal de Confucius</li>
  <li><strong>23 novembre</strong> — Journée du patrimoine culturel du Vietnam</li>
</ul>
""",
    },

    "cac-hoat-dong/su-kien/dang-dien-ra": {
        "en": """
<p>Events currently taking place at the Temple of Literature – Imperial Academy.</p>
<div class="note">Updated in real time. Please verify information before attending.</div>
""",
        "fr": """
<p>Événements en cours au Temple de la Littérature – Académie Impériale.</p>
<div class="note">Mis à jour en temps réel. Veuillez vérifier les informations avant de vous y rendre.</div>
""",
    },

    # ── E. Services ───────────────────────────────────────────────────────────
    "dich-vu/tour-dem": {
        "en": """
<p>The Night Tour of the Temple of Literature offers an immersive after-dark experience, combining modern artistic lighting with traditional performing arts.</p>
<h2>Tour information</h2>
<table class="info-table">
  <tr><th>Time</th><td>19:30 – 21:30 (Friday, Saturday, Sunday)</td></tr>
  <tr><th>Group size</th><td>Maximum 30 persons per tour</td></tr>
  <tr><th>Language</th><td>Vietnamese; English on request</td></tr>
  <tr><th>Advance booking</th><td>Minimum 2 days</td></tr>
</table>
<h2>Programme</h2>
<ul>
  <li>Visit to 5 areas under artistic lighting</li>
  <li>Guide narrates history and legends</li>
  <li>Traditional arts performance at the Khuê Văn Pavilion</li>
  <li>Calligraphy experience by candlelight</li>
</ul>
""",
        "fr": """
<p>La Visite nocturne du Temple de la Littérature offre une expérience immersive à la tombée de la nuit, alliant mise en lumière artistique moderne et arts de la scène traditionnels.</p>
<h2>Informations pratiques</h2>
<table class="info-table">
  <tr><th>Horaire</th><td>19h30 – 21h30 (vendredi, samedi, dimanche)</td></tr>
  <tr><th>Groupe</th><td>30 personnes maximum par visite</td></tr>
  <tr><th>Langue</th><td>Vietnamien ; anglais sur demande</td></tr>
  <tr><th>Réservation</th><td>Minimum 2 jours à l'avance</td></tr>
</table>
<h2>Programme</h2>
<ul>
  <li>Visite de 5 zones sous éclairage artistique</li>
  <li>Le guide raconte l'histoire et les légendes</li>
  <li>Spectacle d'arts traditionnels au Pavillon Khuê Văn</li>
  <li>Expérience calligraphique à la bougie</li>
</ul>
""",
    },

    "dich-vu/audio-guide": {
        "en": """
<p>The audio guide lets you explore the site at your own pace with in-depth commentary at each point of interest.</p>
<h2>Languages available</h2>
<p>8 languages: Vietnamese, English, French, Spanish, Korean, Japanese, Chinese, Thai.</p>
<h2>Device rental</h2>
<div class="price-table">
  <div class="price-row"><div class="price-cat"><p>Vietnamese</p></div><p class="price-val">30,000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Foreign language</p></div><p class="price-val">50,000 VND</p></div>
</div>
<div class="note">Ask staff at the ticket counter to rent a device.</div>
""",
        "fr": """
<p>L'audioguide vous permet de visiter le site à votre rythme avec un commentaire approfondi à chaque point d'intérêt.</p>
<h2>Langues disponibles</h2>
<p>8 langues : vietnamien, anglais, français, espagnol, coréen, japonais, chinois, thaïlandais.</p>
<h2>Location d'appareils</h2>
<div class="price-table">
  <div class="price-row"><div class="price-cat"><p>Vietnamien</p></div><p class="price-val">30 000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Langue étrangère</p></div><p class="price-val">50 000 VND</p></div>
</div>
<div class="note">Demandez à l'agent à la billetterie pour louer un appareil.</div>
""",
    },

    "dich-vu/huong-dan-vien": {
        "en": """
<p>Our team of professional guides is trained in the history, culture and architecture of the Temple of Literature — providing expert commentary at each site.</p>
<h2>Languages</h2>
<ul>
  <li>Vietnamese</li>
  <li>English</li>
  <li>French</li>
  <li>Chinese</li>
</ul>
<h2>Booking</h2>
<table class="info-table">
  <tr><th>Phone</th><td>024.3823.5601</td></tr>
  <tr><th>Advance booking</th><td>Minimum 1 day</td></tr>
  <tr><th>Minimum group</th><td>5 persons</td></tr>
</table>
""",
        "fr": """
<p>Notre équipe de guides professionnels est formée à l'histoire, à la culture et à l'architecture du Temple de la Littérature — pour un commentaire expert à chaque point du site.</p>
<h2>Langues</h2>
<ul>
  <li>Vietnamien</li>
  <li>Anglais</li>
  <li>Français</li>
  <li>Chinois</li>
</ul>
<h2>Réservation</h2>
<table class="info-table">
  <tr><th>Téléphone</th><td>024.3823.5601</td></tr>
  <tr><th>Délai</th><td>Minimum 1 jour à l'avance</td></tr>
  <tr><th>Groupe minimum</th><td>5 personnes</td></tr>
</table>
""",
    },

    "dich-vu/qua-luu-niem": {
        "en": """
<p>The souvenir shop carries products reflecting the cultural identity of the Temple of Literature – Imperial Academy.</p>
<h2>Featured products</h2>
<ul>
  <li>Books and publications on the Temple, Hanoi heritage and Confucianism</li>
  <li>Doctoral Stele rubbings (artistic editions)</li>
  <li>Traditional-style ceramics and bronzeware</li>
  <li>Scholarly stationery — brush, ink, inkstone, paper</li>
  <li>Áo dài and accessories with Temple motifs</li>
</ul>
<table class="info-table">
  <tr><th>Location</th><td>Main exit and Thái Học sector</td></tr>
  <tr><th>Opening hours</th><td>Same as site visiting hours</td></tr>
</table>
""",
        "fr": """
<p>La boutique de souvenirs propose des produits reflétant l'identité culturelle du Temple de la Littérature – Académie Impériale.</p>
<h2>Produits phares</h2>
<ul>
  <li>Livres et publications sur le Temple, le patrimoine de Hanoï et le confucianisme</li>
  <li>Estampages des stèles doctorales (éditions artistiques)</li>
  <li>Céramiques et bronzes de style traditionnel</li>
  <li>Papeterie savante — pinceau, encre, pierre à encre, papier</li>
  <li>Áo dài et accessoires aux motifs du Temple</li>
</ul>
<table class="info-table">
  <tr><th>Emplacement</th><td>Sortie principale et secteur Thái Học</td></tr>
  <tr><th>Heures d'ouverture</th><td>Mêmes que les heures de visite du site</td></tr>
</table>
""",
    },

    "dich-vu/thu-phap": {
        "en": """
<p>Try calligraphy at the Temple of Literature — where art and heritage combine to offer visitors a meditative and culturally meaningful experience.</p>
<h2>Activities</h2>
<ul>
  <li>Guided practice in Vietnamese and Chinese calligraphy</li>
  <li>Requesting an auspicious character at New Year — a traditional custom</li>
  <li>Short calligraphy classes (weekends)</li>
  <li>Group calligraphy workshops</li>
</ul>
<table class="info-table">
  <tr><th>Location</th><td>Văn Lake area (especially during Tết)</td></tr>
  <tr><th>Contact</th><td>024.3747.1322</td></tr>
</table>
""",
        "fr": """
<p>Essayez la calligraphie au Temple de la Littérature — là où art et patrimoine se rencontrent pour offrir aux visiteurs une expérience méditative et culturellement riche.</p>
<h2>Activités</h2>
<ul>
  <li>Pratique guidée de la calligraphie vietnamienne et chinoise</li>
  <li>Demande d'un caractère de bon augure pour le Nouvel An — coutume traditionnelle</li>
  <li>Cours de calligraphie courts (week-ends)</li>
  <li>Ateliers de calligraphie en groupe</li>
</ul>
<table class="info-table">
  <tr><th>Emplacement</th><td>Zone du Lac Văn (surtout pendant le Tết)</td></tr>
  <tr><th>Contact</th><td>024.3747.1322</td></tr>
</table>
""",
    },

    "dich-vu/nuoc-uong": {
        "en": """
<p>Refreshment kiosks serving visitors within the site grounds.</p>
<h2>Menu</h2>
<ul>
  <li>Bottled mineral water</li>
  <li>Herbal teas, lotus tea</li>
  <li>Coffee, milk tea</li>
  <li>Fresh fruit juices</li>
</ul>
<table class="info-table">
  <tr><th>Location</th><td>Tiền Đường courtyard (Thái Học sector) and near the exit</td></tr>
  <tr><th>Opening hours</th><td>Same as site visiting hours</td></tr>
</table>
""",
        "fr": """
<p>Kiosques de rafraîchissements au service des visiteurs dans l'enceinte du site.</p>
<h2>Menu</h2>
<ul>
  <li>Eau minérale en bouteille</li>
  <li>Tisanes, thé au lotus</li>
  <li>Café, thé au lait</li>
  <li>Jus de fruits frais</li>
</ul>
<table class="info-table">
  <tr><th>Emplacement</th><td>Cour Tiền Đường (secteur Thái Học) et près de la sortie</td></tr>
  <tr><th>Heures d'ouverture</th><td>Mêmes que les heures de visite du site</td></tr>
</table>
""",
    },
}
