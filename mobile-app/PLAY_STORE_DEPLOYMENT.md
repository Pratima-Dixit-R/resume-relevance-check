# Play Store Deployment Guide

This guide will help you deploy the Resume AI Analyzer app to the Google Play Store.

## Prerequisites

1. A Google Play Developer account ($25 one-time registration fee)
2. Android Studio installed
3. The app built and tested

## Step 1: Create a Signed APK or App Bundle

### Using Android Studio:

1. In Android Studio, go to **Build** > **Generate Signed Bundle / APK**
2. Select **Android App Bundle** (recommended) or **APK**
3. Click **Next**

### Create a Keystore (if you don't have one):

1. Click **Create new...**
2. Fill in the following:
   - **Key store path**: Choose a location to save your keystore file
   - **Password**: Create a strong password
   - **Key alias**: resume-ai-analyzer
   - **Key password**: Create another strong password
   - **First and Last Name**: Your name
   - **Organizational Unit**: Optional
   - **Organization**: Your organization or personal name
   - **City or Locality**: Your city
   - **State or Province**: Your state
   - **Country Code**: Your country code (e.g., US)

4. Click **OK** and remember to save your keystore file in a secure location

### Sign the App:

1. Select your keystore file
2. Enter your keystore password
3. Select your key alias
4. Enter your key password
5. Click **Next**
6. Select **release** for the destination folder
7. Select **V2 (Full APK Signature)** (and V1 if targeting Android < 7.0)
8. Click **Finish**

## Step 2: Create a Google Play Developer Account

1. Go to [Google Play Console](https://play.google.com/console)
2. Click **Get started** or **Create Account**
3. Follow the registration process
4. Pay the $25 registration fee

## Step 3: Create a New Application

1. In Google Play Console, click **Create App**
2. Fill in the following:
   - **App name**: Resume AI Analyzer
   - **Default language**: English (US)
   - **App or game**: App
   - **Free or paid**: Free
   - **Category**: Productivity
3. Click **Create app**

## Step 4: Fill in App Details

### Dashboard Information:
1. Go to **Main store presence** > **Dashboard**
2. Fill in the required information:
   - **Short description**: AI-powered resume analysis tool that matches your resume with job descriptions
   - **Full description**: 
     ```
     Resume AI Analyzer is an advanced tool that helps job seekers optimize their resumes by matching them with job descriptions. Using artificial intelligence, it analyzes your resume against job requirements and provides detailed feedback on how to improve your chances of getting hired.
     
     Features:
     - AI-powered resume analysis
     - Job description matching
     - Detailed scoring and feedback
     - Keyword gap analysis
     - Cross-platform compatibility
     - Free to use
     ```
   - **Application type**: Applications
   - **Category**: Productivity
   - **Tags**: resume, job, career, AI, analyzer, matching

### Content Rating:
1. Go to **Main store presence** > **Content rating**
2. Complete the questionnaire honestly based on your app's content

### Contact Details:
1. Go to **Main store presence** > **Contact details**
2. Fill in your contact information

## Step 5: Upload Your App

1. Go to **Release** > **Production** > **Create new release**
2. Click **Upload** and select your signed App Bundle (.aab) or APK
3. Review the app content and fill in any missing information

## Step 6: Create Store Listing

### Screenshots:
1. Prepare screenshots of your app (minimum 2, recommended 4-8)
2. Upload them in the **Graphic assets** section:
   - Phone screenshots: 320px to 3840px wide, 16:9 or 9:16 aspect ratio
   - Tablet screenshots: 16:9 aspect ratio

### Graphic Assets:
1. **App icon**: 512x512 PNG
2. **Feature graphic**: 1024x500 JPG or PNG
3. **Promo graphic**: 180x120 JPG or PNG (optional)

## Step 7: Review and Submit

1. Review all information
2. Click **Save** and then **Review release**
3. Confirm all details are correct
4. Click **Start rollout to Production**
5. Wait for Google's review process (usually 1-3 days)

## Important Notes

1. **App Icon**: Make sure your app icon follows Google Play design guidelines
2. **Privacy Policy**: You'll need a privacy policy URL in your app store listing
3. **App Size**: App Bundles are preferred as they reduce app size for users
4. **Testing**: Consider using internal testing tracks before production release
5. **Updates**: You can update your app at any time after approval

## After Approval

Once your app is approved, it will be available on the Google Play Store. You can share the link with users and promote your app.