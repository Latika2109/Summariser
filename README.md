# Chemical Equipment Parameter Visualizer

A hybrid web and desktop application for analyzing chemical equipment data from CSV files.

## Tech Stack

- **Backend**: Django + Django REST Framework + Pandas
- **Web Frontend**: React.js + Chart.js
- **Desktop Frontend**: PyQt5 + Matplotlib
- **Database**: SQLite

## Features

- CSV upload and validation
- Data analytics and visualizations
- PDF and Excel export
- User authentication
- History management (last 5 uploads)
- Admin panel

---

## Setup & Running

### 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs on `http://localhost:8000`

**Optional - Create admin user:**
```bash
python manage.py createsuperuser
# Access admin at http://localhost:8000/admin/
```

---

### 2. Web Frontend Setup

```bash
cd web_frontend
npm install
npm start
```

Web app opens at `http://localhost:3000`

---

### 3. Desktop App Setup

```bash
cd desktop_frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## Usage

1. **Start backend** (required for both web and desktop)
2. **Register/Login** with username and password
3. **Upload CSV** - Use `sample_equipment_data.csv` for testing
4. **View Charts** - See type distribution, temperature, and pressure charts
5. **Export** - Download PDF reports or Excel files
6. **Check History** - View last 5 uploads

### CSV Format Required

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Heat Exchanger HX-101,Heat Exchanger,150.5,25.3,85.2
Pump P-201,Pump,200.0,45.8,35.0
```

---

## API Endpoints

- `POST /api/auth/register/` - Register user
- `POST /api/auth/login/` - Login
- `POST /api/upload/` - Upload CSV
- `GET /api/datasets/` - List datasets
- `GET /api/datasets/{id}/pdf/` - Download PDF
- `GET /api/datasets/{id}/export_excel/` - Export Excel

---

## Project Structure

```
chemical-equipment-visualizer/
├── backend/                 # Django backend
│   ├── equipment_api/      # Main app
│   └── requirements.txt
├── web_frontend/           # React app
│   ├── src/components/
│   └── package.json
├── desktop_frontend/       # PyQt5 app
│   ├── main.py
│   └── requirements.txt
└── sample_equipment_data.csv
```

---

## Troubleshooting

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Module not found:**
```bash
pip install -r requirements.txt  # or npm install
```

**CORS errors:**
- Ensure backend is running
- Check `backend/backend/settings.py` CORS settings

---

## GitHub Repository

```bash
# Initialize and push to GitHub
git remote add origin git@github.com:Latika2109/chemical-equipment-visualizer.git
git branch -M main
git push -u origin main
```

---

## License

Educational project for internship screening.
