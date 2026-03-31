const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

console.log('[API] BASE URL configured as:', BASE)
console.log('[API] import.meta.env.VITE_API_URL:', import.meta.env.VITE_API_URL)

export interface CatProfile {
  id: string
  Name: string
  Species: string
  Breed: string
  Color: string
  Gender: string
  Estimated_Age: number | null
  Weight: number | null
  Location: string
  Current_status: string
  Personality: string
  TNR_Status: boolean
  Is_friendly?: string
  Notes?: string
  image_url?: string
  click_count: number
  likes_count: number
  comments_count: number
  favorites_count: number
  default_rank: number
  heat_score?: number
}

export interface CatsQuery {
  sort?: 'default' | 'hot' | 'category'
  gender?: string
  neutered?: 'all' | 'yes' | 'no'
  status?: string
  category?: string
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

function request<T>(path: string, options?: Partial<UniApp.RequestOptions>): Promise<T> {
  return new Promise((resolve, reject) => {
    const url = `${BASE}${path}`
    console.log('[API] 发送请求:', url)
    uni.request({
      url: url,
      method: 'GET',
      timeout: 10000,
      ...options,
      success: (res) => {
        console.log('[API] 请求成功:', path, res.statusCode)
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

export interface CatDetail extends CatProfile {
  photos: string[]
}

export async function getCatById(id: string): Promise<CatDetail> {
  return request<CatDetail>(`/cats/${id}`)
}

function toQuery(params?: CatsQuery): string {
  if (!params) return ''
  const entries = Object.entries(params).filter(([, value]) => value !== undefined && value !== '')
  if (!entries.length) return ''
  const query = entries
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
    .join('&')
  return `?${query}`
}

export async function getCats(params?: CatsQuery): Promise<CatProfile[]> {
  const data = await request<{ cats: CatProfile[] }>(`/cats/${toQuery(params)}`)
  return data.cats
}

export async function incrementCatClick(id: string): Promise<{ id: string; click_count: number }> {
  return request<{ id: string; click_count: number }>(`/cats/${id}/click`, {
    method: 'POST',
  })
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
  species: string
  breed: string
  color: string
  gender: string
  estimated_age: string
  weight: string
  status: string
  is_friendly: string
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
        species: form.species,
        breed: form.breed,
        color: form.color,
        gender: form.gender,
        estimated_age: form.estimated_age,
        weight: form.weight,
        status: form.status,
        is_friendly: form.is_friendly,
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
