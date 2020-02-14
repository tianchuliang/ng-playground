import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { NeuralStyleComponent } from './neuralstyle.component';
import { ConvertToSpacesPipe } from '../shared/convert-to-spaces.pipe';
import { SharedModule } from '../shared/shared.module';
import { NeuralStyleService } from './neuralstyle.service';

@NgModule({
  imports: [
    RouterModule.forChild([
      { path: 'neuralstyle', component: NeuralStyleComponent },
    ]),
    SharedModule
  ],
  declarations: [
    NeuralStyleComponent,
    ConvertToSpacesPipe
  ],
  providers: [NeuralStyleService]
})
export class NeuralStyleModule { }
