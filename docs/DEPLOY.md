# Deploying the API

The API is one Docker image (this repo's `Dockerfile`) plus a MongoDB database. The frontend is deployed
separately from **dsa-ladder-web** and talks to this API over HTTPS.

## Environment variables

| Variable | Example | Notes |
|---|---|---|
| `MONGODB_URI` | `mongodb+srv://user:pass@cluster0.example.mongodb.net/dsaladder?retryWrites=true&w=majority` | **Required in prod** (no default). The path must name the database — see below. |
| `JWT_SECRET` | output of `openssl rand -base64 48` | At least 32 characters. Changing it signs everyone out. |
| `CORS_ORIGINS` | `https://dsa-ladder-web.example.app` | The frontend's exact origin(s), comma-separated, no trailing slash. |
| `PORT` | `8080` | Most platforms set this for you. |
| `JUDGE_MAX_CONCURRENT` | `2` | How many submissions run at once. Each needs ~300 MB. |

`SPRING_PROFILES_ACTIVE=prod` is already set in the image.

## MongoDB Atlas

* **Put the database name in the URI.** Atlas copies the connection string without one
  (`mongodb+srv://user:pass@cluster0.abcde.mongodb.net/`), and Spring then has no database to connect to.
  Add the path segment: `.../dsaladder?retryWrites=true&w=majority`.
* **Allow the host's IPs.** Under *Network Access*, add the outbound addresses of wherever the API runs
  (your VM's IP, or the egress range your platform documents). A short deploy-time workaround is `0.0.0.0/0`,
  but then the database is reachable from anywhere and only the password protects it.
* URL-encode the password if it contains `@ : / ? # [ ] %`.
* The indexes (unique `email`, the two compound indexes on `submissions`) are created at start-up; the database
  user needs write access to the `dsaladder` database, not just read.
* A free M0 cluster is enough to start; it sleeps under no traffic, so the first request after a pause is slow.

## Requirements

* **≥ 1.5 GB RAM**: the API JVM plus one JVM per running submission.
* The platform must run your **Dockerfile** (the judge needs a full JDK and starts child processes).
* Health check path: `/actuator/health`. First start takes ~30–60 s because every problem is verified.

## Option A: a small VM

```bash
git clone <this repo> && cd dsa-ladder-api
cp .env.example .env    # set JWT_SECRET, CORS_ORIGINS
docker compose up -d --build
```

This runs MongoDB alongside the API, with its data in the `mongodata` volume. To use Atlas instead, set
`MONGODB_URI` in `.env` and start only the api service.

Then put HTTPS in front, e.g. Caddy: `api.your-domain { reverse_proxy localhost:8080 }`.

## Option B: a container platform

Create a web service from this repo using the Dockerfile, point `MONGODB_URI` at a managed MongoDB (Atlas, or the
platform's own), and set the variables above.
After it's live, copy its URL into the frontend's `VITE_API_URL`.
