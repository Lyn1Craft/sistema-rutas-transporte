# Guía de entrega — Actividad 3 (equipo de 4)

Esta guía es solo para el equipo (no hace falta subirla, pero pueden
dejarla si quieren mostrar organización). Resume qué falta hacer y cómo
subir el proyecto a Git para que **el log evidencie el trabajo de cada
integrante**, como lo exige la rúbrica.

## 1. Checklist de la rúbrica

- [x] Trabajo en equipo de máximo 4 estudiantes.
- [x] Sistema en Python que, a partir de una base de conocimiento en
      reglas lógicas, calcula la mejor ruta entre un punto A y un punto B
      del transporte masivo (`base_conocimiento.py` + `motor_busqueda.py`).
- [x] Código fuente en Python + instrucciones de ejecución (`README.md`).
- [x] Documento PDF con las pruebas realizadas (`Pruebas_Sistema_Rutas.pdf`).
- [ ] Video (máx. 10 min) explicando el proyecto, comandos y resultados,
      **con participación de todos los integrantes** (pendiente: grabarlo,
      cada uno con su guion en `INTEGRANTE_N_explicacion.md`).
- [ ] Repositorio Git/GitLab con el tutor agregado como colaborador
      (pendiente: crear el repo y agregar al tutor).
- [ ] El log de Git debe evidenciar el trabajo de cada integrante
      (ver sección 3 más abajo — cada uno debe commitear su propio módulo
      con su propia cuenta de Git).
- [ ] Documento PDF final con el link al repositorio y al video, subido en
      el enlace de entrega del curso.

## 2. Antes de subir a Git

Reemplacen en cada `INTEGRANTE_N_explicacion.md` el texto
`[Reemplazar por: Nombre completo del integrante N]` por el nombre real.
Si cambian los datos de la red de transporte (líneas/estaciones reales de
su ciudad), edítenlo solo en `base_conocimiento.py`, en el diccionario
`LINEAS`; el resto del sistema no necesita cambios.

## 3. Cómo subir el proyecto para que el log muestre el aporte de cada uno

**Importante:** el log de Git evidencia el trabajo de cada integrante
según **quién hace el commit**, no según quién escribió el archivo. Por
eso cada integrante debe clonar el repo con su propia cuenta y hacer su
propio commit. Sugerencia de flujo (uno de ustedes crea el repo primero):

```bash
# 1) Uno del equipo crea el repositorio en GitHub/GitLab y sube la base:
git init
git add README.md GUIA_ENTREGA_Y_GIT.md .gitignore
git commit -m "Estructura inicial del proyecto y README"
git branch -M main
git remote add origin <URL_DEL_REPOSITORIO>
git push -u origin main

# 2) Agregar al tutor como colaborador desde la configuración del
#    repositorio en GitHub/GitLab (Settings > Collaborators).

# 3) Cada integrante clona el repo con SU PROPIA cuenta:
git clone <URL_DEL_REPOSITORIO>
cd <carpeta_del_repositorio>

# 4) Cada integrante agrega y commitea SU módulo por separado:
#    (ejemplo para el Integrante 1)
git add base_conocimiento.py INTEGRANTE_1_explicacion.md
git commit -m "Integrante 1: base de conocimiento y motor de inferencia (reglas logicas)"
git push
```

Repitan el paso 4 para cada integrante con su archivo correspondiente:

| Integrante | Archivos a commitear |
|---|---|
| 1 | `base_conocimiento.py`, `INTEGRANTE_1_explicacion.md` |
| 2 | `grafo_transporte.py`, `INTEGRANTE_2_explicacion.md` |
| 3 | `motor_busqueda.py`, `INTEGRANTE_3_explicacion.md` |
| 4 | `main.py`, `generar_pdf_pruebas.py`, `Pruebas_Sistema_Rutas.pdf`, `INTEGRANTE_4_explicacion.md` |

Si prefieren usar ramas (una rama por integrante y luego un *merge*), es
igual de válido y también queda evidenciado en el log; usen lo que les
resulte más cómodo, lo importante es que cada `commit` quede hecho desde
la cuenta de Git del integrante correspondiente.

## 4. Verificar que el log quedó bien

Cualquiera del equipo puede revisar con:

```bash
git log --oneline --all --graph
```

Deberían ver commits de al menos 4 autores distintos (uno por integrante).

## 5. Para el video (máx. 10 minutos)

Sugerencia de reparto de tiempo (≈2 min por persona + intro/cierre):
1. Integrante 4: breve intro del problema y demo del modo interactivo.
2. Integrante 1: explica la base de conocimiento y las reglas lógicas.
3. Integrante 2: explica cómo se construye el grafo y el costo de transbordo.
4. Integrante 3: explica el algoritmo A* y por qué la heurística es admisible.
5. Integrante 4: cierra mostrando `--pruebas` y el PDF de evidencia.

## 6. Entregable final

Un PDF (pueden usar Word o Google Docs y exportarlo) que contenga:
- Link al repositorio Git/GitLab (con el tutor ya agregado).
- Link al video.

Ese PDF es lo que se sube en el enlace de entrega de la tarea del curso.
