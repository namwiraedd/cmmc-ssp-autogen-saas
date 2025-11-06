# cmmc-ssp-autogen-saas
AI-powered SaaS that ingests PDF/DOCX, auto-maps content to CMMC Level 2 controls, and generates audit-ready System Security Plans. Secure multitenant architecture with role-based access, dashboards, and automated compliance scoring. Built for Defense Industrial Base readiness.
mvp-cmmc-ssp/
├─ README.md
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ auth.py
│  │  ├─ models.py
│  │  ├─ storage.py
│  │  ├─ processor.py
│  │  ├─ mapping.py
│  │  ├─ ssp_generator.py
│  │  └─ deps.py
│  ├─ Dockerfile
│  └─ requirements.txt
├─ frontend/
│  ├─ package.json
│  └─ src/
│     ├─ App.jsx
│     ├─ components/Upload.jsx
│     ├─ components/Dashboard.jsx
│     └─ services/ws.js
├─ infra/
│  ├─ docker-compose.yml
│  ├─ terraform/
│  │  ├─ main.tf
│  │  └─ providers.tf
│  └─ zap_scan.sh
├─ docs/
│  ├─ cmmc_controls.json
│  └─ mapping_template.md
├─ tests/
│  ├─ test_processor.py
│  └─ test_auth.py
└─ scripts/
   └─ local_start.sh
# MVP: CMMC Level 2 SSP Generator (Production-minded demo)

Purpose: Demo-ready SaaS MVP for parsing DOCX/PDF, mapping extracted content to NIST/SP800-171 (CMMC L2) controls, and producing audit-ready SSP/PDF outputs. Includes a React front-end with real-time dashboards.

Important references:
- NIST SP 800-171 Rev.2 (control set used). See NIST. :contentReference[oaicite:3]{index=3}
- CMMC Level 2 aligns to the 110 controls in NIST SP 800-171. :contentReference[oaicite:4]{index=4}

Run locally (dev):
1. copy `.env.template` → `.env` and supply secrets (AWS S3, JWT secret, LLM api key).
2. `./scripts/local_start.sh`
3. Frontend: http://localhost:3000 ; Backend: http://localhost:8000

Acceptance test:
- Upload sample DOCX/PDF → check `/_status` WebSocket progress → download generated `SSP.docx` and `SSP.pdf`.

Security/hardening checklist (must be completed before production):
- HSM-backed key management (AWS KMS with GovCloud keys or dedicated HSM)
- Replace simple JWT with short-lived access tokens + refresh & session revocation
- Pen test & full OWASP ZAP scan (script provided). Ensure no critical findings.
- Host in GovCloud with strictly controlled IAM roles and VPC endpoints.

