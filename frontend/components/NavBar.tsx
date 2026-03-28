'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Search, Map, Grid2X2, PlusCircle } from 'lucide-react';

const tabs = [
  { href: '/',         label: '识别',  Icon: Search     },
  { href: '/map',      label: '地图',  Icon: Map        },
  { href: '/profiles', label: '猫册',  Icon: Grid2X2    },
  { href: '/add',      label: '添加',  Icon: PlusCircle },
];

export default function NavBar() {
  const path = usePathname();
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-orange-100 flex justify-around items-center h-16 max-w-md mx-auto">
      {tabs.map(({ href, label, Icon }) => {
        const active = path === href;
        return (
          <Link
            key={href}
            href={href}
            className={`flex flex-col items-center gap-0.5 px-3 py-1 rounded-xl transition-colors ${
              active ? 'text-brand' : 'text-paw-soft hover:text-brand'
            }`}
          >
            <Icon size={22} strokeWidth={active ? 2.5 : 1.8} />
            <span className={`text-[10px] font-medium ${active ? 'text-brand' : 'text-paw-soft'}`}>{label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
