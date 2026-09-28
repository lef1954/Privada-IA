#!/usr/bin/env bash
#
# TIERRA ALTA - Ensamblado del primer video
#
# Toma los 14 clips generados (T01.mp4 ... T14.mp4), los normaliza a 2.39:1 dentro de un
# cuadro de 1920x1080, les aplica grano de 35 mm, arma las placas de titulo y de cierre,
# concatena todo con los timings de 02-montaje.md y pega los dos rotulos.
#
# USO
#   1. Poner los 14 clips en una carpeta, con los nombres T01.mp4 ... T14.mp4
#      (cualquier extension de video sirve: .mp4, .mov, .webm)
#   2. Si generaste con Veo 3 (clips de 8 s fijos), ajustar el arreglo OFFS de abajo para
#      elegir que parte de cada clip se usa. Ver la tabla en 04-veo3-prompts.md.
#   3. bash 03-ensamblar.sh /ruta/a/la/carpeta/de/clips
#   4. El resultado queda en <carpeta>/salida/TIERRA_ALTA_APERTURA.mp4
#
# REQUISITOS: ffmpeg y ffprobe (https://ffmpeg.org/download.html)
#
# NOTA: este script hace el ensamblado tecnico. El LUT de color y el diseno de sonido
# se hacen despues, en tu editor. Ver 02-montaje.md.

set -euo pipefail

# ---------------------------------------------------------------- configuracion

CLIPS_DIR="${1:-.}"
OUT_DIR="$CLIPS_DIR/salida"
WORK_DIR="$OUT_DIR/tmp"
FINAL="$OUT_DIR/TIERRA_ALTA_APERTURA.mp4"

W=1920              # ancho de entrega
H=1080              # alto de entrega
CH=804              # alto de la imagen en 2.39:1 (1920 / 2.39)
PAD_Y=$(( (H - CH) / 2 ))
FPS=24
GRAIN=7             # intensidad del grano de 35 mm (0 = sin grano, 12 = mucho)
SAT=0.88            # saturacion global
CON=1.04            # contraste global

# Duraciones exactas de cada clip, en segundos (ver 02-montaje.md)
CLIPS=(T01 T02 T03 T04 T05 T06 T07 T08 T09 T10 T11 T12 T13 T14)
DURS=(  8   6   8   6   8   8   7   5   5   5   5   6   6   7)

# Punto de entrada dentro de cada clip generado, en segundos.
# Veo 3 devuelve clips de 8 segundos fijos y el montaje necesita menos, asi que aca se elige
# QUE PARTE de esos 8 segundos se usa. Ver la tabla al final de 04-veo3-prompts.md.
# Ejemplo: si en T02 los pajaros despegan en el segundo 3, poner 2 para entrar un segundo antes.
OFFS=(  0   0   0   0   0   0   0   0   0   0   0   0   0   0)

TITLE_DUR=4
END_DUR=5

# ---------------------------------------------------------------- verificaciones

for bin in ffmpeg ffprobe; do
  command -v "$bin" >/dev/null 2>&1 || { echo "ERROR: falta $bin. Instalar ffmpeg."; exit 1; }
done

# Buscar una tipografia monoespaciada para los rotulos
FONT_MONO=""
for f in \
  /usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf \
  /usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf \
  /System/Library/Fonts/Menlo.ttc \
  /Library/Fonts/Courier New.ttf \
  C:/Windows/Fonts/consola.ttf ; do
  [ -f "$f" ] && { FONT_MONO="$f"; break; }
done
[ -n "$FONT_MONO" ] || { echo "ERROR: no encontre una tipografia monoespaciada. Editar FONT_MONO."; exit 1; }

FONT_TITLE=""
for f in \
  /usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf \
  /usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf \
  /System/Library/Fonts/Supplemental/Times New Roman Bold.ttf \
  C:/Windows/Fonts/timesbd.ttf ; do
  [ -f "$f" ] && { FONT_TITLE="$f"; break; }
done
[ -n "$FONT_TITLE" ] || FONT_TITLE="$FONT_MONO"

mkdir -p "$WORK_DIR"

# Resolver el archivo de cada clip (cualquier extension)
declare -a SRC
missing=0
for i in "${!CLIPS[@]}"; do
  name="${CLIPS[$i]}"
  found=""
  for ext in mp4 mov webm mkv m4v MP4 MOV WEBM; do
    if [ -f "$CLIPS_DIR/$name.$ext" ]; then found="$CLIPS_DIR/$name.$ext"; break; fi
  done
  if [ -z "$found" ]; then
    echo "  FALTA: $name (se esperaba $CLIPS_DIR/$name.mp4)"
    missing=1
  fi
  SRC[$i]="$found"
done
if [ "$missing" -eq 1 ]; then
  echo
  echo "Faltan clips. Generarlos con primer-video/01-prompts-listos.md y volver a correr."
  exit 1
fi

echo "==> 14 clips encontrados en $CLIPS_DIR"

# ---------------------------------------------------------------- 1. normalizar

VF="scale=${W}:-2:flags=lanczos,crop=${W}:${CH}:(iw-${W})/2:(ih-${CH})/2"
VF="${VF},pad=${W}:${H}:0:${PAD_Y}:black,fps=${FPS}"
VF="${VF},eq=saturation=${SAT}:contrast=${CON}"
VF="${VF},noise=alls=${GRAIN}:allf=t+u"
VF="${VF},format=yuv420p"

for i in "${!CLIPS[@]}"; do
  name="${CLIPS[$i]}"
  dur="${DURS[$i]}"
  off="${OFFS[$i]:-0}"
  src="${SRC[$i]}"
  out="$WORK_DIR/n_${name}.mp4"

  # Verificar que el clip generado alcance para el punto de entrada pedido
  srcdur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src" 2>/dev/null || echo 0)
  need=$(awk -v o="$off" -v d="$dur" 'BEGIN{print o+d}')
  if awk -v s="$srcdur" -v n="$need" 'BEGIN{exit !(s < n - 0.05)}'; then
    echo "  AVISO: $name dura ${srcdur}s y se piden ${need}s (entrada ${off}s + ${dur}s)."
    echo "         Bajar OFFS[$i] o volver a generar el clip mas largo."
  fi

  echo "==> normalizando $name  (entrada ${off}s, ${dur}s)"

  # Si el clip no trae audio, se le agrega silencio para que el concat no se rompa
  if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$src" | grep -q .; then
    ffmpeg -y -v error -stats -ss "$off" -i "$src" \
      -t "$dur" -vf "$VF" -af "aresample=48000" \
      -c:v libx264 -crf 18 -preset medium \
      -c:a aac -b:a 192k -ac 2 -ar 48000 \
      "$out"
  else
    ffmpeg -y -v error -stats -ss "$off" -i "$src" -f lavfi -i anullsrc=r=48000:cl=stereo \
      -t "$dur" -vf "$VF" \
      -c:v libx264 -crf 18 -preset medium \
      -c:a aac -b:a 192k -ac 2 -ar 48000 \
      -shortest "$out"
  fi
done

# ---------------------------------------------------------------- 2. las placas

make_card () {
  local out="$1" dur="$2" ; shift 2
  local drawtexts=""
  for spec in "$@"; do
    local txt="${spec%%|*}" ; local y="${spec##*|}"
    [ -n "$drawtexts" ] && drawtexts="${drawtexts},"
    drawtexts="${drawtexts}drawtext=fontfile='${FONT_TITLE}':text='${txt}'"
    drawtexts="${drawtexts}:fontcolor=white:fontsize=54:x=(w-text_w)/2:y=${y}"
  done
  ffmpeg -y -v error -stats \
    -f lavfi -i "color=c=black:s=${W}x${H}:r=${FPS}:d=${dur}" \
    -f lavfi -i "anullsrc=r=48000:cl=stereo" \
    -t "$dur" -vf "${drawtexts},fade=in:0:6,format=yuv420p" \
    -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k -ac 2 -ar 48000 \
    -shortest "$out"
}

echo "==> placa de titulo"
make_card "$WORK_DIR/n_TITLE.mp4" "$TITLE_DUR" "T I E R R A   A L T A|(h-text_h)/2"

echo "==> placa final"
ffmpeg -y -v error -stats \
  -f lavfi -i "color=c=black:s=${W}x${H}:r=${FPS}:d=${END_DUR}" \
  -f lavfi -i "anullsrc=r=48000:cl=stereo" \
  -t "$END_DUR" \
  -vf "drawtext=fontfile='${FONT_TITLE}':text='TIERRA ALTA':fontcolor=white:fontsize=58:x=(w-text_w)/2:y=h/2-120,\
drawtext=fontfile='${FONT_MONO}':text='EPISODIO 1 · \"HORA CERO\"':fontcolor=white@0.85:fontsize=32:x=(w-text_w)/2:y=h/2-20,\
drawtext=fontfile='${FONT_MONO}':text='PROXIMAMENTE':fontcolor=white@0.7:fontsize=28:x=(w-text_w)/2:y=h/2+70,\
fade=in:0:8,fade=out:$(( END_DUR * FPS - 20 )):20,format=yuv420p" \
  -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k -ac 2 -ar 48000 \
  -shortest "$WORK_DIR/n_END.mp4"

# ---------------------------------------------------------------- 3. concatenar

LIST="$WORK_DIR/concat.txt"
: > "$LIST"
add () { echo "file '$WORK_DIR/n_$1.mp4'" >> "$LIST"; }

for n in T01 T02 T03 T04 T05 T06 ; do add "$n" ; done
add TITLE
for n in T07 T08 T09 T10 T11 T12 T13 T14 ; do add "$n" ; done
add END

echo "==> concatenando"
ffmpeg -y -v error -stats -f concat -safe 0 -i "$LIST" \
  -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k "$WORK_DIR/montaje.mp4"

# ---------------------------------------------------------------- 4. rotulos

# Dos rotulos y nada mas. Monoespaciada, blanca al 70 %, abajo a la izquierda.
R1A="drawtext=fontfile='${FONT_MONO}':text='TRES ARROYOS, BUENOS AIRES':fontcolor=white@0.7:fontsize=30:x=90:y=h-170:enable='between(t,2,7)'"
R1B="drawtext=fontfile='${FONT_MONO}':text='H − 31:40':fontcolor=white@0.7:fontsize=30:x=90:y=h-128:enable='between(t,2,7)'"
R2A="drawtext=fontfile='${FONT_MONO}':text='H − 22:00 · COTA 112 m':fontcolor=white@0.7:fontsize=30:x=90:y=h-128:enable='between(t,88,93)'"

echo "==> rotulos y render final"
ffmpeg -y -v error -stats -i "$WORK_DIR/montaje.mp4" \
  -vf "${R1A},${R1B},${R2A},format=yuv420p" \
  -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p \
  -c:a copy -movflags +faststart \
  "$FINAL"

# ---------------------------------------------------------------- listo

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FINAL" | cut -d. -f1)
echo
echo "=============================================================="
echo " LISTO: $FINAL"
echo " Duracion: ${DUR}s  (esperado: 99s)"
echo "=============================================================="
echo
echo " Lo que falta hacer en tu editor:"
echo "   - LUT de color calido sobre todo el video"
echo "   - Vineteado suave al 10 %"
echo "   - Las 5 capas de sonido de 02-montaje.md"
echo "   - Los 3 silencios: 0:12-0:14, 1:08-1:10, 1:21-1:22.5"
echo "   - El infrasonido de 25 Hz entrando en 1:27"
echo
echo " Los archivos intermedios quedan en $WORK_DIR (se pueden borrar)."
