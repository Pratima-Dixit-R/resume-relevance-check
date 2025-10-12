# Resume AI Analyzer - Mobile App

This is the mobile application version of the Resume AI Analyzer, built using Capacitor to wrap the web application in a native container.

## Prerequisites

Before you can build and deploy this app, you'll need:

1. Node.js (v14 or higher)
2. Android Studio (for Android deployment)
3. Xcode (for iOS deployment, macOS only)
4. Android SDK
5. Java Development Kit (JDK)

## Setup Instructions

1. Install dependencies:
   ```bash
   npm install
   ```

2. Add the Android platform:
   ```bash
   npx cap add android
   ```

3. Sync the project:
   ```bash
   npx cap sync
   ```

4. Open the project in Android Studio:
   ```bash
   npx cap open android
   ```

## Building for Android

1. After opening the project in Android Studio, you can build the APK:
   - Go to Build > Build Bundle(s) / APK(s) > Build APK
   - Or use the terminal in Android Studio:
     ```bash
     ./gradlew assembleRelease
     ```

2. The APK will be located in:
   ```
   android/app/build/outputs/apk/release/
   ```

## Building for iOS (macOS only)

1. Add the iOS platform:
   ```bash
   npx cap add ios
   ```

2. Open the project in Xcode:
   ```bash
   npx cap open ios
   ```

3. Configure the signing and build in Xcode.

## Customization

You can customize the app by modifying:

- `capacitor.config.json` - Configuration settings
- `www/index.html` - Loading screen and redirect logic
- Native platform files in `android/` and `ios/` directories

## Deployment to Play Store

To deploy to the Google Play Store:

1. Create a signed APK or App Bundle
2. Create a developer account on Google Play Console
3. Create a new application listing
4. Upload your signed APK/App Bundle
5. Complete the store listing information
6. Submit for review

## Deployment to App Store (iOS)

To deploy to the Apple App Store:

1. Enroll in the Apple Developer Program
2. Create an app record in App Store Connect
3. Archive and upload your app using Xcode
4. Complete the app store listing
5. Submit for review

## Notes

- This is a hybrid app that wraps the web version at https://resume-relevance-check.streamlit.app
- All functionality is provided by the web application
- The native wrapper provides installation and offline capabilities