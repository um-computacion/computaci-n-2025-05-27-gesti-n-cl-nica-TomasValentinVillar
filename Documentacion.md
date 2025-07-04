## Ejecucion del sistema
Para ejecutar el sistema se hace desde la interfaz CLI, la interfaz se ejecuta de la siguiente manera:

```text
python -m interfaz.cli
```

## Ejecucion de los test
Para ejecutar todos los tests de la siguiente manera:

```text
python -m unittest
```

## Explicación del diseño general

El sistema está separado en 3 carpetas, interfaz donde se encuentra la interfaz por consola (CLI), src donde los archivos de las clases y tests donde están los test unitarios.

Las clases Paciente, Medico, Especialidad, Turno, Recta e Historia Clinica tienen cada una sus atributos correspondientes y su representación, algunas tiene metodos para registro de datos como Historia Clinica con agregar receta y agregar turno, tambien hay metodos para para el acceso a la información como obtener dni en Paciente y obtener matricula en Medico, he agregado algunos metodos para acceder a la información como obtener especialidad turno y obtener paciente en la clase Turno.

En la clase principal CLinica se encuentran todos los metodos para registrar la informacion de los pacientes, medicos, especialidades, turnos, recetas e historia clinica. También hay metodos que devuelven a un objeto especifico de los atributos diccionario de clinica como get_paciente o obtenr_medico_por_matricula (que devuelven a un objeto especifico segun el dni o matricula ingresado), en dichos metodos si se ingresa un dni o matricula que no existe se lanzará una excepción de que no existe el paciente o medico. También se encuantran las validaciones que verificaran la existencia de los registros, que no se hayan ingresado datos vacios, el formato de las fechas y dni, las especialidades y disponibilidad del medico, entre otros. He agragado algunas validaciones ademas de las pedidas en el README como validar epecialidad que verifica que el medico no tenga la especialidad que se quiere agregar y verifica que no se ingresen datos vacios.

En la interfaz se llamarán los metodos de clinica para registrar información como agregar_paciente, agregar_medico, agendar_turno, emitir_recta o agregar_especialidad y podrá mostrar todos los pacientes y medicos registardos, las histotias clinicas de los pacientes y todos los turnos registrados. También la interfaz llamara los metodos de validaciones antes de registrar la información para para que Clinica pueda detectar los posibles errores como registrar un medico o paciente ya existente, ingresar formatos de fecha o dni invalidaos, duplicar especialidades, registrar datos vacios, agendar turnos o emitir recetas con medicos o pacientes no existentes, evitar turnos duplicados, etc. Todos estos posibles casos pricipales para registrar correctamente los datos ingresados por consola y mostrar por consola los mensajes ante posibles errores son testeados en en tests_cli.py que son los casos mencionados en el apartado Unit Testing de la consigna.

En la carpeta de tests se encuentan también los archivos que testetan el correcto funcionamiento de todos los métodos (incluyendo las excepciones personalizadas que se lanzan en Clinica) de las clases. 
