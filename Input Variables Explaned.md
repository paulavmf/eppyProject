https://www.ashrae.org/technical-resources/ashrae-handbook/ashrae-handbook-online
---
title: "Output Variables"
output:
    revealjs::revealjs_presentation
        theme: league
---    


```
{r include = FALSE}
knitr::optsopts_chunk$set(echo = FALSE)
library(viridis)

```
### Group: Simulation Parameters
#### Timestep
Number of Timesteps per Hour. The value entered here is
usually known as the Zone Timestep. __This is used in the Zone Heat Balance Model calculation as
the driving timestep for heat transfer and load calculations.__
El Time step recomendado es de 10 minutos, sobre todo su hay HVAC system
El time step en los datos weather data  no tienen porque coincidir con el que le pido porque EP los interpola

** Shorter zone timesteps improve
the numerical solution of the Zone Heat Balance Model because they improve how models
for surface temperature and zone air temperature are coupled together.**
el Time step del HVAC parece que va a su bola
.. mirar en 'Integrated Solution Manager'


#### Building:


Field: Terrain
The site’s terrain affects how the wind hits the building – as does the building height. In addition,
the external conduction method usually has its own parameters for the calculation.


##### Warmup Convergence (esto hay que ponerlo????)

 The process of the convergence checks begins by tracking four parameters such including the maximum zone air temperature, the minimum zone air temperature, the maximum heating load, and the maximum cooling load for individual zone. 
 Differences in these parameters between two consecutive days are then compared with the convergence tolerance values at the end of the day during the warmup period

 
 ------
 The warm up time is the time that the simulation will run before starting to collect results. 
 This allows the Queues (and other aspects in the simulation) to get into conditions that are typical of normal running conditions in the system you are simulating.
 
 -----

Field: Loads Convergence Tolerance Value
This value represents the number at which the loads values must agree before “convergence” is
reached. Loads tolerance is the change in peak zone heating and cooling loads that are predicted
from previous warmup day to the current day, in units of W
Field: Temperature Convergence Tolerance Valuw


explicado bien aquí
 https://bigladdersoftware.com/epx/docs/8-0/engineering-reference/page-006.html
__Please note–other “convergence tolerance” inputs are required for certain HVAC equipment (unit
ventilator, unit heater, window AC, etc.)__
Field: Maximum/min Number of Warmup Days

minimo y máximos días de simulación hasta terminar el warm up
Field: Solar distribution
determines how EnergyPlus treats beam solar radiation and reflectances from
exterior surfaces that strike the building and, ultimately, enter the zone
MinimalShadowing, FullExterior and FullInteriorAndExterior, FullExteriorWithReflec-
tions, FullInteriorAndExteriorWithReflections.


#### SurfaceConvectionAlgorithm:Inside / SurfaceConvectionAlgorithm:Outside

models used for surface convection at the inside face of
all the heat transfer surfaces in the model
Por defecto es TARP: correlates the heat transfer coefficient to the temperature difference for various orientations. This model is based on flat plate experiments.

#### Time step 

saltos de tiempo por hora . En este caso es cada 10 min (6). Lo recomendado


#### HeatBalanceAlgorithm

type of heat and moisture transfer
algorithm will be used for calculating the performance of the building’s surface assemblies.

__ConductionTransferFunction__(Usado por defecto) no tiene en cuenta el almacenamiento o difusión de humedad en los elementos de contrucción


#### HeatBalanceSettings:ConductionFiniteDifference

used to control the behavior of the Conduction Finite Difference algorithm for surface
heat transfer.
The default is FullyIm-
plicitFirstOrder is defaoult


#### SimulationControl

(importante)
Field: Do Zone Sizing Calculation - Yes
Performs a special
calculation, using a theoretical ideal zonal system, and determines the zone design heating and
cooling flow rates and loads, saving the results in the zone sizing arrays.

Field: Do System Sizing Calculation - Yes
also performs
a special calculation that, to oversimplify, sums up the results of the zone sizing calculation and
__saves the results in the system sizing arrays__ for reporting on component size requirements.
Field: Do Plant Sizing Calculation -No
    xq no tengo ninguna planta, solo tengo una zona y un sistema
    
Field: Run Simulation for Sizing Periods -YEs

Yes implies that the simulation will be run on all
the included SizingPeriod objects (i.e., SizingPeriod:DesignDay, SizingPeriod:WeatherFileDays, and
SizingPeriod:WeatherFileConditionType).

Field: Run Simulation for Weather File Run Periods

Se ejecuta la simulación en todos los RunPeriod objects (cada RunPeriod Describe un weather file) eso es por si hay más de uno...





#### PerformancePrecisionTradeoffs

The PerformancePrecisionTradeoffs object can be used to control tradeoffs between performance
(speed) and precision for certain EnergyPlus features. En mi caso no lo voy a usar

### Group – Location – Climate – Weather File Access

#### Site:Location

Only one location is allowed.
__Weather data file location, if it exists, will override any location data in the IDF__ la localización será la que le pongo en el weather data


#### Site:VariableLocation
Puedo darle parámetros para cambiar de sitio ( para experimentar o para un vehículo).
También se puede aplicar a barcos utilizando “SurfaceProperty:Underwater”

#### SizingPerdiod:Designday

The design day input describes the parameters to effect a “design day” simulation, often used for
load calculations or sizing equipment. Using the values in these fields, Utilizando los valores de estos campos, EnergyPlus "crea" un
días completos de datos meteorológicos

A system (air loop) sizing simulation is performed when AirloopHVAC objects are included and a plant sizing simulation is performed when chllled or hot water loop are included.

Estos dias de diseño son los días extremos que se usarán para definit¡r el sistema HVAC si se utiliza el autosize en el objeto Simulation Control
 Wetbulb bulbo húmedo (temperatura de bulbo húmedo)
 
 DewPoint: Punto de rocío
 
 ..... Esto es importante y no termino de ver qué significa realmente cada objeto....
 
 Tiene pinta de que yo debría elegir un winter design day y un summer design day....
 
 Mediante el objeto SizingPeriod:WeatherFileDays puedo seleccionar periodos dde mi wheather file days que serán los que se usen para als cargas y el sizing de kis equipos
 
 #### Runperiod
 Básicamente información sobre en que mes acaba y qué mes empieza la simulación... puedo definir diferentes run periods salteados durante el año... Supongo que esto es últil cuando la simulación sea muy tocha.....
Field: Use Weather File Daylight Saving Period
Si elDaylight Saving period está en el weather file (que no es siempre así..) (se refiere al periodo de cambio de hora... por lo que entiendo


### Group: schedules
This group of objects allows the user to influence scheduling of many items (such as occupancy
density, lighting, thermostatic controls, occupancy activity)
n addition, schedules are used to
control shading element density on the building.
OSea el Schedules de utilzia par añadir una variable tiempo a muchos datos.
EnergyPlus schedules consist of three pieces: a day description, a week description, and an
annual description. y a Schedule Type (fracional, Temperature... )

### Group – Surface Construction Elements

This group of objects describes the physical properties and configuration for the building envelope
and interior elements. That is, the walls, roofs, floors, windows, doors for the building.

#### Materials

Especifica las características físicas de los materiales presentes en la construcción
- grosor.
- Densidad
- conductividad
- calor específico

#### Materia No mass

Se usa para describir materiales opacos (supongo materiales usados para la  isolación)
 
 #### Material:AirGap
 
This material is used to describe the air gap in an opaque construction element.

#### Window material

...no hay nada en este objeto.... eso es raro

### Group – Thermal Zone Description/Geometry

Esto es lo que realmente describe mi espacio. Thermal Zones es lo que Energy plus llama a cada lugar simulado por separado.
Aquí también se incluyen las superficies que dan sombra

#### Zone
Field(s): (X,Y,Z) Origin
epending
on the values in “GlobalGeometryRules” (see description later in this section), these will be used to
completely specify the building coordinates in “world coordinate” or not.
Zone Origin coordinates are
specified relative to the Building Origin (which always 0,0,0). The following figure illustrates the
use of Zone North Axis as well as Zone Origin values.
Se especifica las coordenadas de comienzo de la zona y los grados de la parte frontal con respecto a la dirección norte. en mi caso, solo hay un termal zone por lo que es 000

Field: Ceiling Height

Energyplus automatically calculates the zone ceiling height (m) from the average height of the zone 
#### Building Surfaces - Detailed . .

Es necesario para todos los cáculos y debe haber un duilding surface por zona
En este objeto se describen los vértices de cada surface (con respeto a la zona)
Entre otras cosas se pueden determinar la exposición al viento o al sol

#### FenestrationSurface:Detailed

Se definen materiales y coordenadas de puertas, ventanas y puertas acristaladas.

## HVAC
#### HVAC Templates


Relamente los una vez elegido un template el subrpograma ExpandObjects es el que se encarga de crear todos los objetos para el hvac si se define un template no es necesario definir los objetos Sizing:Zone o sizonf :System 

### Group – Internal Gains (People, Lights, Other internal zone equipment)

#### People

The people statement is used to model the occupant’s effect on the space conditions.
The following
definition addresses the basic affects as well as providing information that can be used to report the
thermal comfort of a group of occupants

Field: Number of People Calculation Method

People,People/Area,Area/Person en mi caso mi dato está dato por people área por lo que suele ser la ocupación de una oficina.

##### Field: Activity Level Schedule Name

This field is the name of the schedule that determines the amount of heat gain per person in the zone
under design conditions.

This heat gain impacts the basic zone heat balance as well as the modeling of
thermal comfort.


Values for activity level can range anywhere from approximately 100-150 Watts per person for most
office activities up to over 900 Watts per person for strenuous physical activities such as competitive
wrestling

is based on Table 1.10 from the 2005 ASHRAE Handbook
of Fundamentals,

###### Field: Thermal Comfort Model Type (up to 5 allowed)
The final one to five fields are optional and are intended to trigger various thermal comfort models within
EnergyPlus
... eN mic aso no uso ninguno

Outputs relativos a este cambo:
People objects have output variables for individual objects and for zone totals.
People specific outputs include:
• Zone,Average,People Occupant Count []
• Zone,Sum,People Radiant Heating Energy [J]
• Zone,Average,People Radiant Heating Rate [W]
• Zone,Sum,People Convective Heating Energy [J]
• Zone,Average,People Convective Heating Rate [W]
• Zone,Sum,People Sensible Heating Energy [J]
• Zone,Average,People Sensible Heating Rate [W]
• Zone,Sum,People Latent Gain Energy [J]
• Zone,Average,People Latent Gain Rate [W]
• Zone,Sum,People Total Heating Energy [J]
• Zone,Average,People Total Heating Rate [W]
• Zone,Average,Zone People Occupant Count []
• Zone,Sum,Zone People Radiant Heating Energy [J]
• Zone,Average,Zone People Radiant Heating Rate [W]
• Zone,Sum,Zone People Convective Heating Energy [J]
• Zone,Average,Zone People Convective Heating Rate [W]
• Zone,Sum,Zone People Sensible Heating Energy [J]
• Zone,Average,Zone People Sensible Heating Rate [W]
• Zone,Sum,Zone People Latent Gain Energy [J]
• Zone,Average,Zone People Latent Gain Rate [W]
• Zone,Sum,Zone People Total Heating Energy [J]
• Zone,Average,People Air Temperature [C]
• Zone,Average,People Air Relative Humidity [%]
• Zone,Average,Zone People Total Heating Rate [W]

• Zone,Average,Zone Thermal Comfort Mean Radiant Temperature [C]
• Zone,Average,Zone Thermal Comfort Operative Temperature [C]
• Zone,Average,Zone Thermal Comfort Fanger Model PMV []
• Zone,Average,Zone Thermal Comfort Fanger Model PPD [%]
• Zone,Average,Zone Thermal Comfort Clothing Surface Temperature [C]
• Zone,Average,Zone Thermal Comfort Pierce Model Effective Temperature PMV []
• Zone,Average,Zone Thermal Comfort Pierce Model Standard Effective Temperature PMV []
• Zone,Average,Zone Thermal Comfort Pierce Model Discomfort Index []
• Zone,Average,Zone Thermal Comfort Pierce Model Thermal Sensation Index []
• Zone,Average,Zone Thermal Comfort Pierce Model Standard Effective Temperature [C]
• Zone,Average,Zone Thermal Comfort KSU Model Thermal Sensation Index []
• Zone,Average,Zone Thermal Comfort ASHRAE 55 Adaptive Model 80% Acceptability Status []
• Zone,Average,Zone Thermal Comfort ASHRAE 55 Adaptive Model 90% Acceptability Status []
• Zone,Average,Zone Thermal Comfort ASHRAE 55 Adaptive Model Running Average Outdoor Air
Temperature [C]
• Zone,Average,Zone Thermal Comfort ASHRAE 55 Adaptive Model Temperature [C]
• Zone,Average,Zone Thermal Comfort CEN 15251 Adaptive Model Category I Status []
• Zone,Average,Zone Thermal Comfort CEN 15251 Adaptive Model Category II Status []
• Zone,Average,Zone Thermal Comfort CEN 15251 Adaptive Model Category III Status
• Zone,Average,Zone Thermal Comfort CEN 15251 Adaptive Model Running Average Outdoor Air
Temperature [C]
• Zone,Average,Zone Thermal Comfort CEN 15251 Adaptive Model Temperature [C]



#### Lights
The Lights statement allows you to specify information about a zone’s electric lighting system, including
design power level and operation schedule, and how the heat from lights is distributed thermally.
