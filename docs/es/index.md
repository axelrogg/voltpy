# Ohmly

**Ohmly** es una librería en Python para el análisis mecánico de conductores aéreos,
con cálculos alineados con la normativa española **ITC-LAT 07**.

Se centra en los problemas mecánicos reales que los ingenieros resuelven en
proyectos de líneas aéreas:

- Cálculos de flecha–tensión  
- Cargas de viento y hielo  
- Evaluación de múltiples hipótesis de carga  
- Comportamiento dependiente de la temperatura  
- Salvaguardas explícitas conforme a normativa  


!!! Important
    Ohmly es una herramienta de apoyo al cálculo, no sustituye el criterio
    profesional del ingeniero.
    Consulte la sección de **Disclaimer** para más detalles.


## Ejemplo rápido


```python
from ohmly import ConductorRepository, MechAnalysis, MechAnalysisZone

conductor = ConductorRepository().get(legacy_code="LA 180")
mech = MechAnalysis(conductor, zone=MechAnalysisZone.A)

