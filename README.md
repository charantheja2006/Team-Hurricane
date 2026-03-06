# Style Sense AI 🌟
### AI-Powered Personal Fashion Styling Advisor

A full-stack web application that provides personalized outfit recommendations based on skin tone, occasion, budget, and style vibe. Built with Flask + Claude AI (Anthropic API).

---

## Features

- **Outfit Generator** — Get complete outfit recommendations (top, bottom, shoes, accessories) tailored to your skin tone, occasion, and budget
- **Color Matching** — AI-selected color palettes that complement your skin tone
- **Shop Links** — Direct links to Amazon.in, Myntra, and Flipkart for every item
- **Outfit Analyzer** — Upload a photo of your outfit and get AI-powered feedback, style score, and improvement suggestions
- **Hairstyle Tips** — Matching hairstyle recommendations
- **Wardrobe Tips** — How to mix the outfit with existing pieces

---

## Tech Stack

- **Backend**: Python 3.8+, Flask, Flask-CORS
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI**: Anthropic Claude API (claude-sonnet-4-20250514)
- **Fonts**: Playfair Display + DM Sans (Google Fonts)

---

## Project Structure

```
stylesense/
├── app.py                  # Flask backend + API routes
├── requirements.txt        # Python dependencies
├── .env                    # (Create this — API key goes here)
├── templates/
│   └── index.html          # Main HTML page
├── static/
│   ├── css/
│   │   └── style.css       # All styles
│   └── js/
│       └── app.js          # Frontend logic
└── uploads/                # Auto-created for image uploads
```

---

## Setup & Run

### 1. Clone / Extract the project

```bash
cd stylesense
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get your Anthropic API key

- Visit https://console.anthropic.com
- Sign up or log in
- Create an API key

### 5. The API key is pre-configured

The app uses Anthropic's API. If you need to set your own key, create a `.env` file:

```
ANTHROPIC_API_KEY=your_api_key_here
```

> **Note**: The app is pre-configured to use the Anthropic API without an explicit key when deployed in Claude's environment. For local deployment, you may need to configure the API key.

### 6. Run the application

```bash
python app.py
```

### 7. Open your browser

```
http://127.0.0.1:5000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main page |
| POST | `/api/recommend` | Generate outfit recommendations |
| POST | `/api/analyze-outfit` | Analyze uploaded outfit image |

### POST /api/recommend

```json
{
  "gender": "Male",
  "occasion": "Office",
  "skin_tone": "Medium",
  "budget": "3000",
  "style_vibe": "Smart Casual"
}
```

### POST /api/analyze-outfit

Multipart form with `image` field containing the outfit photo.

---

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| MAX_CONTENT_LENGTH | 16MB | Max upload size |
| Allowed formats | png, jpg, jpeg, gif, webp | Image types |
| AI Model | claude-sonnet-4-20250514 | Anthropic model |
| Max tokens | 1500 | Response length |

---

## Potential Enhancements

- User accounts and saved outfit history
- Virtual try-on with AR
- Seasonal trend integration
- Expanded skin tone categories (continuous mapping)
- Budget tracking across all items
- Wardrobe inventory management
- Social sharing of outfits

---

© 2025 Style Sense AI — Built for SmartBridge / Skill Wallet
