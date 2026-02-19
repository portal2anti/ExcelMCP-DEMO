# Push this project to GitHub

The repo is already initialized and committed. To get it on GitHub and share the link:

## 1. Create the repository on GitHub

1. Go to **https://github.com/new**
2. Set **Repository name** to: **`excel-mcp-demo`**
3. Leave it **empty** (no README, no .gitignore, no license).
4. Click **Create repository**.

## 2. Push from your machine

The remote is already set to:

`https://github.com/nikolazivanovic/excel-mcp-demo.git`

If your GitHub username is different, update it:

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/excel-mcp-demo.git
```

Then push (you’ll be prompted for your GitHub credentials or use SSH):

```bash
cd /Users/nikolazivanovic/CursorProjects/ExcelMCP-DEMO
git push -u origin main
```

## 3. Share the link

After a successful push, your colleague can use:

**https://github.com/nikolazivanovic/excel-mcp-demo**

(Replace `nikolazivanovic` with your GitHub username if you changed the remote.)

They can clone the repo or download the files (Code → Download ZIP).
