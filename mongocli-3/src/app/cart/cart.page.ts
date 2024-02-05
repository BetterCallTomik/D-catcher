import { Component, OnInit , NgZone } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router"
import { getAuth,createUserWithEmailAndPassword, signInWithEmailAndPassword, onAuthStateChanged } from "firebase/auth";

import { getDatabase, ref,  query, orderByChild, equalTo, limitToLast, set, update, child, onValue  } from "firebase/database";


@Component({
  selector: 'app-cart',
  templateUrl: './cart.page.html',
  styleUrls: ['./cart.page.scss'],
})
export class CartPage implements OnInit {



goods: Array<{id: string; market: string; category: string; item: string; price: number;} > = [];


metro_sum = 0;
perekrestok_sum = 0;
html_form=0;
raschet = "";
pb=0;

rs=0;


timeLeft: number = 0;
  interval: any;

startTimer() {
    this.interval = setInterval(() => {
      if(this.timeLeft < 2) {
        this.timeLeft++;
      } else {
        this.timeLeft = 0;
        this.pb=0;
        this.rs=1;
      }
    },300)
  }


  constructor() {



















   const auth = getAuth();
onAuthStateChanged(auth, (user) => {
  if (user) {
    // User is signed in, see docs for a list of available properties
    // https://firebase.google.com/docs/reference/js/firebase.User
    const uid = user.uid;





console.log(uid);

 const db = getDatabase();



onValue(ref(db, '/users/' + uid), (poisk) => {


    let res = query(ref(db, 'users/' + uid + '/goods'));





    onValue(res, (snapshot) => {




	    snapshot.forEach((childSnapshot) =>
		{
			const childKey = childSnapshot.key;



           const childData = childSnapshot.val();

 console.log(Number(childData.price.replace("\"","").replace("'","").replace(" ","").trim()));


   this.goods.push({
            id: childKey,
            market: childData.market,
            category: childData.category,
			      item: childData.item,
					  price: Number(childData.price.replace("\"","").replace("'","").replace(" ","").trim())});

		//	this.profs.push({sovp: totalS, imya:childSnapshot.val().imya,img:im, rot: childKey + "", distm: this.distm});





        });

	  // console.log(this.goods);
let metro = Array();
let perekrestok = Array();

	  var newArray = this.goods.filter(function (el) {
  /*
  return el.price <= 1000 &&
         el.sqft >= 500 &&
         el.num_of_beds >=2 &&
         el.num_of_baths >= 2.5;
         */
         if (el.market=="metro")
         {
         metro.push(Number(String(el.price).replace("\"","").replace("'","").trim()));
        // console.log(el)
         }
         if (el.market=="perekrestok")
         {
         perekrestok.push(Number(String(el.price).replace("\"","").replace("'","").trim()));
         //console.log(el)
         }
});

this.metro_sum = Number(eval(metro.join('+')));
this.perekrestok_sum = Number(eval(perekrestok.join('+')));

console.log(this.metro_sum);

if (this.metro_sum > 0 && this.perekrestok_sum>0)
{
this.html_form=1

}
else this.html_form=0;

console.log(this.html_form);

        }, {
           onlyOnce: true // если данные должны быть получены в реалтайм
          });


}, {
  onlyOnce: true // если данные должны быть получены в реалтайм
});






  }
});



}


Calc(){

this.startTimer();
this.pb=1;

if (this.metro_sum > 0 && this.perekrestok_sum>0)
{
this.html_form==1

if (this.metro_sum >this.perekrestok_sum)
{
  this.raschet = "Дешевле купить в Перекресток - <b>" + this.perekrestok_sum + "</b>. В Metro будет - <b>" + this.metro_sum + "</b>";
}
else
{
 this.raschet = "Дешевле купить в Metro - <b>" + this.metro_sum + "</b>. В Перекресток будет <b>" + this.perekrestok_sum + "</b>";
}
console.log(this.metro_sum);
console.log(this.perekrestok_sum);
}



}





  ngOnInit() {
  }

}
