const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export interface CatProfile {
  id: string
  Name: string
  Location: string
  Personality: string
  TNR_Status: boolean
  Notes?: string
  image_url?: string
}

export interface Hotspot {
  tag: string
  lat: number | null
  lng: number | null
  cats: string[]
}

export interface IdentifyResult {
  no_match: boolean
  confidence?: number
  match: {
    name: string
    location: string
    personality: string[]
    tnr_status: boolean
    notes?: string
    confidence: number
  } | null
}

function request<T>(path: string, options?: UniApp.RequestOptions): Promise<T> {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE}${path}`,
      method: 'GET',
      ...options,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data as T)
        } else {
          reject(new Error(`HTTP ${res.statusCode}`))
        }
      },
      fail: (err) => reject(new Error(err?.errMsg || "Request failed")),
    })
  })
}

export async function getCats(): Promise<CatProfile[]> {
  const data = await request<{ cats: CatProfile[] }>('/cats')
  return data.cats
}

export async function getMapData(): Promise<Hotspot[]> {
  const data = await request<{ hotspots: Hotspot[] }>('/cats/map-data')
  return data.hotspots
}

export function identifyCat(filePath: string): Promise<IdentifyResult> {
  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: `${BASE}/identify`,
      filePath,
      name: 'image',
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(JSON.parse(res.data) as IdentifyResult)
        } else {
          reject(new Error(`HTTP ${res.statusCode}`))
        }
      },
      fail: (err) => reject(new Error(err?.errMsg || "Request failed")),
    })
  })
}

export function addCat(form: {
  name: string
  location: string
  personality: string
  tnr_status: boolean
  notes: string
  filePath: string
}): Promise<{ id: string }> {
  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: `${BASE}/cats/add`,
      filePath: form.filePath,
      name: 'image',
      formData: {
        name: form.name,
        location: form.location,
        personality: form.personality,
        tnr_status: String(form.tnr_status),
        notes: form.notes,
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(JSON.parse(res.data) as { id: string })
        } else {
          reject(new Error(`HTTP ${res.statusCode}`))
        }
      },
      fail: (err) => reject(new Error(err?.errMsg || "Request failed")),
    })
  })
}
