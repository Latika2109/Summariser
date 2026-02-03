# 🚀 Quick Start Guide

## Running All Components

### 1. Backend Server (Django)

```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

**Access:** http://localhost:8000/
**Status:** Should show "Django version 4.2.7, using settings 'backend.settings'"

---

### 2. Web Frontend (React)

```bash
cd web_frontend
npm start
```

**Access:** http://localhost:3000/
**Note:** Use `npm start` (NOT `npm run dev`)

---

### 3. Desktop App (PyQt5)

```bash
cd desktop_frontend
source venv/bin/activate
python main.py
```

**Note:** Desktop app connects to backend at http://localhost:8000/

---

## Testing the New Features

### Email Functionality
1. Start backend and web frontend
2. Login/Register
3. Upload a dataset
4. Go to "Charts" tab
5. Find "Email Report" section at top
6. Enter email: `your-email@gmail.com`
7. Click "Send Report"
8. Check inbox for PDF report

### Alerts Feature
1. Upload a dataset
2. Go to "Alerts" tab
3. Set thresholds (e.g., Temperature warning: 80, critical: 100)
4. Click "Save"
5. View color-coded alerts

### Comparison Feature
1. Upload 2 datasets
2. Go to "Compare" tab
3. Select both datasets
4. Click "Compare"
5. View differences

### Dark Mode
1. Click 🌙 icon in navbar
2. Theme switches instantly
3. Refresh - theme persists

### Batch Upload
1. Go to "Batch Upload" tab
2. Drag multiple CSV files
3. Click "Upload X Files"
4. View results

### Validation Dashboard
1. Upload a dataset
2. Go to "Validation" tab
3. View quality score and metrics

---

## Troubleshooting

**Backend not starting?**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Web frontend errors?**
```bash
cd web_frontend
npm install
npm start
```

**Desktop app errors?**
```bash
cd desktop_frontend
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## Current Status

Backend: Running at http://localhost:8000/
Web Frontend: Running at http://localhost:3000/
Email: Configured with Gmail SMTP


**Ready to test!**
