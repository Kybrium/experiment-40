# Dev Quick Start

1. **Install Docker**
2. **Install Git**
3. **Clone repo**
   ```bash
   git clone https://github.com/Kybrium/experiment-40.git
   cd experiment-40
   ```

4) **Make `.env` files**

   - Copy any `*.env.example` to `.env` **in the same folder**.
   - Example:

     - mac/Linux: `cp docker/dev/.env.example docker/dev/.env`
     - Windows: `Copy-Item docker/dev/.env.example docker/dev/.env`

5) **Docker commands**

   - **Windows (PowerShell):**

     - **start:** `.\dev.ps1 -cmd up`
     - **stop:** `.\dev.ps1 -cmd down`
     - **Backend shell:** `.\dev.ps1 -cmd sh-backend`
     - **Frontend shell:** `.\dev.ps1 -cmd sh-frontend`

   - **macOS/Linux:**

     - **start:** `make up`
     - **stop:** `make down`
     - **Backend shell:** `make sh-backend`
     - **Frontend shell:** `make sh-frontend`

6) **Apps**

   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend: [http://localhost:8000](http://localhost:8000)
   - phpMyAdmin: [http://127.0.0.1:8080](http://127.0.0.1:8080)

7) **Known bugs / quick fixes**

   - **`entrypoint.sh` permission denied:**
     `chmod +x backend/entrypoint.sh`
   - **Windows line endings on script:**
     `perl -pi -e 's/\r\n|\r/\n/g' backend/entrypoint.sh`
   - **Backend can’t reach DB:** ensure `.env` has `DB_HOST=db`, `DB_PORT=3306`; wait ~10–20s.
   - **Port busy (3000/8000/8080):** stop the other app or change the port in `docker/dev/compose.yml`.
