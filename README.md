# Just Poly Games

**Indie games by Anthony, a game developer from the Philippines.**

[Visit the portfolio](https://justpolygames.github.io/) · [Project Pencil guide](https://justpolygames.github.io/games/project-pencil.html) · [QUINTARC guide](https://justpolygames.github.io/games/quintarc.html)

I’m Anthony, the creator behind Just Poly Games. With experience in Web Design and UI/UX Design and a current role as a Product Manager, I’m turning a lifelong love of games into playable worlds.

- **Project Pencil:** a first-person drawing adventure where sketches become tools, weapons, and new ways forward.
- **QUINTARC:** elemental spellcasting with five elements, 126 spells, a narrative campaign, and arena modes.

Both games are in development. This repository hosts their portfolio and player guides, including a searchable spell grimoire.

A lightweight static website for GitHub Pages. No build step or dependencies are required.

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

## Studio branding

The header, footer, and PNG favicon reuse the supplied `just-poly-icon.png` unchanged. Bold stacked lettering and the shared cyan, blue, and violet colors align the site with the Just Poly Games brand.

## Search and social metadata

Each page has a unique title and description, an absolute canonical URL, Open Graph and Twitter card metadata, and JSON-LD describing the studio, developer, website, or game. The game guides include breadcrumb data. No ratings, release dates, or download offers are invented.

`robots.txt` permits crawling and points to `sitemap.xml`. After adding a page, add its entry in `tools/update_seo.py` and run `python3 tools/update_seo.py` to regenerate metadata and the sitemap. Image dimensions must match the original PNGs.

Repository topics help discovery on GitHub. Indexing and rankings are determined by search engines; these changes do not establish indexing. Google Search Console ownership verification and sitemap submission have not been performed.

References: [Google structured data guidance](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data), [Google sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
