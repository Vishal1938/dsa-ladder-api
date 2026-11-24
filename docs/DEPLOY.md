# Deploying the API

The API is one Docker image (this repo's `Dockerfile`) plus a PostgreSQL database. The frontend is deployed
separately from **dsa-ladder-web** and talks to this API over HTTPS.

## Environment variables

| Variable | Example | Notes |
|---|---|---|
| `DATABASE_URL` | `jdbc:postgresql://host:5432/dsaladder` | **JDBC form.** If your host gives `postgres://user:pass@host:5432/db`, rewrite it as `jdbc:postgresql://host:5432/db` and put user/password in the next two variables. Add `?sslmode=require` if the provider needs SSL. |
| `DATABASE_USER` | `dsaladder` | |
| `DATABASE_PASSWORD` | | |
| `JWT_SECRET` | output of `openssl rand -base64 48` | At least 32 characters. Changing it signs everyone out. |
| `CORS_ORIGINS` | `https://dsa-ladder-web.example.app` | The frontend's exact origin(s), comma-separated, no trailing slash. |
| `PORT` | `8080` | Most platforms set this for you. |
| `JUDGE_MAX_CONCURRENT` | `2` | How many submissions run at once. Each needs ~300 MB. |

`SPRING_PROFILES_ACTIVE=prod` is already set in the image.

## Requirements

* **≥ 1.5 GB RAM**: the API JVM plus one JVM per running submission.
* The platform must run your **Dockerfile** (the judge needs a full JDK and starts child processes).
* Health check path: `/actuator/health`. First start takes ~30–60 s because every problem is verified.

## Option A: a small VM

```bash
git clone <this repo> && cd dsa-ladder-api
cp .env.example .env    # set POSTGRES_PASSWORD, JWT_SECRET, CORS_ORIGINS
docker compose up -d --build
```

Then put HTTPS in front, e.g. Caddy: `api.your-domain { reverse_proxy localhost:8080 }`.

## Option B: a container platform

Create a web service from this repo using the Dockerfile, add a managed PostgreSQL, and set the variables above.
After it's live, copy its URL into the frontend's `VITE_API_URL`.
