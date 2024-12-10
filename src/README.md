# MultiApp  

MultiApp es una aplicación de escritorio desarrollada en Python que combina múltiples funcionalidades en una sola interfaz gráfica. Utiliza la biblioteca `customtkinter` para la creación de la interfaz de usuario y está diseñada para ser modular, integrando diferentes servicios y herramientas como un monitor del sistema, un juego de Tetris, un gestor de procesos, y un scrapper web.  

## Características principales  

- **Interfaz gráfica moderna**: Construida con `customtkinter` para una experiencia de usuario mejorada.  
- **Scrapping web**: Permite extraer enlaces de páginas web y almacenarlos en una base de datos.  
- **Monitor del sistema**: Muestra métricas en tiempo real como uso de CPU, RAM y red.  
- **Juego de Tetris**: Incluye un juego de Tetris completamente funcional.  
- **Gestión de procesos**: Abre programas, archivos o URLs directamente desde la aplicación.  
- **Gestión de hilos**: Maneja múltiples tareas concurrentes de manera eficiente.  

---  

## Estructura del proyecto  

El proyecto está organizado en diferentes módulos y clases, cada uno con una responsabilidad específica. A continuación, se describen las clases principales y sus funcionalidades.  

### 1. `CenteredWindow` (ubicada en `src/ui/centered_window.py`)  

Esta es la clase principal de la aplicación que gestiona la interfaz gráfica y la interacción del usuario.  

- **Responsabilidades**:  
  - Configurar la ventana principal y centrarla en la pantalla.  
  - Crear paneles (izquierdo, derecho, central y barra inferior) para organizar las funcionalidades.  
  - Manejar el inicio y cierre de la aplicación.  
  - Integrar los diferentes componentes como el monitor del sistema, el scrapper y el juego de Tetris.  

---  

### 2. `ThreadsManager` (ubicada en `src/services/threads_manager.py`)  

Gestiona los hilos de ejecución para las diferentes tareas de la aplicación.  

- **Responsabilidades**:  
  - Iniciar y detener hilos para tareas como actualización de tiempo, temperatura, correos, monitor del sistema y el juego de Tetris.  
  - Coordinar la ejecución de tareas concurrentes.  
  - Proveer métodos para actualizar métricas del sistema, tiempo, temperatura y correos.  

---  

### 3. `ThreadenTask` (ubicada en `src/services/threaden_task.py`)  

Clase auxiliar para manejar hilos individuales.  

- **Responsabilidades**:  
  - Iniciar y detener hilos de manera segura.  
  - Garantizar que los hilos se ejecuten en segundo plano como demonios.  

---  

### 4. `ProcessManager` (ubicada en `src/services/processes_manager.py`)  

Permite abrir programas, archivos o URLs desde la aplicación.  

- **Responsabilidades**:  
  - Abrir recursos como navegadores web, programas o archivos.  
  - Manejar errores y proporcionar mensajes de fallback en caso de fallos.  

---  

### 5. `Scrapper` (ubicada en `src/services/scrapper.py`)  

Clase encargada de realizar el scrapping web y almacenar los enlaces encontrados en una base de datos.  

- **Responsabilidades**:  
  - Extraer enlaces de páginas web utilizando `BeautifulSoup`.  
  - Almacenar los enlaces en una base de datos MySQL.  
  - Actualizar la interfaz de usuario con los enlaces encontrados.  
  - Manejar múltiples tareas de scrapping de manera concurrente.  

---  

### 6. `SystemMonitor` (ubicada en `src/services/system_monitor.py`)  

Monitorea métricas del sistema en tiempo real y las muestra en gráficos.  

- **Responsabilidades**:  
  - Obtener métricas como uso de CPU, RAM y red utilizando `psutil`.  
  - Mostrar gráficos en tiempo real utilizando `matplotlib`.  
  - Actualizar los gráficos dinámicamente con nuevos datos.  

---  

### 7. `TetrisGame` (ubicada en `src/services/tetris_game.py`)  

Implementa un juego de Tetris completamente funcional dentro de la aplicación.  

- **Responsabilidades**:  
  - Gestionar la lógica del juego, incluyendo movimiento, rotación y colocación de piezas.  
  - Detectar líneas completas y actualizarlas.  
  - Manejar eventos de teclado para controlar el juego.  

---  

## Requisitos del sistema  

- Python 3.8 o superior.  
- Bibliotecas necesarias (instalables con `pip`):  
  - `customtkinter`  
  - `psutil`  
  - `matplotlib`  
  - `requests`  
  - `beautifulsoup4`  
  - `mysql-connector-python`  

---  

## Instalación  

1. Clona este repositorio:  
```
bash
git clone https://github.com/DennisEckerskorn/MultiAppRepo.git
cd MultiAppRepo
```
  

2. Instala las dependencias:  
bash
pip install -r requirements.txt

  

3. Configura la base de datos MySQL:  
   - Crea una base de datos llamada `scrap_links_db`.  
   - Asegúrate de que las credenciales en `Scrapper` coincidan con tu configuración.  

4. Ejecuta la aplicación:  
bash
python src/main.py

  

---  

## Uso  

1. **Scrapping**:  
   - Introduce una URL en el panel izquierdo y haz clic en "Iniciar Scrapping".  
   - Los enlaces encontrados se mostrarán en la pestaña "Scrapping".  

2. **Monitor del sistema**:  
   - Ve a la pestaña "Sistema" para ver gráficos en tiempo real de CPU, RAM y red.  

3. **Juego de Tetris**:  
   - Ve a la pestaña "Juego" y haz clic en "Start Game" para comenzar a jugar.  

4. **Gestión de procesos**:  
   - Usa los botones del panel izquierdo para abrir programas o URLs.  

---  

## Enlace al video de demostración:

## Autor  

Desarrollado por Dennis Eckerskorn.  