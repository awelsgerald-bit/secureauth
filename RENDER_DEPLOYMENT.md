# Deploy to Render (Free) - Step by Step

Render is the **easiest and best free option** for deploying your Flask app!

## ✅ 5-Minute Deployment

### Step 1: Sign Up (1 minute)

1. Go to https://render.com
2. Click "Get Started"
3. Choose "Sign up with GitHub" (easiest)
4. Authorize Render to access your GitHub

### Step 2: Create Web Service (2 minutes)

1. On Render dashboard, click "New +" button
2. Select "Web Service"
3. You'll see your GitHub repositories
4. Click "Connect" next to `secureauth`

### Step 3: Configure (2 minutes)

Fill in the form:

```
Name:                    secureauth
Runtime:                 Python 3
Build Command:           pip install -r requirements.txt
Start Command:           gunicorn app:app
```

Scroll down and add **Environment Variables**:

```
SECRET_KEY = your-super-secret-key-12345
FLASK_ENV = production
```

(Optional but recommended)
```
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = your-email@gmail.com
MAIL_PASSWORD = your-app-password
```

### Step 4: Deploy (Click one button!)

Click "Create Web Service"

Render will:
- ✓ Pull from GitHub
- ✓ Install dependencies
- ✓ Start your app
- ✓ Give you a live URL

### Step 5: Your Live App! 🎉

You'll get a URL like:
```
https://secureauth.onrender.com
```

**That's it! Your app is live!**

---

## After Deployment

### View Your App

Click the URL in Render dashboard to open it

### Watch Logs

Click "Logs" tab to see what's happening:
```
Building...
Installing dependencies...
Starting gunicorn...
✓ Web service is live
```

### Test Your App

Visit:
- `https://secureauth.onrender.com` - Main site
- `https://secureauth.onrender.com/profile` - Try login
- Test all features!

### Update GitHub

Add this to your GitHub repository:

```markdown
## 🚀 Live Demo

[Visit Live Demo](https://secureauth.onrender.com)
```

In GitHub repo → About → Website, paste your Render URL

---

## Troubleshooting

### App shows "Service Unavailable"

This is normal! Free tier on Render spins down after 15 min of no activity.
- Wait 30 seconds for restart
- It will be back up

### "Build failed" error

1. Check Logs tab for error message
2. Common issues:
   - Missing `requirements.txt`
   - Syntax error in code
   - Missing environment variable
3. Fix and push to GitHub
4. Render auto-redeploys!

### Logs show 500 error

1. Check Logs for specific error
2. Usually missing environment variable
3. Add to Render dashboard → Environment
4. Restart web service

### How to restart

In Render dashboard:
1. Click "Web Service" name
2. Click "..." menu
3. Select "Restart"

---

## Make It Faster (Optional)

### Reduce Cold Start Time

Add to `Procfile`:
```
web: gunicorn --workers 1 --threads 2 --worker-class gthread app:app
```

### Use Different Region

In Render dashboard → Settings → Region
(Choose closest to users)

---

## Add Custom Domain (Later)

Once app is working:

1. Buy domain (Google Domains, Namecheap, etc.)
2. In Render → Settings → Custom Domains
3. Follow DNS setup instructions
4. Wait 24 hours for propagation

Then your app is at: `https://yourdomain.com`

---

## Free Plan Limits

- ✓ 750 hours/month (enough for always-on)
- ✓ Hibernates after 15 min inactivity
- ✓ 1GB RAM
- ✓ 0.5 vCPU
- ✓ Unlimited databases

**Perfect for hobby projects and portfolios!**

---

## Upgrade Later (If Needed)

When you need:
- Always-on (no hibernation)
- More power
- Professional SLA

Just click "Upgrade" in Render dashboard - pricing starts at $7/month

---

## GitHub Auto-Deploy

Every time you push to GitHub:

```bash
git add .
git commit -m "Update features"
git push origin main
```

Render **automatically redeploys** your app! 🚀

No extra commands needed!

---

## Example: Full Workflow

```bash
# 1. Make changes locally
# (edit files, test with: python app.py)

# 2. Commit and push
git add .
git commit -m "Add new feature"
git push origin main

# 3. Check Render dashboard
# (it will auto-deploy in 1-2 minutes)

# 4. Test live app
# Visit: https://secureauth.onrender.com

# 5. Done! 🎉
```

---

## Need Help?

- Render Docs: https://render.com/docs
- Flask Guide: https://flask.palletsprojects.com
- GitHub Integration: https://render.com/docs/github

Your app is live! 🚀
