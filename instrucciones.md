Universidad del Valle de Guatemala  
Facultad de Ingeniería  
Departamento de Ciencias de la Computación  
CC3089 Base de Datos 2  
Semestre I 2026  
- 1/2 -

Laboratorio No. 4  
MongoDB Charts - GRUPOS DE PROYECTO

I. Modalidad y fecha de entrega

a) El laboratorio debe hacerse en los grupos elaborados para la entrega del Proyecto 01  
b) Debe ser enviado antes de la fecha límite de entrega: Domingo 22 de Febrero a las 23:59 horas a más tardar  
c) Luego de la fecha y hora límites se restará 10 puntos por cada hora de atraso en la entrega  

II. Objetivo y descripción de la actividad

Esta actividad tiene como propósito principal familiarizar a los estudiantes con el entorno de MongoDB Charts, y con herramientas asociadas a tareas de inteligencia de negocios. Se presenta una arquitectura de un caso típico (real) con el objetivo de que los grupos de proyecto puedan replicarlo de manera sencilla pero considerando todos los elementos de dicha arquitectura.

EJERCICIO 02 – MongoDB Charts

En los mismos grupos de proyectos, deberá implementar la arquitectura a continuación utilizando librerías que implementan MongoDB y tengan una integración con una instancia de Atlas propia del grupo, en donde deberá realizar gráficas usando MongoDB Charts. Su desarrollo deberá integrar datos crudos fuentes (archivo .csv) y apoyándose de librerías de python + mongo deberá integrar esta información sobre Atlas.

Finalmente, deberá de construir 3 gráficos y 2 KPIs sobre un dashboard que permita sacar conclusiones sobre la información utilizada.

Consideraciones Importantes

En cuanto a los datos a utilizar, no hay ninguna restricción y hay completa libertad de que el grupo utilice lo mejor que el grupo considere. La única restricción es que sean archivos en formato .csv (especificado como archivos raw en el diagrama anterior). Puede tomar incluso, los mismos datos que está utilizando para su proyecto (o al menos una muestra) si es que cumple la restricción previa. No será necesario cumplir con un

- 2/2 -

mínimo/máximo de colecciones, la idea es que el dashboard que construyan permita sacar conclusiones que refleje coherentemente el negocio que está modelando.

En cuanto al dashboard, se recomienda pensar en el negocio: en cómo se pueden sacar datos estadísticos interesantes según la naturaleza de los datos que estarán utilizando. La calidad y criterio para estas gráficas que estarán construyendo será un criterio importante en su evaluación.

Recuerden colocar gráficas que hagan sentido para lo que están tratando de explicar, y que tengan nombres de ejes y demás detalles estéticos correctamente identificados, según visto en clase.

III. Temas a reforzar

- Operaciones Bulk
- Arquitecturas comúnes de MongoDB
- Agregaciones
- MongoDB Charts

IV. Documentos a entregar

1. Un video por grupo que contenga:

a. El detalle de todos los pasos realizados para la construcción e implementación de esta arquitectura. La idea es explicar cada componente y evidenciar lo que se hizo con todo el detalle posible. No hay un máximo de duración para el video, porque la idea es explicar el detalle de cada elemento de su arquitectura desplegada.

b. Tableros realizados en MongoDB Charts. Los tableros hacen sentido y son coherentes con la lógica de negocio modelada. Incluye KPIs y gráficas que están correctamente identificadas y se permiten entender fácilmente.

2. Scripts (*.js / *.py) debidamente documentado con lo utilizado para la conexión hacia Atlas (ingesta/bulkwrite) y cualquier otra lógica utilizada.

V. Evaluación

EJERCICIO 01

- Video con todo el detalle: 90 puntos (entrega de video con permisos a cualquier persona para poder visualizarlo)
- Tableros coherentes: Esto no tiene puntos como tal pero se podrá llegar a reducir hasta un 30% de la nota en caso no tengan sentido absoluto y sean gráficas que no se puedan interpretar/leer (que no sean intuitivas y que no expliquen nada).
- Scripts documentados: 10 puntos

Total: 100 puntos

VI. Referencias

1. MongoDB Charts: https://www.mongodb.com/docs/charts/
2. Conectividad Python/Atlas:
https://www.mongodb.com/languages/python#:~:text=The%20first%20step%20to%20connect,editor%2C%20like%20Visual%20Studio%20Code.
