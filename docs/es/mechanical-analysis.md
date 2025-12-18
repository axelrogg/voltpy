# Análisis mecánico


## Especificación de características generales de la línea

!!! Danger
    Pendiente de implementación.


## Especificación de detalles del conductor

El análisis mecánico en Ohmly se realiza siempre sobre un modelo de conductor
específico. Un conductor en Ohmly encapsula todas las propiedades mecánicas,
geométricas y eléctricas necesarias para todos los cálculos, siguiendo la
norma UNE-EN 50182.

Ohmly incluye una base de datos de conductores integrada, por lo que en la
mayoría de los casos no es necesario definir estas propiedades manualmente.


## Base de datos de conductores

La base de datos interna incluye actualmente un subconjunto de conductores
estándar definidos en la norma UNE-EN 50182:2002, principalmente de la 
Tabla F.30 (características de los conductores de aluminio reforzado con acero
utilizados en España – Tipo AL1/ST1A).

!!! Important
    La base de datos sigue creciendo. Por el momento, solo hay disponible un
    número limitado de conductores. Las futuras versiones ampliarán la
    cobertura y podrán incluir familias de conductores adicionales.

Cada conductor puede identificarse mediante:

-   su designación oficial (código UNE), o
-   su código antiguo (*legacy/old code*).


## ¿Cómo obtener un conductor?

Para obtener un conductor, crea una instancia del `ConductorRepository` y
realiza la consulta por código nuevo o antiguo.

```python
from ohmly import ConductorRepository

repo = ConductorRepository()

# Obtener por designación oficial
conductor = repo.get(designation="242-AL1/39-ST1A")

# O también por código antiguo
conductor = repo.get(legacy_code="LA 280 HAWK")

# Imprimir una tabla formateada con las propiedades del conductor.
print(conductor)
```

Al imprimir un conductor se muestra una tabla formateada como la siguiente:

```bash
  Attribute              Unit             Value  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  designation                -   242-AL1/39-ST1A  
  legacy_code                -       LA 280 HAWK  
  al_area                  mm²             241.6  
  steel_area               mm²              39.5  
  total_area               mm²             281.1  
  al_strands                 -                26  
  steel_strands              -                 7  
  core_diameter             mm              8.04  
  overall_diameter          mm              21.8  
  mass                   kg/km             976.2  
  rated_strength           daN            8489.0  
  resistance_dc           Ω/km            0.1195  
  elastic_modulus       kN/mm²            7300.0  
  thermal_exp_factor      1/°C          1.89e-05  
  unit_weight            daN/m            0.9573
```


## ¿Dónde puedo encontrar todos los conductores disponibles?

Si no estás seguro de qué conductores están disponibles en la base de datos,
puedes listar todos los conductores registrados.

```python
print(repo.list_all())
```

Esto devuelve una lista de conductores con su designación y código antiguo,
pensada para facilitar el descubrimiento, la creación de menús de selección o
una inspección rápida.


### ¿Cómo modificar las propiedades de los conductores?

Ohmly asume valores estándar nominales; sin embargo, las propiedades reales de
un conductor pueden variar según el fabricante o las hipótesis específicas de
un proyecto.

Por este motivo, las características del conductor no están bloqueadas. Puedes
modificarlos después de la carga si es necesario.

Ejemplos comunes son la sobrescritura del módulo de elasticidad, la carga de
rotura y/o el peso unitario.

```python
conductor.rated_strength = 8456  # (daN) - Resistencia a la tracción asignada

conductor.elastic_modulus = 7700  # (kN/mm²) - Módulo de elasticidad

conductor.unit_weight = 0.96  # (daN/m) - Peso unitario
```

Esto te permite:

-   tener en cuenta datos específicos del fabricante;
-   incluir herrajes adicionales o recubrimientos (aislamientos); y
-   adaptar el modelo a las hipótesis específicas del proyecto.

!!! Note
    Los cambios solo afectan a la instancia actual del conductor y no modifican
    la base de datos interna.


### Definición Manual de un Conductor

Aunque Ohmly proporciona una base de datos integrada de conductores estándar,
su uso no es obligatorio.

Puedes crear una instancia de Conductor manualmente cuando:

-   el conductor no está recogido en la norma UNE-EN 50182;
-   los datos del fabricante difieren de los valores estándar;
-   estás analizando conductores personalizados, experimentales o antiguos
    (*legacy code*); o
-   deseas un control total sobre cada parámetro mecánico.


#### Creación Manual de un Conductor

Se puede instanciar un conductor directamente proporcionando todas las
propiedades requeridas:

```python
from ohmly import Conductor

conductor = Conductor(
    designation="CUSTOM-ACSR-300",
    legacy_code=None,
    al_area=300.0,              # mm² (sección de aluminio)
    steel_area=40.0,            # mm² (sección de acero)
    total_area=340.0,           # mm² (sección total)
    al_strands=26,              # número de hilos de aluminio
    steel_strands=7,            # número de hilos de acero
    core_diameter=8.2,          # mm (diámetro del alma/núcleo)
    overall_diameter=22.5,      # mm (diámetro total exterior)
    mass=1020.0,                # kg/km (masa)
    rated_strength=9000.0,      # daN (resistencia a la tracción asignada)
    resistance_dc=0.118,        # Ω/km (resistencia en CC)
    elastic_modulus=7600.0,     # kN/mm² (módulo de elasticidad)
    thermal_exp_factor=1.9e-5,  # 1/°C (coeficiente de dilatación térmica)
)

print(conductor)
```

En el terminal se imprimirá lo siguiente.

```bash
  Attribute              Unit             Value  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  designation                -   CUSTOM-ACSR-300  
  legacy_code                -              None  
  al_area                  mm²             300.0  
  steel_area               mm²              40.0  
  total_area               mm²             340.0  
  al_strands                 -                26  
  steel_strands              -                 7  
  core_diameter             mm               8.2  
  overall_diameter          mm              22.5  
  mass                   kg/km            1020.0  
  rated_strength           daN            9000.0  
  resistance_dc           Ω/km             0.118  
  elastic_modulus       kN/mm²            7600.0  
  thermal_exp_factor      1/°C            1.9e-05  
  unit_weight            daN/m            1.0003
```

!!! Note
    Todas las unidades DEBEN seguir las mismas convenciones que los conductores
    cargados desde la base de datos, ya que todas las funciones de Ohmly asumen
    estas unidades.

Una vez creado, un conductor definido manualmente es indistinguible de uno
cargado desde la base de datos y puede utilizarse en todos los análisis
mecánicos.


## Definición del contexto de análisis mecánico

Todos los cálculos mecánicos en Ohmly se realizan dentro de un contexto de
análisis mecánico.

Un contexto de análisis mecánico vincula

-   un conductor específico y 
-   una zona de análisis mecánico, según define la ITC-LAT 07.

Este contexto define las hipótesis ambientales bajo las cuales se realizan
todos los cálculos mecánicos posteriores, incluyendo límites de tensión,
manguitos de hielo, efectos del viento y el comportamiento de flechas y
tensiones.

En la práctica, esto refleja cómo se realizan los cálculos de líneas
aéreas: primero se fijan el conductor y su entorno, y, posteriormente, se
evalúan los escenarios de carga.


### Zonas de análisis mecánico (ITC-LAT 07)

La ITC-LAT 07 clasifica las líneas aéreas en zonas basadas en la altitud, las
cuales determinan si deben considerarse cargas de hielo y su severidad.

Ohmly modela estas zonas mediante el enum `MechAnalysisZone`:

| Zona    | Descripción	       | Hielo         |
| ------- | ------------------ | ------------- |
|    A    | Menos de 500 m     | No            |
|    B    | Entre 500 y 1000 m | Sí (moderado) |
|    C    | Más de 1000 m      | Sí (fuerte)   |

La zona seleccionada afecta directamente a:

-   la carga de hielo por unidad de longitud;
-   el cálculo de la carga aparente;
-   los factores de sobrecarga; y
-   los resultados de flechas y tensiones bajo hipótesis con hielo.


### Creación de un contexto de análisis mecánico

Para iniciar cualquier análisis mecánico, crea un objeto `MechAnalysis`
utilizando

-   una instancia de `Conductor`, y
-   la zona de análisis mecánico correspondiente.

```python
from ohmly import MechAnalysis, MechAnalysisZone

mech = MechAnalysis(
    conductor=conductor,
    zone=MechAnalysisZone.B,
)
```

Una vez creado, este objeto se convierte en el punto de entrada para todos los
cálculos mecánicos, incluyendo:

-   Tensión de cada día (EDS - Every-Day Stress).
-   Tensión en la hora más fría (CHS - Cold-Hour Stress).
-   Sobrecarga del conductor y carga aparente.
-   Cálculos del vano ideal de regulación (*ruling span*).
-   Tablas de tendido (flechas y tensiones).


### ¿Por qué la zona pertenece al contexto de análisis?

La zona de análisis mecánico es una propiedad del entorno de la línea, no de
un escenario de carga individual.

Por esta razón

-   la zona queda fijada al crear el objeto `MechAnalysis`,
-   Las hipótesis solo describen condiciones operativas (temperatura, viento,
    porcentaje de la carga de rotura o RTS).
-   Las cargas de manguito de hielo se derivan automáticamente en función de
    la zona.

Este diseño evita combinaciones inconsistentes o físicamente imposibles (por
ejemplo, considerar cargas de hielo en zonas de baja altitud) y mantiene todos
los cálculos alineados con el reglamento.


## Validaciones reglamentarias

Ohmly aplica las reglas de la ITC-LAT 07 de forma explícita.

Por ejemplo, intentar computar magnitudes relacionadas con el hielo en la Zona A
lanzará un error:

```python
mech = MechAnalysis(conductor, zone=MechAnalysisZone.A)
mech.overload(with_ice=True)  # ¡Error! No es válido según el reglamento.
```

Esto es intencionado. Ohmly prefiere un fallo explícito antes que generar
resultados inválidos de forma silenciosa.


## Esquema mental del análisis mecánico en Ohmly

Una forma útil de entender `MechAnalysis` es la siguiente.

-   El conductor define qué se está analizando.
-   La zona define dónde está instalado.
-   Las hipótesis definen cómo está cargado.

Una vez definido el contexto de análisis mecánico, todos los cálculos
resultan consistentes, trazables y conformes a la normativa.


## Sobrecarga del conductor y carga aparente

En el análisis mecánico, un conductor no solo está sometido a su propio peso.
Las acciones ambientales, como el viento y la formación de manguitos de hielo,
introducen cargas adicionales que deben tenerse en cuenta al evaluar las
tensiones y la flecha.

Ohmly modela estos efectos mediante el concepto de carga aparente, siguiendo la
metodología definida en la ITC-LAT 07.


### Carga del conductor desnudo

En ausencia de viento y hielo, el conductor está sometido únicamente a su
propio peso:

-   Carga vertical = peso unitario del conductor.
-   Carga horizontal = 0.

Esto corresponde a las condiciones normales de operación y se utiliza
típicamente para los cálculos de la tensión de cada día (EDS).


### Carga de hielo

Cuando hay hielo presente, se aplica una carga vertical adicional al conductor
(manguito de hielo). La carga de hielo depende de

-   la zona de análisis mecánico (A, B o C) y
-   el diámetro total exterior del conductor.

En Ohmly, la carga de hielo se calcula automáticamente en función de la zona
de análisis:

-   **Zona A**: No se considera hielo.
-   **Zona B**: Carga de hielo moderada.
-   **Zona C**: Carga de hielo fuerte.

!!! Note
    Intentar calcular la carga de hielo en la Zona A lanzará un error, ya que
    el reglamento no define la existencia de manguitos de hielo en dicha zona.


### Carga de viento

El viento produce una carga horizontal distribuida que actúa sobre el
conductor. Su magnitud depende de

-   la velocidad del viento,
-   el diámetro del conductor, y
-   la presencia o ausencia de hielo (que aumenta el diámetro expuesto).

Ohmly calcula la carga de viento utilizando la formulación de presión de
viento definida en la ITC-LAT 07 y la aplica por unidad de longitud de
conductor.

!!! Note
    La velocidad del viento se especifica siempre en km/h.


### Carga aparente

Para los cálculos de flechas y tensiones, las cargas de viento y las cargas
verticales se combinan en una única carga distribuida aparente.

La carga aparente se define como la resultante vectorial de

-   la carga vertical (peso del conductor ± hielo).
-   la carga horizontal de viento.

Esta carga aparente se utiliza directamente en los cálculos de la catenaria,
sustituyendo al peso del conductor desnudo.

En Ohmly, la carga aparente está representada por el objeto
`CatenaryApparentLoad`.


#### Cálculo de la carga aparente

La carga aparente se calcula mediante el método `MechAnalysis.overload()`.

```python
from ohmly import MechAnalysis, MechAnalysisZone

mech = MechAnalysis(conductor, zone=MechAnalysisZone.B)

# Solo viento
load = mech.overload(wind_speed=90)

# Viento + hielo
load = mech.overload(wind_speed=90, with_ice=True)
```

El objeto devuelto contiene

-   la carga horizontal de viento (daN/m),
-   la carga vertical efectiva (daN/m), y
-   la magnitud de la carga aparente resultante (daN/m).


### Coeficiente de sobrecarga

En algunos análisis, resulta útil expresar la severidad de las acciones
ambientales en relación con el peso propio del conductor.

Ohmly proporciona el método `MechAnalysis.overload_factor()`, definido como:

$$
\text{Coeficiente de sobrecarga} = \frac{\text{Peso aparente}}{\text{Peso propio del conductor}}
$$

Este factor es adimensional y suele utilizarse para evaluar rápidamente qué
tan exigente es una hipótesis determinada.

```python
factor = mech.overload_factor(load)
```


## Tabla de tendidos

El análisis de flechas y tensiones (o cálculo de tendido) evalúa cómo
evolucionan la tensión y la flecha del conductor bajo diferentes condiciones
operativas y ambientales, garantizando al mismo tiempo que no se superen los 
límites de tensión admisible.

Esto se realiza definiendo un conjunto de hipótesis (escenarios de carga) y
verificando que una de ellas actúe como la hipótesis de control (o
determinante) para todas las demás.

Ohmly sigue esta metodología de forma explícita.


### Definición de las hipótesis mecánicas

Una hipótesis mecánica representa un único escenario operativo definido por

-   la temperatura del conductor.
-   la fracción de la carga de rotura nominal (RTS).
-   la velocidad del viento.
-   la presencia o ausencia de hielo.

En Ohmly, las hipótesis están representadas por la clase
`MechAnalysisHypothesis`.


### Parámetros de una hipótesis

Cada hipótesis se define utilizando los siguientes parámetros:

| Parámetro    | Significado                                                       |
| ------------ | ----------------------------------------------------------------- |
| `temp`       | Temperatura del conductor (ºC)                                    |
| `rts_factor` | Fracción de la carga de rotura nominal (por ejemplo, 0.15 = 15 %) |
| `wind_speed` | Velocidad del viento en km/h                                      |
| `with_ice`   | Indica si hay presencia de hielo                                  |
| `name`       | Etiqueta descriptiva opcional                                     |


!!! Important
    La tensión admisible para una hipótesis es siempre el producto de
    `rts_factor x rated_strength`.


### Hipótesis típicas de la ITC-LAT 07

Un conjunto típico de hipótesis incluye:

- EDS (Every-Day Stress): Tensión de cada día.
- Viento máximo: Hipótesis de viento reglamentaria.
- Viento + hielo: Hipótesis de sobrecarga combinada.
- Temperatura mínima o CHS (Cold-Hour Stress): Tensión en la hora más fría.

A continuación, se muestra un ejemplo de un conjunto de hipótesis.

```python
from ohmly import MechAnalysisHypothesis

hypos = [
    MechAnalysisHypothesis(
        name="EDS",
        temp=15,
        rts_factor=0.15,
        wind_speed=0,
        with_ice=False,
    ),
    MechAnalysisHypothesis(
        name="Max wind",
        temp=15,
        rts_factor=0.30,
        wind_speed=120,
        with_ice=False,
    ),
    MechAnalysisHypothesis(
        name="Wind + ice",
        temp=0,
        rts_factor=0.30,
        wind_speed=90,
        with_ice=True,
    ),
    MechAnalysisHypothesis(
        name="Cold hour",
        temp=-5,
        rts_factor=0.35,
        wind_speed=0,
        with_ice=False,
    ),
]
```

!!! Note
    Los valores exactos (límites de RTS, temperaturas, velocidades de viento)
    deben elegirse siempre de acuerdo con las especificaciones del proyecto y la
    interpretación reglamentaria aplicable.

    Ohmly **no** impone valores por defecto.

### El concepto de la hipótesis de control

No todas las hipótesis pueden utilizarse como estado de referencia para los
cálculos de flechas y tensiones.

Una **hipótesis de control** se define como aquella que

-   satisface su propia tensión admisible, y
-   al ser utilizada como estado base, no provoca que ninguna otra hipótesis
    supere su propia tensión admisible tras aplicar la ecuación de cambio de
    estado.

!!! Important
    Ohmly determina la hipótesis de control automáticamente.

    Si no existe tal hipótesis, la configuración se considera inválida.


### Cálculo de la Tabla de Tendido

Una vez que:

-   se ha definido un conductor,
-   se ha seleccionado una zona de análisis mecánico, y
-   se ha especificado un conjunto de hipótesis,

se puede calcular una tabla de tendido para uno o más vanos.


#### Ejemplo: cálculo completo de la tabla de tendido

```python

from ohmly import MechAnalysis, MechAnalysisZone

mech = MechAnalysis(
    conductor=conductor,
    zone=MechAnalysisZone.B,
)

vanos = [200, 250, 300]

# Generamos la tabla de tendido (stt: sag-tension table)
table = mech.stt(
    hypos=hypos,
    spans=vanos,
)

print(table)
```

Si existe una hipótesis de control, se devuelve una tabla de tendidos
formateada.

Cada celda contiene

-   la tensión del conductor (daN).
-   el porcentaje correspondiente respecto a la resistencia a la tracción
    asignada (% de la RTS).

Si no se encuentra ninguna hipótesis de control, se devuelve `None`.

!!! Warning
    La ausencia de una hipótesis de control indica que el conductor o el
    conjunto de hipótesis definido violan los límites de tensión 
    reglamentarios. No se trata de un problema numérico, sino de un fallo de
    diseño.


### Cómo realiza Ohmly los cálculos de tendido

Internamente, Ohmly sigue este procedimiento:

1.  Ordena las hipótesis por temperatura.
2.  Asume tentativamente una hipótesis como estado base.
3.  Aplica las ecuaciones de cambio de estado al resto de las hipótesis.
4.  Verifica los límites de tensión admisible para cada caso.
5.  Acepta la primera hipótesis que satisfaga todas las restricciones.

Este proceso es totalmente determinista y trazable.


### Interpretación de resultados

Una tabla de tendido permite

-   verificar el cumplimiento de la normativa (reglamentación vigente).
-   identificar los casos de carga más exigentes.
-   comparar las tensiones entre diferentes vanos.
-   proporcionar datos para comprobaciones posteriores (distancias de
    seguridad/galibos, reacciones en los apoyos y dimensionado de herrajes).

