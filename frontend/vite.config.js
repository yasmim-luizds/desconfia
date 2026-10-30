import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
  plugins: [react()],
  server: { proxy: Object.fromEntries(['/auth', '/analyses', '/me', '/health', '/config'].map(path => [path, 'http://127.0.0.1:8000'])) },
  test: { environment: 'jsdom', setupFiles: ['./src/test-setup.js'], restoreMocks: true }
});
