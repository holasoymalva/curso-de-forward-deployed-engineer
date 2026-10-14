# 🎙️ Transcripción de llamada de descubrimiento inicial

**Fecha:** 14 de Octubre de 2026 · 10:00 AM  
**Participantes:**
- **Alex Morales** (Forward Deployed Engineer - Nexo)
- **Laura Garza** (Directora de Operaciones - Distribuidora Halcón)
- **Roberto Treviño** (Gerente de TI - Distribuidora Halcón)

---

**[00:00:15] Alex Morales:**  
Buenos días Laura, buenos días Roberto. Muchas gracias por su tiempo. El objetivo de esta llamada no es darles una presentación de diapositivas sobre Nexo, sino escucharlos: entender exactamente cómo opera hoy Distribuidora Halcón, dónde sienten las mayores fricciones en el día a día y acordar cómo vamos a conectar sus sistemas para que tengan visibilidad total de inventario sin generar trabajo extra para el equipo de TI. Laura, si te parece bien, ¿podrías contarnos qué pasó el fin de semana pasado con los faltantes de producto en Monterrey?

**[00:01:05] Laura Garza:**  
Hola Alex, gracias. Mira, te soy muy transparente: el fin de semana perdimos cerca de 80,000 pesos en ventas solo en el área metropolitana de Monterrey. Llegaron tres camiones a cargar aceite y azúcar a las 6:00 de la mañana para surtir a más de 40 tiendas abarroteras. En el sistema de pedidos aparecía que sí teníamos stock, pero físicamente las tarimas estaban vacías. Las tiendas se molestaron muchísimo y nos cancelaron las entregas. Mariana, nuestra analista, pasa horas consolidando datos en Excel cada mañana, pero para cuando termina a las 10:30 u 11:00 AM, las decisiones ya se tomaron a ciegas. Necesitamos alertas antes de que empiece el turno de las 6:00 AM.

**[00:02:30] Alex Morales:**  
Es clarísimo, Laura. Ese desface entre el dato del sistema y la realidad física es sumamente costoso. Roberto, pasando a la parte técnica, ¿dónde vive hoy la verdad del inventario y cómo llega la información a manos de Mariana?

**[00:03:00] Roberto Treviño:**  
A ver Alex, te pongo en contexto técnico. Nuestro ERP central es un sistema heredado montado en un servidor local Windows Server en nuestro centro de datos de Monterrey. Es un sistema muy viejo y delicado: no tiene APIs REST nativas ni documentación moderna. Lo que tenemos configurado es un trabajo automatizado que todas las noches, alrededor de las 3:00 AM, exporta una vista de la base a un archivo CSV llamado `inventario_erp.csv` y lo deposita en una carpeta compartida de red. A veces el archivo viene con caracteres extraños o duplicados porque el ERP maneja tablas históricas sin limpiar. Mariana abre ese archivo a mano y lo cruza con las hojas de pedidos.

**[00:04:15] Alex Morales:**  
Entendido. Roberto, una pregunta clave: ¿qué tan factible es que nosotros montemos un pequeño servicio en contenedor (Docker) dentro de esa misma red que lea ese CSV a las 3:15 AM de forma automática, sin que nadie tenga que abrirlo a mano?

**[00:04:40] Roberto Treviño:**  
Mmm... mira Alex, yo soy muy protector con la red corporativa. No quiero que me instalen librerías ni software desconocido en el servidor del ERP. Además, mi equipo de TI somos solo 3 personas: si su conector empieza a consumir el 100 % de la CPU o me satura el disco con logs, no tengo tiempo para estar apagando fuegos. Si corre encapsulado en Docker, con límites estrictos de recursos y solo permisos de lectura sobre la carpeta compartida, puedo autorizar una máquina virtual aislada en nuestra red de pruebas. Pero nada de tocar las bases de datos de producción directamente.

**[00:05:45] Alex Morales:**  
Totalmente de acuerdo, Roberto. Comparto al 100 % tu filosofía: mínimo privilegio, cero permisos de escritura sobre su ERP y límites de memoria estrictos (por ejemplo, máximo 256 MB de RAM). Nosotros escribiremos el script defensivo que limpia los formatos y detecta los errores del CSV sin tocar su base. Laura, una duda sobre la lógica de negocio: ¿cuál es el criterio exacto para que consideren que un producto está en "riesgo de quiebre"?

**[00:06:30] Laura Garza:**  
Generalmente compras define un `stock_minimo` por cada producto, que suele ser de 20 o 50 cajas dependiendo si es abarrotes o limpieza. Si la cantidad física amanece por debajo de ese stock mínimo, los supervisores de almacén deben recibir una alerta inmediata en rojo para no comprometer pedidos de ese día y generar la orden de reabastecimiento al proveedor de inmediato.

**[00:07:20] Alex Morales:**  
Excelente. Y para las órdenes de pedidos nuevas, ¿cómo se comunican con los almacenes de Guadalajara y CDMX?

**[00:07:40] Roberto Treviño:**  
Para pedidos sí tenemos una API interna HTTP que montamos el año pasado. Es una API REST básica que requiere autenticación con token Bearer. Esa API sí soporta crear pedidos y listar pedidos pendientes. Te puedo entregar credenciales de prueba con gusto.

**[00:08:15] Alex Morales:**  
Perfecto. Con esto tenemos un panorama muy claro. Nuestro plan para la Fase 1 será:
1. Conectar nuestro conector en contenedor al CSV nocturno de las 3:15 AM.
2. Limpiar y validar las anomalías de los 3 almacenes (MTY, GDL, CDMX).
3. Publicar las alertas de stock bajo en el tablero de Nexo a las 4:00 AM para que Laura y Mariana las tengan listas antes del turno de las 6:00 AM.
4. Consultar los pedidos pendientes a través de su API interna.
¿Quedamos de acuerdo en que temas como facturación fiscal o aplicaciones para choferes quedan fuera de esta primera fase para asegurar salir a producción en 4 semanas?

**[00:09:10] Laura Garza:**  
100 % de acuerdo, Alex. Si resolvemos el inventario y las alertas para Monterrey antes de fin de mes, Don Javier y yo estaremos más que satisfechos.

**[00:09:30] Roberto Treviño:**  
Me parece un enfoque sensato y prudente. Te envío las credenciales de prueba de la API hoy por la tarde.

**[00:09:45] Alex Morales:**  
Muchísimas gracias a ambos. Les redacto el documento de alcance (SOW) y se los comparto hoy mismo para formalizar el inicio. ¡Excelente día!
