# 🎵 Lyrically

A full-stack AI-powered lyrics transcription application that extracts lyrics from YouTube videos or uploaded audio files using OpenAI Whisper API, built with React and Flask.

## ✨ Features

- 🎬 **YouTube URL Transcription** - Paste any YouTube URL to automatically extract and transcribe audio to lyrics

- 📁 **Audio File Upload** - Upload MP3 files directly for instant transcription

- 🎤 **OpenAI Whisper Integration** - Powered by OpenAI's Whisper-1 model for accurate speech-to-text transcription

- 🎧 **Audio Playback** - Listen to the extracted audio while viewing transcribed lyrics

- 🧹 **Automatic Cleanup** - Temporary files are automatically removed after processing

- 📝 **Title Detection** - Automatically extracts song titles from YouTube videos or uploaded files

## 🛠️ Tech Stack

### Frontend

- **React 19.1.0** - Modern UI library

- **React Scripts 5.0.1** - Build tooling and development server

- **Axios 1.10.0** - HTTP client for API requests

### Backend

- **Python 3** - Programming language

- **Flask 3.0.0** - Lightweight web framework

- **Flask-CORS 4.0.0** - Cross-Origin Resource Sharing support

- **OpenAI API 1.35.0** - Whisper-1 model for audio transcription

- **yt-dlp 2023.12.30** - YouTube video/audio extraction

- **FFmpeg** - Audio format conversion (via yt-dlp)

- **python-dotenv 1.0.0** - Environment variable management

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ installed

- Node.js 18+ installed

- FFmpeg installed (required for audio processing)

- OpenAI API key


## 🔧 API Endpoints

- `GET /api/ping` - Health check endpoint

- `GET /health` - Service health status

- `POST /api/transcribe` - Transcribe audio from YouTube URL
  - Body: `{ "url": "https://youtube.com/watch?v=..." }`

- `POST /api/upload` - Transcribe uploaded MP3 file
  - Body: `FormData` with `file` field (max 50MB)

- `GET /temp/<filename>` - Serve temporary audio files

## 📝 Notes

- Maximum file upload size: 50MB

- Temporary audio files are automatically cleaned up after processing

- FFmpeg must be installed on your system for YouTube audio extraction to work

- The application uses OpenAI's Whisper-1 model, which charges per minute of audio transcribed
