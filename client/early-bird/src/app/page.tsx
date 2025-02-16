"use client"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import Image from "next/image"

async function generatePodcasts() {
  // Simulate podcast generation
  return {
    title: "Your EarlyBird Morning Podcast",
    description: "Fresh insights on tech and web development to start your day.",
    url: "#",
  }
}

export default function Home() {
  async function generatePodcast(event: React.FormEvent) {
    event.preventDefault(); // Fix: Added event parameter
    const podcast = await generatePodcasts(); // This won't work in a client component due to "use server"
    console.log(podcast);
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
        <Button type="submit" size="lg">
          Generate Today's Podcast
        </Button>
      </form>

      <Card>
        <CardHeader>
          <CardTitle>Your Morning Tech Podcast</CardTitle>
          <CardDescription>Fresh insights and updates to kickstart your day</CardDescription>
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
