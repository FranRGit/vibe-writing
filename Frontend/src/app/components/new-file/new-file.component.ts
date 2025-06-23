import { CommonModule } from '@angular/common';
import { Component, NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { Router } from '@angular/router';

@Component({
  selector: 'app-new-file',
  standalone: true,
  imports: [FormsModule],
  providers:[],
  templateUrl: './new-file.component.html',
  styleUrl: './new-file.component.css'
})
export class NewFileComponent {
  fileName: string | null = null;
  titulo: string = '';

  constructor(private router: Router) {}

  onDragOver(event: DragEvent) {
    event.preventDefault();
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    const file = event.dataTransfer?.files[0];
    if (file) {
      this.fileName = file.name;
      this.titulo = this.titulo || file.name;
    }
  }

onFileSelected(event: Event) {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];

  if (file) {
    this.fileName = file.name;
    if (!this.titulo.trim()) {
      this.titulo = file.name;
    }

    const reader = new FileReader();

    reader.onload = () => {
      const contenido = reader.result as string;
      console.log('Contenido del archivo:', contenido);

      localStorage.setItem('contenidoArchivo', contenido);
      localStorage.setItem('tituloArchivo', this.titulo.trim() || 'Documento sin título');
    };

    reader.readAsText(file);
  } else {
    localStorage.setItem('tituloArchivo', this.titulo.trim() || 'Documento sin título');
    this.router.navigate(['/editor-texto']);
  }
}

  crearDocumento() {
    const tituloFinal = this.titulo.trim() || 'Documento sin título';
    localStorage.setItem('tituloArchivo', tituloFinal);
    this.router.navigate(['/editor-texto']);
  }
}
