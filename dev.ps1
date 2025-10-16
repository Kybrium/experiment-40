param(
  [ValidateSet("up","down","down-v","logs","ps","sh-backend","sh-frontend")]
  [string]$cmd = "up"
)

$compose = "docker compose -f docker/dev/compose.yml"

switch ($cmd) {
  "up"          { iex "$compose up --build" }
  "down"        { iex "$compose down" }
  "down-v"      { iex "$compose down -v" }
  "logs"        { iex "$compose logs -f --tail=200" }
  "ps"          { iex "$compose ps" }
  "sh-backend"  { iex "$compose exec backend sh" }
  "sh-frontend" { iex "$compose exec frontend sh" }
}