from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import base64
import json
import re

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_outfit_recommendations(gender, occasion, skin_tone, budget, style_vibe):
    """Generate outfit recommendations using Claude API via the built-in Anthropic API."""
    import urllib.request
    
    prompt = f"""You are a world-class personal fashion stylist. Generate a complete outfit recommendation in JSON format.

User Profile:
- Gender: {gender}
- Occasion: {occasion}
- Skin Tone: {skin_tone}
- Budget (INR): {budget}
- Style Vibe: {style_vibe}

Return ONLY valid JSON (no markdown, no extra text) with this exact structure:
{{
  "outfit_title": "Creative outfit name",
  "style_summary": "2-sentence summary of the look",
  "color_palette": {{
    "primary": "#hexcode",
    "secondary": "#hexcode",
    "accent": "#hexcode",
    "primary_name": "color name",
    "secondary_name": "color name",
    "accent_name": "color name"
  }},
  "items": [
    {{
      "category": "Top/Shirt/Blouse",
      "name": "Specific item name",
      "color": "color",
      "style": "style details",
      "brand_suggestion": "brand",
      "price_range": "INR range",
      "amazon_search": "search query for amazon.in",
      "myntra_search": "search query for myntra",
      "why_it_works": "explanation"
    }},
    {{
      "category": "Bottom/Pants/Skirt",
      "name": "Specific item name",
      "color": "color",
      "style": "style details",
      "brand_suggestion": "brand",
      "price_range": "INR range",
      "amazon_search": "search query",
      "myntra_search": "search query",
      "why_it_works": "explanation"
    }},
    {{
      "category": "Footwear",
      "name": "Specific item name",
      "color": "color",
      "style": "style details",
      "brand_suggestion": "brand",
      "price_range": "INR range",
      "amazon_search": "search query",
      "myntra_search": "search query",
      "why_it_works": "explanation"
    }},
    {{
      "category": "Accessory",
      "name": "Key accessory",
      "color": "color",
      "style": "style details",
      "brand_suggestion": "brand",
      "price_range": "INR range",
      "amazon_search": "search query",
      "myntra_search": "search query",
      "why_it_works": "explanation"
    }}
  ],
  "hairstyle": {{
    "name": "hairstyle name",
    "description": "how to style",
    "suits_skin_tone": "why this works for their skin tone"
  }},
  "styling_tips": ["tip 1", "tip 2", "tip 3"],
  "color_matching_explanation": "Detailed explanation of why these colors work together and suit the skin tone",
  "wardrobe_compatibility": "How this outfit can be mixed with other basics"
}}"""

    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1500,
        "messages": [{"role": "user", "content": prompt}]
    }).encode('utf-8')

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode('utf-8'))
            text = data['content'][0]['text']
            # Clean up any markdown fences
            text = re.sub(r'```json\s*', '', text)
            text = re.sub(r'```\s*', '', text)
            return json.loads(text.strip())
    except Exception as e:
        return get_fallback_recommendations(gender, occasion, skin_tone, budget, style_vibe)

def get_fallback_recommendations(gender, occasion, skin_tone, budget, style_vibe):
    """Fallback static recommendations if API fails."""
    base = {
        "outfit_title": f"The {occasion} Essential",
        "style_summary": f"A carefully curated {style_vibe.lower()} look perfect for {occasion.lower()}. Colors chosen specifically to complement a {skin_tone.lower()} skin tone beautifully.",
        "color_palette": {
            "primary": "#2C3E50",
            "secondary": "#ECF0F1",
            "accent": "#E67E22",
            "primary_name": "Midnight Navy",
            "secondary_name": "Cloud White",
            "accent_name": "Burnt Orange"
        },
        "items": [
            {
                "category": "Top",
                "name": "Classic Oxford Shirt",
                "color": "White",
                "style": "Crisp cotton oxford, slim fit",
                "brand_suggestion": "Arrow / Van Heusen",
                "price_range": "₹800 - ₹2,000",
                "amazon_search": "white oxford shirt men slim fit",
                "myntra_search": "white formal shirt",
                "why_it_works": "Timeless white works beautifully with all skin tones and anchors any outfit."
            },
            {
                "category": "Bottom",
                "name": "Tailored Chinos",
                "color": "Navy Blue",
                "style": "Mid-rise, slim tapered fit",
                "brand_suggestion": "Bonobos / H&M",
                "price_range": "₹1,200 - ₹3,500",
                "amazon_search": "navy chinos slim fit",
                "myntra_search": "navy blue chinos",
                "why_it_works": "Navy creates a sophisticated contrast while remaining versatile."
            },
            {
                "category": "Footwear",
                "name": "Leather Loafers",
                "color": "Tan Brown",
                "style": "Penny loafer, genuine leather",
                "brand_suggestion": "Red Chief / Clarks",
                "price_range": "₹2,000 - ₹5,000",
                "amazon_search": "tan leather loafers men",
                "myntra_search": "tan loafers leather",
                "why_it_works": "Tan complements warm skin undertones and adds richness to the outfit."
            },
            {
                "category": "Accessory",
                "name": "Minimalist Watch",
                "color": "Silver/Black",
                "style": "Slim case, leather strap",
                "brand_suggestion": "Fossil / Titan",
                "price_range": "₹2,500 - ₹8,000",
                "amazon_search": "minimalist watch silver leather",
                "myntra_search": "analog watch slim",
                "why_it_works": "A clean watch elevates any outfit without overpowering it."
            }
        ],
        "hairstyle": {
            "name": "Clean Side Part",
            "description": "Apply light pomade to slightly damp hair, comb to one side with a clean part.",
            "suits_skin_tone": f"A neat, structured style balances features and complements {skin_tone.lower()} tones."
        },
        "styling_tips": [
            "Tuck the shirt in for a polished look, or half-tuck for casual occasions.",
            "Roll sleeves to the elbow for a relaxed, stylish touch.",
            "Add a slim belt in dark brown to tie the look together."
        ],
        "color_matching_explanation": f"Navy and white create a high-contrast pairing that works universally. The tan accent warms up the palette, particularly flattering for {skin_tone.lower()} skin tones by adding complementary warmth.",
        "wardrobe_compatibility": "These pieces are wardrobe workhorses — the chinos pair with any shirt, the loafers work from casual to semi-formal, and the white shirt goes everywhere."
    }
    return base

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        gender = data.get('gender', 'Male')
        occasion = data.get('occasion', 'Casual')
        skin_tone = data.get('skin_tone', 'Medium')
        budget = data.get('budget', '2000')
        style_vibe = data.get('style_vibe', 'Classic')

        result = get_outfit_recommendations(gender, occasion, skin_tone, budget, style_vibe)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analyze-outfit', methods=['POST'])
def analyze_outfit():
    """Analyze user-uploaded outfit image."""
    import urllib.request
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400

        file = request.files['image']
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400

        # Read image and encode to base64
        img_data = file.read()
        b64_img = base64.b64encode(img_data).decode('utf-8')
        ext = file.filename.rsplit('.', 1)[1].lower()
        media_type = f"image/{'jpeg' if ext in ['jpg','jpeg'] else ext}"

        prompt = """Analyze this outfit image as a professional fashion stylist. Return ONLY valid JSON (no markdown) with:
{
  "outfit_detected": "description of what you see",
  "color_analysis": "colors in the outfit",
  "style_score": 8,
  "occasion_suitability": ["suitable occasions"],
  "strengths": ["what works well"],
  "improvements": ["specific suggestions to improve"],
  "color_suggestions": ["better color alternatives"],
  "accessory_suggestions": ["accessories that would elevate this look"],
  "overall_feedback": "2-3 sentence honest style assessment"
}"""

        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": b64_img}},
                    {"type": "text", "text": prompt}
                ]
            }]
        }).encode('utf-8')

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode('utf-8'))
            text = data['content'][0]['text']
            text = re.sub(r'```json\s*', '', text)
            text = re.sub(r'```\s*', '', text)
            result = json.loads(text.strip())
            return jsonify({'success': True, 'data': result})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("✨ Style Sense AI — Running!")
    print("="*50)
    print("🌐 Open: http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
