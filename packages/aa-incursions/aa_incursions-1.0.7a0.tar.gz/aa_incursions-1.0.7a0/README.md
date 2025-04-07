# Incursions for Alliance Auth

Incursion Tools for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/).

## Features

- AA-Discordbot Cogs for information about active incursions, their status and any set Focus
- Webhook notifications for new incursions and them changing state (Mobilizing/Withdrawing)

- WIP Waitlist forked from TLA

## Planned Features

- Waitlist
- AA Fittings Integration
- Secure Groups Integration

## Installation

### Step 1 - Django Eve Universe

Incursions is an App for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/), Please make sure you have this installed. incursions is not a standalone Django Application

Incursions needs the App [django-eveuniverse](https://gitlab.com/ErikKalkoken/django-eveuniverse) to function. Please make sure it is installed before continuing.

Incursions needs the App [Corp Tools](https://github.com/Solar-Helix-Independent-Transport/allianceauth-corp-tools/tree/master/corptools) to feed the Waitlist. You can opt out of using the Waitlist and any of corptools for now. I am transition from Django Eve Universe to Corp Tools #eventually

### Step 2 - Install app

```shell
pip install aa-incursions
```

### Step 3 - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add the following `INSTALLED_APPS` in `local.py`

```python
'incursions',
'corptools',
```

- Add below lines to your settings file:

```python
## Settings for AA-Incursions ##
# Route is Cached for 300 Seconds, if you aren't riding the Kundalini Manifest to the last minute
# Feel free to adjust this to minute='*/5'
CELERYBEAT_SCHEDULE['incursions_update_incursions'] = {
    'task': 'incursions.tasks.update_incursions',
    'schedule': crontab(minute='*/1', hour='*'),
}
```

### Step 4 - Maintain Alliance Auth

- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`
- Restart your project `supervisorctl restart myauth:`

### Step 5 - Pre-Load Django-EveUniverse

- `python manage.py eveuniverse_load_data map` This will load Regions, Constellations and Solar Systems

Preload some expected incursion data. The frontend _should_ adapt to any custom values But it is tested with these.

```shell
python manage.py loaddata waitlist_badges.json
python manage.py loaddata waitlist_category.json
python manage.py loaddata waitlist_category_rule.json
python manage.py loaddata waitlist_roles.json
```

### Step 6 - Setup Waitlist Dependencies

The Waitlist was built to require a Server-Sent Event backend that i have not yet replaced.

#### Bare Metal

Generate a Secret with `openssl rand -hex 32`, use this later in secret=

```shell
git clone https://github.com/luna-duclos/waitlist-sse
docker buildx build . -t tla/sse --load
docker run -d -p 8001:8000 --env SSE_SECRET="0000000000000000000000000000000000000000000000000000000000000000" tla/sse
```

route sse.domain to localhost:8001 in Nginx

#### Docker

git clone <https://github.com/luna-duclos/waitlist-sse>

in NPM route sse.domain route to `sse-server` `8000`
Generate a Secret with `openssl rand -hex 32`, use this in your docker compose
Add the following to your `Docker-Compose.yml`

```docker
  sse-server:
    image: "tla/sse:latest"
    pull_policy: never
    build: ./waitlist-sse
    ports:
      - "8000:8000"
    environment:
      SSE_SECRET: "0000000000000000000000000000000000000000000000000000000000000000"
```

## Contributing

Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at <https://developers.eveonline.com> before submitting any pull requests. All bug fixes or features must not include extra superfluous formatting changes.
