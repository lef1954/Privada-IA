# Plantilla de prompt y reglas anti-deriva

Los prompts se escriben **en inglés** (los modelos de video responden mejor) y los **diálogos
van en español rioplatense**, textuales, entre comillas, para los modelos que generan audio.

---

## 1. Estructura fija del prompt (7 bloques, siempre en este orden)

```
[1 SHOT]      Tipo de plano + lente + movimiento de cámara
[2 SUBJECT]   Personaje(s), copiando TEXTUALMENTE el bloque canónico de abajo
[3 ACTION]    Una sola acción física, clara, que ocurra en 6-8 segundos
[4 SETTING]   Lugar, hora, clima, y los elementos de escala del encuadre
[5 LIGHT]     Fuente de luz, dirección, calidad, temperatura de color
[6 LOOK]      Emulsión, grano, aspecto, paleta del episodio
[7 AUDIO]     Diálogo textual en español + capas de sonido ambiente
NEGATIVE:     Lo que no queremos
```

### Ejemplo completo

```
[SHOT] Medium close-up, 40mm lens, handheld with slight weight, static framing.
[SUBJECT] CAMILA — 34-year-old Argentine woman, 1.68 m, slim build. Fair skin with freckles
across her cheekbones. Dark brown wavy hair to the shoulders, tied in a messy bun with a
pencil through it. Green eyes, thick eyebrows, intense direct gaze. Thin gold metal-framed
glasses. Olive-green windbreaker over a gray sweatshirt, beige cargo trousers.
[ACTION] She stares at a glass laboratory tray of water on a counter, lifts one edge fifteen
centimeters and lets it drop; water spills over the rim onto the countertop; she does not
react, she just watches the water fall.
[SETTING] Empty school science classroom, Argentine technical high school, morning, lights
off, dusty blackboard and glass cabinets out of focus behind her.
[LIGHT] Single soft window light from camera left, cool daylight 5600K, deep shadow on the
right side of her face, no fill.
[LOOK] Cinematic 2.39:1 anamorphic, 35mm film grain, desaturated teal and wheat palette,
shallow depth of field f/2.8.
[AUDIO] Room tone, a fluorescent hum, water spilling. She whispers in Rioplatense Spanish:
"Ay, no."
NEGATIVE: no text overlays, no watermark, no lens flare, no slow motion, no cgi water,
no smiling, no music.
```

---

## 2. Bloques canónicos de personaje (EN INGLÉS — copiar sin modificar)

> Estos textos son la **única** fuente de verdad para la apariencia. No se parafrasean nunca.
> Si un modelo da un resultado distinto, se regenera con la misma semilla/referencia, no se
> cambia el texto.

**NAHUEL**
```
NAHUEL — 42-year-old Argentine man, 1.80 m, sturdy build, broad shoulders. Sun-weathered
olive skin. Short black hair graying at the temples, receding hairline. Three-day stubble.
Dark brown eyes, tired eyelids, sun creases at the corners. Broad nose with a bent bridge.
Blue and gray plaid shirt rolled to the elbows over a white cotton undershirt, worn jeans,
leather belt with a large buckle, brown work sneakers. Cheap steel watch on the left wrist.
Large hands, black grease under the fingernails.
```

**CAMILA**
```
CAMILA — 34-year-old Argentine woman, 1.68 m, slim build. Fair skin with freckles across her
cheekbones. Dark brown wavy hair to the shoulders, tied in a messy bun with a pencil through
it. Green eyes, thick eyebrows, intense direct gaze. Thin gold metal-framed glasses.
Olive-green windbreaker over a gray sweatshirt, beige cargo trousers, brown hiking boots.
A small cloth satchel across her body and a hardcover blue notebook with a pen clipped to it.
```

**DON ALDO**
```
DON ALDO — 68-year-old Argentine man, 1.72 m, lean and wiry. Deeply weathered skin, sun spots
on his hands and forehead. Short white buzzcut, thick white moustache. Small pale blue eyes,
still gaze, deep wrinkles. Faded blue work shirt with two chest pockets, gray workman's
trousers, old black work boots. Blue cotton flat cap with a bent brim. A red rag hanging from
his back pocket. Gold wedding ring on his left hand.
```

**YAMI**
```
YAMI — 19-year-old Argentine woman, 1.60 m, small and slight. Light brown skin. Straight black
hair with a blunt fringe and violet-dyed tips, pulled into a high ponytail. Large brown eyes.
Small nose stud. Big black over-ear headphones hanging around her neck. Black hoodie with a
faded logo, black leggings, worn red sneakers. School backpack covered in patches. A woven
friendship bracelet.
```

**EL RUSO**
```
EL RUSO — 49-year-old Argentine man, 1.75 m, overweight with a prominent belly. Pale skin
reddened by the sun. Bald on top with gray hair at the sides combed back. Light brown eyes,
heavy eyebrows, double chin. Light blue polo shirt with an embroidered grocery-store logo
tucked into gray dress trousers, brown loafers. Thin gold chain and a gold watch. Sweat at the
collar and armpits. A huge keyring hanging from his belt.
```

**TOBI**
```
TOBI — 9-year-old Argentine boy, slight, 1.30 m. Light brown skin, straight dark brown hair
with a long fringe over his eyebrows. Very large brown eyes, long lashes, serious still
expression. Worn light-blue and white football shirt, blue shorts, slouched socks, dirty white
sneakers. He clutches a small red backpack and an orange toy walkie-talkie to his chest.
```

**PAMPA**
```
PAMPA — medium-sized Argentine mixed-breed dog, German shepherd cross, 6 years old. Short
light brown coat with a black mask on the muzzle and ears. The left ear folds forward. Lean,
ribs faintly visible. Old brown leather collar with a small metal tag.
```

**LA PORFIADA (el camión)**
```
LA PORFIADA — a white 1996 Scania 113H long-haul truck, high cab, chrome bull bar, two
vertical exhaust stacks, dented left fender, sun-bleached paint, "LA PORFIADA" hand-painted
in red script on the front bumper, a plastic rosary hanging from the rearview mirror. It pulls
a flatbed semi-trailer covered with a patched olive-green military tarpaulin tied with ropes.
Argentine license plates. A greasy handprint on the driver's door.
```

---

## 3. Bloques de LOOK por episodio (copiar según episodio)

```
EP 1-2  [LOOK] Cinematic 2.39:1, 35mm film grain, warm naturalistic palette of wheat gold,
        brick red and pale blue sky, soft late-afternoon sun, gentle contrast.

EP 3    [LOOK] Cinematic 2.39:1, 35mm grain, night exterior, sodium-vapor orange practicals
        against deep blue-black shadows, strong backlight and lens haze from headlights,
        high contrast, no fill light.

EP 4    [LOOK] Cinematic 2.39:1, 35mm grain, fine gray volcanic ash covering every surface,
        flat diffuse overcast light, no direct sunlight, desaturated palette of gray, bone
        white and dull orange, milky sky.

EP 5    [LOOK] Cinematic 2.39:1, 35mm grain, ash-covered Patagonian steppe, iron-orange glow
        low on the eastern horizon, brown floodwater, cold gray sky, low contrast, wind-blown
        dust in the air.

EP 6    [LOOK] Cinematic 2.39:1, 35mm grain, cold blue dawn, gray ash over dirty snow, deep
        green Andean forest, brown water, pale sun as a dim orange disc, desaturated but with
        color returning.
```

## 4. Bloque NEGATIVE estándar

```
NEGATIVE: no text, no subtitles, no watermark, no logos, no modern smartphones after
episode 3, no American cars, no palm trees, no skyscrapers, no clean clothes, no makeup,
no smiling at camera, no slow motion, no drone orbit, no lens flare, no blue transparent
water, no cartoon or CGI look, no duplicated limbs, no warped faces, no deformed hands,
no extra fingers, no floating objects, no tsunami wave without foreground scale reference.
```

---

## 5. Diez reglas anti-deriva (las que salvan el proyecto)

1. **Una acción por plano.** Si el prompt tiene dos verbos, son dos planos. Ocho segundos no
   alcanzan para "entra, mira y se sienta".
2. **Nunca cambiar el texto del personaje.** Ni una coma. La consistencia es repetición literal.
3. **Máximo dos personajes por plano generado.** Tres o más caras = deriva garantizada.
   Los grupos se construyen en el montaje.
4. **La escala siempre en primer plano.** La ola, la multitud y la montaña necesitan algo
   humano o conocido (molino, poste, auto, persona de espaldas) delante para leerse.
5. **El caos se filma en detalle.** Una mano golpeando la chapa dice más que cien personas
   generadas mal.
6. **Continuidad de suciedad.** Cada prompt de un episodio posterior suma: `dust and gray ash
   on their faces and clothes, sweat, exhausted`. Nunca se retrocede.
7. **La ceniza es permanente desde el Ep. 4.** Si un plano del Ep. 5 sale limpio, se descarta.
8. **Nada de dron.** Solo tres planos aéreos en toda la temporada (Ep. 3.1, Ep. 5.6, Ep. 6.7),
   marcados explícitamente.
9. **Generar de 4 a 6 variantes por plano** y elegir por continuidad, no por belleza.
   El plano más lindo suele ser el que rompe la serie.
10. **Todo plano que no se puede generar bien, se resuelve con sonido y un corte.**
    El espectador completa. Ese es el presupuesto real de esta serie.
