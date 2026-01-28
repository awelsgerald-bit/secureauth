# Heroku Deployment Guide

Deploy your SecureAuth app to Heroku in 5 minutes!

## Prerequisites

1. **Heroku Account**: Sign up at https://www.heroku.com (free tier available)
2. **Heroku CLI**: Download from https://devcenter.heroku.com/articles/heroku-cli

## Installation Steps

### 1. Install Heroku CLI

```bash
# Download and install from the link above, then verify:
heroku --version
```

### 2. Login to Heroku

```bash
heroku login
# Opens browser to authenticate
```

### 3. Create Heroku App

```bash
cd C:\Users\USER\Documents\FlaskAuthSystem

# Create app (replace with your preferred name)
heroku create secureauth-yourname

# Or let Heroku generate a name:
heroku create
```

### 4. Add Gunicorn to Requirements

```bash
# Add gunicorn to requirements.txt (already included in our file)
pip install gunicorn
```

### 5. Set Environment Variables

```bash
# Set SECRET_KEY
heroku config:set SECRET_KEY="your-super-secret-key-here"

# Set Flask environment
heroku config:set FLASK_ENV=production

# Email configuration (optional but recommended)
heroku config:set MAIL_SERVER=smtp.gmail.com
heroku config:set MAIL_PORT=587
heroku config:set MAIL_USE_TLS=True
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-app-password

# Database (Heroku uses SQLite by default, PostgreSQL for production)
# For production, use PostgreSQL Add-on:
heroku addons:create heroku-postgresql:hobby-dev
```

### 6. Update requirements.txt

Make sure `gunicorn` is in requirements.txt. Add it if needed:

```bash
echo gunicorn==21.2.0 >> requirements.txt
pip install -r requirements.txt
```

### 7. Commit Changes

```bash
git add Procfile runtime.txt requirements.txt
git commit -m "Add Heroku deployment configuration"
git push origin main
```

### 8. Deploy to Heroku

```bash
git push heroku main
```

Or if using a different branch:

```bash
git push heroku yourbranch:main
```

### 9. Initialize Database

```bash
# Create database tables
heroku run python -c "from app import create_app, db; app = create_app(); db.create_all()"
```

### 10. View Your App

```bash
heroku open
# Or visit: https://your-app-name.herokuapp.com
```

## View Logs

```bash
# Real-time logs
heroku logs --tail

# View specific number of lines
heroku logs -n 100
```

## Troubleshooting

### App won't start
```bash
heroku logs --tail  # Check error messages
```

### Database issues
```bash
heroku run python
>>> from app import create_app, db
>>> app = create_app()
>>> db.create_all()
>>> exit()
```

### Reset database
```bash
heroku pg:reset DATABASE
heroku run python -c "from app import create_app, db; app = create_app(); db.create_all()"
```

## Useful Commands

```bash
# View app info
heroku apps:info

# View environment variables
heroku config

# Run one-off command
heroku run python -c "print('hello')"

# Access app shell
heroku run python

# Scale dynos
heroku ps:scale web=1

# View running dynos
heroku ps

# Restart app
heroku restart

# View app URL
heroku domains
```

## Production Checklist

- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS (automatic on Heroku)
- [ ] Configure PostgreSQL database
- [ ] Set up email service
- [ ] Configure OAuth credentials for Google/GitHub
- [ ] Enable monitoring and error tracking
- [ ] Set up automatic backups
- [ ] Configure domain (optional)

## Costs

- **Free tier**: 550 free dyno hours/month
- **Paid tier**: $7/month for always-on app
- **PostgreSQL**: $9/month for hobby tier

## Custom Domain (Optional)

```bash
# Add custom domain
heroku domains:add www.yourdomain.com

# Update DNS records as per Heroku instructions
```

## Next Steps

After deployment:

1. **Update GitHub README** with live link
2. **Share live URL** in your portfolio
3. **Test all features** on live site
4. **Monitor app** using `heroku logs`

## Example Live URL

Your app will be at:
```
https://secureauth-yourname.herokuapp.com
```

Copy this URL to your GitHub repository description and portfolio!

---

**Need Help?**
- Heroku Docs: https://devcenter.heroku.com
- Flask Deployment: https://flask.palletsprojects.com/en/stable/deploying/
- GitHub Integration: https://devcenter.heroku.com/articles/github-integration
