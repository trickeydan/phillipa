# Phillipa the Dolphin

A discord bot. Likes flowers.

## Deployment

- Add `DISCORD_TOKEN=token` to a .env file.

- `docker build -t phillipa .`

- `docker stack deploy phillipa -c docker-compose.yml`
    - This is for a docker swarm cluster.

- Rejoyce.

## Development

You probably don't want to use the production bot account :P

Note: There are some token in the history of this repo, they were revoked being publishing.