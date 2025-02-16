"use client"

import { useEffect, useRef } from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export default function PodcastGraph() {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext("2d")

    // Set canvas size
    canvas.width = 600
    canvas.height = 400

    // Draw graph
    ctx.fillStyle = "rgba(59, 130, 246, 0.5)" // Light blue
    ctx.strokeStyle = "rgb(59, 130, 246)" // Blue

    // Draw circles for podcasts
    const podcasts = [
      { x: 100, y: 100, r: 20, name: "Tech Talk" },
      { x: 200, y: 150, r: 25, name: "AI Insights" },
      { x: 300, y: 200, r: 30, name: "Web Weekly" },
      { x: 400, y: 100, r: 22, name: "Your Podcast" },
      { x: 500, y: 300, r: 18, name: "Dev Digest" },
    ]

    podcasts.forEach((podcast) => {
      ctx.beginPath()
      ctx.arc(podcast.x, podcast.y, podcast.r, 0, 2 * Math.PI)
      ctx.fill()
      ctx.stroke()

      // Add podcast names
      ctx.fillStyle = "black"
      ctx.font = "12px Arial"
      ctx.textAlign = "center"
      ctx.fillText(podcast.name, podcast.x, podcast.y + podcast.r + 15)
    })

    // Draw lines between podcasts
    ctx.beginPath()
    ctx.moveTo(podcasts[0].x, podcasts[0].y)
    podcasts.slice(1).forEach((podcast) => {
      ctx.lineTo(podcast.x, podcast.y)
    })
    ctx.stroke()
  }, [])

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Podcast Similarity Graph</h1>
      <Card>
        <CardHeader>
          <CardTitle>Your Podcast in Relation to Others</CardTitle>
        </CardHeader>
        <CardContent>
          <canvas ref={canvasRef} className="mx-auto"></canvas>
        </CardContent>
      </Card>
    </div>
  )
}

