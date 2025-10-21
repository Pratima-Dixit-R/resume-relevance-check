# Custom Domain Setup Guide for Professional AI Resume Analyzer

This guide provides step-by-step instructions for setting up a custom domain with GoogieHost for your Streamlit Cloud application.

## Prerequisites

1. Deployed Streamlit application on Streamlit Cloud
2. GoogieHost account (free)
3. Access to GoogieHost DNS management

## Step 1: Deploy Your Application to Streamlit Cloud

1. Visit https://share.streamlit.io/
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Set the following options:
   - **Repository**: Your forked repository
   - **Branch**: main
   - **Main file path**: `professional_resume_analyzer.py`
6. Click "Deploy!"

Wait for the deployment to complete and note the URL provided by Streamlit Cloud (e.g., `https://your-app-name.streamlit.app`).

## Step 2: Register Domain with GoogieHost

1. Visit https://www.googiehost.com/
2. Sign up for a free account
3. Navigate to the domain registration section
4. Search for `profesionalairesumeanalyzer.in`
5. Complete the registration process (free domains available)

## Step 3: Configure DNS Settings

1. Log in to your GoogieHost account
2. Navigate to DNS Management
3. Add the following DNS records:

### Option 1: CNAME Record (Recommended)
```
Type: CNAME
Name: www
Value: your-streamlit-app.streamlit.app
TTL: 14400
```

### Option 2: URL Redirect
```
Type: URL Redirect
Name: www
Value: https://your-streamlit-app.streamlit.app
Redirect Type: 301
```

## Step 4: Configure Streamlit Cloud Custom Domain

1. Go back to Streamlit Cloud
2. Navigate to your app settings
3. In the "Custom subdomain" section, add your domain:
   - `www.profesionalairesumeanalyzer.in`
4. Click "Save"

## Step 5: SSL Certificate Configuration

Streamlit Cloud automatically provides SSL certificates for custom domains. No additional configuration is needed.

## Step 6: Verify Setup

1. Wait 5-15 minutes for DNS propagation
2. Visit `https://www.profesionalairesumeanalyzer.in`
3. Verify that your application loads correctly

## Troubleshooting

### Common Issues

1. **DNS Not Propagating**
   - Wait up to 24 hours for DNS changes to propagate
   - Check DNS settings with online tools like `nslookup` or `dig`

2. **SSL Certificate Issues**
   - Ensure your domain is correctly configured in Streamlit Cloud
   - Contact Streamlit support if issues persist

3. **Application Not Loading**
   - Verify the Streamlit app URL is correct
   - Check that the CNAME record points to the correct Streamlit URL

### Verification Commands

```bash
# Check DNS resolution
nslookup www.profesionalairesumeanalyzer.in

# Check HTTP response
curl -I https://www.profesionalairesumeanalyzer.in
```

## Alternative Free Domain Providers

If GoogieHost doesn't meet your needs, consider these alternatives:

1. **Freenom** - Free domains with .tk, .ml, .ga extensions
2. **EU.org** - Free subdomains
3. **No-IP** - Free dynamic DNS service

## Best Practices

1. **Use WWW Subdomain**: Always configure the www subdomain for better compatibility
2. **Enable HTTPS**: Ensure SSL is properly configured for security
3. **Monitor Uptime**: Use free monitoring services to track application availability
4. **Regular Updates**: Keep your application updated with new features and security patches

## Support Resources

- Streamlit Cloud Documentation: https://docs.streamlit.io/streamlit-cloud
- GoogieHost Support: https://www.googiehost.com/support
- DNS Checker: https://dnschecker.org/

## Notes on Free Hosting Limitations

1. **Resource Limits**: Free tiers have CPU/memory limitations
2. **Sleep Mode**: Applications may go to sleep after inactivity
3. **No Custom Code**: Limited to Python/Streamlit applications
4. **Bandwidth Limits**: Monthly bandwidth quotas may apply

For production applications with higher requirements, consider upgrading to paid hosting options.