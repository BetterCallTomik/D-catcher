import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { Reg2Page } from './reg2.page';

const routes: Routes = [
  {
    path: '',
    component: Reg2Page
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class Reg2PageRoutingModule {}
