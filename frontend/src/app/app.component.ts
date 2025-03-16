import {Component, ViewChild, ElementRef} from '@angular/core';
import {ApiService} from './services/api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  @ViewChild('fileInput') fileInput!: ElementRef;

  archivo: File | null = null;
  resultado: any = null;
  procesando: boolean = false;
  archivoCargado: boolean = false;
  mostrandoSpinner: boolean = false;

  constructor(private apiService: ApiService) {
  }

  seleccionarArchivo(event: any) {
    this.archivo = event.target.files[0] || null;
    this.resultado = null; // Limpiar resultados anteriores
    this.archivoCargado = !!this.archivo;
  }

  limpiar() {
    this.archivo = null;
    this.resultado = null;
    this.procesando = false;
    this.archivoCargado = false;
    this.mostrandoSpinner = false;
    this.fileInput.nativeElement.value = '';  // Restablece el input file
  }

  ejecutarMetodo(metodo: string) {
    if (!this.archivo) return;
    this.procesando = true;
    this.mostrandoSpinner = true;

    let endpoint = '';
    if (metodo === 'fuerzaBruta') {
      endpoint = '/fuerzaBruta';
    } else if (metodo === 'voraz') {
      endpoint = '/voraz';
    } else if (metodo === 'dinamico') {
      endpoint = '/dinamico';
    }

    this.apiService.enviarArchivo(this.archivo, endpoint).subscribe(
      (response) => {
        this.resultado = response;
        this.procesando = false;
        this.mostrandoSpinner = false;
      },
      (err) => {
        console.error("❌ Error al procesar el archivo:", err);
        this.procesando = false;
        this.mostrandoSpinner = false;
      }
    );
  }

  limpiarResultados() {
    this.resultado = null;
    this.procesando = false;
    this.mostrandoSpinner = false;
  }

}
