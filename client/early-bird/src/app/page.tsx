"use client"
import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { Loader2 } from "lucide-react"
import Image from "next/image"

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [files, setFiles] = useState<string[]>([])
  const [audioBlobs, setAudioBlobs] = useState<{ [key: string]: Blob }>({})
  const [currentFileIndex, setCurrentFileIndex] = useState(-1)
  const [isRecording, setIsRecording] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const audioRef = useRef<HTMLAudioElement>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])

  // Load files and fetch audio blobs
  async function generatePodcast(event: React.FormEvent) {
    event.preventDefault()
    setLoading(true)
    
    try {
      // Get list of files
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })
      
      if (!response.ok) throw new Error('Failed to generate podcast')
      const data = await response.json()
      console.log(data)
      const fileDir = data.file_urls
      const fileList = Array.from({ length: 7 }, (_, i) => `${fileDir}/interaction_${i + 1}.mp3`)
      console.log(fileList)
      setFiles(fileList)

      // Fetch all audio blobs
      const blobs: { [key: string]: Blob } = {}
      for (let i = 0; i < fileList.length; i++) {
        const file = fileList[i]
        const audioResponse = await fetch(`http://localhost:8000/download/${fileDir}/${i + 1}`)
        if (!audioResponse.ok) throw new Error(`Failed to fetch ${file}`)
        blobs[file] = await audioResponse.blob()
      }
      setAudioBlobs(blobs)
      setCurrentFileIndex(0)
      setLoading(false)
        } catch (error) {
      console.error('Error:', error)
      setLoading(false)
        }
      }

  // Handle audio playback
  useEffect(() => {
    if (currentFileIndex >= 0 && currentFileIndex < files.length && audioRef.current) {
      const currentFile = files[currentFileIndex]
      const blob = audioBlobs[currentFile]
      if (blob) {
        audioRef.current.src = URL.createObjectURL(blob)
        audioRef.current.play()
        setIsPlaying(true)
      }
    }
  }, [currentFileIndex, files, audioBlobs])

  // Handle audio ending
  const handleAudioEnd = () => {
    if (currentFileIndex < files.length - 1) {
      setCurrentFileIndex(prev => prev + 1)
    } else {
      setIsPlaying(false)
    }
  }

  // Start recording interrupt
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const recorder = new MediaRecorder(stream)
      mediaRecorderRef.current = recorder
      chunksRef.current = []

      recorder.ondataavailable = (e) => {
        chunksRef.current.push(e.data)
      }

      recorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/mp3' })
        
        // Send interrupt to backend
        const formData = new FormData()
        formData.append('audio', audioBlob)
        
        try {
          const response = await fetch('http://localhost:8000/interrupt', {
            method: 'POST',
            body: formData
          })
          
          if (!response.ok) throw new Error('Failed to process interrupt')
          
          const responseBlob = await response.blob()
          // Insert response audio into playlist
          const newFiles = [...files]
          const responseFileName = `interrupt-response-${Date.now()}.mp3`
          newFiles.splice(currentFileIndex + 1, 0, responseFileName)
          setFiles(newFiles)
          setAudioBlobs(prev => ({
            ...prev,
            [responseFileName]: responseBlob
          }))
        } catch (error) {
          console.error('Error processing interrupt:', error)
        }
      }

      recorder.start()
      setIsRecording(true)
    } catch (error) {
      console.error('Error starting recording:', error)
    }
  }

  // Stop recording interrupt
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="text-center space-y-4">
        <Image
          src="/logo.jpg"
          alt="EarlyBird Logo"
          width={64}
          height={64}
          className="mx-auto dark:invert"
        />
        <h1 className="text-4xl font-bold">Welcome to EarlyBird</h1>
        <p className="text-xl text-muted-foreground">Start your day with personalized podcasts</p>
      </div>

      <form onSubmit={generatePodcast} className="text-center">
        <Button type="submit" size="lg" disabled={loading}>
          {loading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Generating Podcast...
            </>
          ) : (
            "Generate Today's Podcast"
          )}
        </Button>
      </form>

      {files.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Your Morning Tech Podcast</CardTitle>
            <CardDescription>
              {isPlaying ? `Playing part ${currentFileIndex + 1} of ${files.length}` : 'Ready to play'}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <audio
              ref={audioRef}
              onEnded={handleAudioEnd}
              controls
              className="w-full"
            />
            
            {isPlaying && currentFileIndex < 6 && (
              <div className="flex justify-center gap-4">
                <Button
                  onClick={startRecording}
                  disabled={isRecording}
                  className="bg-red-500 hover:bg-red-600"
                >
                  Start Interrupt
                </Button>
                <Button
                  onClick={stopRecording}
                  disabled={!isRecording}
                >
                  Stop Interrupt
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}