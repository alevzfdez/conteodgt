# README #

Aplicación web como demostrador desarrollada para el proyecto: "Conteo Preciso de Vehículos párrafo Situaciones de alta congestión en imágenes de videovigilancia de tráfico" realizado por el grupo de investigación GRAM ubicado en la Universidad de Alcalá en colaboración con la dirección general de tráfico (DGT).

Aplicación desarrollada en base a flask (python web application framework), mysql.

### Pasos para instalar ###

* Descarga
* Instalación

### Descarga ###

Antes de nada accede [aquí](http://roadanalysis.uah.es/dgt/downloads/gramWebApp.tar.gz) para descargarlo.

A continuación descomprimelo:

   * Dirigete a tu carpeta de descargas.
   * Descomprimelo,
        
        tar xvf gramWebApp.tar.gz

### Instalación ###

   * Ejecuta el instalador contenido en la carpeta gramWebApp.

        cd gramWebApp
        
        sudo chmod 755 installer && ./installer

Cuando te pregunte acerca del direcorio de instalación, escribe la ruta donde quieres que sea instalado.

Por último, se te pregunta por un usuario y contraseña que se crea para el acceso a la página web, NOT LO OLVIDES.

### Configuracion bases de datos ###

Si no quiere crear las tablas necesarias a mano siga estos pasos.

	* Cree 2 tablas en una base de datos existente, si no dispone de una creela.
	* Ejecute el configurador.

		sudo chmod 755 install_conf && ./install_conf


### Ya está! ###

Para arrancar la aplicación tienes dos opciones,
  
   * Puedes ejecutar el comando ```sudo initctl start gramWebApp``` como un servicio cualquiera.
   * Otra opción, ya que se iniciará en el arranque, es reiniciar el ordenador.