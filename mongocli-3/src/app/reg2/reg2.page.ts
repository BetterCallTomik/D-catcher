import { Component,  HostListener,  OnInit } from '@angular/core';
import { getAuth,createUserWithEmailAndPassword, signInWithEmailAndPassword, onAuthStateChanged } from "firebase/auth";
import { getDatabase, ref, set, update } from "firebase/database";
import { getStorage, ref as ref_storage, uploadBytesResumable, getDownloadURL } from "firebase/storage";
import {ActivatedRoute, Router} from "@angular/router"

@Component({
  selector: 'app-reg2',
  templateUrl: './reg2.page.html',
  styleUrls: ['./reg2.page.scss'],
})
export class Reg2Page implements OnInit {

loginForm: any = {
  login: '',
  password: ''
}

  constructor(private route: ActivatedRoute, private router: Router) {





    const auth = getAuth();
onAuthStateChanged(auth, (user) => {
  if (user) {
    // User is signed in, see docs for a list of available properties
    // https://firebase.google.com/docs/reference/js/firebase.User
    const uid = user.uid;

    console.log('Reged!!');
//this.router.navigate(['/home', {}]);



  } else {
    // User is signed out
   console.log('not reged');


  }
});







  }

  ngOnInit() {
  }







    printForm(){

  console.log(this.loginForm);

const auth = getAuth();



    createUserWithEmailAndPassword(auth, this.loginForm.login, this.loginForm.password)
  .then((userCredential) => {
    // Signed in
    const user = userCredential.user;

    const uid = user.uid;

    console.log(user);

     const db = getDatabase();
       set(ref(db, 'users/' + uid), {
         login: this.loginForm.login,
         password: this.loginForm.password

       })


       .catch((error) => {
 console.log(error);
});



  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
   console.log(errorCode + ": " + errorMessage);

   alert(errorMessage);
  });



}

}
