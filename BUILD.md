# Article Build System

## Quick Start

To add a new article:

1. Create `sections/your-article-name.html`
2. Make sure it has an `<h4>` tag with the title
3. Run `python3 build.py`
4. Done! Your `index.html` is automatically updated

## Article Structure

Your article HTML should follow this pattern:

```html
<!doctype html>
<html lang="en" class="h-100">
  <head>
    <!-- Standard head section -->
  </head>
  <body class="d-flex flex-column h-100">
    <main role="main" class="flex-shrink-0">
      <div class="container">
        <!-- Navigation section -->
        <div>
          <h4 style="text-align: center">Your Article Title</h4>
          <p>Your first paragraph becomes the description...</p>
          <img src="../images/your-image.png" alt="Alt text">
          <!-- Rest of your content -->
        </div>
      </div>
    </main>
  </body>
</html>
```

## Build Script Features

- **Automatic title extraction** from first `<h4>` tag
- **Description generation** from first paragraph
- **Image detection** for preview thumbnails
- **Date sorting** by file modification time
- **Backup creation** (creates `.backup` files)
- **Smart filtering** (skips navigation pages like `about.html`)

## Commands

```bash
# Build articles list
python3 build.py

# Check what articles were found
python3 build.py  # Shows list of found articles

# Restore from backup if needed
cp index.html.backup index.html
```

## File Organization

```
/
├── sections/           # Your article HTML files
│   ├── submod.html    # Article 1
│   ├── books.html     # Article 2
│   └── new-post.html  # New articles go here
├── images/            # Article images
├── build.py          # Build script
└── index.html        # Auto-updated homepage
```

## Tips

- Keep images in `images/` directory
- Use descriptive filenames for articles
- The first `<h4>` becomes the article title
- The first `<p>` becomes the description (truncated at 200 chars)
- Articles are sorted by modification time (newest first)

Your site stays ultra-fast with zero JavaScript - everything is pre-built!
