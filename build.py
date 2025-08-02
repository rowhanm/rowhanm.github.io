#!/usr/bin/env python3
"""
Build script for rowhanm.github.io
Automatically generates article list from sections/ directory
"""

import os
import re
from datetime import datetime

def extract_article_info(filepath):
    """Extract title and description from article HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from first h4 tag
    title_match = re.search(r'<h4[^>]*>(.*?)</h4>', content, re.IGNORECASE | re.DOTALL)
    if not title_match:
        # Fallback to filename if no h4 found
        filename = os.path.basename(filepath).replace('.html', '').replace('_', ' ').title()
        title = filename
    else:
        title = title_match.group(1).strip()
        # Clean up any HTML tags in title
        title = re.sub(r'<[^>]+>', '', title)
    
    # Extract first paragraph as description
    desc_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
    description = ""
    if desc_match:
        description = desc_match.group(1).strip()
        # Clean up HTML tags and limit length
        description = re.sub(r'<[^>]+>', '', description)
        if len(description) > 200:
            description = description[:200] + "..."
    
    # Extract image if present
    img_match = re.search(r'<img[^>]+src="([^"]*)"[^>]*>', content)
    image = img_match.group(1) if img_match else None
    
    # Get file modification time as date
    mtime = os.path.getmtime(filepath)
    
    return {
        'filename': os.path.basename(filepath),
        'title': title,
        'description': description,
        'image': image,
        'date': mtime
    }

def scan_articles():
    """Scan sections/ directory for article files."""
    articles = []
    sections_dir = 'sections'
    
    if not os.path.exists(sections_dir):
        print(f"Warning: {sections_dir} directory not found")
        return articles
    
    for filename in os.listdir(sections_dir):
        if filename.endswith('.html') and not filename.startswith('.'):
            # Skip navigation pages
            if filename in ['about.html', 'experience.html', 'papers.html']:
                continue
                
            filepath = os.path.join(sections_dir, filename)
            try:
                article_info = extract_article_info(filepath)
                articles.append(article_info)
            except Exception as e:
                print(f"Warning: Could not process {filename}: {e}")
    
    # Sort by modification time, newest first
    articles.sort(key=lambda x: x['date'], reverse=True)
    return articles

def generate_article_html(articles):
    """Generate HTML for article list."""
    html_parts = []
    
    for article in articles:
        # Build article HTML
        article_html = f"""
          <li><h5><a href="./sections/{article['filename']}">{article['title']}</a></h5>
            <p>{article['description']}"""
        
        if article['image']:
            # Ensure image path is correct
            img_src = article['image']
            if not img_src.startswith('images/') and not img_src.startswith('./images/'):
                if img_src.startswith('../images/'):
                    img_src = img_src[3:]  # Remove ../ prefix
            article_html += f"""
            <img src="{img_src}" alt="{article['title']}">"""
        
        article_html += """
            </p>
          </li>

          <br>
"""
        html_parts.append(article_html)
    
    return ''.join(html_parts)

def update_index_html(articles):
    """Update index.html with generated article list."""
    index_path = 'index.html'
    
    if not os.path.exists(index_path):
        print(f"Error: {index_path} not found")
        return False
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate new article HTML
    article_html = generate_article_html(articles)
    
    # Find the articles section and replace it
    # Look for the pattern between <ul> and the papers section
    pattern = r'(<ul>\s*<br>\s*)(.*?)(\s*</ul>\s*<br>\s*<h4>Published Papers/Longer Reads</h4>)'
    
    replacement = f'\\1\n{article_html.rstrip()}\n        \\3'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        # Backup original
        with open(f'{index_path}.backup', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Write updated content
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Updated {index_path} with {len(articles)} articles")
        return True
    else:
        print("No changes needed in index.html")
        return False

def main():
    """Main build function."""
    print("Building article list...")
    
    articles = scan_articles()
    
    if not articles:
        print("No articles found in sections/ directory")
        return
    
    print(f"Found {len(articles)} articles:")
    for article in articles:
        print(f"  - {article['title']}")
    
    success = update_index_html(articles)
    
    if success:
        print("\n✓ Build completed successfully!")
        print("Your index.html has been updated with the latest articles.")
    else:
        print("\n! Build completed but no changes were made.")

if __name__ == "__main__":
    main()
