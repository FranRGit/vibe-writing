import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ModelService {

    constructor(private http: HttpClient) {}
  
    obtenerSugerencia(texto: string) {
        return this.http.post<{ respuesta: any }>(
          'http://localhost:5000/api/sugerencia',
          {texto}
        );
    }

    accionSobreTexto(data: { texto: string, textoSeleccionado: string, accion: string, instruccion: string }) {
      return this.http.post<{ respuesta: string }>(
        'http://localhost:5000/api/acciones', 
        data
      );
    }

    cambiarModelo(modelo: any) {
        return this.http.post<{ modelo: any }>(
          'http://localhost:5000/api/set_model',
          {modelo}
        );
    }
}
