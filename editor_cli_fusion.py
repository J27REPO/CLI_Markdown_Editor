import sys
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TextArea, Static
from textual.containers import Horizontal
from rich.markdown import Markdown 
from textual import on
from textual import events

# --- WIDGET PERSONALIZADO PARA EL RENDERIZADO ---
class RenderView(Static):
    """Un widget estático que renderiza su contenido como Markdown."""
    
    def update_markdown(self, markdown_text: str) -> None:
        if not markdown_text.strip():
            rendered = ""
        else:
            rendered = Markdown(markdown_text)
        self.update(rendered)

# --- APLICACIÓN PRINCIPAL ---
class MarkdownTUIEditor(App):
    """Aplicación TUI con Renderizado al 100% y Marcador de Posición de Escritura."""

    BINDINGS = [
        ("q", "quit", "Salir"),
        ("ctrl+s", "save_file", "Guardar")
    ]
    
    CSS = """
    Horizontal {
        height: 100%;
        width: 100%;
    }
    #editor-panel {
        width: 0%;
        height: 100%;
        padding: 0;
        min-width: 0; 
        max-width: 0;
        border: none;
    }
    #render-panel {
        width: 100%;
        height: 100%;
        padding: 0 1;
        overflow: scroll;
        max-width: 100%; 
    }
    """

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.initial_content = self._load_file()
        self.clean_content = self.initial_content 

    def _load_file(self) -> str:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ""
        except Exception:
            self.exit()
            return ""

    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal():
            yield TextArea(
                text=self.initial_content,
                id="editor-panel",
                language="markdown" 
            )
            yield RenderView(id="render-panel")
        yield Footer()

    def on_mount(self) -> None:
        render_widget = self.query_one(RenderView)
        render_widget.update_markdown(self.initial_content)
        self.query_one(TextArea).focus()
        
    # EVENTO PRINCIPAL: cuando cambia el texto
    @on(TextArea.Changed)
    def handle_text_changed(self, event: TextArea.Changed) -> None:
        editor = self.query_one(TextArea)
        self.clean_content = editor.text
        row, col = editor.cursor_location
        self._render_with_marker(row, col)

    # EVENTO TECLAS: flechas, home, end, enter
    @on(events.Key)
    def handle_key(self, event: events.Key) -> None:
        if event.key in ("up", "down", "left", "right", "home", "end", "enter"):
            editor = self.query_one(TextArea)
            row, col = editor.cursor_location
            self._render_with_marker(row, col)
        
    # INYECTAR Y RENDERIZAR
    def _render_with_marker(self, cursor_row: int, cursor_column: int) -> None:
        render_widget = self.query_one(RenderView)
        lines = self.clean_content.split('\n')
        
        if cursor_row < len(lines):
            current_line = lines[cursor_row]
            col = min(cursor_column, len(current_line))
            marked_line = current_line[:col] + '|' + current_line[col:]
            lines[cursor_row] = marked_line
        
        marked_content = '\n'.join(lines)
        render_widget.update_markdown(marked_content)

    # GUARDAR
    def action_save_file(self) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(self.clean_content)
            self.notify(f"Archivo '{self.filename}' guardado correctamente.", timeout=3)
        except Exception as e:
            self.notify(f"Error al guardar: {e}", severity="error", timeout=5)

# --- EJECUCIÓN ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python editor_cli_fusion.py <nombre_del_archivo.md>")
        sys.exit(1)
        
    filename = sys.argv[1]
    app = MarkdownTUIEditor(filename)
    app.run()
