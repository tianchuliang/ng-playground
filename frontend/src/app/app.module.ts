import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { WelcomeComponent } from './home/welcome.component';
import { NeuralStyleModule } from './neuralstyle/neuralstyle.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { ClarityModule } from '@clr/angular';

@NgModule({
  declarations: [
    AppComponent,
    WelcomeComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot([
      { path: 'welcome', component: WelcomeComponent },
      { path: '', redirectTo: 'welcome', pathMatch: 'full' },
      { path: '**', redirectTo: 'welcome', pathMatch: 'full' }
    ]),
    NeuralStyleModule,
    BrowserAnimationsModule,
    ClarityModule
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }