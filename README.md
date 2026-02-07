# 📰 Tech Daily

A static website that aggregates daily tech news from GitHub Trending and Hacker News.

## 🌟 Features

- **Dark Mode** - Easy on the eyes, perfect for late-night reading
- **Responsive Design** - Works great on desktop and mobile
- **GitHub Trending** - Focus on Cloud, Go, Python, DevOps, and K8s repos
- **Hacker News** - Top 10 stories with points and comments
- **Clean Typography** - Modern card-based layout
- **Zero JavaScript** - Pure HTML/CSS for fast loading

## 📁 Structure

```
tech-daily/
├── index.html           # Main page
├── css/
│   └── style.css        # Dark theme styles
├── js/
│   └── app.js           # (Reserved for future use)
├── scripts/
│   └── generate.sh      # Content regeneration script
└── README.md            # This file
```

## 🚀 Usage

### View Locally

Just open `index.html` in your browser:
```bash
open index.html
# or
xdg-open index.html
```

### Regenerate Content

To fetch fresh data and regenerate the page:
```bash
chmod +x scripts/generate.sh
./scripts/generate.sh
```

## 🎨 Design

- **Color Palette**: GitHub-inspired dark theme
- **Typography**: System fonts for fast loading
- **Layout**: CSS Grid for responsive cards
- **Interactions**: Subtle hover effects

## 🔧 Customization

Edit `css/style.css` to customize:
- Colors via CSS variables (`:root`)
- Card styling (`.card`)
- Grid layout (`.cards-grid`)

## 📊 Content Sources

- [GitHub Trending](https://github.com/trending) - Daily trending repositories
- [Hacker News API](https://hacker-news.firebaseio.com/) - Top stories

## 📝 License

MIT - Feel free to use and modify!

---

Made with ❤️ for Duc | Updated: February 7, 2026
