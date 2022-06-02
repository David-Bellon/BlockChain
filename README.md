# BlockChain
Lio de tres pares de narices para probar que funciona:
Necesitas dos ordenadores distintos, en ambos te descargas el repositrio entero. En un ordenador ejecutas SOLO el archivo deploy.py lo cual va a hacer que te aparezca un archivo .csv que se llama ip_nodes.csv. NO PARES la ejecución del deploy.py nunca, sin parar nada coges el archivo ip_nodes.csv y te lo llevas al otro ordenador y lo metes en la misma carpeta que el rest de archivos.
Una vez que haces esto ejecutas el archivo interact.py y a funcionar.
Cuando estes ejecutando el archivo deploy.py en el otro ordenador saldran prints en la consola, esto es porque está activado el modo debugger y así ves las transacciones que hay y como se le conecta el otro dispositivo y demás.

En el interact.py cuando lo ejecutes te pide que te registres y pongas una contraseña, una vez que lo hagas accedes con dcha contraseña, no hay usuario porque los datos se almacenan en el propio ordenador. De hecho, cuando registres tu contraseña aparece un fichero .txt con datos hasheados que son tus datos para acceder.  
En la aplcación sale para votar, solo una vez, minar, que pone a minar pero solo hasta que mina un bloque y luego para y un explorador básico de transacciones, pinchas en cada transacción y a la derecha sale un desglose de los datos de dicha transacción.  
Solo se ha probado con dos dispositivos, en uno el deploy.py y en el otro el interact.py, supongo que si quieres probar con dos interact.py debería funcionar también, le pones al otro ordenador el archivo.csv y de la misma manera.
