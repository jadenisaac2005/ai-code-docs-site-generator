# AI Code Documentation Site Generator

*A project for the DigitalOcean & Hacktoberfest AI Hackathon (October 2025)*

This repository contains a fully automated CI/CD pipeline that scans a codebase, uses an AI model to generate documentation for each file, and deploys a beautiful, ready-to-use documentation website to GitHub Pages.

[![Documentation Status](https://github.com/jadenisaac2005/ai-code-docs-site-generator/actions/workflows/deploy.yml/badge.svg)](https://github.com/jadenisaac2005/ai-code-docs-site-generator/actions)

**Live Demo Site:** [https://jadenisaac2005.github.io/ai-code-docs-site-generator/](https://jadenisaac2005.github.io/ai-code-docs-site-generator/)

---
## Features
* **Automated Documentation:** Automatically generates documentation for Python files on every push to the `main` branch.
* **AI-Powered:** Leverages a powerful AI model via an API to create clear, technical descriptions of the source code.
* **Static Site Generation:** Uses MkDocs with the Material theme to build a clean, modern, and searchable documentation website.
* **Continuous Deployment:** Deploys the latest version of the documentation website to GitHub Pages automatically using GitHub Actions.

---
## How It Works

The entire process is orchestrated by a GitHub Actions workflow:
1.  **On Push:** The workflow is triggered whenever new code is pushed to the `main` branch.
2.  **Checkout Code:** The action checks out the latest version of the repository.
3.  **Run AI Script:** A Python script (`generate_docs.py`) scans the codebase, sends the content of each file to an AI endpoint, and saves the generated documentation as Markdown files in the `/docs` directory.
4.  **Build Site:** MkDocs builds a static HTML website from the generated Markdown files.
5.  **Deploy:** The final built site is automatically pushed to the `gh-pages` branch, making it live on GitHub Pages.



---
## Technology Stack
* **Backend:** Python
* **AI Model:** Deployed on DigitalOcean's Gradient Platform
* **Website:** MkDocs & MkDocs-Material
* **CI/CD & Hosting:** GitHub Actions & GitHub Pages

---
## Team
* **Jaden Isaac**
* **Tanush Jaisankar** 
* **Shayan Ponnanna Malchira**
