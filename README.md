# ondo

This is a quick and dirty fast api + htmx implementation of my personal website.
It integrates with the IPLD based CMS that I built for myself [here](https://github.com/amiller68/leaky).

Check out the [live site](https://krondor.org) to see it in action.

## requirements

- python 3.12
- tailwindcss@3 (install with `npm install -g tailwindcss@3`)
- virtualenv
- ruby and kamal (for deployments)

## setup

```bash
git clone https://github.com/amiller68/ondo.git
cd ondo
# setup virtualenv and install dependencies
./bin/install.sh
# run the dev server
./bin/dev.sh
```

server should be running locally at [http://localhost:8000](http://localhost:8000)

## maintenance

format code:

```bash
./bin/fmt.sh
```

run linters:

```bash
./bin/lint.sh
```

run type checkers:

```bash
./bin/types.sh
```

run all checks:

```bash
./bin/checks.sh
```

## styling

we use tailwindcss for styling. be sure to run `./bin/tailwind.sh` to build the css when you make changes to `tailwind.config.js` or  `styles/main.css`.

## deploying

Be sure to setup an appropriate `DOCKERHUB_TOKEN` in your environment for the configured [container registry](https://hub.docker.com/repository/docker/amiller68/ondo/general).

Then just run kamal deploy:

```bash
kamal deploy
```

See the [kamal docs](https://kamal-deploy.org/docs) for more information.

CI/CD is fully automated in this repo, so no need to worry about it.
Pushing to main will deploy to the live site.