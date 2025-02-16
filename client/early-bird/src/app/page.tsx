import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"

async function generatePodcast() {
  "use server"
  // Simulate podcast generation
  return {
    title: "Your Daily Tech Podcast",
    description: "Today's episode covers the latest in AI and web development.",
    url: "#",
  }
}

export default function Home() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Welcome to Your Daily Podcast</h1>
      <form action={generatePodcast}>
        <Button type="submit">Generate Today's Podcast</Button>
      </form>
      <Card>
        <CardHeader>
          <CardTitle>Your Daily Tech Podcast</CardTitle>
          <CardDescription>Today's episode covers the latest in AI and web development.</CardDescription>
        </CardHeader>
        <CardContent>
          <audio controls src="#" className="w-full">
            Your browser does not support the audio element.
          </audio>
        </CardContent>
      </Card>
    </div>
  )
}

