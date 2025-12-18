# Mechanical Analysis

## Specifying General Line Characteristics

!!! Danger
    To be implemented.

## Specifying Conductor Details

Mechanical analysis in Ohmly is always performed on a specific conductor model.
A conductor in Ohmly encapsulates all the mechanical, geometric, and electrical
properties required for all calculations, following UNE-EN 50182.

Ohmly comes with a built-in conductor database, so you don't need to define
these properties manually in most cases.

### Built-in Conductor Database

The internal database currently includes a subset of standard conductors defined
in UNE-EN 50182:2002, primarily from Table F.30 (AL1/ST1A).

!!! Important
    The database is still growing. At the moment, only a limited number of
    conductors are available. Future releases will expand coverage and may include
    additional conductor families.

Each conductor can be identified using:
-   its official designation (UNE format), or
-   its legacy / commercial code.

### Loading a Conductor

To retrieve a conductor, create a `ConductorRepository` and query it by
designation or legacy code:

```python
from ohmly import ConductorRepository

repo = ConductorRepository()

# Fetch by official designation
conductor = repo.get(designation="242-AL1/39-ST1A")

# Or fetch by legacy / commercial code
conductor = repo.get(legacy_code="LA 280 HAWK")

# Print a formatted table of conductor properties.
print(conductor)
```

Printing a conductor displays a formatted table like the following.

```bash
  Attribute              Unit             Value  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  designation               -   242-AL1/39-ST1A  
  legacy_code               -       LA 280 HAWK  
  al_area                 mm²             241.6  
  steel_area              mm²              39.5  
  total_area              mm²             281.1  
  al_strands                -                26  
  steel_strands             -                 7  
  core_diameter            mm              8.04  
  overall_diameter         mm              21.8  
  mass                  kg/km             976.2  
  rated_strength          daN            8489.0  
  resistance_dc          Ω/km            0.1195  
  elastic_modulus      kN/mm²            7300.0  
  thermal_exp_factor     1/°C          1.89e-05  
  unit_weight           daN/m            0.9573  
```

### Discovering Available Conductors

If you're not sure which conductors are available in the database, you can list
all registered conductors:

```python
print(repo.list_all())
```

This returns a list of conductors with their designation and legacy code,
intended for discovery, selection menus, or quick inspection.

### Modifying Conductor Properties

Ohmly assumes nominal standard values, but real-world conductor properties may
vary by manufacturer or project assumptions.

For this reason, conductor attributes are not locked. You can modify them after
loading if needed.

Common examples are overriding the elastic modulus, rated strength, and/or unit_weight:

```python
conductor.rated_strength = 8456  # (daN)

conductor.elastic_modulus = 7700  # (kN/mm²)

conductor.unit_weight = 0.96  # (daN/m)
```

This allows you to:
-   account for manufacturer-specific data,
-   include additional fittings or coatings, and
-   adapt the model to project-specific assumptions

!!! Note
    Changes only affect the current conductor instance and do not modify the
    internal database.

### Defining a Conductor Manually

While Ohmly provides a built-in database of standard conductors, you are not
required to use it.

You can create a `Conductor` instance manually when
-   the conductor is **not covered** by UNE-EN 50182,
-   manufacturer data differs from standard values,
-   you are analyzing custom, experimental, or legacy conductors,
-   you want full control over every mechanical parameter.

#### Manual Conductor Creation

A conductor can be instantiated directly by providing all required properties:

```python
from ohmly import Conductor

conductor = Conductor(
    designation="CUSTOM-ACSR-300",
    legacy_code=None,
    al_area=300.0,              # mm²
    steel_area=40.0,            # mm²
    total_area=340.0,           # mm²
    al_strands=26,
    steel_strands=7,
    core_diameter=8.2,          # mm
    overall_diameter=22.5,      # mm
    mass=1020.0,                # kg/km
    rated_strength=9000.0,      # daN
    resistance_dc=0.118,        # Ω/km
    elastic_modulus=7600.0,     # kN/mm²
    thermal_exp_factor=1.9e-5,  # 1/°C
)

print(conductor)
```

The following will be printed in your terminal.

```bash
  Attribute              Unit             Value  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  designation               -   CUSTOM-ACSR-300  
  legacy_code               -              None  
  al_area                 mm²             300.0  
  steel_area              mm²              40.0  
  total_area              mm²             340.0  
  al_strands                -                26  
  steel_strands             -                 7  
  core_diameter            mm               8.2  
  overall_diameter         mm              22.5  
  mass                  kg/km            1020.0  
  rated_strength          daN            9000.0  
  resistance_dc          Ω/km             0.118  
  elastic_modulus      kN/mm²            7600.0  
  thermal_exp_factor     1/°C           1.9e-05  
  unit_weight           daN/m            1.0003
```

!!! Note
    All units MUST follow the same conventions as database-loaded conductors,
    since all Ohmly's functions assume these units.

Once created, a manually defined conductor is indistinguishable from one loaded
from the database and can be used in all mechanical analyses.

## Defining a Mechanical Analysis Context

All mechanical calculations in Ohmly are performed inside a mechanical analysis
context.

A mechanical analysis context binds together:

-   a specific conductor, and
-   a mechanical analysis zone, as defined by ITC-LAT 07

This context defines the environmental assumptions under which all subsequent
mechanical calculations are performed, including stress limits, ice loads,
wind effects, and sag-tension behavior.

In practice, this mirrors how overhead line calculations are done: the conductor
and its environment are fixed first, and load scenarios are evaluated afterward.

### Mechanical Analysis Zones (ITC-LAT 07)

ITC-LAT 07 classifies overhead lines into altitude-based zones that determine
whether ice loads must be considered and their severity.

Ohmly models these zones using the `MechAnalysisZone` enum:

| Zone    | Description            | Ice considered |
| ------- | ---------------------- | -------------- |
|    A    | Below 500 m            | No             |
|    B    | Between 500 and 1000 m | Yes (moderate) |
|    C    | Above 1000 m           | Yes (severe)   |

The selected zone directly affects:

-   ice load per unit length,
-   apparent load calculations,
-   overload factors, and
-   sag-tension results under ice-related hypotheses.


### Creating a Mechanical Analysis Context

To begin any mechanical analysis, create a `MechAnalysis` object using:

-   a `Conductor` instance, and
-   the appropriate mechanical analysis zone.

```python
from ohmly import MechAnalysis, MechAnalysisZone

mech = MechAnalysis(
    conductor=conductor,
    zone=MechAnalysisZone.B,
)
```

Once created, this object becomes the entry point for all mechanical
calculations, including:

-   Every-Day Stress (EDS),
-   Cold-Hour Stress (CHS),
-   conductor overload and apparent load,
-   ruling span calculations, and
-   sag-tension tables.


### Why the Zone Belongs to the Analysis Context?

The mechanical zone is a property of the line environment, not an individual
load scenarios.

For this reason

-   the zone is fixed when creating `MechAnalysis`,
-   hypotheses only describe operating conditions (temperature, wind, RTS),
-   ice loads are derived automatically from the zone.

This design prevents inconsistent or non-physical combinations (for example,
ice loads in low-altitude zones) and keeps all calculations aligned with the
regulation.

### Regulatory Safeguards

Ohmly enforces ITC-LAT 07 assumptions explicitly.

For example, attempting to compute ice-related quantities in **Zona A** will
raise an error:

```python
mech = MechAnalysis(conductor, zone=MechAnalysisZone.A)
mech.overload(with_ice=True)  # Nope! Invalid by regulation
```

This is intentional. Ohmly favors explicit failure over silent invalid results.

### Mental Model

A useful way to think about `MechAnalysis` is:

-   the conductor defines *what* is being analyzed,
-   the **zone** defines *where* it is installed,
-   **hypotheses** define *how* it is loaded.

Once the mechanical analysis context is defined, all calculations become
consistent, traceable, and regulation-compliant.

## Conductor Overload and Apparent Load

In mechanical analysis, a conductor is not only subjected to its own weight.
Environmental actions such as wind and ice accretion introduce additional loads
that must be considered when evaluating stresses and sag.

Ohmly models these effects through the concept of apparent load, following the
methodology defined in ITC-LAT 07.

### Bare Conductor Load

In the absence of wind and ice, the conductor is subjected only to its own
weight:

-   Vertical load = conductor unit weight
-   Horizontal load = 0

This corresponds to normal operating conditions and is typically used for
Every-Day Stress (EDS) calculations.

### Ice Load

When ice is present, an additional vertical load is applied to the conductor.
The ice load depends on

-   the mechanical analysis zone (A, B, or C), and
-   the conductor overall diameter.

In Ohmly, ice load is computed automatically based on the analysis zone:

-   **Zone A**: ice not considered
-   **Zone B**: moderate ice load
-   **Zone C**: heavy ice load

!!! Note
    Attempting to compute ice load in Zone A will raise an error, as ice is not
    defined in that zone by the regulation.

### Wind Load

Wind produces a horizontal distributed load acting on the conductor. Its
magnitude depends on:

-   wind speed,
-   conductor diameter, and
-   whether ice is present (which increases the exposed diameter).

Ohmly computes wind load using the wind pressure formulation defined in
ITC-LAT 07 and applies it per unit length of conductor.

!!! Note
    Wind speed is always specified in km/h.

### Apparent Load

For sag-tension calculations, wind and vertical loads are combined into a single
apparent distributed load.

The apparent load is defined as the vector resultant of

-   vertical load (conductor weight ± ice), and
-   horizontal wind load.

This apparent load is used directly in catenary calculations, replacing the bare
conductor weight.

In Ohmly, apparent load is represented by the `CatenaryApparentLoad` object.

#### Computing Apparent Load in Ohmly

Apparent load is computed through the `MechAnalysis.overload()` method.

```python
from ohmly import MechAnalysis, MechAnalysisZone

mech = MechAnalysis(conductor, zone=MechAnalysisZone.B)

# Wind only
load = mech.overload(wind_speed=90)

# Wind + ice
load = mech.overload(wind_speed=90, with_ice=True)
```

The returned object contains:
-   horizontal wind load (daN/m),
-   vertical effective load (daN/m), and
-   the resultant apparent load magnitude (daN/m).


### Overload Factor

In some analyses, it is useful to express the severity of environmental loading
relative to the conductor's own weight.

Ohmly provides an `MechAnalysis.overload_factor()` method, defined as:

$$
\text{Overload factor} = \frac{\text{Apparent load}}{\text{Bare conductor weight}}
$$


This factor is dimensionless and is often used to quickly assess how demanding a
given hypothesis is.

```python
factor = mech.overload_factor(load)
```

## Sag-Tension Analysis

Sag-tension analysis evaluates how conductor tension and sag evolve under
different operating and environmental conditions, while ensuring that allowable
stress limits are not exceeded.

This is done by defining a set of hypotheses (load scenarios), and verifying
that one of them can act as a controlling hypothesis for all others.

Ohmly follows this methodology explicitly.

### Defining Mechanical Hypotheses

A mechanical hypothesis represents a single operating scenario defined by

-   conductor temperature,
-   fraction of rated tensile strength (RTS),
-   wind speed,
-   presence or absence of ice.

In Ohmly, hypotheses are represented by the `MechAnalysisHypothesis` class.

#### Hypothesis parameters

Each hypothesis is defined using the following parameters:

| Parameter  | Meaning                                               |
| ---------- | ----------------------------------------------------- |
| temp       | Conductor temperature (ºC)                            |
| rts_factor | Fraction of rated tensile strength (e.g. 0.15 = 15 %) |
| wind_speed | Wind speed in km/h                                    |
| with_ice   | Whether ice is present                                |
| name       | Optional descriptive label                            |

!!! Important
    The allowable tension for a hypothesis is always `rts_factor x rated_strength`.

##### Typical ITC-LAT 07 Hypotheses

A typical set of hypotheses includes:

-   Every-Day Stress (EDS)
-   Maximum wind
-   Wind + ice
-   Minimum temperature or CHS (Cold-Hour Stress)

Below is an example hypothesis set consistent with common practice.

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
    The exact values (RTS limits, temperatures, wind speeds) must always be chosen
    according to the applicable project specification and regulatory
    interpretation.
    
    Ohmly does **not** impose defaults.

#### Controlling Hypothesis Concept

Not every hypothesis can be used as the reference state for sag-tension
calculations.

A **controlling hypothesis** is defined as one that

-   satisfies its own allowable tension, and
-   when used as a base state, does not cause any other hypothesis to exceed
    its allowable tension after state change.

!!! Important
    Ohmly determines the controlling hypothesis automatically.

    If not such hypothesis exists, the configuration is considered invalid.

### Sag-Tension Table Calculation

Once

-   a conductor is defined,
-   a mechanical analysis zone is selected, and
-   a set of hypotheses is specified,

a sag-tension table can be computed for one or more spans.

#### Example: Full Sag-Tension calculation

```python
from ohmly import MechAnalysis, MechAnalysisZone

mech = MechAnalysis(
    conductor=conductor,
    zone=MechAnalysisZone.B,
)

spans = [200, 250, 300]

table = mech.stt(
    hypos=hypos,
    spans=spans,
)

print(table)
```

If a controlling hypothesis exists, a formatted sag-tension table is returned.

Each cell contains

-   conductor tension (daN),
-   corresponding percentage of rated strength.

If **no controlling hypothesis** is found, `None` is returned.

!!! Warning
    A missing controlling hypothesis indicates that the conductor or hypothesis
    set violates regulatory stress limits. This is not a numerical issue--it is a
    design failure.

### How Ohmly Performs Sag-Tension Calculations

Internally, Ohmly follows this procedure:

1.  Sort hypotheses by temperature.
2.  Tentatively assume one hypothesis as the base state.
3.  Apply change-of-state equations to all other hypotheses.
4.  Check allowable tension limits for every case.
5.  Accept the first hypothesis that satisfies all constraints.

This process is fully deterministic and traceable.

### Interpreting Results

A sag-tension table allows you to

-   verify regulatory compliance,
-   identify the most demanding load cases,
-   compare tensions across spans,
-   feed downstream checks (clearances, support reactions, hardware sizing).

