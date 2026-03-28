'use client';
import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { getMapData, Hotspot } from '@/lib/api';
import LoadingSpinner from '@/components/LoadingSpinner';

// Leaflet must be client-side only
const MapView = dynamic(() => import('@/components/MapView'), { ssr: false, loading: () => <LoadingSpinner text="地图加载中…" /> });

export default function MapPage() {
  const [hotspots, setHotspots] = useState<Hotspot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getMapData()
      .then(setHotspots)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : '加载失败'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="pt-6">
      <h1 className="text-2xl font-bold text-paw-dark mb-1">猫咪地图</h1>
      <p className="text-sm text-paw-soft mb-4">校园猫咪出没热点</p>
      {loading && <LoadingSpinner />}
      {error && <p className="text-red-500 text-sm text-center py-10">{error}</p>}
      {!loading && !error && <MapView hotspots={hotspots} />}
      {/* Unlocated cats */}
      {!loading && hotspots.filter(h => h.lat === null).length > 0 && (
        <div className="mt-4">
          <p className="text-xs text-paw-soft mb-2">未定位区域</p>
          {hotspots.filter(h => h.lat === null).map(h => (
            <div key={h.tag} className="flex items-center gap-2 py-1">
              <span className="text-xs font-mono bg-cream-200 text-brand px-2 py-0.5 rounded-full">{h.tag}</span>
              <span className="text-xs text-paw-soft">{h.cats.join('、')}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
