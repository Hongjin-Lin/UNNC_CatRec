import Image from 'next/image';
import { CatProfile } from '@/lib/api';
import { MapPin, ShieldCheck } from 'lucide-react';

export default function CatCard({ cat }: { cat: CatProfile }) {
  const traits = cat.Personality ? cat.Personality.split(',').filter(Boolean) : [];
  return (
    <div className="bg-white rounded-2xl border border-orange-100 overflow-hidden shadow-sm">
      <div className="relative w-full h-36 bg-cream-100">
        {cat.image_url ? (
          <Image src={cat.image_url} alt={cat.Name} fill className="object-cover" sizes="50vw" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-4xl">🐱</div>
        )}
      </div>
      <div className="p-3">
        <div className="flex items-center justify-between mb-1">
          <span className="font-semibold text-paw-dark truncate">{cat.Name}</span>
          {cat.TNR_Status && (
            <ShieldCheck size={15} className="text-green-500 shrink-0" />
          )}
        </div>
        <div className="flex items-center gap-1 text-xs text-paw-soft mb-2">
          <MapPin size={11} />
          <span>{cat.Location || '未知'}</span>
        </div>
        <div className="flex flex-wrap gap-1">
          {traits.slice(0, 3).map((t) => (
            <span key={t} className="px-2 py-0.5 rounded-full bg-cream-200 text-brand text-[10px] font-medium">
              {t.trim()}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
