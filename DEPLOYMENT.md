# Deployment Guide for Lyrically

This guide covers deploying both the backend (Flask) and frontend (React) components of the Lyrically application.

## Prerequisites

- GitHub repository with your code
- OpenAI API key
- FFmpeg installed on your system (for local development)

## Backend Deployment Options

### Option 1: Render (Recommended)

1. **Sign up for Render** at https://render.com
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure the service:**
   - **Name:** lyrically-backend
   - **Root Directory:** `server`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free (or paid for better performance)

5. **Set Environment Variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `FLASK_ENV`: `production`
   - `BASE_URL`: Your Render URL (e.g., `https://lyrically-backend.onrender.com`)
   - `ALLOWED_ORIGINS`: Your frontend URL (e.g., `https://lyrically-frontend.vercel.app`)

6. **Deploy**

### Option 2: Heroku

1. **Install Heroku CLI**
2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku app:**
   ```bash
   cd server
   heroku create lyrically-backend
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set OPENAI_API_KEY=your_api_key
   heroku config:set FLASK_ENV=production
   heroku config:set BASE_URL=https://lyrically-backend.herokuapp.com
   heroku config:set ALLOWED_ORIGINS=https://your-frontend-url.com
   ```

5. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## Frontend Deployment Options

### Option 1: Vercel (Recommended)

1. **Sign up for Vercel** at https://vercel.com
2. **Import your GitHub repository**
3. **Configure the project:**
   - **Framework Preset:** Create React App
   - **Root Directory:** `client`
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`

4. **Set Environment Variables:**
   - `REACT_APP_API_URL`: Your backend URL (e.g., `https://lyrically-backend.onrender.com`)

5. **Deploy**

### Option 2: Netlify

1. **Sign up for Netlify** at https://netlify.com
2. **Import your GitHub repository**
3. **Configure the build:**
   - **Base directory:** `client`
   - **Build command:** `npm run build`
   - **Publish directory:** `build`

4. **Set Environment Variables:**
   - `REACT_APP_API_URL`: Your backend URL

5. **Deploy**

## Local Development Setup

### Backend
```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd client
npm install
npm start
```

## Environment Variables

### Backend (.env file in server/)
```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
BASE_URL=http://127.0.0.1:5001
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env file in client/)
```
REACT_APP_API_URL=http://localhost:5001
```

## Troubleshooting

### Common Issues

1. **CORS Errors:** Make sure `ALLOWED_ORIGINS` includes your frontend URL
2. **API Key Issues:** Verify your OpenAI API key is set correctly
3. **Build Failures:** Check that all dependencies are in requirements.txt
4. **Audio Processing:** Ensure FFmpeg is available on your deployment platform

### Testing Deployment

1. **Test backend endpoints:**
   ```bash
   curl https://your-backend-url.com/api/ping
   ```

2. **Test frontend:** Visit your frontend URL and try uploading a file or pasting a YouTube URL

## Security Notes

- Never commit API keys to version control
- Use environment variables for all sensitive data
- Enable HTTPS in production
- Consider rate limiting for API endpoints 