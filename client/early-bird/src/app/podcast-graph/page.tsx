"use client"

import { useEffect, useRef } from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export default function PodcastGraph() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext("2d")
    if (!ctx) return

    canvas.width = 600
    canvas.height = 400

    ctx.fillStyle = "rgba(59, 130, 246, 0.5)"
    ctx.strokeStyle = "rgb(59, 130, 246)"

    const podcasts = [
      { x: 100, y: 100, r: 20, name: "Morning Tech" },
      { x: 200, y: 150, r: 25, name: "Dawn AI" },
      { x: 300, y: 200, r: 30, name: "EarlyBird Daily" },
      { x: 400, y: 100, r: 22, name: "Sunrise Dev" },
      { x: 500, y: 300, r: 18, name: "AM Insights" },
    ]

    podcasts.forEach((podcast) => {
      ctx.beginPath()
      ctx.arc(podcast.x, podcast.y, podcast.r, 0, 2 * Math.PI)
      ctx.fill()
      ctx.stroke()

      ctx.fillStyle = "black"
      ctx.font = "12px Arial"
      ctx.textAlign = "center"
      ctx.fillText(podcast.name, podcast.x, podcast.y + podcast.r + 15)
    })

    ctx.beginPath()
    ctx.moveTo(podcasts[0].x, podcasts[0].y)
    podcasts.slice(1).forEach((podcast) => {
      ctx.lineTo(podcast.x, podcast.y)
    })
    ctx.stroke()
  }, [])

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">EarlyBird Podcast Network</h1>
      <Card>
        <CardHeader>
          <CardTitle>Your Morning Podcast in the EarlyBird Network</CardTitle>
        </CardHeader>
        <CardContent>
          <canvas ref={canvasRef} className="mx-auto"></canvas>
        </CardContent>
      </Card>
    </div>
  )
}

