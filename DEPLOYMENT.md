# Deployment Guide

Complete guide for deploying your Chemical Equipment Visualizer to production.

## Overview

- **Frontend**: Deployed on Vercel ✅
- **Backend**: Deploy on Render (instructions below)
- **Desktop App**: Distribute as executable (see [Desktop Distribution](#desktop-distribution))

---

## Backend Deployment (Render)

### Prerequisites

1. GitHub account with your code pushed
2. [Render account](https://render.com) (free tier available)

### Step-by-Step Instructions

#### 1. Create New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select `chemical-equipment-visualizer` repository

#### 2. Configure Build Settings

Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `chemical-equipment-backend` (or your choice) |
| **Region** | Choose closest to your users |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn backend.wsgi:application` |
| **Instance Type** | `Free` |

#### 3. Add Environment Variables

Click **"Advanced"** and add these environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `SECRET_KEY` | `<generate-random-key>` | [Generate here](https://djecrety.ir/) |
| `DEBUG` | `False` | Must be False in production |
| `ALLOWED_HOSTS` | `your-app.onrender.com` | Your Render URL (add after deployment) |
| `CORS_ALLOWED_ORIGINS` | `https://your-app.vercel.app` | Your Vercel frontend URL |
| `DATABASE_URL` | _Auto-added by Render_ | Don't add manually |
| `OPENROUTER_API_KEY` | `your_api_key` | From your `.env` file |
| `EMAIL_HOST_USER` | `your_email@gmail.com` | Your Gmail address |
| `EMAIL_HOST_PASSWORD` | `your_app_password` | Gmail App Password |
| `PYTHON_VERSION` | `3.13.0` | Match your local version |

> [!IMPORTANT]
> After deployment, you'll get a URL like `https://chemical-equipment-backend.onrender.com`. Update `ALLOWED_HOSTS` to include this URL.

#### 4. Add PostgreSQL Database

1. On Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Name: `chemical-equipment-db`
3. Database Name: `equipment_db`
4. Region: Same as your web service
5. Instance Type: **Free**
6. Click **"Create Database"**

#### 5. Link Database to Web Service

1. Go back to your web service settings
2. In **Environment** tab, the `DATABASE_URL` should be auto-added
3. If not, copy **Internal Database URL** from PostgreSQL service and add it manually

#### 6. Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes first time)
3. Watch build logs for any errors

#### 7. Create Superuser (Admin Account)

Once deployed:

1. Go to your web service in Render
2. Click **"Shell"** tab (opens terminal)
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow prompts to create admin account

#### 8. Verify Deployment

Test these URLs (replace with your actual URL):

- **Admin Panel**: `https://your-backend.onrender.com/admin/`
- **API Root**: `https://your-backend.onrender.com/api/`

---

## Update Frontend to Use Production Backend

### Update React API URL

1. Open `web_frontend/src/App.js` or wherever you define API base URL
2. Find lines like:
   ```javascript
   const API_URL = "http://localhost:8000/api";
   ```
3. Replace with:
   ```javascript
   const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";
   ```

4. In Vercel, add environment variable:
   - Go to Project Settings → Environment Variables
   - Add: `REACT_APP_API_URL` = `https://your-backend.onrender.com/api`
   - Redeploy frontend

---

## Desktop Distribution

The PyQt5 desktop app can be packaged as a standalone executable:

### Using PyInstaller

```bash
cd desktop_frontend
pip install pyinstaller

# For macOS
pyinstaller --onefile --windowed --name ChemicalEquipmentVisualizer main.py

# For Windows
pyinstaller --onefile --noconsole --name ChemicalEquipmentVisualizer main.py
```

The executable will be in `desktop_frontend/dist/`

### Distribution

Upload the executable to:
- **GitHub Releases** (recommended)
- Google Drive / Dropbox
- Your own website

> [!WARNING]
> The desktop app still needs to connect to your deployed backend. Update the API URL in `main.py` to point to your Render backend.

---

## Troubleshooting

### Build Failures

**Error**: `Permission denied: ./build.sh`
- **Fix**: Ensure `build.sh` is executable: `chmod +x backend/build.sh` and push to GitHub

**Error**: `psycopg2` installation fails
- **Fix**: Already using `psycopg2-binary` in requirements.txt (should work)

### Runtime Errors

**Error**: `DisallowedHost at /`
- **Fix**: Add your Render URL to `ALLOWED_HOSTS` environment variable

**Error**: `CORS error` in browser console
- **Fix**: Add your Vercel URL to `CORS_ALLOWED_ORIGINS` environment variable

**Error**: Database connection fails
- **Fix**: Ensure PostgreSQL database is created and `DATABASE_URL` is set

### Slow First Load

Render's free tier spins down after 15 minutes of inactivity. First request after idle period takes ~30 seconds to wake up. This is normal for free tier.

---

## Cost Summary

| Service | Tier | Cost |
|---------|------|------|
| Vercel (Frontend) | Free | $0/month |
| Render Web Service (Backend) | Free | $0/month |
| Render PostgreSQL (Database) | Free | $0/month |
| **Total** | | **$0/month** |

> [!TIP]
> Free tier is perfect for personal projects, portfolios, and demonstrations. For production apps with high traffic, consider upgrading to paid tiers.

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Create superuser account
3. ✅ Update frontend environment variables
4. ✅ Test end-to-end workflow (register → login → upload CSV)
5. 📱 Share your deployed URLs on your portfolio/resume!

---

## Support Resources

- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
