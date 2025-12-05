# Quickstart: Building the Docusaurus Book

## Prerequisites

- **Node.js**: Version 18.0 or higher (LTS recommended)
- **Git**: Installed and configured
- **OS**: Windows 10/11 or macOS (12+)

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```
   *Note: We use `npm` for consistency.*

## Running Locally

Start the development server:

```bash
npm start
```

- The site will open at `http://localhost:3000`.
- Live reload is enabled; editing `docs/` files updates the browser instantly.

## Building for Production

Generate the static files in `build/`:

```bash
npm run build
```

Test the build locally:

```bash
npm run serve
```

## Deployment (GitHub Pages)

This project uses GitHub Actions. Pushing to `main` (or manually triggering the workflow) handles deployment.

To verify deployment config, check `docusaurus.config.ts`:
- `url`: Your GitHub Pages URL
- `baseUrl`: `/repo-name/`
- `organizationName`: Your GitHub username
- `projectName`: Your repo name
