const BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export interface CatProfile {
  id: string;
  Name: string;
  Location: string;
  Personality: string;
  TNR_Status: boolean;
  Notes?: string;
  image_url?: string;
}

export interface Hotspot {
  tag: string;
  lat: number | null;
  lng: number | null;
  cats: string[];
}

export interface IdentifyResult {
  no_match: boolean;
  confidence?: number;
  match: {
    name: string;
    location: string;
    personality: string[];
    tnr_status: boolean;
    notes?: string;
    confidence: number;
  } | null;
}

export async function identifyCat(file: File): Promise<IdentifyResult> {
  const fd = new FormData();
  fd.append('image', file);
  const res = await fetch(`${BASE}/identify`, { method: 'POST', body: fd });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getCats(): Promise<CatProfile[]> {
  const res = await fetch(`${BASE}/cats`);
  if (!res.ok) throw new Error(await res.text());
  const data = await res.json();
  return data.cats;
}

export async function getMapData(): Promise<Hotspot[]> {
  const res = await fetch(`${BASE}/cats/map-data`);
  if (!res.ok) throw new Error(await res.text());
  const data = await res.json();
  return data.hotspots;
}

export async function addCat(formData: FormData): Promise<{ id: string }> {
  const res = await fetch(`${BASE}/cats/add`, { method: 'POST', body: formData });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
