import type { Metadata } from 'next';
import './globals.css';
import NavBar from '@/components/NavBar';

export const metadata: Metadata = {
  title: 'UNNC CatRec',
  description: '校园猫咪识别与社区应用',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen bg-cream-50">
        <main className="max-w-md mx-auto min-h-screen pb-20 px-4">
          {children}
        </main>
        <div className="max-w-md mx-auto">
          <NavBar />
        </div>
      </body>
    </html>
  );
}
