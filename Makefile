.PHONY: runserver migrate shell createsuperuser makemigrations

TAG="\n\n\033[0;32m\#\#\# "
END=" \#\#\# \033[0m\n"

HOST=localhost
PORT=8080
PYTHONPATH=ecommerce
DJANGO_SETTINGS=ecommerce.settings.base

django-command = django-admin $(1) $(2) --settings $(DJANGO_SETTINGS) --pythonpath $(PYTHONPATH)

runserver:
	@echo $(TAG)Running Server $(END)
	$(call django-command, runserver, $(HOST):$(PORT))

shell:
	@echo $(TAG)Running Shell $(END)
	$(call django-command, shell)

migrate:
	@echo $(TAG)Migrating Database$(END)
	$(call django-command, migrate)

makemigrations:
	@echo $(TAG)Creating Migrations$(END)
	$(call django-command, makemigrations)

createsuperuser:
	@echo $(TAG)Create Superuser$(END)
	$(call django-command, createsuperuser)

test:
	@echo $(TAG)Test$(END)
	$(call django-command, test api)

load_initial_data:
	@echo $(TAG)Test$(END)
	$(call django-command, load_initial_data)
