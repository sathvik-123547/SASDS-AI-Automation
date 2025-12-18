## SASDS Frontend

Minimal React + Vite UI to drive the SASDS backend.

### Prerequisites
- Node.js 18+
- Backend running locally on `http://localhost:8000` (default) or set `VITE_API_BASE_URL`.

### Install
```bash
cd frontend
npm install
```

### Run Dev Server
```bash
npm run dev
# open http://localhost:5173
```

### Build for Production
```bash
npm run build
npm run preview
```

### Notes
- Forms map directly to backend routes:
  - `/requirements/analyze`
  - `/code/generate` and `/code/write`
  - `/tests/generate`
  - `/self/fix`
- Generated projects are saved under `backend/generated_projects/` by the backend—this UI does not modify that directory directly.


