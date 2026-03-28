'use client';
import { useState, useRef, ChangeEvent, DragEvent } from 'react';
import Image from 'next/image';
import { identifyCat, IdentifyResult } from '@/lib/api';
import { Upload, Search, ShieldCheck, MapPin, RefreshCw } from 'lucide-react';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function IdentifyPage() {
  const [preview, setPreview] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<IdentifyResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  function handleFile(f: File) {
    if (!f.type.startsWith('image/')) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
    setError(null);
  }

  function onChange(e: ChangeEvent<HTMLInputElement>) {
    if (e.target.files?.[0]) handleFile(e.target.files[0]);
  }

  function onDrop(e: DragEvent) {
    e.preventDefault();
    setDragging(false);
    if (e.dataTransfer.files?.[0]) handleFile(e.dataTransfer.files[0]);
  }

  async function identify() {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const res = await identifyCat(file);
      setResult(res);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '识别失败，请重试');
    } finally {
      setLoading(false);
    }
  }

  function reset() {
    setPreview(null);
    setFile(null);
    setResult(null);
    setError(null);
    if (inputRef.current) inputRef.current.value = '';
  }

  return (
    <div className="pt-6">
      <h1 className="text-2xl font-bold text-paw-dark mb-1">猫咪识别</h1>
      <p className="text-sm text-paw-soft mb-6">上传一张照片，AI 帮你认出是哪只猫~</p>

      {!preview ? (
        <div
          onClick={() => inputRef.current?.click()}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={onDrop}
          className={`border-2 border-dashed rounded-3xl p-10 flex flex-col items-center gap-3 cursor-pointer transition-colors ${
            dragging ? 'border-brand bg-orange-50' : 'border-orange-200 bg-cream-100 hover:border-brand'
          }`}
        >
          <Upload size={40} className="text-brand-light" />
          <p className="text-sm text-paw-soft text-center">点击或拖拽图片到此处</p>
          <input ref={inputRef} type="file" accept="image/*" className="hidden" onChange={onChange} />
        </div>
      ) : (
        <div className="relative w-full aspect-square rounded-3xl overflow-hidden bg-cream-100 shadow">
          <Image src={preview} alt="preview" fill className="object-cover" />
          <button
            onClick={reset}
            className="absolute top-3 right-3 bg-white/80 backdrop-blur rounded-full p-1.5 shadow"
          >
            <RefreshCw size={16} className="text-paw-dark" />
          </button>
        </div>
      )}

      {preview && !result && (
        <button
          onClick={identify}
          disabled={loading}
          className="mt-4 w-full bg-brand text-white py-3 rounded-2xl font-semibold text-sm flex items-center justify-center gap-2 disabled:opacity-60 active:scale-95 transition-transform"
        >
          {loading ? <LoadingSpinner text="识别中…" /> : <><Search size={18} /> 开始识别</>}
        </button>
      )}

      {error && <p className="mt-4 text-red-500 text-sm text-center">{error}</p>}

      {result && (
        <div className="mt-5 bg-white rounded-3xl border border-orange-100 shadow p-5">
          {result.no_match ? (
            <div className="text-center">
              <p className="text-4xl mb-2">🤔</p>
              <p className="font-semibold text-paw-dark">没找到匹配的猫咪</p>
              <p className="text-xs text-paw-soft mt-1">
                置信度 {result.confidence !== undefined ? (result.confidence * 100).toFixed(1) : '--'}% — 要不要添加这只新猫？
              </p>
              <a
                href="/add"
                className="mt-3 inline-block bg-brand text-white px-5 py-2 rounded-full text-sm font-medium"
              >
                去添加
              </a>
            </div>
          ) : (
            <div>
              <div className="flex items-center gap-2 mb-3">
                <span className="text-2xl">😺</span>
                <div>
                  <p className="font-bold text-lg text-paw-dark">{result.match!.name}</p>
                  <p className="text-xs text-paw-soft">置信度 {(result.match!.confidence * 100).toFixed(1)}%</p>
                </div>
                {result.match!.tnr_status && <ShieldCheck size={20} className="ml-auto text-green-500" />}
              </div>
              <div className="flex items-center gap-1 text-sm text-paw-soft mb-3">
                <MapPin size={14} />
                <span>{result.match!.location}</span>
              </div>
              {result.match!.personality?.length > 0 && (
                <div className="flex flex-wrap gap-1 mb-3">
                  {result.match!.personality.map((t) => (
                    <span key={t} className="px-2 py-0.5 bg-cream-200 text-brand rounded-full text-xs font-medium">{t}</span>
                  ))}
                </div>
              )}
              {result.match!.notes && (
                <p className="text-xs text-paw-soft border-t border-orange-50 pt-3">{result.match!.notes}</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
