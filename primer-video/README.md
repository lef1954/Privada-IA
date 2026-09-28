# VIDEO Nº 1 — "TIERRA ALTA · APERTURA"

**Duración final: 1 minuto 39 segundos (1:34 de imagen + 5 s de placa de cierre). 14 clips a generar.**

---

## Por qué este es el primer video y no el Episodio 1

El Episodio 1 son 52 planos y 96 cortes. Si arrancás por ahí, el primer material publicado
llega en un mes y medio. **Este video son 14 clips y se termina en tres o cuatro días de
trabajo**, y cumple tres funciones al mismo tiempo:

1. **Es la prueba de concepto (Fase 0).** Si los personajes quedan consistentes en estos 14
   planos, el resto de la serie es viable. Si no, lo sabés en cuatro días y no en tres meses.
2. **Es material publicable.** No es un test descartable: es el teaser oficial de la serie,
   se sube y empieza a juntar público mientras producís el Ep. 1.
3. **Diez de los catorce planos se reusan tal cual en el Episodio 1.** No es trabajo tirado:
   es el primer 20 % del episodio, generado en orden distinto.

## Qué contiene

| Archivo | Para qué |
|---|---|
| `04-veo3-prompts.md` | **Si generás con Veo 3, usá este y no el 01.** Los 14 prompts en forma de párrafo, con el `negative_prompt` en campo aparte, el audio nativo aprovechado, los tres planos que necesitan el reescritor apagado y el presupuesto estimado. |
| `01-prompts-listos.md` | La versión genérica de los 14 prompts, **autocontenidos**: las fichas de personaje ya están pegadas adentro. Para cualquier generador que no sea Veo. |
| `02-montaje.md` | El timeline con timecodes exactos, rótulos, y las cinco capas de audio. |
| `03-ensamblar.sh` | Script de ffmpeg que toma los 14 clips y arma el video final: punto de entrada por clip, recorte a 2.39:1, grano, rótulos, placas y concatenado. |
| `animatico.html` | El animático jugable con los tiempos reales de montaje. |

## Estructura del video

```
BLOQUE A — EL MUNDO NORMAL              0:00 – 0:44   6 clips
  Un campo de trigo. Los pájaros se van. La perra mira al este.
  Una cocina. Una mujer entiende algo. Un vaso de agua se derrama.

TÍTULO                                  0:44 – 0:48
  TIERRA ALTA

BLOQUE B — LA CUENTA                    0:48 – 1:15   5 clips
  Un mapa de papel. Un cajero vacío. Una góndola vacía.
  Una radio que se queda muda. Humo sobre un pueblo.

BLOQUE C — LA SALIDA                    1:15 – 1:34   3 clips

PLACA FINAL                             1:34 – 1:39
  Manos golpeando la chapa de un camión. El cartel de salida del pueblo.
  Y en el espejo retrovisor, una luz en el cielo del este.
```

## Regla que decide todo el video

**El teaser no muestra nada.** No hay meteorito, no hay ola, no hay agua, no hay ceniza,
no hay catástrofe. Hay un pueblo donde algo está pasando y una mujer que lo entendió primero.
Lo único que el espectador ve del apocalipsis es **una luz rara en el espejo retrovisor del
último plano**, y eso es todo.

Es más difícil de resistir y es mucho más efectivo: la ola en el teaser convierte la serie en
una película de catástrofe más. La perra mirando al este la convierte en algo que se quiere ver.

## Orden de trabajo (4 días)

```
DÍA 1   Fijar a CAMILA: 20 generaciones del bloque canónico, distintos ángulos, misma ropa.
        Elegir 3 imágenes de referencia y guardarlas. Sin esto, no arranca nada.
DÍA 2   Generar los 6 clips del BLOQUE A, 4 variantes cada uno (24 generaciones).
        Elegir por continuidad de cara y de luz, no por belleza.
DÍA 3   Generar los 8 clips de los BLOQUES B y C (32 generaciones).
DÍA 4   Montaje con 02-montaje.md, correr 03-ensamblar.sh, sonido, subir.
```

## Antes de generar, leer una vez

- **4 variantes por plano, mínimo.** La primera generación nunca es la buena.
- **El plano más lindo suele ser el que rompe la serie.** Se elige por continuidad.
- **Un solo LUT para todo el video**, aplicado al final sobre los 14 clips juntos. Es lo que
  hace que 14 generaciones distintas parezcan una sola pieza filmada el mismo día.
- **Grano de 35 mm sobre todo, misma intensidad.** Tapa las inconsistencias de textura de la
  IA mejor que cualquier otra cosa.
