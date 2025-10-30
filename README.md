# api-map

A full-stack application for visualizing power station data across Brazilian states. The project consists of a Vue.js frontend for data visualization and a Python FastAPI backend for API integration and data management.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Vue.js)                 │
│            (Dashboard/Visualização)                 │
└────────────────────┬────────────────────────────────┘
                     │ HTTP Requests
                     ▼
┌─────────────────────────────────────────────────────┐
│           Backend (Python - FastAPI)                │
├─────────────────────────────────────────────────────┤
│  • Integration with ONS API                         │
│  • Data validation and processing                   │
│  • Scheduled tasks (future implementation)          │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         Database (PostgreSQL/SQLite)                │
│  • Real-time data (updated every 5 min - future)    │
│  • Complete history (monthly heavy queries - future)│
│  • Automatic backup (future implementation)         │
└─────────────────────────────────────────────────────┘
```

## Project Structure

```
api-map/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Data models
│   ├── config.py            # Configuration settings
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── Dockerfile           # Backend container configuration
│
├── frontend/
│   ├── src/
│   │   ├── App.vue          # Main Vue component
│   │   ├── components/      # Vue components
│   │   │   └── MapComponent.vue
│   │   └── services/
│   │       └── api.js       # Backend API service
│   ├── package.json         # Frontend dependencies
│   └── .env.example         # Frontend environment variables template
│
├── docker-compose.yml       # Docker orchestration
└── README.md               # This file
```

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) 
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Prerequisites

- **Node.js**: v20.19.0 or v22.12.0+
- **Python**: 3.11+
- **Docker & Docker Compose** (optional, for containerized deployment)

## Quick Start with Docker

1. **Clone the repository**
   ```sh
   git clone https://github.com/Bandeco03/api-map.git
   cd api-map
   ```

2. **Set up environment variables**
   ```sh
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env with your API credentials
   
   # Frontend
   cp frontend/.env.example frontend/.env
   # Edit frontend/.env if needed
   ```

3. **Run with Docker Compose**
   ```sh
   docker-compose up
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Local Development Setup

### Backend Setup

1. **Navigate to backend directory**
   ```sh
   cd backend
   ```

2. **Create a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```sh
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the backend server**
   ```sh
   python main.py
   # Or with uvicorn directly:
   uvicorn main:app --reload
   ```

   The backend will be available at http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory**
   ```sh
   cd frontend
   ```

2. **Install dependencies**
   ```sh
   npm install
   ```

3. **Set up environment variables**
   ```sh
   cp .env.example .env
   # Edit .env if needed (default backend URL is http://localhost:8000)
   ```

4. **Run the development server**
   ```sh
   npm run dev
   ```

   The frontend will be available at http://localhost:5173

## Build for Production

### Frontend
```sh
cd frontend
npm run build
```

### Backend
The backend doesn't require a build step. Ensure all dependencies are installed and run with:
```sh
cd backend
python main.py
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /api/power-data` - Fetch power station data
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

## Features

- 🗺️ **Interactive Map**: Visualize power data across Brazilian states
- 📊 **Real-time Data**: Display active power and installed capacity
- 🔄 **Toggle Views**: Switch between active power and installed capacity
- 📈 **State Comparison**: Compare multiple states side by side
- 🎨 **Visual Heat Map**: Color-coded map based on power levels
- 🔌 **Backend API**: FastAPI backend for centralized API calls
- 🐳 **Docker Support**: Easy deployment with Docker Compose

## Future Enhancements

- [ ] Database integration (PostgreSQL/SQLite)
- [ ] Scheduled data updates (every 5 minutes)
- [ ] Historical data tracking
- [ ] Monthly heavy data requests
- [ ] Automatic backup system
- [ ] User authentication
- [ ] Data export functionality

## Environment Variables

### Backend (.env)
- `API_ACCESS_KEY`: Access key for external API
- `API_SYS_CODE`: System code for external API
- `API_TOKEN`: Authentication token
- `API_APPKEY`: Application key
- `DATABASE_URL`: Database connection string
- `DEBUG`: Debug mode (True/False)
- `HOST`: Server host
- `PORT`: Server port
- `CORS_ORIGINS`: Comma-separated list of allowed origins

### Frontend (.env)
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
