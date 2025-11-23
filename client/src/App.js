import React, { useState, useRef } from "react"
import axios from "axios"
import "./App.css"

// Get API URL from environment variable or default to localhost
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5001"

// Add error handling for API URL
if (!API_URL) {
  console.error("REACT_APP_API_URL is not set")
}

function App() {
 const [url, setUrl] = useState("")
 const [file, setFile] = useState(null)
 const [lyrics, setLyrics] = useState("")
 const [songTitle, setSongTitle] = useState("")
 const [audioUrl, setAudioUrl] = useState("")
 const [loading, setLoading] = useState(false)
 const [error, setError] = useState("")
 const [isPlaying, setIsPlaying] = useState(false)
 const audioRef = useRef(null)

 const handleSubmit = async () => {
   setLoading(true)
   setLyrics("")
   setSongTitle("")
   setAudioUrl("")
   setError("")
   setIsPlaying(false)

   // Stop any playing audio
   if (audioRef.current) {
     audioRef.current.pause()
     audioRef.current.currentTime = 0
   }

   try {
     let res
     if (file) {
       const formData = new FormData()
       formData.append("file", file)
       res = await axios.post(`${API_URL}/api/upload`, formData, {
         headers: { "Content-Type": "multipart/form-data" }
       })
     } else if (url) {
       res = await axios.post(`${API_URL}/api/transcribe`, { url })
     } else {
       setError("Please provide a YouTube URL or upload an MP3 file.")
       return
     }

     setLyrics(res.data.lyrics)
     setSongTitle(res.data.title)
     setAudioUrl(res.data.audioUrl)

   } catch (err) {
     console.error(err)
     setError("Something went wrong. Please try again.")
   } finally {
     setLoading(false)
   }
 }

 const toggleAudio = () => {
   if (!audioRef.current) return
   if (isPlaying) {
     audioRef.current.pause()
   } else {
     audioRef.current.play()
   }
   setIsPlaying(!isPlaying)
 }

 return (
   <div className="container">
     <h1 className="title">🎵 AI Lyrics Transcriber</h1>

     <input
       className="input"
       type="text"
       placeholder="Paste a YouTube URL..."
       value={url}
       onChange={(e) => setUrl(e.target.value)}
     />

     <input
       className="input"
       type="file"
       accept=".mp3"
       onChange={(e) => setFile(e.target.files[0])}
     />

     <button className="button" onClick={handleSubmit} disabled={loading}>
       {loading ? "Transcribing..." : "Generate Lyrics"}
     </button>

     {error && <p className="error">{error}</p>}

     {songTitle && <h2 className="subtitle">🎶 {songTitle}</h2>}
     {audioUrl && (
       <div>

         <audio
           ref={audioRef}
           src={audioUrl}
           onEnded={() => setIsPlaying(false)}
         />
       </div>
     )}
     {lyrics && (
       <div className="lyrics-box">
         {lyrics}
       </div>
     )}
   </div>
 )
}

export default App



