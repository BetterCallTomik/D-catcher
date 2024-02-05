import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Reg2Page } from './reg2.page';

describe('Reg2Page', () => {
  let component: Reg2Page;
  let fixture: ComponentFixture<Reg2Page>;

  beforeEach(async(() => {
    fixture = TestBed.createComponent(Reg2Page);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
