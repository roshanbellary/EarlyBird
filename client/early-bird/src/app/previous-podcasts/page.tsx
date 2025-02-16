import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"

const previousPodcasts = [
  { id: 1, title: "Yesterday's EarlyBird Tech", description: "Your morning dose of tech news", date: "2025-02-14" },
  { id: 2, title: "Morning AI Insights", description: "Wake up to AI breakthroughs", date: "2025-02-13" },
  { id: 3, title: "Dawn of Web Dev", description: "Early morning web development trends", date: "2025-02-12" },
]

export default function PreviousPodcasts() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Previous EarlyBird Episodes</h1>
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

