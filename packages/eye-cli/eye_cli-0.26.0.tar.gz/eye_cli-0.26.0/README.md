# eye

The CLI for moving files and processing photogrammetry data. 

## Install

```shell
pipx install eye-cli
```

open a new terminal

```shell
eye --install-completion
```

## Upgrade

```shell
pipx upgrade eye-cli
eye --install-completion
```


---



## Contributing to the CLI

### Run latest code you have in your IDE

Run the installed package:
```bash
eye
```

Run your latest code, not as an installed package
```shell
poetry run eye
```

### Commit + Publish a change

- Write the updated code and test it
- Run the appropriate Publish command, below
- make the final commit after publish, which commits the version number updated by publish

### Publish

```shell
poetry version major
poetry publish --build
```

```shell
poetry version minor
poetry publish --build
```

```shell
poetry version patch
poetry publish --build
```

