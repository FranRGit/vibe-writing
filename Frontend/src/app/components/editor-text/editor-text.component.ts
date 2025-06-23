import { CommonModule } from '@angular/common';
import { Component, ElementRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { QuillModule } from 'ngx-quill';
import { ViewChild } from '@angular/core';
import { QuillEditorComponent } from 'ngx-quill';
import { ModelService } from '../../core/services/model.service';
import { HttpClientModule } from '@angular/common/http';
import { Router } from 'express';

@Component({
  selector: 'app-editor-text',
  standalone: true,
  imports: [CommonModule, FormsModule,QuillModule, HttpClientModule],
  providers: [ModelService],
  templateUrl: './editor-text.component.html',
  styleUrl: './editor-text.component.css'
})
export class EditorTextComponent {
  @ViewChild('tooltip') tooltipEl?: ElementRef;
  @ViewChild('editorWrapper') editorWrapper?: ElementRef<HTMLElement>;
  @ViewChild('quillRef', { static: false }) editor?: QuillEditorComponent;

  fileName = '';
  htmlContent = '';
  modelo = "";
  sugerencia = "";
  sugerenciaParcial= "";
  sugerenciaActiva = false;
  escribiendo = false;
  typingTimeout: any;
  mostrarAyuda = false;
  mostrarAcciones = false;
  mostrarAccionSeleccionada = false;
  accionesTop = 0;
  accionesLeft = 0;
  accionSeleccionada = "";
  instruccionUsuario = ""
  ultimaAccion = '';
  ultimaInstruccion: string = '';
  ultimaAccionReal: string = '';  
  ultimaSeleccion: string = '';
  ultimaSugerenciaTexto: string = '';


  constructor(private model:ModelService){}

ngOnInit(): void {
  const guardado = localStorage.getItem('tituloArchivo');
  const contenido = localStorage.getItem('contenidoArchivo');

  if (guardado) {
    this.fileName = guardado;
  }

  if (contenido) {
    this.htmlContent = contenido; 
  }
}

  toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],
    [{ 'header': 1 }, { 'header': 2 }],
    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
    [{ 'script': 'sub' }, { 'script': 'super' }],
    [{ 'indent': '-1' }, { 'indent': '+1' }],
    [{ 'direction': 'rtl' }],
    [{ 'size': ['small', false, 'large', 'huge'] }],
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
    [{ 'color': [] }, { 'background': [] }],
    [{ 'font': [] }],
    [{ 'align': [] }],
    ['clean']
  ]

  modules = {
    toolbar: this.toolbarOptions
  };

  //MODELO SERVICE FUNCIONES
  getSugerenciaAuto(){
      const text = this.editor?.quillEditor.getText();

      if (typeof text !== 'string' || text.trim() === '') {
        console.warn('Texto vacío o inválido. No se enviará al backend.');
        return;
      }

      this.ultimaAccion = 'auto';
      this.ultimaSugerenciaTexto = text;

      this.model.obtenerSugerencia(text).subscribe({
        next: res => {
          console.log('Respuesta de Flask:', res.respuesta); 
          const sugerencia = res.respuesta || "Sugerencia automática..."
          this.sugerencia = sugerencia;
          this.simularEscritura(sugerencia)
        },
        error: err => {
          console.error('Error:', err);
        }
      });
      this.mostrarAyuda= false;
  }


  //EFECTOS VISUALES
  simularEscritura(texto: string) {
      this.sugerenciaParcial = '';
      this.escribiendo = true;

      let index = 0;
      const intervalo = setInterval(() => {
        if (index < texto.length) {
          this.sugerenciaParcial += texto[index];
          index++;
        } else {
          clearInterval(intervalo);
          this.escribiendo = false;
          this.sugerenciaActiva = true;
        }
      }, 10);
  }

  aceptarSugerencia() {
      this.htmlContent += `<p>${this.sugerencia}</p>`;
      this.resetSugerencia();
  }

  rechazarSugerencia() {
      this.resetSugerencia();
  }

  resetSugerencia() {
      this.sugerencia = '';
      this.sugerenciaParcial = '';
      this.sugerenciaActiva = false;
  }

  rechazarAyuda(){
    this.mostrarAyuda= false;
    this.mostrarAcciones= false;
    this.mostrarAccionSeleccionada = false;

  }

  ngAfterViewInit() {
    this.editor?.onContentChanged.pipe().subscribe(() => {
      if (this.mostrarAccionSeleccionada) return;
      if (this.mostrarAcciones) return;

      this.mostrarAyuda = false;

      clearTimeout(this.typingTimeout);
      this.typingTimeout = setTimeout(() => {
        this.mostrarTooltipCercaDelCursor();
      }, 3000);
    });

    // Escucha cambios en la selección
    this.editor?.onSelectionChanged.subscribe((range: any, oldRange: any, source: string) => {
      console.log(range)
      if (range.source === 'user' && range.range.length > 50) {
        this.mostrarAyuda = false;
        const bounds = this.editor?.quillEditor.getBounds(range.range.index, range.range.length);
        const wrapperRect = this.editorWrapper?.nativeElement.getBoundingClientRect();

        if (!bounds || !wrapperRect) return;

        // Calcula la posición absoluta del tooltip
        this.accionesTop = bounds.top + bounds.height + wrapperRect.top;
        this.accionesLeft = bounds.left + wrapperRect.left;
        this.mostrarAcciones = true;
      } else {
        this.mostrarAcciones = false;
      }
    });
}

  mostrarTooltipCercaDelCursor() {

    if (this.mostrarAccionSeleccionada || this.mostrarAcciones) return;
    this.mostrarAyuda = true;

    setTimeout(() => {
      const tooltipElem = this.tooltipEl?.nativeElement;
      const wrapperElem = this.editorWrapper?.nativeElement;
      const editorInstance = this.editor?.quillEditor;

      if (!tooltipElem || !wrapperElem || !editorInstance) return;

      const selection = editorInstance.getSelection();
      if (!selection) return;

      const bounds = editorInstance.getBounds(selection.index);

      if (!bounds || typeof bounds.top !== 'number' || typeof bounds.left !== 'number' || typeof bounds.height !== 'number') {
        return;
      }

      const wrapperRect = wrapperElem.getBoundingClientRect();

      const top = bounds.top + bounds.height + 100;
      const left = bounds.left;

      tooltipElem.style.position = 'absolute'; // Por si acaso
      tooltipElem.style.top = `${top}px`;
      tooltipElem.style.left = `${left}px`;
    }, 10);
  }

accionIA(tipo: string) {
    const selection = this.editor?.quillEditor.getSelection();
    const textoSeleccionado = this.editor?.quillEditor.getText(selection?.index, selection?.length);
    this.mostrarAcciones = false;
    this.mostrarAccionSeleccionada = true;

    if (textoSeleccionado && selection) {
      this.accionSeleccionada = tipo; 
      this.instruccionUsuario = '';   
    }

  }

enviarInstruccion() {
    if (!this.accionSeleccionada || !this.instruccionUsuario.trim()) return;

    const seleccion = this.editor?.quillEditor.getSelection();
    const textoSeleccionado = this.editor?.quillEditor.getText(seleccion?.index, seleccion?.length);
    const textoCompleto = this.editor?.quillEditor.getText();

    if (!textoSeleccionado || !textoCompleto) {
      console.warn("Texto incompleto para enviar.");
      return;
    }

    const data = {
      texto: textoCompleto,
      textoSeleccionado,
      accion: this.accionSeleccionada,
      instruccion: this.instruccionUsuario
    };

    this.ultimaAccion = 'instruccion';
    this.ultimaAccionReal = this.accionSeleccionada; 
    this.ultimaInstruccion = this.instruccionUsuario;
    this.ultimaSeleccion = textoSeleccionado;

    this.model.accionSobreTexto(data).subscribe({
      next: res => {
        const sugerencia = res.respuesta || "Sugerencia automática...";
        this.sugerencia = sugerencia;
        this.simularEscritura(sugerencia);
      },
      error: err => {
        console.error("Error en petición:", err);
      }
    });

    this.accionSeleccionada = '';
    this.instruccionUsuario = '';
    this.mostrarAccionSeleccionada = false;
}


repetirUltimaAccion() {
  const textoCompleto = this.editor?.quillEditor.getText();

  if (this.ultimaAccion === 'instruccion') {
    if (!this.ultimaSeleccion || !this.ultimaInstruccion || !textoCompleto) {
      console.warn("Faltan datos para repetir la acción personalizada.");
      return;
    }

    const data = {
      texto: textoCompleto,
      textoSeleccionado: this.ultimaSeleccion,
      accion: this.ultimaAccionReal,
      instruccion: this.ultimaInstruccion
    };

    this.model.accionSobreTexto(data).subscribe({
      next: res => {
        const sugerencia = res.respuesta || "Sugerencia automática...";
        this.sugerencia = sugerencia;
        this.simularEscritura(sugerencia);
      },
      error: err => {
        console.error("Error al repetir acción personalizada:", err);
      }
    });

  } else if (this.ultimaAccion === 'auto') {
    if (!this.ultimaSugerenciaTexto.trim()) {
      console.warn("No hay texto para repetir sugerencia automática.");
      return;
    }

    this.model.obtenerSugerencia(this.ultimaSugerenciaTexto).subscribe({
      next: res => {
        const sugerencia = res.respuesta || "Sugerencia automática...";
        this.sugerencia = sugerencia;
        this.simularEscritura(sugerencia);
      },
      error: err => {
        console.error("Error al repetir sugerencia automática:", err);
      }
    });

  } else {
    console.warn("No hay acción anterior para repetir.");
  }
}

}

