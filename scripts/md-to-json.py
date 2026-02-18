#!/usr/bin/env python3
"""
Convert ai-daily-digest markdown output to JSON for the website.
Usage: python3 md-to-json.py /path/to/digest.md > data/blog-digest.json
"""

import sys
import json
import re
from datetime import datetime

def parse_digest(md_content: str) -> dict:
    result = {
        "generatedAt": datetime.now().strftime("%Y-%m-%d"),
        "highlights": "",
        "topPicks": [],
        "categories": {}
    }
    
    lines = md_content.split('\n')
    current_section = None
    current_article = None
    in_highlights = False
    in_top_picks = False
    current_category = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Detect sections
        if '## 📝' in line or 'Điểm nổi bật' in line:
            in_highlights = True
            in_top_picks = False
            continue
        elif '## 🏆' in line or 'Bài đọc tiêu biểu' in line:
            in_highlights = False
            in_top_picks = True
            continue
        elif line.startswith('## 📊') or 'Tổng quan' in line:
            in_highlights = False
            in_top_picks = False
            continue
        elif line.startswith('## ') and ('🤖' in line or '🔒' in line or '⚙️' in line or '🛠' in line or '💡' in line or '📝' in line):
            in_highlights = False
            in_top_picks = False
            # Category section
            current_category = line.replace('## ', '').strip()
            result["categories"][current_category] = []
            continue
        
        # Parse highlights
        if in_highlights and line and not line.startswith('#') and not line.startswith('---'):
            result["highlights"] += line + " "
        
        # Parse top picks (🥇, 🥈, 🥉)
        if in_top_picks:
            if line.startswith('🥇') or line.startswith('🥈') or line.startswith('🥉'):
                if current_article:
                    result["topPicks"].append(current_article)
                # Extract title
                title_match = re.search(r'\*\*(.+?)\*\*', line)
                current_article = {
                    "title": title_match.group(1) if title_match else line,
                    "titleVi": title_match.group(1) if title_match else line,
                    "link": "",
                    "source": "",
                    "category": "",
                    "score": 0,
                    "summary": "",
                    "reason": ""
                }
            elif current_article:
                # Parse link line
                if line.startswith('[') and '](' in line:
                    link_match = re.search(r'\[(.+?)\]\((.+?)\)', line)
                    if link_match:
                        current_article["title"] = link_match.group(1)
                        current_article["link"] = link_match.group(2)
                    source_match = re.search(r'— (.+?) ·', line)
                    if source_match:
                        current_article["source"] = source_match.group(1)
                    cat_match = re.search(r'· ([🤖🔒⚙️🛠💡📝].+?)$', line)
                    if cat_match:
                        current_article["category"] = cat_match.group(1)
                # Parse summary (blockquote)
                elif line.startswith('>'):
                    current_article["summary"] = line[1:].strip()
                # Parse reason
                elif 'Tại sao nên đọc' in line or '为什么值得读' in line:
                    reason_match = re.search(r':\s*(.+)$', line)
                    if reason_match:
                        current_article["reason"] = reason_match.group(1)
                # Parse score
                elif '⭐' in line:
                    score_match = re.search(r'⭐\s*(\d+)/30', line)
                    if score_match:
                        current_article["score"] = int(score_match.group(1))
        
        # Parse category articles
        if current_category and line.startswith('### '):
            if current_article and current_category:
                result["categories"][current_category].append(current_article)
            title_match = re.search(r'###\s*\d+\.\s*(.+)', line)
            current_article = {
                "title": title_match.group(1) if title_match else "",
                "titleVi": title_match.group(1) if title_match else "",
                "link": "",
                "source": "",
                "score": 0,
                "summary": ""
            }
        elif current_category and current_article:
            if line.startswith('[') and '](' in line:
                link_match = re.search(r'\[(.+?)\]\((.+?)\)', line)
                if link_match:
                    current_article["title"] = link_match.group(1)
                    current_article["link"] = link_match.group(2)
                source_match = re.search(r'— \*\*(.+?)\*\*', line)
                if source_match:
                    current_article["source"] = source_match.group(1)
                score_match = re.search(r'⭐\s*(\d+)/30', line)
                if score_match:
                    current_article["score"] = int(score_match.group(1))
            elif line.startswith('>'):
                current_article["summary"] = line[1:].strip()
    
    # Add last article
    if current_article and in_top_picks:
        result["topPicks"].append(current_article)
    elif current_article and current_category:
        result["categories"][current_category].append(current_article)
    
    # Clean up
    result["highlights"] = result["highlights"].strip()
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 md-to-json.py /path/to/digest.md", file=sys.stderr)
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    result = parse_digest(md_content)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
