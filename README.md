# codeanddrive.com

Personal site of Tomasz Sułkowski – software developer and drift driver. Bilingual (English / Polish), built with
[Jekyll](https://jekyllrb.com/) and published by **GitHub Pages** straight from the `master` branch.

## How it is built

GitHub Pages uses its classic Jekyll builder (Jekyll 3.10, see <https://pages.github.com/versions/>), which runs
**only the plugins on its whitelist**. `_config.yml` therefore lists just `jekyll-seo-tag` (meta description,
canonical, Open Graph / Twitter cards, JSON-LD) and `jekyll-sitemap` (`sitemap.xml` + `robots.txt`). Anything else
has to be plain Liquid, CSS or JavaScript – which is how the language switching and the photo gallery work.
The site makes no third-party requests: the fonts (Bebas Neue, Open Sans – OFL) are self-hosted in `assets/fonts/`.

### Local build

Ruby 3.2 and the gems installed with `gem install --user-install` (no bundler needed):

```sh
gem install --user-install jekyll:3.10.0 kramdown-parser-gfm jekyll-seo-tag:2.8.0 jekyll-sitemap:1.4.0 webrick
export PATH="$HOME/.local/share/gem/ruby/3.2.0/bin:$PATH"

jekyll build --strict_front_matter      # -> _site/
jekyll serve                             # http://127.0.0.1:4000/ (extensionless post URLs work here)
jekyll build --unpublished               # also render posts marked `published: false`
```

Prefer bundler? Create a `Gemfile` with `gem "github-pages", group: :jekyll_plugins` and use `bundle exec jekyll …`.
Note that once a `Gemfile` exists Jekyll insists on bundler (set `JEKYLL_NO_BUNDLER_REQUIRE=1` to opt out).

## Content conventions

| What | How |
| --- | --- |
| Languages | Every page/post exists twice: `name.en.html` and `name.pl.html` (or `.md`), each with `lang: en` / `lang: pl` in its front matter. Pages use explicit `permalink: /en/…/` and `/pl/…/`; the header switcher finds the twin by swapping the language token in the file name (`_includes/alternate_page.html`). |
| Navigation | A page appears in the top menu when it has `public: true`, `layout: default`, a `title` and the same `lang` as the page being viewed; `nav_title` is the short label shown in the menu. |
| Posts | `_posts/YYYY-MM-DD-slug.<lang>.md`, `public: true` to list them (home page, sidebar, RSS). A draft gets `published: false` so it is not built at all. Post URLs are `/slug.<lang>` (kept for existing inbound links). |
| SEO | `description:` (one sentence), `image:` (`path`, `width`, `height` – the page's own photo, used as `og:image`) and `twitter: {card: …}` per page and post; defaults live in `_config.yml`. |
| Dates | `{% include post_date.html date=post.date lang=post.lang %}` renders localised `<time>` elements. |

### Adding an event or a result

Edit the tables in both `_pages/driver.en.html` and `_pages/driver.pl.html`. Links are rendered as small labels:

```html
<a class="media-link" href="https://youtu.be/…" target="_blank" rel="noopener" title="Watch on YouTube">&#x25B6;&#xFE0E; YouTube</a>
<a class="media-link" href="https://www.instagram.com/p/…/" target="_blank" rel="noopener" title="See the post on Instagram">Instagram</a>
```

### Adding gallery photos

The gallery is folder-driven (`_includes/gallery.html`): every `*.jpg`, `*.jpeg` or `*.png` in the folder becomes a
tile, opened in a same-page lightbox ([GLightbox](https://github.com/biati-digital/glightbox) 3.3.1, MIT, vendored
in `assets/vendor/glightbox/` together with its `LICENSE`). Three columns on desktop, two on phones.

1. Copy the photo(s) into `assets/images/driver/e46/` (files are sorted by name – use `01.jpg`, `02.jpg`, … if order matters).
2. Generate the thumbnails (`<name>_t.<ext>`, 600×400, needs Pillow ≥ 9.1: `pip install "pillow>=9.1"`):
   ```sh
   python3 scripts/make_thumbnails.py assets/images/driver/e46
   ```
3. Optionally add a bilingual caption / alt text in `_data/galleries.yml` (photos without one get "BMW E46 drift car – photo N" /
   "Samochód driftingowy BMW E46 – zdjęcie N", built from the include's `alt`).
4. Commit the photo, its thumbnail and the caption.

A page that shows a gallery needs `gallery: true` in its front matter (loads the lightbox CSS/JS) and
`{% include gallery.html dir="/assets/images/<folder>/" name="<gallery-name>" alt="<generic alt>" %}`.

## Layout

```
_config.yml          site settings, plugins, front matter defaults
_layouts/            default (header + sidebar + footer), post
_includes/           head, header, sidebar, alternate_page, post_date, gallery
_pages/              developer.*.html, driver.*.html
home.*.html          language home pages; index.html redirects by browser language
404.html, feed.xml   error page, RSS feed (both languages, each item carries xml:lang)
_posts/              blog posts (per language)
_data/galleries.yml  gallery captions
_sass/, css/         styles (Sass, compiled by Jekyll)
assets/              images, self-hosted fonts (+ OFL), vendored JS/CSS (+ GLightbox LICENSE)
scripts/             maintenance scripts (not published)
CNAME, *.pdf         custom domain for GitHub Pages; the CV and the drift-taxi passenger form
```
