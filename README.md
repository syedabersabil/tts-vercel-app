# Syed's TTS Studio (Vercel Ready)

A clean, fast Text-to-Speech web app built specially for **Vercel** deployment.

- Backend: Python (Edge-TTS) serverless function at `/api/tts`
- Frontend: Pure HTML/CSS/JS (`index.html`) optimized for mobile + desktop
- Voices: Hindi, Hinglish (Indian English) and US English

## Deploy to Vercel

1. **Import this repo** from GitHub into [Vercel](https://vercel.com)
2. Vercel will auto-detect `vercel.json`
3. Framework preset: `Other`
4. Click **Deploy**

## API Endpoint

`POST /api/tts`

```json
{
  "text": "string (required)",
  "voice": "hi_female | hi_male | en_in_female | en_in_male | en_us_female | en_us_male",
  "rate": "-40 to 40 (int)",
  "pitch": "-40 to 40 (int)"
}
```

Response: `audio/mpeg` binary (MP3 stream).

## Local Dev (optional)

```bash
# Create virtual env and install deps
pip install edge-tts

# Run local test server
python api/tts.py  # or use any minimal HTTP wrapper
```

Then open `index.html` in a browser and point `/api/tts` to your local endpoint with a proxy or by editing the fetch URL.
