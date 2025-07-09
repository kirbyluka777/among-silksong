# Requerimientos

- [ ] Sobre los participantes (Equipos de Astronautas):
  - [-] Cada jugador debe registrar el equipo, que se identificará con el nombre de la nave que hará la expedición (este nombre corresponderse con alguna de las constelaciones estelares como Orión, Casiopea, Andrómeda, Leo, Scorpius,etc), además debe registrar una clave de acceso, un correo electrónico y el país que financia la expedición (seleccionado de una lista de países más poderosos de la Tierra, identificados con códigos únicos como USA: Estados Unidos, RUS: Rusia, etc.).
  - [ ] A cada equipo también se le debe asociar un ODS. Ejemplo; Orión – Energía Asequible y Limpia y los astronautas que lo conforman.
  - [ ] El nombre del equipo no podrá existir más de una vez.
  - [-] La clave de acceso debe crearse cumpliendo los siguientes criterios:
    - [x] Debe poseer entre 6 y 10 caracteres.
    - [x] Ser una combinación de letras en mayúscula y minúscula (sin acento y sin la letra Ñ o ñ), números y caracteres especiales.
    - [x] Los caracteres especiales permitidos son: el asterisco (*), el igual (=), el numeral (#) o el guión bajo ( _ ).
    - [-] No debe contener el mismo carácter más de dos veces de forma consecutiva. Por ejemplo, no está permitido: aaa, 222, ***
    - [-] IMPORTANTE : La aplicación debe informar sobre los criterios para la creación de la clave e igualmente debe ir indicando cuales de los criterios no se cumplen al momento de crear la clave, para orientar al usuario sobre su creación.
  - [-] Para la generación de la clave debe utilizar algoritmos recursivos.
  - [-] La clave de seguridad debe almacenarse encriptada. Para ello el sistema debe ofrecer la opción de que el usuario decida encriptarla o no. Se debe diseñar libremente el algoritmo de encriptamiento a utilizar.
  - [x] Se debe mantener un registro de los países que pueden realizar este tipo de expediciones, con códigos únicos y nombres. Ejemplo : USA : Estados Unidos de Norteamérica, RUS : Rusia, etc, a esta lista se le podrían incorporar nuevos países.
  - [-] La información de los equipos (identificador, clave, país al que pertenecen, ODS asociado, etc), se deben almacenar en estructuras de almacenamiento permanentes (archivos).

- [x] Sobre el juego:
  - [x] Podrán participar 2 equipos (cada uno controlando a un astronauta).
  - [x] Cada juego que se inicie, representará una expedición o viaje estelar, el cual debe quedar identificado con un código único.
  - [x] El juego se desarrollará en un mapa estelar de N x N sectores, donde N es un número impar entre 5 y 19 inclusive.
  - [x] La dimensión del mapa, será acordado entre los dos participantes.
  - [x] El punto de partida será la Tierra (sector 1,1) y el objetivo final será un planeta habitable ubicado en el punto central del mapa, al cual se llegará en un recorrido en espiral.
  - [x] Al inicio del juego, a cada equipo, se le asignará aleatoriamente (en un rango de 5 a 15) una cantidad de "unidades de energía".
  - [x] Para el desplazamiento, los jugadores activarán alternadamente los propulsores de sus naves que les permitirá avanzar un número k de sectores en un recorrido en espiral sobre el mapa estelar. Donde k es un número aleatorio entre 1 y 5 inclusive y cada activación de propulsores consume una unidad de energía.
  - [x] El recorrido del mapa, se podrá hacer en sentido horario o antihorario, elegido por los jugadores.
  - [x] Existirán tres niveles de dificultad, lo que determinará la cantidad de obstáculos espaciales y estaciones de apoyo que se conseguirán distribuidas en el mapa estelar. El porcentaje se calculará sobre la cantidad de sectores del mapa.
      Nivel de dificultad  Porcentaje de obtáculos espaciales (%)   Porcentaje de estaciones de apoyo (%)
    - [x] Básico           10                                       20
    - [x] Medio            15                                       15
    - [x] Avanzado         20                                       10
  - [x] Cada jugador seleccionará a un equipo con el que hará la expedición (para ello debe estar registrados). Cada equipo tendrá asociado un ODS desde su inicio (ejemplo: Orión - Energía Asequible y Limpia). La aplicación, debe permitir la incorporación de nuevos equipos y asociales su ODS.
  - [x] Cada sector del mapa se debe identificar con un número consecutivo (1,2, …) en el mapa, que indicará el recorrido en espiral.
  - [x] El recorrido lo iniciará el equipo que obtenga el mayor número, entre un par de números aleatorios generados uno por cada equipo, al comienzo del juego.
  - [x] El mapa se recorrerá en forma de espiral, en sentido horario o sentido antihorario, opción que debe escogerse antes de iniciar el juego.
  - [x] Cada jugador activará sus propulsores de forma alterna y avanzará tantos sectores en el mapa como lo permitan los propulsores.
  - [x] Durante el recorrido se presentarán obstáculos que tendrán consecuencias no favorables para el viaje, estos obstáculos o anomalías espaciales pueden presentarse o encontrarse en un determinado sector, así mismo habrá estaciones espaciales que apoyarán a las naves a completar su recorrido. No todos los sectores tendrán anomalías espaciales ni estaciones espaciales.
  - [x] Por acuerdos internacionales, dos naves pueden llegar a un mismo sector, sin que una afecte el recorrido de la otra.
  - [x] Para llegar hasta el Planeta destino se debe llegar con la energía de propulsión exacta, de no ser así se producirá un efecto rebote, que lo hará retroceder tantos sectores como energía excedente a la requerida para llegar al planeta objetivo, sin desperdicio, luego se debe intentar avanzar nuevamente para llegar al sector donde se encuentra la Planeta objetivo.
  - [x] En algunas de los sectores existirán, de forma aleatoria, ayudas u obstáculos espaciales, que facilitarán o dificultarán el avance de las expediciones, estas se detallan a continuación:
    - [x] Ayudas:
        Estación espacial          Consecuencia
      - [x] Titán                  Recargar 10 unidades de energía
      - [x] Sakaar                 Avanza al sector más cercano desocupado
      - [x] Ego                    Activación de propulsores
      - [x] Asgard                 Inmunidad a la siguiente anomalia espacial
      - [x] Xandar                 Avanza a la estación espacial más cercana ubicada en la diagonal principal del mapa
    - [x] Obstáculos espaciales:
        Anomalía                   Consecuencia
      - [x] Escombros espaciales   Retrocede un sector
      - [x] Meteoritos             Sin avance
      - [x] Impacto de asteroide   Pérdida de 3 unidades de energía
      - [x] Radiación cósmica      Pérdida de 2 unidad de energía
      - [x] Radiación solar        Retrocede al sector espacial mas cercano ubicado en la diagonal secundaria del mapa
  - [x] Los sectores que contendrán los estaciones espaciales o anomalías espaciales deben ser escogidas por el sistema de forma aleatoria, según el dificultad del juego (Básico, Medio o Avanzado).

- [ ] Otros requerimientos:
  - [-] Antes del juego, los equipos deben registrarse (si no lo están) y elegir el sentido del recorrido (horario o antihorario), asignar las unidades de energía iniciales para cada nave y seleccionar el nivel de dificultad del viaje (básico, medio, avanzado).
  - [x] Registrar en un archivo llamado EXPEDICIONES ESPACIALES, los datos básicos del viaje, entre los cuales están : el identificador de la expedición(código único que identificará el viaje), los nombre de los equipos que lo realizan, las unidades de energías asignadas inicialmente, el nivel de dificultad de la expedición, el sentido del recorrido del mapa (horario o antihorario) y la fecha de la expedición.
  - [x] Durante el juego, se mostrará la información de los equipos o naves espaciales (nombre y ODS asociado), el resultado de cada "activación de propulsores", así como las unidades de energía que le van quedando disponibles a cada equipo.
  - [x] Durante todo el juego, se debe presentar, a modo de espónsor, las imágenes de ODS y acciones alusivos a cada uno de estos, durante cada desplazamiento de las naves.
  - [x] Durante el viaje, se debe ir almacenando, en un archivo que pudiera llamarse DETALLE DE VIAJE, los movimientos realizado por cada uno de las naves y los eventos ocurridos durante el viaje. Almacenando entre otros datos: el Código del viaje, Nombre del Equipo, Fecha y Hora de la actividad, Unidades de Propulsión, Tipo de ayuda u obstáculo encontrado, la consecuencia generada, distancia en miles de kilómetros del sector en el que arriba la nave (este dato viene dado por el número consecutivo con el que se identifica cada sector).
  - [x] Identificar (con imágenes) en el mapa estelar, la existencia de alguna estación espacial o de alguna anomalía espacial.
  - [x] Proponer su propio diseño del mapa estelar, sean creativos.

- [ ] Reportes:
  - [ ] A partir de los datos almacenados en los archivos EQUIPOS, EXPEDICIONES ESPACIALES y DETALLE DE VIAJES , se pide :
  - [x] a) Dado el identificador de un país en particular, presentar por pantalla el mayor recorrido alcanzado por alguna de sus naves, así mismo mostrar el detalle de las expediciones donde se lograron estos recorridos. Para ello utilizar un método de búsqueda binario.
  - [x] b) Elaborar un reporte, que muestre los datos básicos de un equipo en particular, dado su identificador y que muestre las expediciones en los que ha participado y la cantidad de kilometrajes obtenidos. Utilice alguno de los métodos de búsqueda.
  - [ ] c) Hacer un reporte que muestre el TOP 10, de las expediciones con mayor kilometraje recorrido, presentando el identificador del viaje, el nombre del equipo que lo hizo, el pais de procedencia y total de kilómetros recorrido, para ello utilizar el método de ordenamiento Quicksort

- [ ] Algunas recomendaciones para la construcción de la aplicación:
  - [x] Utilizar menú intuitivo que permita acceder a cada una de las opciones que ofrece el sistema, para la realización de un juego.
  - [-] Desarrollar la aplicación en el lenguaje Python. No todas las funcionalidades están permitidas. Estas deben ser consultadas con el profesor. Por ejemplo, NO está permitido usar funciones de búsqueda y ordenamiento provista por el lenguaje, sino que generen sus propios algoritmos de búsquedas y ordenamientos, así mismo el manejo de exploración de cadenas.
  - [x] Puede utilizar cualquier desarrollador de interfaz compatible con Python, que le permita la construcción de una interfaz amigable, intuitiva y atractiva para los jugadores. Sea creativo.
  - [x] No olvidar incorporar los elementos de ODS, solicitados.

- [ ] Ideas nosotros:
  - [x] Mensaje de consecuencia al caer en obstaculo/estación
  - [x] Renderizar nombre de obstaculo/estación
  - [x] Poner de color las naves de cada equipo
  - [ ] Hacer clickable los botones del menú de juego
  - [ ] Programar Endgame
  - [ ] ...
