# Los 14 prompts del primer video — versión Veo 3

Reescritos para Veo 3 específicamente. **No son los mismos prompts que `01-prompts-listos.md`**:
cambian de forma, de estructura y de estrategia de audio. Usá este archivo, no el otro, si
generás con Veo.

---

## Lo que cambia con Veo 3 (leer una vez antes de empezar)

### 1. Todos los clips salen de 8 segundos
Veo 3 genera **8 segundos fijos**. No podés pedirle 5. Entonces: **generá los 14 planos en
8 segundos y recortalos en el montaje.** El script `03-ensamblar.sh` ya lo hace, y ahora
además te deja elegir qué parte de esos 8 segundos usar (ver "punto de entrada" más abajo).

### 2. Las negaciones van en el campo `negative_prompt`, nunca en el prompt
Veo 3 no entiende "sin meteorito": lee la palabra *meteorito* y te pone uno. Todo lo que no
querés va en el campo aparte, como **lista de sustantivos separados por comas**, nunca como
frase negativa. Cada plano de abajo trae su lista ya armada.

### 3. El audio lo genera Veo, y eso es mitad regalo y mitad problema
Veo 3 genera diálogo, ambiente y efectos. Aprovechalo para el ambiente y los efectos: te
resuelve las chicharras, el diésel, el vidrio, la estática. Pero:

> **El diálogo generado te va a salir en español neutro o con acento mexicano las más de las
> veces, aunque le pidas rioplatense.** Para este video son cinco intervenciones de voz.
> Usá el audio de Veo como **pista guía** y regrabá las cinco voces aparte con gente real.
> Un "¡Llevame!" con acento neutro te rompe el video en tres segundos.

En los prompts de abajo el diálogo está incluido igual, porque ayuda a que Veo genere la
actuación y el movimiento de boca correctos. Lo que se descarta después es la voz, no la toma.

### 4. Apagá el reescritor de prompts en los planos ambiguos
Veo reescribe tu prompt antes de generar, y el reescritor **ama el drama**: si le das un punto
de luz quieto en el cielo, te lo convierte en un meteorito con cola de fuego. En Vertex AI se
apaga con `enhancePrompt: false`. Es obligatorio en **T02, T03 y T14**, que son los tres planos
donde el efecto depende de que *no pase nada*.

### 5. El texto en pantalla, mejor hacelo en post
Veo escribe carteles, pero con faltas de ortografía y en inglés cuando se le da la gana. Tres
planos de este video tienen texto legible como elemento central:

| Plano | Texto | Qué hacer |
|---|---|---|
| `T04` | el gráfico del noticiero | Generar la pantalla de TV con un gráfico genérico y **componer el mapa y los dos puntos rojos en el editor**. Queda mejor y tarda diez minutos. |
| `T08` | `SIN EXISTENCIA DE BILLETES` | Generar el cajero con pantalla en blanco o con texto ilegible y **componer el texto encima**. |
| `T13` | `TRES ARROYOS — GRACIAS POR SU VISITA` | Generar el cartel de ruta en blanco y **componer el texto**. Es un cartel plano, de frente: es un compuesto de cinco minutos. |

Si aun así querés que Veo lo intente, dejá el texto en el prompt (está incluido) y generá
8 variantes en vez de 4. Una de ocho suele salir bien escrita.

### 6. Configuración fija para los 14 planos
```
Relación de aspecto      16:9   (el recorte a 2.39:1 lo hace el script, no Veo)
Resolución               1080p
Duración                 8 s (fijo)
Persona generada         permitir adultos
Semilla (Vertex)         anotala por cada plano que te guste — es tu única forma de repetirlo
Reescritor de prompts    ON, salvo en T02, T03 y T14 (ver punto 4)
```

### 7. Marca de agua
Todo lo que sale de Veo lleva **SynthID**, una marca invisible, y eso no molesta. Lo que sí
molesta es que **algunas superficies y planes agregan una marca de agua visible** en la esquina.
Antes de generar los 14 planos, generá uno solo y mirá la esquina: si aparece un logo visible,
cambiá de plan o de superficie antes de gastar el presupuesto, porque no se puede sacar.

### 8. Consistencia de personajes
Este video tiene **una sola cara**: Camila, en T05. Es la mayor ventaja del teaser y es
deliberada.

Aun así, antes de generar T05, hacé la ficha de personaje:
```
1. Generá una imagen fija de Camila (Imagen, Nano Banana, o el generador de imagen que uses)
   con el bloque canónico de texto de prompts/00-plantilla-y-reglas.md.
2. Iterá hasta tener 3 imágenes de la misma persona: frente, perfil, 3/4.
3. Usá esas imágenes como referencia en Veo (Flow: "Ingredients to Video" / Veo 3.1: imágenes
   de referencia, hasta 3 por prompt).
4. Recién entonces generá T05.
```
Sin esto, Camila en el Ep. 1 va a ser otra persona distinta en cada plano, y el teaser no te
sirve de base.

### 9. Presupuesto
Veo 3 se cobra por segundo de video generado, y hay una versión **Fast** bastante más barata.
Al momento de escribir esto el orden de magnitud es de unos **US$ 0,40 por segundo** en calidad
estándar y alrededor de **US$ 0,15 por segundo** en Fast — **verificá el precio actual antes de
presupuestar, que cambia seguido.**

Con eso, la cuenta de este video:

```
14 planos × 4 variantes × 8 segundos  =  448 segundos de generación

Fast      448 s × ~0,15  ≈   US$ 67
Estándar  448 s × ~0,40  ≈  US$ 180
```

**Estrategia recomendada:** generá las 4 variantes de cada plano en **Fast**, elegí el encuadre
y la actuación que querés, y después **regenerá en estándar solamente los 5 o 6 planos que van
a quedar en pantalla más tiempo** (T01, T03, T05, T06, T14). Te queda en el orden de los
US$ 90 en total en vez de 180, y la diferencia de calidad no se nota en los planos cortos.

---

# BLOQUE A — EL MUNDO NORMAL

## T01 · Campo de trigo al amanecer
*Usar los 8 segundos completos.*

**PROMPT**
```
A static wide shot on a tripod, 40mm lens, of an endless field of ripe golden wheat in the
Argentine pampas at sunrise. The wheat sways slowly in a light breeze, long waves of movement
travelling across the entire frame from left to right. The horizon is completely flat and
empty, with a single distant line of eucalyptus trees far away on the left. Low golden sunrise
light rakes in from the left, casting long soft shadows across the crop, under a clean pale blue
cloudless sky. Cinematic 35mm film look, warm naturalistic colors of wheat gold and pale blue,
deep focus, everything sharp, gentle contrast, subtle film grain. Audio: loud cicadas, one
distant rooster, the faint hum of a tractor very far away, a light wind through dry wheat.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, timestamp, letterboxing, black bars, people,
animals, buildings, roads, fences, mountains, hills, clouds, birds, lens flare, slow motion,
drone movement, camera movement, zoom, push in, CGI look, video game look, oversaturated colors,
teal and orange grade, music
```

---

## T02 · Los pájaros se van
*Generar 8 s. Punto de entrada: elegir el segundo en que despegan y usar los 6 s desde ahí.*
**Reescritor de prompts: APAGADO.**

**PROMPT**
```
A static low-angle wide shot on a tripod, 28mm lens. About forty small brown birds sit close
together along a rusted barbed wire fence that fills the lower third of the frame, with golden
wheat behind them at sunrise. All the birds take off at the same instant, in one single motion,
and fly out of the top right of the frame, leaving the wire empty and vibrating. Backlit
sunrise behind the fence turns the birds into dark silhouettes against a pale sky. Cinematic
35mm film look, warm gold and pale blue palette, deep focus, subtle film grain. Audio: loud
cicadas, then a burst of forty pairs of wings, then complete silence for the last three seconds.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, people, slow
motion, murmuration, flocking swirl, CGI birds, flock formations in the sky, camera movement,
zoom, lens flare, music, dramatic score
```
> **Ojo:** el reescritor te va a querer hacer una bandada haciendo figuras en el cielo. Apagalo.
> Los pájaros tienen que irse y desaparecer de cuadro, no coreografiar nada.

---

## T03 · La perra mira hacia el este
*Generar 8 s. Usar los 8 completos.* **Reescritor de prompts: APAGADO.**

**PROMPT**
```
A static shot at dog height on a tripod, 50mm lens, shallow depth of field. A lean
medium-sized Argentine mixed-breed dog, a German shepherd cross with a short light brown coat,
a black mask on her muzzle and ears, her left ear folding forward, and an old brown leather
collar with a small metal tag, sits on a cracked concrete sidewalk facing directly away from
camera, looking straight down the length of an empty small-town street. Her ears are rigid and
upright and she stays completely motionless, then growls low without moving a muscle. Behind
her the street runs straight away to a flat empty horizon, lined with low brick and plastered
houses with barred windows, one parked 1990s pickup truck, and concrete telephone poles with
sagging cables; a closed metal roller shutter on a workshop at the right edge of frame. Dawn
before sunrise, flat cool light, no shadows, pale grey-blue sky at the end of the street.
Cinematic 35mm film look, muted palette of brick, concrete and pale blue, subtle film grain.
Audio: total silence, then one low growl, then a metal roller shutter beginning to rise far
behind camera.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, people, other
animals, moving cars, dog turning to camera, dog facing camera, tail wagging, cute expression,
barking, panting, camera movement, zoom, slow motion, lens flare, music, sunny light, hard
shadows
```
> **Ojo:** Veo quiere que los perros miren a cámara y muevan la cola. Si en las 4 variantes se
> da vuelta, generá 4 más. Este plano sólo funciona si la perra nunca mira a cámara.

---

## T04 · El mapa en la televisión
*Generar 8 s, usar 6.* **El gráfico se compone en post (ver punto 5).**

**PROMPT**
```
An extreme close-up on a tripod, 85mm lens, of an old convex CRT television screen filling the
whole frame, with visible scanlines and chromatic fringing at the edges. On the screen is a
crude 1990s television news graphic: a simple map of the southern hemisphere with two dotted
white curved lines coming in from the top, each ending in a red dot, and a red banner strip
across the bottom of the graphic. The image holds completely still, then the two red dots pulse
once together. The faint reflection of a kitchen window and a floral curtain shows in the curved
glass. The only light is the unstable greenish glow of the television itself. Cinematic 35mm
film grain over the video texture, low contrast. Audio: a distorted small television speaker,
a formal male Argentine news anchor saying "Las autoridades solicitan a la población mantener
la calma. No hay motivo para el pánico." followed by a two-tone emergency alert beep.
```
**NEGATIVE PROMPT**
```
subtitles, captions, closed captions, text overlay, watermark, logo, letterboxing, black bars,
flat screen television, modern HD graphics, news channel branding, anchor visible, presenter,
English text, readable legible text, camera movement, zoom, music
```

---

## T05 · Camila entiende
*Generar 8 s, usar los 8.* **Usar imágenes de referencia de Camila (punto 8).**

**PROMPT**
```
A close-up, 85mm lens, very shallow depth of field, handheld with almost no movement. A
34-year-old Argentine woman with fair freckled skin, dark brown wavy shoulder-length hair still
wet from a shower and loosely tied back, green eyes, thick eyebrows and thin gold metal-framed
glasses, wearing a grey sweatshirt, sits down slowly onto a kitchen chair without looking at it,
her eyes fixed on something off-screen to the left. Her mouth opens very slightly. She does not
blink. One hand still holds a set of car keys, forgotten, halfway raised. The setting is a small
1970s Argentine kitchen in the morning; out of focus in the foreground is the shoulder of an
older woman in a pink quilted housecoat sitting at a table with floral oilcloth. Soft warm
morning window light from the left, the right side of her face falling into shadow, no fill
light. Cinematic 35mm film look, warm naturalistic palette, only her eyes in focus, subtle film
grain. Audio: a television reduced to a muffled underwater hum, her shallow breathing, a wall
clock ticking.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, crying, tears,
hand over mouth, gasping, dramatic reaction, smiling, makeup, glamour lighting, camera movement,
zoom, push in, slow motion, music, score, dialogue
```
> **Ojo:** es el único plano con cara en todo el video, y el que fija a Camila para toda la
> serie. Generá 8 variantes, no 4. Y anotá la semilla de la que elijas.

---

## T06 · La bandeja de agua
*Generar 8 s, usar los 8.*

**PROMPT**
```
A static close-up on a tripod, 50mm lens, side angle at counter height. A rectangular glass
laboratory tray half full of water sits on a school laboratory counter, with three small wooden
blocks standing upright in the shallow end like tiny buildings. A woman's hand enters from the
right, lifts the far edge of the tray about fifteen centimeters and lets it drop; the water
surges along the full length of the tray, jumps the near rim, spills across the counter and runs
off the edge, knocking all three wooden blocks flat. The room is a dark empty science classroom
in an Argentine technical high school with the lights off, brass gas taps and a deep sink out of
focus behind, dust on the counter. Hard window light rakes low across the counter from the left,
catching highlights on the moving water; the rest of the room is in deep shadow. Cinematic 35mm
film look, cool desaturated palette, shallow focus on the spilling edge, subtle film grain.
Audio: glass shifting on a hard counter, water sloshing heavily, water hitting floor tiles, and
a woman whispering "Ay, no" almost inaudibly.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, slow motion,
high speed photography, floating droplets, splash art, blue tinted water, glowing water, CGI
water simulation, face visible, person visible, camera movement, zoom, music
```

---

# BLOQUE B — LA CUENTA

## T07 · El mapa de papel
*Generar 8 s, usar 7.*

**PROMPT**
```
A static overhead top-down shot on a tripod, 35mm lens. A yellowed Argentine paper road map
from 2003 is spread flat over the bonnet of an old car, repaired along its folds with strips of
yellowed adhesive tape. A thick weathered sun-spotted index finger with a grease-blackened nail
enters from the right, lands hard on a town in the east of the map, drags slowly west across the
entire sheet following a road line, stops at the mountain range and taps the spot twice. The
setting is a small-town Argentine mechanic's workshop at dusk with a single bare work lamp
hanging directly above, making a hot bright pool in the center of the map that falls off rapidly
to darkness at the edges of frame. Cinematic 35mm film look, warm tungsten palette, macro
texture of paper fibre, folds and tape, shallow focus, subtle film grain. Audio: paper
crinkling, a fingertip tapping paper twice, and a low certain older man's voice saying "Ruta 3
hasta Bahía. Después la 22, todo derecho."
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, English place
names, modern branding, GPS screen, phone, tablet, glowing screen, camera movement, zoom,
slow motion, music
```

---

## T08 · El cajero sin billetes
*Generar 8 s, usar 5.* **El texto de la pantalla se compone en post.*

**PROMPT**
```
A static extreme close-up on a tripod, 85mm lens, of the scratched screen of an exterior ATM at
a small-town Argentine bank branch, with the faint reflection of a queue of people and plane
trees in the glass. The screen shows a plain block Spanish message reading "SIN EXISTENCIA DE
BILLETES". A man's hand enters the frame and presses a rubber keypad button twice, hard. The
message does not change. Hard high mid-morning daylight, strong reflections on the glass, deep
shadow inside the ATM alcove. Cinematic 35mm film look, slightly overexposed daylight, warm
brick and concrete palette, shallow focus, subtle film grain. Audio: street ambience, a passing
motorbike, two flat electronic error beeps, and several people waiting behind without speaking.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, bank logos, brand
names, English text, modern touchscreen interface, colorful interface, faces, portrait, camera
movement, zoom, music
```

---

## T09 · La góndola vacía
*Generar 8 s, usar 5.*

**PROMPT**
```
A slow lateral tracking shot, 40mm lens, dollying steadily to the right at walking pace past
three supermarket shelving units that are almost completely empty: bare metal shelving, a few
scattered tins lying on their sides, one broken bag of flour spilled white across the floor
tiles, and an abandoned wire trolley standing crooked in the aisle. The setting is a small-town
Argentine grocery store at night with worn checkerboard floor tiles and hand-written cardboard
price tags still clipped to the empty shelf edges. Overhead fluorescent tubes give flat greenish
white light with hard shadows under the shelves, and one tube flickers. Cinematic 35mm film
look, cold green-white fluorescent palette, deep focus, subtle film grain. Audio: a fluorescent
hum, a flickering tube ticking, a trolley wheel squeaking somewhere off screen, and a metal
roller shutter rattling far away.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, brand names,
readable product labels, people, shoppers, looting, running, broken glass, smoke, fire, camera
shake, handheld, zoom, music
```

---

## T10 · La radio se queda muda
*Generar 8 s, usar 5.*

**PROMPT**
```
A static extreme close-up on a tripod, 85mm macro lens, extremely shallow depth of field, of the
front panel of an old VHF radio transceiver: an illuminated green frequency display, an analogue
signal-strength meter with a white needle, a chrome tuning knob and worn lettering. The needle
jumps twice, hard, to the right, then falls flat to zero and stays completely still for the rest
of the shot. The transceiver sits on the concrete floor of a dark workshop with a coil of cable
and a car battery out of focus beside it. The only light is the green glow of the radio's own
panel; everything around it is black. Cinematic 35mm film look, green monochrome palette, macro,
subtle film grain. Audio: a man's voice in Chilean Spanish cutting through heavy static saying
"...están evacuando el puerto, repito, están evacuando el..." and then stopping mid-word,
leaving only pure white noise for the last three seconds.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, brand names,
hands, people, modern digital display, LCD screen, blue light, camera movement, zoom, music
```

---

## T11 · Humo detrás de la iglesia
*Generar 8 s, usar 5.*

**PROMPT**
```
A static wide shot on a tripod from a slightly low angle, 40mm lens. The silhouette of a
small-town Argentine church tower stands against a night sky, with thick black smoke rising
steadily from behind it, lit orange from below by an unseen fire. A blue and red emergency light
sweeps rhythmically across the face of the tower from off screen right. In the foreground, plane
trees in silhouette and the base of a monument; scattered rubbish on the ground. Orange fire
glow from below and behind, a blue-red police strobe sweeping across, one orange sodium
streetlamp at the edge of frame, deep blue-black shadows. Cinematic 35mm film look, night
palette of sodium orange against blue-black, high contrast, smoke visible in the light beams,
deep focus, subtle film grain. Audio: a distant crowd, a siren, breaking glass, and a car horn
stuck on one note.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, people, crowd
visible, visible flames, fire in frame, explosion, firefighters, fire truck, camera movement,
zoom, lens flare, music, dramatic score
```

---

# BLOQUE C — LA SALIDA

## T12 · Las manos en la chapa
*Generar 8 s, usar 6.*

**PROMPT**
```
A close-up, 50mm lens, handheld, travelling slowly alongside a moving truck. Many human hands
of different ages and sizes are pressed against the white painted steel door of the truck. The
hands slap the metal, press flat and slide along it as the truck creeps forward; one hand grabs
the door mirror arm and is pulled out of frame. A greasy handprint is already on the door. The
setting is a small-town street at night with a dense crowd pressing in on both sides, headlights
and torch beams flashing across the white paintwork. Hard mixed light: an orange sodium
streetlamp from above and white torch beams crossing, with strong moving shadows. Cinematic
35mm film look, night palette of sodium orange and blue-black, high contrast, dust in the air,
shallow focus, subtle film grain. Audio: palms slapping steel, dozens of overlapping voices, a
desperate man shouting "¡Llevame! ¡Llevame!" and a diesel engine at low revs underneath.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, faces in focus,
portraits, violence, fighting, weapons, blood, breaking glass, riot, slow motion, CGI crowd,
duplicated hands, extra fingers, deformed hands, music
```

---

## T13 · El cartel de salida del pueblo
*Generar 8 s, usar 6.* **El texto del cartel se compone en post.*

**PROMPT**
```
A static wide shot on a tripod from a low position at the roadside, 28mm lens. A white 1996
Scania long-haul truck with a high cab, a chrome bull bar, two vertical exhaust stacks and
sun-bleached paint, pulling a flatbed semi-trailer covered with a patched olive-green military
tarpaulin tied down with ropes, drives away from camera along a two-lane road at night, passing
a roadside sign that reads "TRES ARROYOS - GRACIAS POR SU VISITA". Its red tail lights shrink
and shrink into total darkness. The setting is the edge of a small town: one last orange
streetlamp, then flat open farmland and complete blackness beyond. The only light is the sodium
streetlamp on the sign, then the truck's red tail lights and a faint band of stars. Cinematic
35mm film look, almost monochrome night palette, heavy grain in the shadows, deep focus. Audio:
the noise of a crowd cutting out sharply in one step, a heavy diesel stretching up through three
gears, then crickets returning.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, other vehicles,
traffic, people, pedestrians, American truck, modern truck, chrome sleeper cab, neon lights,
camera movement, zoom, lens flare, music
```

---

## T14 · El espejo retrovisor
*Generar 8 s, usar 7.* **Reescritor de prompts: APAGADO. El plano más difícil del video.**

**PROMPT**
```
A static extreme close-up, 85mm lens, extremely shallow depth of field, with visible engine
micro-vibration, of a dusty rectangular truck wing mirror in a black plastic housing, mounted on
the driver's door of a moving truck at night. Inside the mirror's reflection: a two-lane road
receding into the night, the faint orange glow of a burning town very far away at the end of it,
and above the horizon line in the reflected sky a single small point of cold white light,
slightly elongated and too bright, that stays perfectly still. The whole reflection trembles
with the engine. A human figure runs across the far end of the reflected road and is gone. The
mirror housing itself is almost black; the small white point of light in the reflected sky is
the brightest thing in frame. Cinematic 35mm film look, night palette, macro, subtle film grain.
Audio: a heavy diesel at cruising revs, wind, and underneath it a very low sustained 25 Hz tone.
```
**NEGATIVE PROMPT**
```
subtitles, captions, text overlay, watermark, logo, letterboxing, black bars, meteor, meteor
trail, shooting star, streak of light, comet, fireball, explosion, glowing object, lens flare,
light rays, moon, planet, aurora, CGI object, camera movement, zoom, slow motion, music
```
> **Ojo, es el plano que cierra el video.** Veo va a querer darte un meteorito. Apagá el
> reescritor, mantené la lista negativa completa, y generá 8 variantes. El criterio de
> selección es uno solo: **si mirando el plano te preguntás "¿qué es eso?", está bien. Si sabés
> qué es, está mal** y hay que regenerar.
>
> Plan B si a las 8 variantes Veo insiste con el meteorito: generá el plano **sin ningún punto
> de luz** (sacá esa frase del prompt) y **componé el punto en el editor**. Es un punto blanco
> de cuatro píxeles con un poco de glow. Tarda dos minutos y te garantiza el resultado.

---

## Punto de entrada de cada clip

Como Veo devuelve 8 segundos y el montaje necesita menos, hay que elegir **qué parte de los 8
segundos usar**. El script `03-ensamblar.sh` tiene un arreglo `OFFS` para eso: poné en qué
segundo del clip generado arranca el trozo que querés.

| Plano | Dur. final | Qué buscar al elegir el punto de entrada |
|---|---|---|
| T01 | 8 s | Usar completo. |
| T02 | 6 s | **Empezar 1 s antes del despegue.** Es el plano donde el punto de entrada importa más. |
| T03 | 8 s | Usar completo. |
| T04 | 6 s | Justo antes del pulso de los puntos rojos. |
| T05 | 8 s | Usar completo. |
| T06 | 8 s | Usar completo; si el derrame arranca tarde, recortar del principio. |
| T07 | 7 s | Que el dedo entre en cuadro en el primer segundo. |
| T08 | 5 s | Centrado en los dos apretones de tecla. |
| T09 | 5 s | El tramo más parejo del travelling, sin arranque ni frenada. |
| T10 | 5 s | **Empezar 1 s antes de que la aguja salte.** |
| T11 | 5 s | Cualquier tramo con el barrido azul y rojo completo. |
| T12 | 6 s | El tramo con más manos en cuadro. |
| T13 | 6 s | Desde que el camión pasa el cartel. |
| T14 | 7 s | El tramo más quieto, donde el punto de luz no se mueve. |

## Checklist Veo 3

```
[ ] Un plano de prueba generado y revisado por marca de agua visible ANTES de gastar el resto
[ ] Ficha de Camila hecha (3 imágenes de referencia) ANTES de generar T05
[ ] 16:9, 1080p, 8 s en los 14 planos
[ ] Reescritor de prompts APAGADO en T02, T03 y T14
[ ] Semillas anotadas de todas las tomas elegidas
[ ] 8 variantes (no 4) en T05 y T14
[ ] Las listas de negative_prompt pegadas en el campo correcto, NO dentro del prompt
[ ] Texto de T04, T08 y T13 compuesto en post, no confiado a Veo
[ ] Audio de Veo conservado como pista guía; las 5 voces regrabadas aparte
```

---

## Nota para cuando sigas con el Episodio 1

**Veo 3 restringe la generación de menores.** Tobi tiene 9 años y está en 14 planos del Ep. 1
y del Ep. 2, incluida la última línea de la temporada. Vas a chocar con esa política.

Formas de resolverlo sin perder el personaje, en orden de preferencia:
1. **Nunca mostrarle la cara.** Manos, nuca, la espalda, la silueta, los pies, el dibujo, el
   handy naranja. Funciona dramáticamente mejor de lo que parece: Tobi es el que mira, y un
   personaje del que nunca ves la cara es más inquietante.
2. **Filmar a un chico real** para esos planos y mezclarlo con el material generado. Son pocos
   planos, y es un chico sentado en una cabina.
3. **Reemplazar los planos por su punto de vista:** lo que Tobi ve, en vez de Tobi.

La opción 1 está a mano: revisá los planos de Tobi en el pack del Ep. 1 y vas a ver que la
mitad ya están escritos así (`1.34` es el dibujo, no la cara).
