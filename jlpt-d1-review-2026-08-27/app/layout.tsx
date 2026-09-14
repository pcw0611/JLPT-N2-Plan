import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import './globals.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  metadataBase: new URL('https://jlpt-d1-review-0827.pcwww.chatgpt.site'),
  title: 'JLPT D+1 翌日想起テスト',
  description: '形容詞活用・語彙・読解・聴解を確認する15問の翌日復習テスト',
  openGraph: {
    title: 'JLPT D+1 翌日想起テスト',
    description: '15問・18分・翌日復習',
    images: ['/og.png'],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'JLPT D+1 翌日想起テスト',
    description: '15問・18分・翌日復習',
    images: ['/og.png'],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
