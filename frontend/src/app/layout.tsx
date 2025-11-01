import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Wakfu Builder Crafter',
  description: 'Generate optimal Wakfu equipment builds based on stats and difficulty',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">{children}</body>
    </html>
  )
}

