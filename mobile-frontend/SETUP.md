# QuantumAlpha Mobile Frontend - Setup Guide

## Prerequisites

- Node.js >= 16
- React Native CLI
- For iOS: Xcode 14+, CocoaPods
- For Android: Android Studio, JDK 11+

## Installation

1. Install dependencies:

   ```bash
   npm install
   # or
   yarn install
   ```

2. Install iOS pods (iOS only):

   ```bash
   cd ios && pod install && cd ..
   ```

3. Create .env file (copy from .env.example):

   ```bash
   cp .env.example .env
   ```

4. Update .env with your API endpoint and credentials

## Running the App

### Development Mode

```bash
# Start Metro bundler
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android
```

### Building

```bash
# Build Android APK
npm run build:android

# Build iOS (requires Mac)
npm run build:ios
```

## Testing

```bash
# Run unit tests
npm test

# Run E2E tests (iOS)
npm run test:e2e:ios

# Run E2E tests (Android)
npm run test:e2e:android
```

## Backend Setup

The mobile app connects to the QuantumAlpha backend. To run the backend locally:

```bash
cd ../backend
# Follow backend README for setup
docker-compose up
```

The default API endpoint is `http://localhost:8080`. Update this in your `.env` file if needed.

## Troubleshooting

### iOS

- Clean build: `cd ios && xcodebuild clean && cd ..`
- Reset pods: `cd ios && pod deintegrate && pod install && cd ..`

### Android

- Clean gradle: `cd android && ./gradlew clean && cd ..`
- Reset cache: `npm start -- --reset-cache`

### General

- Clear watchman: `watchman watch-del-all`
- Reset Metro: `npm start -- --reset-cache`
- Reinstall: `rm -rf node_modules && npm install`
