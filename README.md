# downloader-4anime
Automated anime downloader from the [*4anime.to*](https://4anime.to/) website
### Install
```bash
pip install downloader-4anime
```
### Usage
This library can be used from python scripts and from the CLI
#### CLI
 * Downloading a single episode
   ```bash
   animed naruto-shippuden -e 86 # can use --episode instead of -e
   ```
 * Downloading multiple episodes
   ```bash
   animed naruto-shippuden -E "86 88 90" # can use --episodes instead of -E
   ```
 * Downloading episodes in a specific range
   ```bash
   animed naruto-shippuden -r 86 90 # can use --rangw instead of -r
   ```
The videos are downloaded by default in the current working directory. You can change this by adding the `-d /some/output/dir` or `--dir /some/output dir`.

