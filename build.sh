#!/bin/bash

echo "🚀 Building Lyrically for deployment..."

# Build frontend
echo "📦 Building React frontend..."
cd client
npm install
npm run build
cd ..

# Check backend dependencies
echo "🐍 Checking Python backend dependencies..."
cd server
pip install -r requirements.txt
cd ..

echo "✅ Build complete!"
echo ""
echo "📋 Next steps:"
echo "1. Deploy backend to Render/Heroku"
echo "2. Deploy frontend to Vercel/Netlify"
echo "3. Set environment variables"
echo "4. Test the deployment"
echo ""
echo "📖 See DEPLOYMENT.md for detailed instructions" 