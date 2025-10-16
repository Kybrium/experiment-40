COMPOSE=docker compose -f docker/dev/compose.yml

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

down-v:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f --tail=200

ps:
	$(COMPOSE) ps

sh-backend:
	$(COMPOSE) exec backend sh

sh-frontend:
	$(COMPOSE) exec frontend sh