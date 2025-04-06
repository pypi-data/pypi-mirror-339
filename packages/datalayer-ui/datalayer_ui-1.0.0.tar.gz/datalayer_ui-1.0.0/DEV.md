[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

# Ξ Datalayer UI

The `UI` (User Interface) it-self (aka the React.js WEB Application) are pure static (HTML, JavaScript and CSS) artifacts hosted on any CDN (Content Delivery Network).

The UI depends on a `Plane` (aka the Backend services), are the cloud services running on a Kubernetes cluster to which the UI connects.

## Setup

Ensure you have a conda environment as described in the [metarepo](https://github.com/datalayer/metarepo) and get the source code.

```bash
git clone https://github.com/datalayer/ui.git
cd ui
git clone https://github.com/datalayer/images.git src/assets/images
```

We recommend giving more memory to Node.js... otherwise you won't be able to compile the source code.

```bash
export NODE_OPTIONS="--max-old-space-size=8192"
```

Install the dependencies.

```bash
npm i
```

Ensure you have installed the following Jupyter extensions:

- [Datalayer Core](https://github.com/datalayer/datalayer-ui) with `pip install datalayer-core`.
- [Jupyter IAM](https://github.com/datalayer/jupyter-iam) with `pip install jupyter-iam`.
- [Jupyter Kernels](https://github.com/datalayer/jupyter-kernels) with `pip install jupyter-kernels`.

Alternatively, you can install all the needed Jupyter extensions with a single command `pip install datalayer`.

If you need to change those Jupyter extensions, you can install them from source. For that, you will need to clone the respective GitHub repositories and follow the instructions in the README.md.

## Datalayer UI - Cloud Plane

Start the Datalayer UI with a Datalayer Plane in the Cloud.

```bash
# Terminal 1.
export DATALAYER_RUN_URL=https://prod1.datalayer.run
export DATALAYER_WHITE_LABEL=true
# npm run jupyter:server
plane jupyter-server
```

```bash
# Terminal 2.
# open http://localhost:3063
npm run app:prod
```

```bash
# Terminal 2 (option).
# open http://localhost:3063
# export DATALAYER_RUN_URL=https://prod1.datalayer.run
# export JUPYTER_SERVER_URL=https://prod1.datalayer.run/api/jupyter-server
# export DATALAYER_WHITE_LABEL=true
# npm run all|app|core|iam|runtimes|mock|example|editor
npm run app
```

```bash
# Terminal 2 (option).
ENTRY="./src/App" npm run start
```

## Datalayer UI - Local Plane

For local Development, setup the environment variables expected by the local servers and use the following scripts to run the Datalayer Plane locally.

```bash
# Terminal 1 - Start a proxy to Solr.
# open http://localhost:8983
plane pf-solr
```

```bash
# Terminal 2 - Start a proxy to OpenFGA.
# open http://localhost:8098/stores
plane pf-openfga
```

```bash
# Terminal 3 - Start a proxy to Vault.
# open http://localhost:8200
plane pf-vault
```

```bash
# Terminal 4 - Start the local Jupyter Server.
# open http://localhost:8686/api/jupyter-server?token=60c1661cc408f978c309d04157af55c9588ff9557c9380e4fb50785750703da6
# With Plane.
unset DATALAYER_RUN_URL
plane jupyter-server
```

```bash
# Terminal 5 - Start the local Plane.

# IAM API
# open http://localhost:9700/api/iam/v1/ui
# open http://localhost:9700/api/iam/v1/ping
# open http://localhost:9700/api/iam/version

# Spacer API
# open http://localhost:9900/api/spacer/v1/ui
# open http://localhost:9900/api/spacer/v1/ping
# open http://localhost:9900/api/spacer/version

# Library API
# open http://localhost:9800/api/library/v1/ui
# open http://localhost:9800/api/library/v1/ping
# open http://localhost:9800/api/library/version

plane local
```

```bash
# Terminal 6 - Start the local Web Application.
# Tune the the configuration in `./public/index-local.html`
# open http://localhost:3063
npm run app:local
```

Browse the Web pages.

```bash
export DATALAYER_CDN_URL=http://localhost:3063

# Anonymous Pages.
open $DATALAYER_CDN_URL
open $DATALAYER_CDN_URL/about
open $DATALAYER_CDN_URL/compare
open $DATALAYER_CDN_URL/connect
open $DATALAYER_CDN_URL/docs
open $DATALAYER_CDN_URL/dataliens
open $DATALAYER_CDN_URL/features
open $DATALAYER_CDN_URL/join
open $DATALAYER_CDN_URL/join?form=true
open $DATALAYER_CDN_URL/legacy/landing
open $DATALAYER_CDN_URL/library
open $DATALAYER_CDN_URL/login
open $DATALAYER_CDN_URL/pricing
open $DATALAYER_CDN_URL/privacy
open $DATALAYER_CDN_URL/guide
open $DATALAYER_CDN_URL/reports/ai
open $DATALAYER_CDN_URL/reports/gdpr
open $DATALAYER_CDN_URL/reports/security
open $DATALAYER_CDN_URL/support
open $DATALAYER_CDN_URL/team
open $DATALAYER_CDN_URL/terms
open $DATALAYER_CDN_URL/terms-of-service
open $DATALAYER_CDN_URL/testimonials
open $DATALAYER_CDN_URL/tos

open $DATALAYER_CDN_URL/ai

open $DATALAYER_CDN_URL/reports
open $DATALAYER_CDN_URL/reports/ai
open $DATALAYER_CDN_URL/reporst/gdpr
open $DATALAYER_CDN_URL/security

# Anonymous Example Pages.
open $DATALAYER_CDN_URL/examples/article
open $DATALAYER_CDN_URL/examples/category
open $DATALAYER_CDN_URL/examples/features
open $DATALAYER_CDN_URL/examples/features/ai
open $DATALAYER_CDN_URL/examples/features/ai/0
open $DATALAYER_CDN_URL/examples/features/ai/1
open $DATALAYER_CDN_URL/examples/features/ai/2
open $DATALAYER_CDN_URL/examples/features/bento
open $DATALAYER_CDN_URL/examples/features/landing
open $DATALAYER_CDN_URL/examples/loom
open $DATALAYER_CDN_URL/examples/stars
# open $DATALAYER_CDN_URL/examples/features/sides1
# open $DATALAYER_CDN_URL/examples/features/sides2

# Authenticated Pages.
open $DATALAYER_CDN_URL
open $DATALAYER_CDN_URL/docs
open $DATALAYER_CDN_URL/support
open $DATALAYER_CDN_URL/costs
open $DATALAYER_CDN_URL/logout
open $DATALAYER_CDN_URL/settings/run
```

## JupyterLab - Full or Headless

```bash
# Terminal 1.
# open http://localhost:8686/api/jupyter-server?token=60c1661cc408f978c309d04157af55c9588ff9557c9380e4fb50785750703da6
unset DATALAYER_RUN_URL
# DATALAYER_RUN_URL=https://prod1.datalayer.run
# DATALAYER_WHITE_LABEL=true
plane jupyter-server
```

```bash
# Terminal 2.
# open http://localhost:3063
npm run core
npm run core:local
npm run core:jupyterlab
npm run core:jupyterlab:local
#
npm run iam
npm run iam:local
npm run iam:jupyterlab
npm run iam:jupyterlab:local
#
npm run runtimes
npm run runtimes:local
npm run runtimes:jupyterlab
npm run runtimes:jupyterlab:local
#
npm run runtimes:debug
#
npm run all
npm run all:local
npm run all:jupyterlab
npm run all:jupyterlab:local
#
npm run cli # open http://localhost:3063/datalayer/login/cli
#
npm run example
npm run example:local
npm run example:jupyterlab
npm run example:jupyterlab:local
```

## Storybook

Start the Storybook.

```bash
# mkdir ../../../node_modules/@jupyterlite/javascript-kernel-extension/style
# cp -r style/icons ../../../node_modules/@jupyterlite/javascript-kernel-extension/style
# open http://localhost:6006
npm run storybook
```

## Benchmarks

```bash
# open http://localhost:3063
npm run benchmarks
npm run benchmarks:local
```

## Mocks

```bash
# Start Web Application with Mock.
# open http://localhost:3063
npm run app:mock
```

```bash
# Start JupyterLab Headless with Mock.
# open http://localhost:3063
npm run mock
```

```bash
# Start JupyterLab with Mock.
# open http://localhost:3063
npm run mock:jupyterlab
```

## Build

```bash
# Build TypeScript.
npm run run build:tsc
```

```bash
# Build and watch TypeScript.
npm run watch:tsc
```

```bash
# Build the Web Application.
npm run run build:webpack
```

## Kill

```bash
# Run this command if any server does not stop or is in a "ghost" state.
npm run kill
```

## Connect to External Provider

```bash
# Terminal 1.
DATALAYER_RUN_URL=https://datalayer.anacondaconnect.com \
  DATALAYER_WHITE_LABEL=true \
  plane jupyter-server
```

Launch and add via your Browser Devtool a `refresh_token` cookie with the value you will get from your provider, or click on `Login with a Token` and submit with the token. You can also set the cookie pasting this command in your Browser Devtools.

```js
document.cookie = "refresh_token=YOUR_TOKEN; path=/";
```

```bash
# Terminal 2.
# open http://localhost:3063
npm run runtimes:jupyterlab
```

You can run JupyterLab with traits.

```bash
jupyter lab \
  --DatalayerExtensionApp.run_url="https://datalayer.anacondaconnect.com" \
  --DatalayerExtensionApp.white_label="True" \
  --DatalayerExtensionApp.Launcher.category="Datalayer" \
  --DatalayerExtensionApp.Launcher.name="Anaconda Runtimes" \
  --DatalayerExtensionApp.Launcher.icon_svg_url="https://raw.githubusercontent.com/datalayer/icons/main/svg/data1/anaconda.svg" \
  --DatalayerExtensionApp.Brand.name="Anaconda" \
  --DatalayerExtensionApp.Brand.about="Anaconda Notebooks" \
  --DatalayerExtensionApp.Brand.docs_url="https://www.anaconda.com/docs/tools/anaconda-notebooks/gpu-kernels#gpu-kernels-beta" \
  --DatalayerExtensionApp.Brand.support_url="https://anaconda.com" \
  --DatalayerExtensionApp.Brand.pricing_url="https://anaconda.com/pricing" \
  --DatalayerExtensionApp.Brand.terms_url="https://anaconda.com" \
  --DatalayerExtensionApp.Brand.privacy_url="https://anaconda.com"
```

## Deployments

```bash
# Deploy Datalayer UI to Production.
# open https://datalayer.io
make deploy-io
```

```bash
# Deploy Datalayer UI to Development.
# open https://dev1.datalayer.io
make deploy-dev
```

```bash
# Deploy the Storybook.
# open https://storybook.datalayer.tech
make deploy-storybook
```

## Pyodide

```bash
pip install jupyterlite-pyodide-kernel
```

## [DEPRECATED] Develop without UI

You can use `pip install -e .` after removing the Datalayer UI dependencies.

The following files must be modified to remove the Datalayer UI dependencies:

### 1. `src/CLIApp.tsx`

Remove the entire content.

### 2. `src/jupyterlab/index.ts`

Remove the entire content.

### 3. `dalayer_ui/__init__.py`

Remove the line `from dalayer_ui._version import __version__`.

Add `__version__ = '1.0.24'`.

### 4. `pyproject.toml`

Remove the following lines:

```toml
[tool.hatch.version]
source = "nodejs"
```

```toml
[tool.hatch.metadata.hooks.nodejs]
fields = ["description", "authors", "urls"]
```

```toml
[tool.hatch.build.hooks.jupyter-builder]
dependencies = ["hatch-jupyter-builder>=0.5"]
build-function = "hatch_jupyter_builder.npm_builder"
ensured-targets = [
    "dalayer_ui/labextension/static/style.js",
    "dalayer_ui/labextension/package.json",
]
skip-if-exists = ["dalayer_ui/labextension/static/style.js"]

[tool.hatch.build.hooks.jupyter-builder.build-kwargs]
build_cmd = "build:prod"
npm run = ["jlpm"]

[tool.hatch.build.hooks.jupyter-builder.editable-build-kwargs]
build_cmd = "install:extension"
npm run = ["jlpm"]
source_dir = "src"
build_dir = "dalayer_ui/labextension"

[tool.jupyter-releaser.options]
version_cmd = "hatch version"
```

Add the following lines:

```toml
[tool.hatch.version]
path = "dalayer_ui/__init__.py"
```
