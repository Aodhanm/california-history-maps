# California History Maps

Interactive maps of Spanish- and Mexican-era California expeditions and frontier geography, reconstructed from primary sources and secondary scholarship.

**Live site:** https://aodhanm.github.io/california-history-maps/

## Maps

| Map | Period | Description |
|-----|--------|-------------|
| [Zalvidea & Moraga Expeditions](zalvidea-moraga-1806.html) | 1806–1807 | Two interior routes — togglable legs, campsites, Indian villages, missions |
| [Gabriel Moraga — All Expeditions](moraga-expeditions-master.html) | 1806–1817 | Master map of Moraga's Central Valley and Delta reconnaissance |
| [Military Engagements of California](california-military-battles.html) | 1769–1840 | Armed engagements across the Spanish and Mexican periods |
| [Bay Area Borderlands](borderlands-imperial-frontier.html) | 1775–1841 | The contested Spanish/Russian/British imperial frontier around SF Bay |

## Technical

Each map is a self-contained HTML file using [Leaflet.js](https://leafletjs.com) with OpenTopoMap tiles — no build step. Waypoints are JS arrays; add stops by pushing `{n, lat, lng, name, detail, note}` objects.
