# AstroPredictor Mobile UI Scaffold

This directory contains the structure for the React Native mobile application.

## Recommended Stack
- **Framework**: React Native (Expo)
- **Language**: TypeScript
- **State Management**: Redux Toolkit or Context API
- **Navigation**: React Navigation
- **UI Library**: React Native Paper or Tamagui (for themes)
- **PDF Viewing**: react-native-pdf

## Setup Instructions
1. Initialize project:
   ```bash
   npx create-expo-app .
   ```
2. Install dependencies:
   ```bash
   npm install @react-navigation/native axios react-native-paper
   ```

## Directory Structure (Recommended)
- `src/`
  - `api/`: API client services (connect to FastAPI backend)
  - `components/`: Reusable UI components (InputForm, CategoryCard, ScoreBar)
  - `screens/`: Main screens
    - `HomeScreen.tsx`
    - `InputDetailsScreen.tsx`
    - `PredictionPreviewScreen.tsx`
    - `PDFReportScreen.tsx`
  - `navigation/`: Stack/Tab navigators
  - `assets/`: Images and fonts

## Connecting to Backend
Ensure your FastAPI server is running (`uvicorn app.main:app --reload`) and point your API client to `http://<YOUR_IP>:8000`.
