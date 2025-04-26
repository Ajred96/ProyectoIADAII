import { Component, ViewChild, ElementRef } from '@angular/core';
import { ApiService } from './services/api.service';

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
  metodoUsado: string | null = null;

  contenidoArchivo: string = '';
  gruposResumen: { personas: number, opinion1: number, opinion2: number, terquedad: number }[] = [];
  esfuerzoTotal: number | null = null;
  ciOriginal: number | null = null;

  constructor(private apiService: ApiService) {}

  seleccionarArchivo(event: any) {
    this.archivo = event.target.files[0] || null;
    this.resultado = null;
    this.archivoCargado = !!this.archivo;
    this.contenidoArchivo = '';
    this.gruposResumen = [];
    this.esfuerzoTotal = null;
    this.ciOriginal = null;

    if (this.archivo) {
      const reader = new FileReader();
      reader.onload = () => {
        this.contenidoArchivo = (reader.result as string).trim();
        const lineas = this.contenidoArchivo.split(/\r?\n/).map(l => l.trim()).filter(l => l !== '');
        const numGrupos = parseInt(lineas[0]);
        const grupos = lineas.slice(1, 1 + numGrupos);

        this.gruposResumen = grupos.map(linea => {
          const valores = linea.trim().split(/[\s,]+/).map(v => Number(v));
          const [personas, op1, op2, terquedad] = valores;

          return {
            personas: isNaN(personas) ? 0 : personas,
            opinion1: isNaN(op1) ? 0 : op1,
            opinion2: isNaN(op2) ? 0 : op2,
            terquedad: isNaN(terquedad) ? 0 : terquedad
          };
        });

        this.esfuerzoTotal = parseInt(lineas[lineas.length - 1]);

        this.apiService.calcularConflicto(this.archivo!).subscribe({
          next: (res) => this.ciOriginal = res.CI,
          error: (err) => console.error("❌ Error al calcular CI original:", err)
        });
      };
      reader.readAsText(this.archivo);
    }
  }

  limpiar() {
    this.archivo = null;
    this.resultado = null;
    this.procesando = false;
    this.archivoCargado = false;
    this.mostrandoSpinner = false;
    this.contenidoArchivo = '';
    this.gruposResumen = [];
    this.esfuerzoTotal = null;
    this.ciOriginal = null;
    this.fileInput.nativeElement.value = '';
  }

  ejecutarMetodo(metodo: string) {
    if (!this.archivo) return;

    this.procesando = true;
    this.mostrandoSpinner = true;
    this.metodoUsado = metodo;

    this.apiService.enviarArchivo(this.archivo, metodo).subscribe(
      (response) => {
        this.resultado = response;
        this.procesando = false;
        this.mostrandoSpinner = false;

        // Descargar automáticamente el archivo generado
        const nombreBase = this.archivo!.name.split('.')[0];
        const nombreDescarga = `${nombreBase}_${metodo}.txt`;

        this.apiService.descargarArchivo(metodo, nombreBase).subscribe(blob => {
          const link = document.createElement('a');
          link.href = URL.createObjectURL(blob);
          link.download = nombreDescarga;
          link.click();
          URL.revokeObjectURL(link.href);
        });
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
