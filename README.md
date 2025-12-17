# 1. Introduccion

"Asyncio" es una libreria para escribir codigo concurrente usando la sintaxis `async/await`.

La API de "asyncio" es compleja porque trata de resolver dos problemas para dos grupos de personas distintas:
1. Desarrolladores finales: estos usuarios hacen aplicaciones que necesitan ejecutar tareas de manera concurrente.
2. Desarrolladores de "frameworks": estos usuarios crean "frameworks" y librerias para otros usuarios finales.
Uno de los problemas que hay al comenzar a usar "asyncio" es que esta diferencia no se presenta claramente en la documentacion. La documentacion oficial esta mas orientada al segundo grupo y si estas en el primer grupo tienes una tarea muy grande de rebuscar en la documentacion o en tutoriales la informacion que te es relevante.

La pieza mas importante de esta libreria es el "event loop". De forma simplificada es un elemento que ejecuta un conjunto de tareas y que son capaces de soltar el control de vuelta al "event loop" cuando es necesario y no bloquear el flujo de otras tareas.

El "event loop" contiene una coleccion de tareas que ejecutar. Algunas de estas tareas las creamos nosotros y otras son creadas indirectamente por `asyncio`. El bucle coge una tarea y la ejecuta hasta el momento en el que la tarea notifica que se pausa o se completa, momento en el que devuelve el control al bucle. Entonces el bucle selecciona otra tarea de la cola y la ejecuta. Este proceso se ejecuta de manera indefinida y si no quedan tareas en la cola el bucle es inteligente y descansa para no hacer un uso ineficiente de los recursos.
# 2. Toma de contacto
Vamos a realizar un ejemplo simple que realice lo siguiente:
1. Arrancar el "event loop".
2. Utilizar las palabras reservadas "async/await".
3. Crear una "task" para ejecutar en el bucle de eventos.
4. Esperar a que la tarea termine.
5. Cerrar el bucle de eventos cuando todas las tareas han terminado.

Primero utilizando las funciones de bajo nivel:

```
# quickstart.py
import asyncio
import time

async def main():
	print(f"{time.ctime()} Hello!")
	await asyncio.sleep(1.0)
	print(f"{time.ctime()} Goodbye!")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
task = loop.create_task(main())
loop.run_until_complete(task)
pending = asyncio.all_tasks(loop=loop)
for task in pending:
	task.cancel()
loop.close()
```

1. `asyncio.new_event_loop()` instancia el bucle de eventos, como `Singleton` lo asignamos a `asyncio`.
2. `task = loop.create_task(main())` toma como argumento un `Coroutine` y devuelve un `Task`.
3. `loop.run_until_complete(task)` bloquea el hilo hasta que la `Coroutine` del argumento se termina. Ademas cualquier otra tarea que estaba programada en el bucle seguira ejecutandose.
4. `loop.close()` un bucle "closed" ya no se puede utilizar de nuevo, es la ultima accion que se invoca al utilizar un bucle de eventos. Antes de cerrarlo nos aseguramos de cancelar todas las tareas para evitar dejar recursos pendientes en memoria o comportamientos inesperados. Por ejemplo podria haber tareas periodicas o tareas que han introducido en el bucle otras tareas.

Podemos simplificar el ejemplo usando las funciones de alto nivel como `run(...)`:

```
# quickstart.py
import asyncio, time

async def main():
	print(f'{time.ctime()} Hello!')
	await asyncio.sleep(1.0)
	print(f'{time.ctime()} Goodbye!')

asyncio.run(main())
```

Ahora vemos un ejemplo un poco mas complejo:
```
# quickstart_exe.py
import time
import asyncio

async def first_use_case():
	print(f'{time.ctime()} Hello!')
	await asyncio.sleep(1.0)
	print(f'{time.ctime()} Goodbye!')

def second_use_case():
	time.sleep(0.5)
	print(f"{time.ctime()} Hello from a thread!")

loop = asyncio.get_event_loop()
task = loop.create_task(first_use_case())

loop.run_in_executor(None, second_use_case)
loop.run_until_complete(task)

pending = asyncio.all_tasks(loop=loop)
for task in pending:
	task.cancel()
group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.close()
```
Explicamos las partes mas importantes del codigo:
1. `second_use_case()` es una funcion que bloquea el proceso, si la llamamos en cualquier parte de nuestro "script" se va a bloquear la ejecucion durante los 0.5 segundos que dura. Para solucionar este problema lo ejecutamos en un `executor` paralelo.
2. `loop.run_in_executor(None, second_use_case)` es una de las funciones basicas que conocer y sirve para ejecutar cualquier funcion que vaya a bloquear nuestra ejecucion. Se utiliza un "executor" por defecto y va a empezar a ejecutarse despues de una llamada a `run_until_complete()`, que dispara el bucle de eventos a comenzar a procesar tareas.
3. La lista de tareas de `pending` no incluye ninguna funcion introducida en `run_in_executor()`. Si revisamos los tipos, `run_in_executor()` devuelve un `Future` en lugar de un `Task`.
# 3. Corrutinas
## 3.1 Palabra reservada async

Nos paramos un momento para entender la diferencia entre una funcion asincrona y una corrutina:
```
>>> async def foo():
...     await asyncio.sleep(5)
... 
>>> foo
<function foo at 0x7ab91df7cae0>
>>> a = foo()
>>> a
<coroutine object foo at 0x7ab91dc09840>
```

La corrutina es el resultado de llamar a la funcion asincrona.
## 3.2 Palabra reservada await
Esta palabra reservada necesita de un parametro a la derecha que debe ser lo que se define como `awaitable`. Esto significa una de estas dos cosas:
1. Una corrutina.
2. Un objeto que implementa el metodo `__await__()` y que debe devolver un `iterator`.

Un ejemplo del segundo caso:
```
import asyncio


class MyClass:
    def __await__(self):
        for i in range(3):
            yield from asyncio.sleep(i).__await__()
        return self

async def main():
    r = await MyClass()
    print(r)
    return r

asyncio.run(main())
```
Repasamos:
1. `__await__()` debe devolver un iterador de objetos del tipo que "asyncio" considera correctos. En caso de no serlo lanza `RuntimeError`.
2. Solo se puede usar `await` dentro de una function `async`, en caso contrario el interprete lanza un `SyntaxError: 'await' outside function`.
# 4. Event Loop
En la mayoria de las situaciones un desarrollador no va a necesitar interactuar directamente con el bucle de eventos. El codigo asincrono se puede gestionar usando las palabras reservadas de `await` y `async` y todo ello sumado a una invocacion de `asyncio.run(coro)`. No obstante hay algunas ocasiones en las que puede resultar util tener acceso al bucle y hacer alguna llamada sobre el.
```
import asyncio

async def f():
    loop_1 = asyncio.get_running_loop()
    loop_2 = asyncio.get_running_loop()
    print(loop_1 is loop_2)

asyncio.run(f())
```
Este ejemplo demuestra que dentro de una corrutina la instancia del bucle de eventos siempre va a ser la misma. No es necesario pasar de manera explicita el bucle como parametro a traves de las funciones. No obstante, si estas desarrollando un framework si es posible que quieras que tus funciones tengan el bucle parametrizado.

Existe el metodo `asyncio.get_event_loop()` pero se diferencia del anterior en que solo funciona en un mismo hilo y va a fallar si se invoca en un hilo en el que no se ha configurado correctamente la instancia del bucle de enventos. En cualquier caso este metodo no es la forma recomendada para obtener la instancia del bucle de eventos. `asyncio.get_running_loop()` siempre va a funcionar dentro del contexto de una corrutina, tarea o funcion asincrona.

Ademas la introduccion de `asyncio.get_running_loop()` ha simplificado la creacion de tareas dentro de otra tarea.
```
import asyncio

async def foo():
    print("foo started")
    await asyncio.sleep(3)
    print("foo resumed")

async def old_way():
    loop = asyncio.get_running_loop()
    for i in range(3):
        loop.create_task(foo())

async def new_way():
    for i in range(3):
        asyncio.create_task(foo())


async def main():
    await new_way()
    await old_way()
    await asyncio.sleep(4)

asyncio.run(main())
```

Tener en cuenta que `asyncio.run()` espera a que la corrutina que el has pasado termine, pero no sabe esperar las tareas que se han creado dentro de otras corrutinas a no ser que esas sean `awaited` explicitamente.

# 5. Tasks/Futures
## 5.1 Entendiendo Future
En el dia a dia la clase que mas se va a usar es `Task`, pero es util conocer la otra clase `Future` que es una "superclase" de `Task`.

`Future` pretende representar el estado de algo que esta interactuando con el bucle de eventos. Cuando un objeto de esa clase es creado tiene un estado de "no completado aun" y en algun momento en el futuro el estado terminara siendo "completado". De hecho existe el metodo `done()` para comprobar su estado.

```
from asyncio import Future
f = Future()
f.done()
```

Ejemplo de interaccion con la clase `Future`:

```
import asyncio

async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    f.set_result("Hello world")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

fut: asyncio.Future = asyncio.Future()
print(fut.done())

loop.create_task(main(fut))
loop.run_until_complete(fut)
print(fut.done())
print(fut.result())

loop.close()
```

1. Creamos una funcion asincrona. Dentro de la misma establecemos el resultado del `Future`.
2. Instanciamos manualmente un `Future`. Esta instancia esta por defecto vinculada a nuestro bucle de eventos. Pero no esta vinculada a ninguna tarea ni corrutina de forma automatica.
3. Antes de nada verificamos que el futuro no esta completado.
4. Creamos la tarea en nuestro bucle.
5. Ejecutamos el bucle con `run_until_complete` pero ahora le hemos pasado como argumento un `Future`, que es algo distinto a lo que hemos ido haciendo en los ejemplos anterioes.
6. Finalmente el bucle termina de ejecutarse al terminar con el futuro y pintamos los resultados.

Este ejemplo es poco realista porque en la practica se trabaja con instancias de tareas pero como ejemplo educativo es interesante. Si no envolvemos el futuro en una tarea con `main(fut)` la corrutina `main` nunca se iba a ejecutar. El futuro iba a quedarse pendiente indefinidamente, el futuro es simplemente el contenedor de un resultado.

## 5.2 Semejanzas con Node.js
Tanto en `asyncio.Future` como en las Promesa de Node.js, la idea de estas clases es representar el resultado eventual de una operacion asincrona. 
1. Ambas clases tienen tres estados: `pending`, `fulfilled`, `rejected`.
2. Es posible encadenar objetos de estas clases entre ellos: 
	1. `asyncio.gather`, `add_done_callback`
	2. `.then()`, `.catch()`, `.finally()`
3. Ambas clases no bloquean el bucle de eventos.
4. `asyncio.Future` es una clase de bajo nivel, en el codigo de un desarrollador normal se trabajara con corrutinas y sintaxis `await`, abstrayendonos de `Future`. En Node.js las Promesas son la forma estandar de gestionar las operaciones asincronas.
# 6. Context managers
El uso de contextos para tareas asincronas con `asyncio` resulta muy util y sencillo. Para el caso [normal, sincrono](https://book.pythontips.com/en/latest/context_managers.html) tenemos el siguiente ejemplo:
```
class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, traceback):
        self.file_obj.close()
```
Lo importante es que la clase que usa el contexto implemente una serie de metodos `__enter__`, `__exit__`, etc.

El caso asincrono es analogo:
```
class Connection:
	def __init__(self, host, port):
		self.host = host
		self.port = port
	async def __aenter__(self):
		self.conn = await get_conn(self.host, self.port)
		return conn
	async def __aexit__(self, exc_type, exc, tb):
		await self.conn.close()

async with Connection('localhost', 9001) as conn:
	pass
```
Existe la libreria de `contextlib` que nos ayuda con la gestion de contextos, de forma que a traves de decoradores nos ahorramos escribir clases con `__enter__` y `__exit__` o sus versiones asincronas. El siguiente ejemplo es muy sencillo pero podemos imaginar que para descargar una web necesitariamos una clase que realizara una peticion HTTP, descargara el contenido de la web en memoria o en persistencia y luego limpiara aquellos recursos que no son necesarios, devolviendo la informacion de la web como `str`.

```
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def web_page(url):
    await asyncio.sleep(1)
    data = f"Hello world: {url}"
    yield data

async def main():
    async with web_page('google.com') as data:
        print(data)

asyncio.run(main())
```
Con el contexto de `web_page` nuestra corrutina se abstrae de la gestion de obtener los datos de la web y gracias a `contextlib` el desarrollador se ahorra escribir "boilerplate" repetitivo.
# 7. Iterators y Generators
## 7.1 Async Iterators
En Python se define un iterador (sincrono) como un objeto que implementa `__iter__()` y `__next__()`.
```
class A:
    def __init__(self):
        print("__init__ called")

    def __iter__(self):
        print("__iter__ called")
        self.n = 0
        return self

    def __next__(self):
        if self.n < 3:
            self.n += 1
            return self.n
        else:
            raise StopIteration

for i in A():
    print(f"Loop iteration: {i}")
```
Para definir un iterador asincrono hay que seguir un estandar analogo:
1. Implementar `__aiter__()`. No tiene que ser un metodo asincrono. Debe devolver un objeto que implemente `__anext__()`. 
2. El metodo `__anext__()` debe devolver un valor para cada iteracion y devolver `StopAsyncIteration` al terminar.

En el siguiente ejemplo aprovechamos un objeto iterable con `iter()` para nuestra operacion asincrona. Cuando se llega al final de los elementos de `self.ikeys` se gestiona la excepcion de `StopIteration` para convertirla en un `StopAsyncIteration`.
```
import asyncio


class OneAtATime:
    def __init__(self, keys):
        self.keys = keys
    def __aiter__(self):
        self.ikeys = iter(self.keys)
        return self
    async def __anext__(self):
        try:
            await asyncio.sleep(1)
            return next(self.ikeys)
        except StopIteration:
            raise StopAsyncIteration
        

async def main():
    keys = ['Americas', 'Africa', 'Europe', 'Asia']
    async for it in OneAtATime(keys):
        print(it)

asyncio.run(main())
```
Se puede simplificar este codigo un poco mas gracias a la palabra reservada `yield`, aprovechando los generadores.
## 7.2. Async Generators
Estos generadores son funciones asincronas que usan `yield` para devolver valores.
- Las corrutinas y los generadores son conceptos separados.
- Los generadores asincronos siguen la misma logica que sus homologos sincronos pero tienen la peculiaridad de usar la sintaxis `async for`.
Se va a repetir el ejemplo anterior usando este concepto:
```
import asyncio
from typing import AsyncGenerator


async def one_at_a_time(keys: list[str]) -> AsyncGenerator[str]:
    for k in keys:
        await asyncio.sleep(1)
        yield k

async def main():
    keys = ['Americas', 'Africa', 'Europe', 'Asia']
    async for it in one_at_a_time(keys):
        print(it)

asyncio.run(main())
```
Aprovechando el tipado que proporciona Python para dar un poco mas de claridad:
- `one_at_a_time` es una funcion asincrona que devuelve un generador asincrono de `str`.
- `yield` ahorra escribir una clase con `__aiter__()` y `__anext__()`.
- `async for` permite parar la iteracion mientras espera a que el siguiente elemento del generador este disponible. Esto permite devolver el control al bucle de eventos y habilitar la concurrencia.


# Referencias
1. [Using asyncio in Python.](https://www.oreilly.com/library/view/using-asyncio-in/9781492075325/)
2. [# Yury Selivanov - async/await in Python 3.5 and why it is awesome](https://www.youtube.com/watch?v=m28fiN9y_r8)
3. [PEP-492](https://peps.python.org/pep-0492/)
