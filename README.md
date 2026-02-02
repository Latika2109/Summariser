# Chemical Equipment Parameter Visualizer

A hybrid web and desktop application for analyzing chemical equipment data from CSV files. Built for semester internship screening.

## Features

- **CSV Upload & Processing**: Upload equipment data with automatic validation
- **Data Analytics**: Calculate summary statistics and equipment type distribution
- **Visualizations**: Interactive charts using Chart.js (web) and Matplotlib (desktop)
- **History Management**: Automatically keeps last 5 uploads per user
- **PDF Reports**: Generate downloadable PDF reports with charts
- **Authentication**: Secure user login for both web and desktop apps
- **Dual Interface**: Access via web browser or desktop application

## Tech Stack

### Backend
- Django 4.2.7
- Django REST Framework
- Pandas (data processing)
- ReportLab (PDF generation)
- SQLite database

### Web Frontend
- React.js
- Chart.js (visualizations)
- Axios (API calls)

### Desktop Frontend
- PyQt5
- Matplotlib (charts)
- Requests (HTTP client)

## Project Structure

```
chemical-equipment-visualizer/
├── backend/                    # Django backend
│   ├── backend/               # Project settings
│   ├── equipment_api/         # Main app
│   │   ├── models.py         # Database models
│   │   ├── views.py          # API endpoints
│   │   ├── serializers.py    # DRF serializers
│   │   └── services/         # Business logic
│   │       ├── csv_processor.py
│   │       ├── analytics_service.py
│   │       └── pdf_service.py
│   └── requirements.txt
│
├── web_frontend/              # React web app
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── LoginComponent.jsx
│   │   │   ├── UploadComponent.jsx
│   │   │   ├── ChartsComponent.jsx
│   │   │   └── HistoryComponent.jsx
│   │   └── utils/
│   │       └── api.js        # API client
│   └── package.json
│
├── desktop_frontend/          # PyQt5 desktop app
│   ├── main.py               # Entry point
│   ├── login_window.py       # Login dialog
│   ├── upload_window.py      # Main window
│   ├── charts_window.py      # Chart popups
│   ├── api_client.py         # HTTP client
│   └── requirements.txt
│
└── sample_equipment_data.csv  # Sample data file
```

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Start development server:
```bash
python manage.py runserver
```

Backend will run on `http://localhost:8000`

### Web Frontend Setup

1. Navigate to web frontend directory:
```bash
cd web_frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

Web app will open at `http://localhost:3000`

### Desktop App Setup

1. Navigate to desktop frontend directory:
```bash
cd desktop_frontend
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run application:
```bash
python main.py
```

## Usage

### First Time Setup

1. Start the backend server
2. Register a new user account (via web or desktop app)
3. Login with your credentials

### Uploading Data

**Web App:**
- Navigate to Upload tab
- Drag and drop CSV file or click to browse
- Click "Upload CSV"
- View data in Charts tab

**Desktop App:**
- Click "Select and Upload CSV"
- Choose CSV file
- View data in table
- Click chart buttons to see visualizations

### CSV Format

Your CSV file must have these columns:
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Heat Exchanger HX-101,Heat Exchanger,150.5,25.3,85.2
Pump P-201,Pump,200.0,45.8,35.0
```

### Viewing History

- Web: Click "History" tab to see last 5 uploads
- Each upload shows summary statistics
- Download PDF reports from history

### PDF Reports

- Generated automatically for each upload
- Contains summary statistics and charts
- Download from web history or via API

## API Endpoints

- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `POST /api/upload/` - Upload CSV file
- `GET /api/datasets/` - List user's datasets
- `GET /api/datasets/{id}/` - Get specific dataset
- `GET /api/datasets/{id}/pdf/` - Download PDF report

## Development Notes

- Backend uses token authentication
- CORS enabled for localhost:3000
- Database automatically keeps only last 5 uploads per user
- All numeric validations handled by Pandas
- Charts use responsive design

## Troubleshooting

**Backend won't start:**
- Check if port 8000 is available
- Verify all dependencies installed
- Run migrations again

**Web app can't connect:**
- Ensure backend is running
- Check CORS settings in backend/settings.py
- Verify API_BASE_URL in web_frontend/src/utils/api.js

**Desktop app errors:**
- Make sure backend is running
- Check API base URL in api_client.py
- Verify PyQt5 installed correctly

## Future Enhancements

- Add more chart types
- Export data to Excel
- Real-time data updates
- Multi-user collaboration
- Advanced filtering options

## Author

Built as part of semester internship screening project.

## License

Educational project - free to use and modify.
