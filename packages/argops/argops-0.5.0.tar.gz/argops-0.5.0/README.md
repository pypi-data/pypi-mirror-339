# argops

A command-line interface for promoting Argocd applications between environments.

Features:

- smart promote of value files between environments
- Dry-run option to see the changes.

## Installing

```bash
pipx install argops
```

It's recommended that you add to your ArgoCD `.gitignore` the `*-decrypted.yaml` string. This pattern will exclude these temporary files from being committed to your git repository. These files are created by `argops` during the decryption and encryption of sops secrets. Although `argops` cleans up these files after use, there's a possibility that they might be left behind if an error occurs during processing.

## Usage

To use the tool, simply run it from your terminal on the directory where your environment directories are.

```bash
argops \
  --src-dir=<source directory> \
  --dest-dir=<destination directory> \
  --dry-run
```

By default the source directory is `staging` and the destination directory `production`. The `--dry-run` flag will show you what changes will it do without making them.

Once you know that the changes are OK, remove the `--dry-run` option.

## Known issues

### Comments of promoted secrets are over the changed line 

When you promote an environment specific values file, there are inline comments on the keys that have changed. However, sops doesn't support this format and adds the comment above the changed line. It's an upstream issue that is difficult to be addressed by us.

## Development

If you want to run the tool from source, make sure you have Python and all required packages installed. You can do this using:
```bash
git clone https://codeberg.org/lyz/argops 
cd argops
make init
```

## Help

If you need help or want to report an issue, please see our [issue tracker](https://codeberg.org/lyz/argops/issues).

## License

GPLv3

## Authors

Lyz
