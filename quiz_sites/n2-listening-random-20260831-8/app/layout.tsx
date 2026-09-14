import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  metadataBase: new URL('https://jlpt-n2-due-review-44-20260831.pcwww.chatgpt.site'),
  title: 'JLPT N2 랜덤 청해 8문항',
  description: '반복 문제를 피한 N2 수준 랜덤 청해 연속 시험',
  openGraph: {
    title: 'JLPT N2 ランダム聴解 8問',
    description: '2026.08.31 · 連続試験',
    type: 'website',
    images: [{ url: '/og.png', width: 1200, height: 630, alt: 'JLPT N2 ランダム聴解 8問' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'JLPT N2 ランダム聴解 8問',
    description: '2026.08.31 · 連続試験',
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
      <body>{children}</body>
    </html>
  );
}
