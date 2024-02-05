import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { Reg2PageRoutingModule } from './reg2-routing.module';

import { Reg2Page } from './reg2.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    Reg2PageRoutingModule
  ],
  declarations: [Reg2Page]
})
export class Reg2PageModule {}
