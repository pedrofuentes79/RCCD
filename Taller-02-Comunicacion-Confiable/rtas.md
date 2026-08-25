# Ejercicio 2.1
tux.bmp se transmite "con exito". Pero el tamaño del archivo no es el mismo. 330k vs 333k (el original). Por eso no se puede abrir correctamente. Lo que falla es que de manera aleatoria se simula una falla en la cual se pierde el frame, y este no se guarda en el archivo de salida. Por lo tanto, queda incompleto. Parece que la falta de un paquete implica corrupción total del archivo. 
Una vez que se pasa "--loss 0", el archivo se transmite correctamente.

# Ejercicio 2.2.d
Para que esto ande hay que tener un RTT acotado, y el timeout debe estar por encima de ese RTT.

