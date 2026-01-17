// Підключення vite

npm create vite@latest

// Підключення css

npm install tailwindcss @tailwindcss/vite

```
# tailwind.config.js
```
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
})
```

# index.css
```
@import "tailwindcss";
```

npm i antd axios
 