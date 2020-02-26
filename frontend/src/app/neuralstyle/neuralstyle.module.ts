import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { NeuralStyleComponent } from './neuralstyle.component';
import { ConvertToSpacesPipe } from '../shared/convert-to-spaces.pipe';
import { SharedModule } from '../shared/shared.module';
import { NeuralStyleService } from './neuralstyle.service';
import {MatSliderModule} from '@angular/material/slider';
import {MatInputModule} from '@angular/material/input';

@NgModule({
  imports: [
    RouterModule.forChild([
      { path: 'neuralstyle', component: NeuralStyleComponent },
    ]),
    SharedModule,
    MatSliderModule,
    MatInputModule
  ],
  declarations: [
    NeuralStyleComponent,
    ConvertToSpacesPipe
  ],
  providers: [NeuralStyleService]
})
export class NeuralStyleModule { }