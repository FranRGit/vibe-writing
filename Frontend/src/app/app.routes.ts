import { Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { EditorTextComponent } from './components/editor-text/editor-text.component';
import { NewFileComponent } from './components/new-file/new-file.component';

export const routes: Routes = [
    { path: '', component: NewFileComponent },
    { path: 'editor-texto', component: EditorTextComponent }
];
