import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';
import { environment } from './environments/environment';




// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCKhhnOXdBkD2udkP1hZiGrdjlCuSll5OA",
  authDomain: "nearmeeting-afc99.firebaseapp.com",
  projectId: "nearmeeting-afc99",
  storageBucket: "nearmeeting-afc99.appspot.com",
  messagingSenderId: "819922553345",
  appId: "1:819922553345:web:42cb6c77c8281ede78ce00"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

if (environment.production) {
  enableProdMode();
}

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.log(err));
