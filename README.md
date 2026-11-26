# carbonhandprint.org

Source for [carbonhandprint.org](https://carbonhandprint.org). A plain [Jekyll](https://jekyllrb.com/) site that GitHub Pages builds automatically. No build tools needed.

## Add a blog post

1. On GitHub, open the `_posts` folder and click **Add file → Create new file**.
2. Name it `YYYY-MM-DD-short-title.md`, for example `2027-01-15-cycling-to-school.md`.
3. Paste this at the top, then write the post below it in Markdown:

   ```markdown
   ---
   title: Cycling to school
   description: One sentence summary shown on the home page and in search results.
   ---

   Your post starts here. **Bold**, *italics*, [links](https://example.com) and lists all work.
   ```

   Add `tags: [paris-agreement]` under the title to list the post on the Paris Agreement page too. Drafts can live in `_drafts/`, which is never published.

4. Click **Commit changes**. The post is live in a minute or two, and appears on the home page, the blog page and the RSS feed.

Images: upload them to `assets/images/` and use `![Description](/assets/images/photo.jpg)`. Always fill in the description (it is the alt text).

SEO: the `description:` line is what Google and social media show, so keep it to one clear sentence. Add `image: /assets/images/your-photo.jpg` to give a post its own share picture; otherwise the default share card is used.

## Kinds of content

Articles live in `_posts/`. Add a `type:` line to say which kind it is. News links live in `_news/` and have no page of their own.

| Type | Use it for | Front matter |
|---|---|---|
| `editorial` (default) | Our own articles and opinion | nothing extra needed |
| `response` | Our take on an outside article, report or announcement | `link:` the URL, `link_title:` its title, `source:` who published it |

Example response:

```markdown
---
title: Nokia doubles down on the handprint
type: response
link: https://www.nokia.com/...
link_title: Nokia climate transition plan
source: Nokia
description: Why Nokia's new plan matters.
---

Your commentary here.
```

### News links

Add a file to `_news/`, named like a post:

```markdown
---
title: "Their headline"
link: https://example.com/story
source: The Guardian
date: 2027-01-15
description: "One line on why it matters."
card_image: "https://example.com/their-share-image.jpg"
tags: [paris-agreement]
---
```

News links show as cards on /news/ and the home page and go straight to the source. Tag one `paris-agreement` to list it on the Paris Agreement page too.

### Link cards

News links and responses show a card for the linked page. Add the publisher's sharing image and headline to the front matter:

```yaml
card_image: "https://example.com/their-share-image.jpg"
link_title: "Their headline"
```

To fill these in automatically, run this on your computer (Python 3, no extra packages):

```
python3 tools/og.py _news/2027-01-15-some-story.md
```

It reads the post's `link:`, looks up the page's Open Graph tags and adds `card_image:` and `link_title:`. Without an image, the card still shows the source and headline.

Each type has its own page: /editorial/ and /responses/. /blog/ shows all articles, and /news/ shows news links.

## Events and milestones

The History page timeline comes from `_data/milestones.yml`. Add an entry like:

```yaml
- when: "March 2027"
  date: "2027-03"
  kind: event        # or milestone, for this site's own milestones
  text: "What happened, with an <a href=\"https://...\">optional link</a>."
```

## Edit pages

| Page | File |
|---|---|
| Home | `index.html` |
| What is a carbon handprint? | `what-is-a-carbon-handprint.md` |
| Grow your handprint | `grow-your-handprint.md` |
| History | `history.md` |
| About | `about.md` |
| Menu and footer | `_includes/header.html`, `_includes/footer.html` |
| Colours and fonts | `assets/css/main.css` |

## Preview locally (optional)

```bash
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000.

## Licence

Content is shared under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
