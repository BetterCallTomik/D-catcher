import { Component, OnInit , NgZone } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router"
import { getAuth,createUserWithEmailAndPassword, signInWithEmailAndPassword, onAuthStateChanged } from "firebase/auth";

import { getDatabase, ref as ref_database, set, update, child, get  } from "firebase/database";

import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage  {




goods: Array<{id: string; market: string; category: string; item: string; price: number;} > = [];

loginForm: any = {
  login: '',
  password: '',
}
schForm: any = {
  query: ''
}

html_form = 0;
gcount = 0;
ProfName = "";

  constructor(private route: ActivatedRoute, private router: Router, private http: HttpClient) {






  const auth = getAuth();
onAuthStateChanged(auth, (user) => {
  if (user) {
    // User is signed in, see docs for a list of available properties
    // https://firebase.google.com/docs/reference/js/firebase.User
    const uid = user.uid;

    console.log(user.email);


   this.html_form = 0;
    //this.ProfName = "Privet " + uid + " !";
    this.ProfName =  "Пользователь: <b>" + String(user.email) + "</b>";



  const dbRef = ref_database(getDatabase());
get(child(dbRef, 'users/' + uid + '/goods')).then((snapshot) => {
  if (snapshot.exists()) {
   // console.log(snapshot.size);

    this.gcount = snapshot.size;
}else this.gcount = 0;
});



  } else {
    // User is signed out

   console.log('not reged');

this.html_form = 1;
  }
});




//console.log(this.html_form )


  }

Search()
{

this.goods = [];

if (this.schForm.query!=''){







  const config = {
		headers: {


        }
      };

  this.http.get('http://localhost:3000/login?query=' + this.schForm.query, {})






	  .subscribe(
		  data => { // json data


//console.log("дата: " + data)


 (Object.keys(data)).forEach((key, index) => {
  // 👇️ name Bobby Hadz 0, country Chile 1
  //console.log(Docs[key]['ID']+ ", " + Docs[key]['Doctor']);

  //console.log(Object.values(data)[index]);


   this.goods.push({
            id: Object.values(data)[index]["id"],
            market: Object.values(data)[index]["market"],
            category: Object.values(data)[index]["category"],
			      item: Object.values(data)[index]["item"],
					  price: Object.values(data)[index]["price"].replace("\"","").replace("'","").trim()});




/*
     this.faqs.push({
            id: Object.values(data)[index]["id"],
			      vopros: Object.values(data)[index]["vopros"],
					  otvet: Object.values(data)[index]["otvet"]});
					  */

});





		   },
		   error => {
			   console.log('Error: ', error);
			  });







}

}

  SignIn(){


   const auth = getAuth();
signInWithEmailAndPassword(auth, this.loginForm.login, this.loginForm.password)
  .then((userCredential) => {


    // Signed in
    const user = userCredential.user;









	 if (user) {
    // User is signed in, see docs for a list of available properties
    // https://firebase.google.com/docs/reference/js/firebase.User
   // const uid = user.uid;
















  }












    console.log(user);
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;


    //alert(errorMessage);
    console.log(errorMessage);
  });

}

SignOut(){

const auth = getAuth();

   auth.signOut().then(function() {
    console.log('Signed Out');
    window.location.reload();

    },
    function(error) {
    console.error('Sign Out Error', error);
  });
}

InCart(id:any, market:any, category:any, item:any, price: any)
{


  const auth = getAuth();
onAuthStateChanged(auth, (user) => {
  if (user) {
    // User is signed in, see docs for a list of available properties
    // https://firebase.google.com/docs/reference/js/firebase.User
    const uid = user.uid;



//console.log(uid)


 const db = getDatabase();
       update(ref_database(db, 'users/' + uid + '/goods/' + id + item.replace(".","") + price.replace(".","")), {
         market: market,
         category: category,
         item: item,
		     price: price.replace("\"","").replace("'","").trim()

       });

     //  console.log(id + " / " + item)

  const dbRef = ref_database(getDatabase());
get(child(dbRef, 'users/' + uid + '/goods')).then((snapshot) => {
  if (snapshot.exists()) {
   // console.log(snapshot.size);

    this.gcount = snapshot.size;
}else this.gcount = 0;
});




  }
});





//console.log(id + item)






}


}
