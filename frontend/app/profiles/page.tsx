'use client';
import { useEffect, useState } from 'react';
import { getCats, CatProfile } from '@/lib/api';
import CatCard from '@/components/CatCard';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function ProfilesPage() {
  const [cats, setCats] = useState<CatProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getCats()
      .then(setCats)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : '加载失败'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="pt-6">
      <h1 className="text-2xl font-bold text-paw-dark mb-1">猫咪名册</h1>
      <p className="text-sm text-paw-soft mb-6">校园里的每一只小可爱</p>
      {loading && <LoadingSpinner />}
      {error && <p className="text-red-500 text-sm text-center py-10">{error}</p>}
      {!loading && !error && cats.length === 0 && (
        <p className="text-paw-soft text-sm text-center py-10">还没有猫咪档案，快去添加吧~</p>
      )}
      <div className="grid grid-cols-2 gap-3">
        {cats.map((cat) => <CatCard key={cat.id} cat={cat} />)}
      </div>
    </div>
  );
}
