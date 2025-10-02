#!/bin/bash

# --- Configuración ---
PYTHON_SCRIPT="editor_cli_fusion.py"
INSTALL_LOCATION="/usr/local/bin/md_editor"
SHELL_CONFIG=""

# --- 1. Detectar el Shell y la Configuración ---
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    echo "Shell no compatible detectado. Por favor, configura el comando 'md' manualmente."
    exit 1
fi

echo "Iniciando instalación para $SHELL_CONFIG..."

# --- 2. Instalar Dependencia 'textual' ---
echo "--- 1/3: Verificando/Instalando dependencia 'textual' ---"

if python3 -c "import textual" &> /dev/null; then
    echo "La librería 'textual' ya está instalada."
else
    echo "Instalando la librería 'textual'..."
    # Intenta instalación de usuario, si falla, intenta instalación global con sudo.
    pip3 install textual --user || sudo pip3 install textual || sudo pip install textual
    if [ $? -ne 0 ]; then
        echo "Advertencia: No se pudo instalar 'textual'. Instálalo manualmente con 'pip install textual'."
    else
        echo "Dependencia 'textual' instalada correctamente."
    fi
fi

# --- 3. Mover y hacer ejecutable el Script Python ---

echo "--- 2/3: Instalando el script de la aplicación ---"

# Mover el archivo a /usr/local/bin (requiere sudo)
sudo cp "$PYTHON_SCRIPT" "$INSTALL_LOCATION"
# Hacerlo ejecutable
sudo chmod +x "$INSTALL_LOCATION"

if [ $? -ne 0 ]; then
    echo "Error al copiar el script a $INSTALL_LOCATION. Saliendo."
    exit 1
fi
echo "Script de Python instalado y hecho ejecutable."


# --- 4. Crear la FUNCIÓN 'md' (Más Robusta que un Alias) ---

echo "--- 3/3: Creando la función 'md' en $SHELL_CONFIG ---"

# Usaremos una FUNCIÓN porque maneja mejor el argumento de archivo ($1) y el comando 'sudo python3'.
MD_COMMAND="sudo python3 $INSTALL_LOCATION"

MD_FUNCTION="
# Función 'md' para abrir el editor TUI de Markdown. Requiere sudo para guardar.
md() {
    if [ \"\$1\" ]; then
        $MD_COMMAND \"\$1\"
    else
        echo \"Uso: md <nombre_del_archivo.md>\"
    fi
}
"

# Asegurarse de que no haya una versión anterior y añadir la nueva función
sed -i '/# Función .md. para abrir el editor TUI de Markdown/d' "$SHELL_CONFIG" 2>/dev/null
echo "$MD_FUNCTION" >> "$SHELL_CONFIG"
echo "Función 'md' creada con éxito."


# --- Finalización ---
echo "------------------------------------------------------"
echo "¡Instalación completa!"
echo "Se ha creado la función 'md' en tu archivo de configuración."
echo "Para usar el comando 'md', **reinicia tu terminal** o ejecuta:"
echo "source $SHELL_CONFIG"
echo "------------------------------------------------------"
