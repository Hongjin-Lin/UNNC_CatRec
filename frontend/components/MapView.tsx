'use client';
import { useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Hotspot } from '@/lib/api';

interface Props { hotspots: Hotspot[]; }

// UNNC campus center
const CENTER: [number, number] = [31.8315, 121.6832];

export default function MapView({ hotspots }: Props) {
  const located = hotspots.filter(h => h.lat !== null) as (Hotspot & { lat: number; lng: number })[];

  return (
    <div className="w-full h-72 rounded-2xl overflow-hidden border border-orange-100 shadow">
      <MapContainer center={CENTER} zoom={16} style={{ height: '100%', width: '100%' }} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {located.map(h => (
          <CircleMarker
            key={h.tag}
            center={[h.lat, h.lng]}
            radius={10 + h.cats.length * 2}
            pathOptions={{ color: '#F97316', fillColor: '#FDBA74', fillOpacity: 0.7 }}
          >
            <Popup>
              <strong>{h.tag}</strong><br />
              {h.cats.join('、')}
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
