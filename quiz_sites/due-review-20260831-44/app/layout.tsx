import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  metadataBase: new URL('https://jlpt-n2-due-review-44-20260831.pcwww.chatgpt.site'),
  title: 'JLPT N2 9월 2일 만기 복습 50문항',
  description: 'D+1·D+3·D+7 만기 약점을 새 문맥으로 묻는 연속 복습시험',
  openGraph: {
    title: 'JLPT N2 9月2日 満期復習 50問',
    description: '2026.09.01 · 一括試験',
    type: 'website',
    images: [{ url: '/og.png', width: 1200, height: 630, alt: 'JLPT N2 満期復習 44問' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'JLPT N2 9月2日 満期復習 50問',
    description: '2026.09.01 · 一括試験',
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
