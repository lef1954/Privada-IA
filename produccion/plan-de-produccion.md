# Plan de producción — Temporada 1

## 1. Números del proyecto

| Métrica | Valor |
|---|---|
| Episodios | 6 |
| Duración por episodio | 13 a 16 min |
| Duración total | ~85 min (equivale a un largometraje) |
| Planos a generar | ~590 (96 + 118 + 112 + 124 + 108 + 130 según escaletas) |
| Variantes por plano | 4 a 6 |
| Generaciones totales estimadas | 2.400 a 3.500 clips |
| Duración media del clip | 6–8 s |

## 2. Orden de trabajo (no cronológico)

El error clásico es empezar por el Episodio 1, escena 1. El orden correcto es por **riesgo**:

```
FASE 0 — PRUEBA DE CONCEPTO (1 semana)
  Generar solamente 5 planos: 5.K5 (la ola), 4.K2 (la luz), 1.11 (la bandeja de agua),
  1.38 (el primer plano de Nahuel) y 6.K8 (el mar nuevo).
  Si estos cinco funcionan, el proyecto es viable. Si no, se replantea antes de gastar meses.

FASE 1 — BIBLIA VISUAL (1 semana)
  Fijar los 8 personajes: 20 generaciones por personaje, distintos ángulos, misma ropa.
  Guardar las mejores como imágenes de referencia. Esto es la base de todo lo demás.
  Fijar el camión: 20 generaciones, mismo ángulo de 3/4 delantero y lateral.

FASE 2 — EPISODIO 1 COMPLETO (3 a 4 semanas)
  Generar, montar, sonorizar y terminar el Ep. 1 de punta a punta antes de tocar el Ep. 2.
  Un episodio terminado enseña más que seis episodios a medias.

FASE 3 — EPISODIOS 2 y 3 (en paralelo, 5 semanas)
  Comparten locaciones (ruta, noche, multitud): se generan juntos y se reparten los planos.

FASE 4 — EPISODIOS 4, 5, 6 (7 semanas)
  Son los caros. Se entra con el pipeline ya aceitado y con la biblia visual cerrada.
```

## 3. Pipeline por plano

```
1. Leer el plano en el pack de prompts.
2. Pegar los bloques canónicos de personaje (sin editar).
3. Adjuntar la imagen de referencia del personaje (Fase 1) si el modelo lo permite.
4. Generar 4 variantes.
5. Descartar por continuidad, no por belleza (ver checklist).
6. Nombrar el archivo: EP01_S04_P11_v3.mp4  (episodio_escena_plano_versión).
7. Anotar en produccion/continuidad.md cualquier detalle nuevo que aparezca y quede.
8. Al montaje.
```

**Regla de nombres de archivo:** `EP##_S##_P##_v#.mp4`. Sin excepciones. Con 3.000 clips,
el nombre del archivo es la única defensa contra el caos.

## 4. Post-producción

| Etapa | Qué se hace | Por qué importa |
|---|---|---|
| **Montaje** | Cortes cortos en el caos, planos largos en la catástrofe. Al revés de lo intuitivo. | La secuencia del impacto (4.4) tiene un plano de 40 segundos: ahí está el miedo. |
| **Corrección de color** | Un LUT por episodio, aplicado a TODO el episodio. | Es lo que une planos generados en momentos distintos. Sin esto, se ve el patchwork. |
| **Grano y textura** | Grano de 35 mm sobre todo, misma intensidad en todos los planos. | El grano tapa las inconsistencias de textura de la IA. Es la herramienta más útil que existe. |
| **Reencuadre** | Todo se genera 16:9 y se recorta a 2.39:1. | Da margen para corregir composición y esconder errores en los bordes. |
| **Sonido** | 5 capas: motor, ambiente, foley, diálogo, infrasonido. | **El 50 % de la credibilidad de esta serie está en el sonido, no en la imagen.** |
| **Diálogo** | Grabar voces aparte con actores reales si es posible; el lip-sync generado se resuelve con planos de espalda, de nuca y de detalle. | Un acento rioplatense mal generado rompe la serie en tres segundos. |

## 5. Presupuesto de dificultad por episodio

```
EP 1  ██░░░░░░░░  20 %   interiores, dos personas, luz natural. El más fácil.
EP 2  ██████░░░░  60 %   multitudes de noche, estación de servicio.
EP 3  █████░░░░░  50 %   noche casi total (la noche perdona), pero mucho militar y multitud.
EP 4  ████████░░  80 %   la secuencia del impacto + ceniza en todos los planos.
EP 5  ███████░░░  70 %   la ola. Un solo plano concentra el riesgo del episodio.
EP 6  █████████░  90 %   multitud + montaña + agua + nieve + el mar nuevo. El más caro.
```

## 6. Distribución

- **YouTube:** episodios completos, estreno semanal, jueves 21:00 (hora de Argentina).
- **Adelantos verticales (9:16):** un corte de 45 s por episodio para redes. Los mejores
  candidatos: 1.11 (la bandeja), 2.K5 (las manos en la chapa), 5.K5 (la ola), 6.K1 (el río al
  revés).
- **Título de cada video:** `TIERRA ALTA — Ep. N: "TÍTULO" | Serie apocalíptica argentina`.
- **Miniaturas:** el camión chico, la amenaza grande, y una cara. Nunca texto gigante.
- **Subtítulos:** español e inglés, obligatorios. El acento rioplatense cerrado necesita
  subtítulos incluso en español para público de otros países.

## 7. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Los personajes cambian de cara entre planos | Bloques canónicos textuales + imágenes de referencia de la Fase 1 + máximo 2 personas por plano |
| La ola se ve de juguete | Escala en primer plano obligatoria (molinos, pylons), teleobjetivo, agua marrón, sin sonido en el primer avistaje |
| El proyecto se abandona en el Ep. 3 | Terminar el Ep. 1 completo antes de empezar el 2. Publicar. El feedback sostiene el resto. |
| Deriva de continuidad (suciedad, ceniza) | `produccion/continuidad.md` actualizado plano a plano. Es tedioso y es lo que separa una serie de un carrete de clips. |
| Diálogo generado que suena a español neutro | Voces grabadas aparte + planos de nuca y de detalle para el 40 % del diálogo |
| Geografía inverosímil para público argentino | La ruta es real, las cotas son reales, los nombres son reales. Ya está resuelto en `docs/03-ruta-y-locaciones.md`. |
