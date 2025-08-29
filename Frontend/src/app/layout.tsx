import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { ToastProviderWrapper } from "@/components/ui/useToast" 

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'LinkedIn AI Agent - Intelligent Content Generation',
  description: 'AI-powered LinkedIn content generation and personal branding platform',
  keywords: 'LinkedIn, AI, Content Generation, Personal Branding, GPT-4',
  authors: [{ name: 'LinkedIn AI Agent' }],
  openGraph: {
    title: 'LinkedIn AI Agent',
    description: 'Transform your LinkedIn presence with AI',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className={`${inter.className} bg-background text-foreground antialiased`}>
        <ToastProviderWrapper>
          <div className="relative min-h-screen flex flex-col">
            {/* Optional header */}
            <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
              <div className="container flex h-14 items-center">
                <div className="mr-4 flex">
                  <a className="mr-6 flex items-center space-x-2" href="/">
                    <span className="font-bold text-xl bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                      LinkedIn AI Agent
                    </span>
                  </a>
                </div>
              </div>
            </header>

            {/* Main content */}
            <main className="flex-1">
              {children}
            </main>

            {/* Footer */}
            <footer className="border-t py-6 md:py-0">
              <div className="container flex flex-col items-center justify-between gap-4 md:h-16 md:flex-row">
                <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
                  Built with ❤️ using AI • LinkedIn AI Agent © 2024
                </p>
              </div>
            </footer>
          </div>
        </ToastProviderWrapper>
      </body>
    </html>
  )
}
