# Mobile Strategy App
A React native app that will fetch data from our strategy API and display information about our car (at the moment, the plan is current velocity, recommended velocity, and current elevation).

## Setup
Everything for setting up initially is available in the [documentation](https://reactnative.dev/docs/environment-setup).

## Some Notes for Windows:
+ You can only run Android version of the app (on the Android emulator or a connected device). Open android folder in Android Studio and run it on the device. If you haven't run before, you might be missing the right Android emulator device requirements. See React Native getting started documentation.
+ From command prompt, run `npx react-native run-android`. You may also need to run  `npm install` to install the various node_modules.
+ If you encounter a build error saying `:app:processDebugResources FAILED`, try cleaning android folder. From root project folder (MobileStrategyApp), `cd android` and run `gradlew clean`. 