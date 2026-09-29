# Just Poly Games

Anthony’s static indie-game portfolio, ready for GitHub Pages. No build step or dependencies are required.

## Preview

Run `python3 -m http.server 8080` in this directory, then open http://localhost:8080.

## Pages

- `index.html`: introduction, three-column game collection, and background.
- `games/project-pencil.html`: overview, drawing mechanics, equipment, story, modes, controls, and FAQ.
- `games/quintarc.html`: mechanics, modes, arenas, campaign, controls, and 126 searchable spell entries.

## Publishing

GitHub Pages is configured to serve `main` at the repository root. Push the reviewed files to `main` to deploy. `.nojekyll` enables plain static delivery.

## Editing

Edit HTML directly; shared styles and behavior live in `style.css` and `site.js`. To add a game, replace the third placeholder card with a link and create its dedicated page. All content and navigation work without JavaScript; JavaScript adds spell filtering.

## Content and artwork

Game copy was checked against Project Pencil README and QUINTARC README, STORY_CAMPAIGN, SPELL_CATALOG, and generated spell descriptions on 2026-09-29. Development details may change. No public game download or hardware validation is promised.

The existing Project Pencil cover and QUINTARC seal are reused from the owner’s game projects. The seal incorporates the previously licensed open-book silhouette from Game-icons.net; see `assets/ATTRIBUTION.md`. The portfolio controller is original CSS geometry. Visual inspiration: https://gitmastery.me/; no reference website code or assets were copied.
