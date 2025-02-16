import Link from "next/link"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
  title: "Daily Podcast Generator",
  description: "Generate personalized daily podcasts based on your interests",
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex flex-col min-h-screen">
          <header className="bg-primary text-primary-foreground shadow-md">
            <nav className="container mx-auto px-4 py-4">
              <ul className="flex space-x-4">
                <li>
                  <Link href="/" className="hover:underline">
                    Home
                  </Link>
                </li>
                <li>
                  <Link href="/previous-podcasts" className="hover:underline">
                    Previous Podcasts
                  </Link>
                </li>
                <li>
                  <Link href="/podcast-graph" className="hover:underline">
                    Podcast Graph
                  </Link>
                </li>
              </ul>
            </nav>
          </header>
          <main className="flex-grow container mx-auto px-4 py-8">{children}</main>
          <footer className="bg-primary text-primary-foreground py-4">
            <div className="container mx-auto px-4 text-center">© 2025 Daily Podcast Generator</div>
          </footer>
        </div>
      </body>
    </html>
  )
}

