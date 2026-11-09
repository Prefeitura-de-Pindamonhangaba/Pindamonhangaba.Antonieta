import { vi } from 'vitest'
export const navigateTo = vi.fn()
export const useRuntimeConfig = () => ({ public: { backendUrl: 'http://api.test' } })
