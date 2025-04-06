## Dev Setup
### Setup Python
1. Install Python
```zsh
uv python list
uv python install 3.13.2
```
2. Setup Project
```zsh
uv init --package --name langgate
```

# Debug Docker Image
```zsh
docker run --rm -it --entrypoint /bin/sh langgate
```
