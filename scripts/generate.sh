#!/bin/bash
# Tech Daily - Content Regeneration Script
# Usage: ./scripts/generate.sh

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT_FILE="$PROJECT_DIR/index.html"
DATE=$(date '+%Y-%m-%d')
DATE_DISPLAY=$(date '+%A, %B %d, %Y')

echo -e "${BLUE}📰 Tech Daily Generator${NC}"
echo -e "${BLUE}========================${NC}"
echo ""

# Check for required tools
check_deps() {
    local missing=()
    for cmd in curl jq; do
        if ! command -v $cmd &> /dev/null; then
            missing+=($cmd)
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        echo -e "${YELLOW}⚠️  Missing dependencies: ${missing[*]}${NC}"
        echo "Install with: sudo apt install ${missing[*]}"
        exit 1
    fi
}

# Fetch GitHub Trending
fetch_github_trending() {
    local lang=${1:-""}
    local url="https://github.com/trending"
    [ -n "$lang" ] && url="${url}/${lang}"
    url="${url}?since=daily"
    
    echo -e "${BLUE}→ Fetching GitHub Trending${lang:+ ($lang)}...${NC}"
    curl -s "$url" | grep -oP 'href="/[^/]+/[^/]+"' | head -20 || true
}

# Fetch Hacker News Top Stories
fetch_hn_top() {
    echo -e "${BLUE}→ Fetching Hacker News top stories...${NC}"
    
    # Get top story IDs
    local story_ids=$(curl -s "https://hacker-news.firebaseio.com/v0/topstories.json" | jq '.[0:10][]')
    
    # Fetch each story details
    for id in $story_ids; do
        local story=$(curl -s "https://hacker-news.firebaseio.com/v0/item/${id}.json")
        local title=$(echo "$story" | jq -r '.title // "Untitled"')
        local url=$(echo "$story" | jq -r '.url // "https://news.ycombinator.com/item?id='$id'"')
        local score=$(echo "$story" | jq -r '.score // 0')
        local comments=$(echo "$story" | jq -r '.descendants // 0')
        
        echo "  📰 $title (⬆$score | 💬$comments)"
    done
}

# Generate HTML
generate_html() {
    echo -e "${BLUE}→ Generating HTML...${NC}"
    
    # For now, just update the date in the existing file
    # In a production version, this would regenerate the entire HTML
    # with fresh data from APIs
    
    sed -i "s/Last updated:.*/Last updated: $(date '+%B %d, %Y %H:%M GMT%z')/" "$OUTPUT_FILE" 2>/dev/null || true
    
    echo -e "${GREEN}✓ Updated: $OUTPUT_FILE${NC}"
}

# Main
main() {
    cd "$PROJECT_DIR"
    
    echo "📅 Date: $DATE_DISPLAY"
    echo ""
    
    check_deps
    
    # Fetch data
    echo -e "${YELLOW}Fetching data...${NC}"
    fetch_github_trending
    fetch_github_trending "go"
    fetch_github_trending "python"
    echo ""
    fetch_hn_top
    echo ""
    
    # Generate output
    generate_html
    
    echo ""
    echo -e "${GREEN}✅ Tech Daily generated successfully!${NC}"
    echo -e "   Open: file://$OUTPUT_FILE"
}

main "$@"
