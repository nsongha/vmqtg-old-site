import { MigrateUpArgs, MigrateDownArgs } from '@payloadcms/db-postgres'

// Polished EN + FR translations for the /tham-quan page. Replaces the rough
// translations originally seeded from vmqtg-v5/translations.py with friendlier,
// fully formatted versions. Runs once — admin edits made after this deploy
// are preserved by future seeds.

const EN = `
<p>Welcome to the Temple of Literature – Imperial Academy, Vietnam's first university and a Special National Heritage Site. Below is everything you need to plan a smooth visit.</p>

<h2>Opening hours</h2>
<table class="info-table">
  <tr><th>Summer (Apr – Oct)</th><td>07:30 – 18:00, daily</td></tr>
  <tr><th>Winter (Nov – Mar)</th><td>08:00 – 17:00, daily</td></tr>
  <tr><th>Ticket counter</th><td>Closes 30 minutes before site closing</td></tr>
</table>

<h2>Admission</h2>
<div class="price-table">
  <div class="price-row"><div class="price-cat"><p>Adults (16+)</p></div><p class="price-val">30,000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Students &amp; pupils (with ID)</p></div><p class="price-val">15,000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Seniors (60+)</p></div><p class="price-val">15,000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Children under 15</p></div><p class="price-val">Free</p></div>
</div>

<h2>Getting here</h2>
<table class="info-table">
  <tr><th>Address</th><td>58 Quoc Tu Giam Street, Van Mieu Ward, Dong Da District, Hanoi</td></tr>
  <tr><th>By bus</th><td>Lines 02, 23 and 38 stop directly at Văn Miếu</td></tr>
  <tr><th>Parking</th><td>Cars on Văn Miếu Street · motorbikes and bicycles at Vườn Giám</td></tr>
  <tr><th>From Hoan Kiem Lake</th><td>About 3 km — a short taxi or 15-minute bike ride</td></tr>
</table>

<h2>Visitor guidelines</h2>
<ol>
  <li>Please purchase your ticket and show it at the entrance gate.</li>
  <li>Help us protect the site: do not touch, mark or lean on artefacts, stelae or buildings; please keep off the lawns and do not pick flowers.</li>
  <li>The grounds are non-smoking; please follow all fire-safety signage.</li>
  <li>Wear respectful clothing inside the shrines and keep noise to a minimum in sacred areas.</li>
  <li>Superstitious practices, gambling and fraudulent activity are strictly prohibited.</li>
  <li>Visitors are responsible for any damage they cause to the site.</li>
  <li>Security staff may end a visit if these rules are not respected.</li>
  <li>Feedback or assistance: call <strong>024.3747.1322</strong> or <strong>024.3211.5793</strong>.</li>
</ol>

<h2>On-site facilities</h2>
<ul>
  <li>Car park on Văn Miếu Street; motorbike and bicycle park at Vườn Giám</li>
  <li>Café and refreshment kiosks inside the grounds</li>
  <li>Souvenir shop located near the exit</li>
  <li>Free Wi-Fi, benches throughout the gardens, and public restrooms</li>
</ul>
`.trim()

const FR = `
<p>Bienvenue au Temple de la Littérature – Académie Impériale, première université du Vietnam et site du patrimoine national spécial. Voici toutes les informations utiles pour préparer votre visite.</p>

<h2>Heures d'ouverture</h2>
<table class="info-table">
  <tr><th>Été (avr. – oct.)</th><td>07h30 – 18h00, tous les jours</td></tr>
  <tr><th>Hiver (nov. – mars)</th><td>08h00 – 17h00, tous les jours</td></tr>
  <tr><th>Billetterie</th><td>Ferme 30 min avant la fermeture du site</td></tr>
</table>

<h2>Tarifs</h2>
<div class="price-table">
  <div class="price-row"><div class="price-cat"><p>Adulte (16 ans et +)</p></div><p class="price-val">30 000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Élèves &amp; étudiants (avec carte)</p></div><p class="price-val">15 000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Seniors (60 ans et +)</p></div><p class="price-val">15 000 VND</p></div>
  <div class="price-row"><div class="price-cat"><p>Enfants de moins de 15 ans</p></div><p class="price-val">Gratuit</p></div>
</div>

<h2>Accès</h2>
<table class="info-table">
  <tr><th>Adresse</th><td>58 rue Quoc Tu Giam, quartier Van Mieu, district de Dong Da, Hanoï</td></tr>
  <tr><th>Bus</th><td>Lignes 02, 23 et 38 — arrêt Văn Miếu</td></tr>
  <tr><th>Stationnement</th><td>Voitures : rue Văn Miếu · motos et vélos : Vườn Giám</td></tr>
  <tr><th>Depuis le lac Hoan Kiem</th><td>Environ 3 km — quelques minutes en taxi ou 15 min à vélo</td></tr>
</table>

<h2>Règlement de visite</h2>
<ol>
  <li>Veuillez acheter et présenter un billet valide à l'entrée.</li>
  <li>Aidez-nous à préserver le site : ne touchez pas et n'écrivez pas sur les œuvres, stèles ou bâtiments ; respectez les pelouses et ne cueillez pas les fleurs.</li>
  <li>Le site est non-fumeur ; merci de respecter les consignes de sécurité incendie.</li>
  <li>Tenue correcte exigée dans les lieux de culte ; gardez le silence dans les espaces sacrés.</li>
  <li>Les pratiques superstitieuses, jeux d'argent et activités frauduleuses sont strictement interdits.</li>
  <li>Les visiteurs sont responsables des dommages qu'ils causeraient au site.</li>
  <li>La sécurité peut interrompre une visite en cas de manquement au règlement.</li>
  <li>Renseignements ou réclamations : <strong>024.3747.1322</strong> ou <strong>024.3211.5793</strong>.</li>
</ol>

<h2>Services sur place</h2>
<ul>
  <li>Parking voitures rue Văn Miếu ; parking motos/vélos à Vườn Giám</li>
  <li>Café et kiosques de boissons dans l'enceinte</li>
  <li>Boutique de souvenirs à proximité de la sortie</li>
  <li>Wi-Fi gratuit, bancs dans les jardins et toilettes publiques</li>
</ul>
`.trim()

export async function up({ payload }: MigrateUpArgs): Promise<void> {
  const result = await payload.find({
    collection: 'pages',
    where: { slug: { equals: 'tham-quan' } },
    limit: 1,
    depth: 0,
  })
  const page = result.docs[0]
  if (!page) {
    payload.logger.warn('[migration] tham-quan page not found — skipping')
    return
  }
  for (const [locale, html] of [['en', EN], ['fr', FR]] as const) {
    await payload.update({
      collection: 'pages',
      id: page.id,
      locale,
      data: { content_html: html } as any,
    })
  }
  payload.logger.info('[migration] tham-quan EN + FR polished')
}

export async function down(_: MigrateDownArgs): Promise<void> {
  // No-op: the previous text was the rough auto-translation; rolling back has no value.
}
