declare function require(path: string);
import { Component, OnInit } from '@angular/core';
import { NeuralStyleService } from './neuralstyle.service';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { ControlContainer } from '@angular/forms';

class ImageSnippet {
  constructor(public src: string, public file: File) {}
}

@Component({
  selector:'nstyle',
  templateUrl: './neuralstyle.component.html',
  styleUrls: ['./neuralstyle.component.css']
})
export class NeuralStyleComponent implements OnInit {
  pageTitle = 'Neural Style Transfer';
  imageWidth = 50;
  imageMargin = 2;
  showImage = false;
  errorMessage = '';
  styleImgURL: string | ArrayBuffer;
  contentImgURL: string | ArrayBuffer;
  defaultStyleImgURL: string | ArrayBuffer;
  defaultContentImgURL: string | ArrayBuffer;
  displayDefaultStyle = true;
  displayDefaultContent = true;
  outputImgURL: SafeUrl;
  selectedStyleFile: ImageSnippet;
  selectedContentFile: ImageSnippet;
  defaultItrs = 3;
  
  constructor(private NeuralStyleService: NeuralStyleService,
                    private domSanitizer: DomSanitizer) {}

  onStyleFileChanged(event) {
    this.selectedStyleFile = new ImageSnippet('image',event.target.files[0]);
    const reader = new FileReader();
    reader.readAsDataURL(this.selectedStyleFile.file);
    reader.onload = event => {
      this.styleImgURL = reader.result;
      this.displayDefaultStyle = false;
    };
  }
  
  onContentFileChanged(event) {
    this.selectedContentFile = new ImageSnippet('image',event.target.files[0]);
    const reader = new FileReader();
    reader.readAsDataURL(this.selectedContentFile.file);
    reader.onload = event => {
      this.contentImgURL = reader.result;
      this.displayDefaultContent = false;
    };  
  }

  onMash(){
    this.outputImgURL = null;
    if (this.displayDefaultStyle && this.displayDefaultContent){
      console.log("default shit")
    } else {
      console.log("with new pics")

      this.NeuralStyleService.
      mash(this.selectedStyleFile.file, this.selectedContentFile.file).
      subscribe((val) => {
        console.log(val);
        this.createImageFromBlob(val);
      });
    };
    this.outputImgURL = null;
  }

  createImageFromBlob(image: Blob) {
    let reader = new FileReader();
    if (image) {
      reader.readAsDataURL(image);
    };
    reader.addEventListener("load", () => {
      this.outputImgURL = this.domSanitizer.bypassSecurityTrustUrl(<string>reader.result);
    }, false);
  }

  ngOnInit(): void {   
    this.defaultStyleImgURL = require('../../assets/images/default_style.jpg');
    this.defaultContentImgURL = require('../../assets/images/default_content.jpg');
    this.NeuralStyleService.loadNeuralModel().subscribe(
      (res) => {
        console.log(res)
      },
      (err) => {
        console.log(err)
      }); 
  }
}