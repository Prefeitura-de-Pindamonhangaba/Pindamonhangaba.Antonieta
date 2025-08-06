import { defineConfig, devices } from '@playwright/test'

/**
 * Configuração dos testes E2E para o sistema Antonieta
 * Testa frontend + backend integrados
 */
export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  
  // ✅ CORRIGIR: Separar output folders
  outputDir: 'test-results/artifacts',
  
  reporter: [
    ['html', { outputFolder: 'playwright-report' }], // ✅ Mudança aqui
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['list'] // Adicionar reporter de lista para console
  ],
  
  use: {
    // URLs das aplicações
    baseURL: process.env.FRONTEND_URL || 'http://localhost:3000',
    
    // Configurações globais
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    
    // Timeouts
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },

  projects: [
    // Apenas Chromium por enquanto para testar
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    
    // Comentar outros browsers por enquanto
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
  ],

  // Configuração para diferentes ambientes
  globalSetup: require.resolve('./utils/global-setup.ts'),
  globalTeardown: require.resolve('./utils/global-teardown.ts'),
})