import { beforeEach, vi } from 'vitest'
import { useRuntimeConfig, navigateTo } from './nuxt-stub'

const storage = new Map<string, string>()
vi.stubGlobal('localStorage', {
  getItem: (key: string) => storage.get(key) ?? null,
  setItem: (key: string, value: string) => storage.set(key, value),
  removeItem: (key: string) => storage.delete(key),
  clear: () => storage.clear(),
})
Object.assign(process, { client: true })
vi.stubGlobal('useRuntimeConfig', useRuntimeConfig)
vi.stubGlobal('defineNuxtRouteMiddleware', (callback: unknown) => callback)
vi.stubGlobal('navigateTo', navigateTo)
beforeEach(() => {
  storage.clear()
  vi.clearAllMocks()
  vi.stubGlobal('fetch', vi.fn())
})
