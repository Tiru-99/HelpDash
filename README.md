
# HelpDash Multiagent Service

MultiAgent Backend is a FastAPI‑based service that exposes two AI agents—**Support Agent** and **Dashboard Agent**—through a versioned REST API.  
It integrates **CrewAI** to coordinate multi-agent workflows, uses **MongoDB Atlas** for structured data persistence, and leverages the **Gemini API** for LLM-powered prompt processing.  
This backend is production‑ready, configured for **Gunicorn + Uvicorn** behind **NGINX**, and secured with **HTTPS via Certbot**.


---

## Features
- Deployed on AWS EC2 with nginx 
- API versioning under `/api/v1`
- Two independent AI agents using CREW AI with Gemini API
  
  • Support Agent for external client queries  
  • Dashboard Agent for internal analytics  
- Health‑check endpoint at `/health`
- CORS enabled
- MongoDB Atlas integration
- Environment‑variable support via `dotenv`
- Deployment‑ready with Gunicorn workers and NGINX reverse proxy

---

## 📄 Documentation & Sample Prompts

Access the full API documentation and sample prompt usage here:  
🔗 **https://documenter.getpostman.com/view/28016254/2sB34co2ZD**  

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
```
## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/multiagent-backend.git
cd multiagent-backend
```
### 2. Setup the virtual enviornment 
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Create your .env file
```bash
touch .env
```
### 5. Add the following env 
```bash
#Backend env 
MONGO_CONNECTION_URL = your url
MONGO_DB_NAME= your db name
MODEL= your model 
LITELLM_PROVIDER= your provider
GEMINI_API_KEY= your api key
 
#frontend env
NEXT_PUBLIC_API_URL= your api url (localhost one)

```
### 6. Run the application locally 
```bash
PYTHONPATH=src uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

# License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this software with proper attribution.

---

## Support

For issues, bugs, or feature requests, please open an issue on the [GitHub Issues](https://github.com/Tiru-99/HelpDash/issues) page.

---

## Author

**Aayush Tirmanwar**  
_Computer Science Student | Full Stack Developer_  
Built with purpose, speed, and flexibility in mind.



