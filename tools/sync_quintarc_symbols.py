"""Copy the game's licensed element/rune glyphs into the QUINTARC guide."""
import argparse, hashlib, html, json, re, shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args()
site=Path(__file__).resolve().parents[1];root=a.source.resolve()
symbols=root/'assets/quintarc/symbols';dest=site/'assets/quintarc-symbols';dest.mkdir(exist_ok=True)
provenance=json.loads((symbols/'sources.json').read_text())
elements=['fire','water','earth','air','arcane']
colors=re.search(r'const COLORS = \[(.*?)\]',(root/'scripts/invocation_state.gd').read_text()).group(1)
colors=re.findall(r'Color\("(\w+)"\)',colors)
assert len(colors)==5
rune_colors=re.findall(r'Color\("(\w+)"\)',re.search(r'const COLORS = \[(.*?)\]',(root/'scripts/runes.gd').read_text()).group(1))
rune_symbols=['life','mana','arcane','air','rune']
used=set(["element-"+name for name in elements]+rune_symbols)
for name in elements:
 key="element-"+name
 provenance[key]={"source":"QUINTARC scripts/element_marks.gd and scripts/ui.gd draw_element_mark", "author":"Just Poly Games", "modifications":"SVG export of shared HUD/orb geometry", "runtime_sha256":hashlib.sha256((symbols/(key+".svg")).read_bytes()).hexdigest()}
for name in used: shutil.copy2(symbols/(name+'.svg'),dest/(name+'.svg'))
(dest/'sources.json').write_text(json.dumps({k:provenance[k] for k in sorted(used)},indent=2)+'\n')
shutil.copy2(symbols/'license.txt',dest/'LICENSE.txt')
def icon(name,color):
 return f'<span class="quintarc-symbol" style="--glyph:url(/assets/quintarc-symbols/{name}.svg);--glyph-color:#{color}" aria-hidden="true"></span>'
page=site/'games/quintarc/index.html';text=page.read_text()
# Idempotent: replace only heading decoration inside the arena section.
start=text.index('id="arenas"');end=text.index('</section>',start)
section=text[start:end]
for name,color in zip(elements,colors):
 section=re.sub(r'<h3>(?:<span class="quintarc-symbol"[^>]*></span>)?'+name.capitalize()+r'</h3>', '<h3>'+icon("element-"+name,color)+name.capitalize()+'</h3>', section)
text=text[:start]+section+text[end:]
tuning=json.loads((root/'data/rune_tuning.json').read_text())
entries=[('Health',f'Restores up to {tuning["health_amount"]:g} health.'),('Mana',f'Restores up to {tuning["mana_amount"]:g} mana.'),('Magic',f'+{tuning["damage_bonus"]*100:g}% magic damage for {tuning["damage_duration"]:g} seconds.'),('Movement',f'+{tuning["speed_bonus"]*100:g}% movement speed for {tuning["speed_duration"]:g} seconds.'),('Invisibility',f'Conceals you for up to {tuning["invisibility_duration"]:g} seconds. Casting or taking damage reveals you.')]
block='<section class="wiki-section" id="runes"><h2>Know your runes</h2><p>Look for these symbols on rune pickups. Timed rune buffs use the same symbol and color in your HUD.</p><div class="info-grid">'
for (name,description),symbol,color in zip(entries,rune_symbols,rune_colors):
 block+='<article class="info-card"><h3>'+icon(symbol,color)+name+'</h3><p>'+html.escape(description)+'</p></article>'
block+='</div><p>Five ground pickups and two health/mana pickups at stair-accessible terrace tops reward exploring each arena. Pickups respawn after 30 seconds. Health and mana restore immediately; timed bonuses refresh instead of stacking.</p></section>'
text=re.sub(r'<section class="wiki-section" id="runes">.*?</section>','',text,flags=re.S)
text=text.replace('<section class="wiki-section" id="campaign">',block+'<section class="wiki-section" id="campaign">')
page.write_text(text)
attrs=site/'assets/ATTRIBUTION.md';note='\n## QUINTARC element and rune symbols\n\nElement shapes are exported from QUINTARC’s shared HUD/orb geometry. Rune SVGs are copied unchanged from the game. Rune artwork: Game-icons.net contributors, CC BY 3.0; transparent-background adaptations and author/source hashes are listed in [quintarc-symbols/sources.json](quintarc-symbols/sources.json). See [license](quintarc-symbols/LICENSE.txt). Colors match the game.\n'
if '## QUINTARC element and rune symbols' not in attrs.read_text(): attrs.write_text(attrs.read_text()+note)
print('Synced five element and five rune symbols with source attribution.')
