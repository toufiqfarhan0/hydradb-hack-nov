# Deploying Lucen to Render (Free Tier)

This guide walks you through deploying the complete Lucen end-to-end stack (FastAPI HydraDB Backend + Next.js 15 Web Studio) to the free hosting tier on [Render](https://dashboard.render.com/).

---

## Method 1: 1-Click Blueprint (Recommended)

Render Blueprints automatically parse the repository's [`render.yaml`](../render.yaml) file to set up and configure everything in one click on the Free Tier.

### Steps:
1. Open the [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** in the top navigation and select **Blueprint**.
3. Connect your GitHub repository: `https://github.com/toufiqfarhan0/hydradb-hack-nov`.
4. Render will detect `render.yaml` and configure the **lucen-app** service:
   - **Runtime**: Docker (Multi-stage build)
   - **Plan**: Free ($0/mo)
   - **Region**: Oregon (or Frankfurt)
5. Click **Apply**.
6. Render builds the Next.js frontend, installs Python dependencies, and launches both services via `run_production.py`.
7. Once deployed, your live URL will be active: `https://lucen-app.onrender.com`.

---

## Method 2: Manual Web Service Setup (Docker)

If you prefer setting up the web service manually through the Render UI:

1. In the [Render Dashboard](https://dashboard.render.com/), click **New +** &rarr; **Web Service**.
2. Select **Build and deploy from a Git repository** and connect `toufiqfarhan0/hydradb-hack-nov`.
3. Configure the following settings:
   - **Name**: `lucen`
   - **Region**: Any (e.g. Oregon)
   - **Branch**: `main`
   - **Root Directory**: Leave blank (repo root)
   - **Runtime**: `Docker`
   - **Dockerfile Path**: `Dockerfile`
   - **Instance Type**: `Free`
4. Under **Environment Variables**, add:
   - `NODE_ENV`: `production`
   - `PYTHONUNBUFFERED`: `1`
5. Click **Create Web Service**.

---

## Method 3: Separate Services (Native Python + Node)

If you prefer deploying separate native services without Docker:

### 1. Backend Service (FastAPI)
- **Runtime**: `Python 3`
- **Root Directory**: `.`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn backend.server:app --host 0.0.0.0 --port $PORT`
- **Plan**: `Free`
- Note your backend URL (e.g., `https://lucen-backend.onrender.com`).

### 2. Frontend Service (Next.js)
- **Runtime**: `Node`
- **Root Directory**: `web`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm run start`
- **Plan**: `Free`
- **Environment Variables**:
  - `BACKEND_URL`: `https://lucen-backend.onrender.com`

---

## Verifying the Deployment

Once your Render service status shows **Live**:
1. **Home Studio**: Visit `https://<your-render-subdomain>.onrender.com/` to interact with the GraphBLAS Matrix Viewer.
2. **Traversal Studio**: Open `/console` to run real-time OpenCypher traversals.
3. **Research Article**: Open `/blog` to read the empirical evaluation report.
4. **Technical Documentation**: Open `/docs` to review protocol specifications.
5. **Health Endpoint**: `https://<your-render-subdomain>.onrender.com/api/health` returns status `200 OK`.

> [!NOTE]
> On Render's Free tier, services automatically spin down after 15 minutes of inactivity. When a new request arrives, Render spins the container back up in approximately 30-40 seconds. Both Lucen's frontend and backend include automatic resilience fallbacks so the application remains functional even during container warm-up.
