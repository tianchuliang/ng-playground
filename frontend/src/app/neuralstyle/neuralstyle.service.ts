import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';
import {API_URL} from '../env';


@Injectable({
  providedIn: 'root'
})
export class NeuralStyleService {

  constructor(private http: HttpClient) { }

  public uploadStyleImage(image: File): Observable<Response> {
    const formData: FormData = new FormData();
    formData.append('image',image);
    return this.http.post(`${API_URL}/upload_style`, formData).pipe(map((res:Response) => res));
  }

  public uploadContentImage(image: File): Observable<Response> {
    const formData: FormData = new FormData();
    formData.append('image',image);
    return this.http.post(`${API_URL}/upload_content`, formData).pipe(map((res:Response) => res));
  }

  public downloadResultImage(): Observable<Blob> {
    return this.http.get(`${API_URL}/dnload`, {
      responseType: "blob"
    });
  }

  public loadNeuralModel():Observable<Response> {
    return this.http.post(`${API_URL}/nstylehome`,'').pipe(map((res:Response) => res));
  }

  private handleError(err: HttpErrorResponse) {
    // in a real world app, we may send the server to some remote logging infrastructure
    // instead of just logging it to the console
    let errorMessage = '';
    if (err.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      errorMessage = `An error occurred: ${err.error.message}`;
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      errorMessage = `Server returned code: ${err.status}, error message is: ${err.message}`;
    }
    console.error(errorMessage);
    return throwError(errorMessage);
  }

}
