// api.service.ts - Servicio para comunicarse con Flask
import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) {
  }

  enviarArchivo(archivo: File, endpoint: string): Observable<any> {
    const formData = new FormData();
    formData.append('file', archivo);
    return this.http.post<any>(`${this.apiUrl}/procesar/${endpoint}`, formData);
  }

  calcularConflicto(archivo: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', archivo);
    return this.http.post<any>(`${this.apiUrl}/calcular_ci`, formData);
  }

  descargarArchivo(metodo: string, nombreArchivo: string): Observable<Blob> {
    const url = `${this.apiUrl}/descargar_archivo/${metodo}/${nombreArchivo}`;
    return this.http.get(url, { responseType: 'blob' });
  }
  
}
