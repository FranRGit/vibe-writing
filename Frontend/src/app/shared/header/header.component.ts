import { Component } from '@angular/core';
import { ModelService } from '../../core/services/model.service';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [HttpClientModule],
  providers: [ModelService],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
    modeloSeleccionado: string = "LLaMA 3.2"
    constructor(private model:ModelService){}

    seleccionarModelo(modelo: string){
      this.modeloSeleccionado = modelo
      this.model.cambiarModelo(this.modeloSeleccionado).subscribe({
        next: res => {
          console.log('Respuesta de Flask:', res.modelo); 
        },
        error: err => {
          console.error('Error:', err);
        }
      });     
      
      this.model.cambiarModelo(this.modeloSeleccionado)
    }
}
