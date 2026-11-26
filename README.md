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

Images: upload them to `assets/images/` and use `![Description](/assets/images/photo.jpg)`.

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
