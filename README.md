### Características

- Monitorea la ip de tu servidor de correo para enterarte si entras en una lista negra.
- Si detecta que la ip esta en alguna lista negra, notifica vía correo y telegram.

### Necesitas

+ Python3
    + dns.resolver
    + smtplib
    + requests

### Como funciona

En el código del script debes agregar la ip a monitorear y las listas a verificar (trae las mas utilizadas por defecto) Al ejecutar el script este verifica la ip contra las listas y si detecta que está en alguna lista negra te notificará vía correo y telegram (si realizas la ejecuición manual te notificará en pantalla).

### Como ejecutar

`python3 blacklist.sh`

### Ejecutar en producción

Se recomienda vía crontab

`0 * * * * python3 blacklist.sh`