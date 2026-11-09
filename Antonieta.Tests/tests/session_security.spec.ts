import { test, expect } from '@playwright/test'

const token = `a.${Buffer.from(JSON.stringify({ sub: 'user@example.com', exp: Date.now() / 1000 + 300 })).toString('base64url')}.c`

test.beforeEach(async ({ page }) => {
  // All API requests are intercepted: no development/production data is modified.
  await page.route('http://localhost:8000/**', async route => {
    const path = new URL(route.request().url()).pathname
    let body: unknown = {}
    if (path === '/auth/me') body = { id: 2, email: 'user@example.com', full_name: 'User', role: 'comum' }
    else if (path.includes('beneficiaries-dashboard')) body = { data: [], total: 0, skip: 0, limit: 10 }
    else if (path.includes('total-inputs') || path.includes('total-distributions')) body = { total_amount: 0 }
    else if (path.includes('current-total-stock')) body = { current_stock: 0 }
    else body = [[], 0]
    await route.fulfill({ json: body, headers: { 'Access-Control-Allow-Origin': '*' } })
  })
})

test('anonymous visitors cannot open protected pages', async ({ page }) => {
  await page.goto('/beneficiary')
  await expect(page).toHaveURL(/\/login$/)
})

test('expired stored tokens are cleared and redirected to login', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('access_token', 'a.eyJleHAiOjF9.c')
    localStorage.setItem('current_user', JSON.stringify({ role: 'administrador' }))
  })
  await page.goto('/dashboard')
  await expect(page).toHaveURL(/\/login$/)
  await expect.poll(() => page.evaluate(() => localStorage.getItem('access_token'))).toBeNull()
})

test('server role overrides forged administrator role in local storage', async ({ page }) => {
  await page.addInitScript(value => {
    localStorage.setItem('access_token', value)
    localStorage.setItem('current_user', JSON.stringify({ role: 'administrador' }))
  }, token)
  await page.goto('/admin')
  await expect(page).toHaveURL(/\/dashboard$/)
})

test('API 401 clears credentials and returns to login', async ({ page }) => {
  await page.addInitScript(value => localStorage.setItem('access_token', value), token)
  await page.route('http://localhost:8000/beneficiary/**', route => route.fulfill({
    status: 401, json: { detail: 'Invalid credentials' }, headers: { 'Access-Control-Allow-Origin': '*' },
  }))
  await page.goto('/beneficiary')
  await expect(page).toHaveURL(/\/login$/)
  await expect.poll(() => page.evaluate(() => localStorage.getItem('access_token'))).toBeNull()
})
