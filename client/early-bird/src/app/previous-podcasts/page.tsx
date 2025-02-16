import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"

const previousPodcasts = [
  { id: 1, title: "Yesterday's Tech Roundup", description: "A summary of yesterday's tech news", date: "2025-02-14" },
  { id: 2, title: "AI Breakthroughs", description: "Discussing recent advancements in AI", date: "2025-02-13" },
  { id: 3, title: "Web Dev Trends", description: "Exploring current trends in web development", date: "2025-02-12" },
]

export default function PreviousPodcasts() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Previous Podcasts</h1>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {previousPodcasts.map((podcast) => (
          <Card key={podcast.id}>
            <CardHeader>
              <CardTitle>{podcast.title}</CardTitle>
              <CardDescription>{podcast.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">Date: {podcast.date}</p>
              <audio controls src="#" className="w-full mt-2">
                Your browser does not support the audio element.
              </audio>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

