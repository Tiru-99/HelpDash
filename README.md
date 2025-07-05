
# MultiAgent Backend

MultiAgent Backend is a FastAPI‑based service that exposes two AI agents—**Support Agent** and **Dashboard Agent**—through a versioned REST API.  
It is production‑ready, configured for Gunicorn + Uvicorn behind NGINX, and secured with HTTPS via Let’s Encrypt.

---

## Features

- API versioning under `/api/v1`
- Two independent AI agents  
  • Support Agent for external client queries  
  • Dashboard Agent for internal analytics  
- Health‑check endpoint at `/health`
- CORS enabled
- MongoDB Atlas integration
- Environment‑variable support via `dotenv`
- Deployment‑ready with Gunicorn workers and NGINX reverse proxy
- Optional GitHub Actions workflow for CI/CD

---

## 📄 Documentation & Sample Prompts

Access the full API documentation and sample prompt usage here:  
🔗 **[https://documenter.getpostman.com/view/28016254/2sB34co2ZD]**  

---

## Project Structure

```text
multiagent-backend/
│
├─ src/
│  ├─ config/            # Agent and DB configuration
│  ├─ routes/            # FastAPI routers
│  ├─ tools/             # Agent tools
│  └─ main.py            # FastAPI app entry point
│
├─ .env                  # Environment variables (git‑ignored)
├─ requirements.txt      # Python dependencies
└─ README.mdx            # Documentation
