# 📝 CLI_Markdown_Editor

Un editor de texto minimalista con interfaz de usuario en terminal (TUI) para Markdown, construido con Python y Textual.

## 🌟 Descripción del Proyecto

**Markdown TUI Editor** (`md_editor`) es una herramienta diseñada para la edición eficiente de archivos Markdown directamente en la terminal.

Su funcionalidad clave es el **renderizado en tiempo real** del contenido Markdown junto al área de edición. Además, cuenta con un **marcador visual** (`|`) que aparece en la vista renderizada para indicar la posición exacta de tu cursor en el código fuente, facilitando la depuración del formato.

---

### ⚠️ Nota de Permisos (`sudo`)

El editor está diseñado para ser invocado con **privilegios de superusuario (`sudo`)** para asegurar que los cambios de archivo se puedan guardar correctamente bajo diversas configuraciones de sistema.

El *script* de instalación se encarga de configurar el comando de acceso para que el editor se ejecute automáticamente con `sudo`, simplificando la experiencia del usuario.

---

## 🚀 Instalación

Sigue estos sencillos pasos para instalar el editor y configurar el comando de acceso `md` en tu *shell* (`bash` o `zsh`).

### Requisitos

* **Python 3** (Se recomienda `python3.8+`).
* **pip** (Administrador de paquetes de Python).
* Permisos de **sudo** para instalar el *script* en una ubicación global (`/usr/local/bin`).

### 1. Preparación de Archivos

Asegúrate de tener los dos archivos principales en el mismo directorio:

* `editor_cli_fusion.py` (Tu aplicación)
* `install.sh` (El script de instalación)

### 2. Ejecución del Script de Instalación

El *script* `install.sh` automatiza la instalación de dependencias, la copia del ejecutable y la configuración del *shell*.

```bash
# 1. Dar permisos de ejecución al script
chmod +x install.sh

# 2. Ejecutar la instalación
# Se solicitará la contraseña de sudo para mover el archivo de la aplicación.
./install.sh
