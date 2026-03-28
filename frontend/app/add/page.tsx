'use client';
import { useState, useRef, ChangeEvent } from 'react';
import Image from 'next/image';
import { addCat } from '@/lib/api';
import { Camera, CheckCircle } from 'lucide-react';

export default function AddCatPage() {
  const [preview, setPreview] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const [form, setForm] = useState({
    name: '',
    location: '',
    personality: '',
    tnr_status: false,
    notes: '',
  });

  function onImage(e: ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (!f) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) { setError('请选择一张猫咪照片'); return; }
    if (!form.name.trim()) { setError('请输入猫咪名字'); return; }
    setLoading(true);
    setError(null);
    try {
      const fd = new FormData();
      fd.append('image', file);
      fd.append('name', form.name.trim());
      fd.append('location', form.location.trim());
      fd.append('personality', form.personality.trim());
      fd.append('tnr_status', String(form.tnr_status));
      fd.append('notes', form.notes.trim());
      await addCat(fd);
      setSuccess(true);
      setForm({ name: '', location: '', personality: '', tnr_status: false, notes: '' });
      setFile(null);
      setPreview(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : '添加失败，请重试');
    } finally {
      setLoading(false);
    }
  }

  if (success) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen gap-4">
        <CheckCircle className="text-green-500" size={64} />
        <h2 className="text-2xl font-bold">添加成功！</h2>
        <button
          className="px-6 py-2 bg-blue-600 text-white rounded-xl"
          onClick={() => setSuccess(false)}
        >继续添加</button>
      </div>
    );
  }

  return (
    <main className="max-w-lg mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">添加新猫咪</h1>
      <form onSubmit={submit} className="flex flex-col gap-4">
        {/* 图片上传 */}
        <div
          className="relative w-full aspect-square rounded-2xl overflow-hidden bg-gray-100 flex items-center justify-center cursor-pointer border-2 border-dashed border-gray-300 hover:border-blue-400 transition"
          onClick={() => inputRef.current?.click()}
        >
          {preview ? (
            <Image src={preview} alt="preview" fill className="object-cover" />
          ) : (
            <div className="flex flex-col items-center gap-2 text-gray-400">
              <Camera size={40} />
              <span>点击上传猫咪照片</span>
            </div>
          )}
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={onImage}
          />
        </div>

        {/* 名字 */}
        <div className="flex flex-col gap-1">
          <label className="font-medium">名字 <span className="text-red-500">*</span></label>
          <input
            className="border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={form.name}
            onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
            placeholder="例如：橘猫小花"
          />
        </div>

        {/* 位置 */}
        <div className="flex flex-col gap-1">
          <label className="font-medium">常见位置</label>
          <input
            className="border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={form.location}
            onChange={e => setForm(f => ({ ...f, location: e.target.value }))}
            placeholder="例如：图书馆门口"
          />
        </div>

        {/* 性格 */}
        <div className="flex flex-col gap-1">
          <label className="font-medium">性格特点</label>
          <input
            className="border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={form.personality}
            onChange={e => setForm(f => ({ ...f, personality: e.target.value }))}
            placeholder="例如：亲人、爱撒娇"
          />
        </div>

        {/* TNR状态 */}
        <div className="flex items-center gap-3">
          <input
            type="checkbox"
            id="tnr"
            checked={form.tnr_status}
            onChange={e => setForm(f => ({ ...f, tnr_status: e.target.checked }))}
            className="w-5 h-5 accent-blue-600"
          />
          <label htmlFor="tnr" className="font-medium">已完成 TNR（绝育）</label>
        </div>

        {/* 备注 */}
        <div className="flex flex-col gap-1">
          <label className="font-medium">备注</label>
          <textarea
            className="border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
            rows={3}
            value={form.notes}
            onChange={e => setForm(f => ({ ...f, notes: e.target.value }))}
            placeholder="其他需要记录的信息…"
          />
        </div>

        {error && <p className="text-red-500 text-sm">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 disabled:opacity-50 transition"
        >
          {loading ? '正在添加…' : '添加猫咪'}
        </button>
      </form>
    </main>
  );
}
