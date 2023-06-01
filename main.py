import json
import requests
import calendar
from datetime import datetime
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
from kivy.config import Config
from matplotlib.pylab import plt
from matplotlib.pyplot import plot, ylabel, xlabel, gcf
from pyrebase import pyrebase

Config.set('kivy', 'exit_on_escape', '0')

'''
[OBJETO]
firebaseConfig

[INFO]
este objeto posee todas las credenciales para
conectarse a firebase

'''

firebaseConfig = {
  'apiKey': "AIzaSyDIat2CC75pdR06-wLwCldLbOBh4CkvekU",
  'authDomain': "spimanager-ac17e.firebaseapp.com",
  'databaseURL': "https://spimanager-ac17e-default-rtdb.firebaseio.com",
  'projectId': "spimanager-ac17e",
  'storageBucket': "spimanager-ac17e.appspot.com",
  'messagingSenderId': "526909123263",
  'appId': "1:526909123263:web:0b32cbbf1a42e14567740a",
  'measurementId': "G-XSZPE7GEWM"
}

_initfirebase = pyrebase.initialize_app(firebaseConfig)
_authfirebase = _initfirebase.auth()

'''
[CLASE]
FirestoreHandling()

[PARAMETROS]
uid -> uuid del usuario logeado

[INFO]
esta clase permite conectarnos a firestores y
obtener las colecciones necesarias segun el id
del usuario
'''
class FirestoreHandling():
    uid = ''
    project_id = firebaseConfig['projectId']
    coleccionOrdenes = 'Ordenes'
    coleccionPlatillos = 'Platillos'
    coleccionBebidas = 'Bebidas'
    coleccionRestaurante = 'Restaurante'
    urlordenes = f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{coleccionOrdenes}'
    urlplatillos = f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{coleccionPlatillos}'
    urlRestaurante = f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{coleccionRestaurante}'
    urlBebidas = f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{coleccionBebidas}'

    data = []
    ordenesValores = []
    bebidasValores = []
    platillosValores = []
    restauranteValores = []

    def getData(self):
        self.resOrdenes = requests.get(self.urlordenes)
        self.resPlatillos = requests.get(self.urlplatillos)
        self.resRestaurante = requests.get(self.urlRestaurante)
        self.resBebidas = requests.get(self.urlBebidas)

        if self.resOrdenes.status_code == 200 and self.resPlatillos.status_code == 200 and self.resRestaurante.status_code == 200 and self.resBebidas.status_code == 200:
            dataOrdenes = self.resOrdenes.json()
            dataPlatillos = self.resPlatillos.json()
            dataRestaurante = self.resRestaurante.json()
            dataBebidas = self.resBebidas.json()

            print("[INFO]: colecion ORDENES")
            for doc in dataOrdenes.get('documents', []):
                #document_id = doc.get('name').split('/')[-1]
                idDueno_dic = doc.get('fields',{}).get('idDueño') 
                fecha_dic = doc.get('fields',{}).get('fecha')
                platillos_array = doc.get('fields',{}).get('platillo')
                precioPagar_dic = doc.get('fields',{}).get('precioPagar')

                platillosValues = []

                if idDueno_dic is None:
                    pass
                elif precioPagar_dic is None:
                    pass
                elif fecha_dic is None:
                    pass
                elif platillos_array is None:
                    pass
                else:
                    idDuenoValue = idDueno_dic.get('stringValue')
                    print(f'idDueno: {idDueno_dic}')
                    print(f'uid: {self.uid}')

                    if idDuenoValue == self.uid:
                        precioPagarValue = int(precioPagar_dic.get('integerValue'))
                        fechaNativa = fecha_dic.get('timestampValue')
                        fechaValue = datetime.strptime(fechaNativa, '%Y-%m-%dT%H:%M:%S.%fZ')

                        platillos_array_values = platillos_array['arrayValue'].get('values',[])

                        for value in platillos_array_values:
                            platillos_map_values = value.get('mapValue',{})
                            platillos_native_values = platillos_map_values['fields']

                            precios = float(platillos_native_values.get('precioPlato').get('stringValue'))

                            platillosValues.append(precios)

                        print(platillosValues)
                        self.ordenesValores += [precioPagarValue,fechaValue,platillosValues]
            
            print("\n")
            print("[INFO]: colecion BEBIDAS")
            for doc in dataBebidas.get('documents',[]):
                idDueno_dic = doc.get('fields',{}).get('idDueño')
                bebida_dic = doc.get('fields',{}).get('platillo')
                precio_dic = doc.get('fields',{}).get('precio')
                contadorVentas_dic = doc.get('fields',{}).get('contadorVenta')

                if idDueno_dic is None:
                    pass
                elif bebida_dic is None:
                    pass
                elif precio_dic is None:
                    pass
                elif contadorVentas_dic is None:
                    pass
                else:
                    idDuenoValue = idDueno_dic.get('stringValue')
                    print(f"idDueño: {idDuenoValue}")
                    print(f'uid: {self.uid}')
                    
                    if idDuenoValue == self.uid:
                        bebidaValue = bebida_dic.get('stringValue')
                        precioValue = float(precio_dic.get('stringValue'))
                        contadorVentasValue = int(contadorVentas_dic.get('integerValue'))

                        print(f'bebida: {bebidaValue}')
                        print(f'precio: {precioValue}')
                        print(f'contadorVenta: {contadorVentasValue}')

                        self.bebidasValores += [bebidaValue,precioValue,contadorVentasValue]

            print("\n")
            print("[INFO]: colecion PLATILLOS")
            for doc in dataPlatillos.get('documents',[]):
                idDueno_dic = doc.get('fields',{}).get('idDueño')
                platillo_dic = doc.get('fields',{}).get('platillo')
                precio_dic = doc.get('fields',{}).get('precio')
                contadorVentas_dic = doc.get('fields',{}).get('contadorVenta')

                if idDueno_dic is None:
                    pass
                elif platillo_dic is None:
                    pass
                elif precio_dic is None:
                    pass
                elif contadorVentas_dic is None:
                    pass
                else:
                    idDuenoValue = idDueno_dic.get('stringValue')
                    print(f'idDueno: {idDuenoValue}')
                    print(f'uid: {self.uid}')

                    if idDuenoValue == self.uid:
                        platilloValue = platillo_dic.get('stringValue')
                        precioValue = float(precio_dic.get('stringValue'))
                        contadorVentasValue = int(contadorVentas_dic.get('integerValue'))

                        print(f'platillo: {platilloValue}')
                        print(f'precio: {precioValue}')
                        print(f'contadorVenta: {contadorVentasValue}')

                        self.platillosValores += [platilloValue, precioValue, contadorVentasValue]

            print("\n")
            print("[INFO]: colecion RESTAURANTE")
            for doc in dataRestaurante.get('documents', []):
                idDueno_dic = doc.get('fields',{}).get('idDueño')
                restaurante_dic = doc.get('fields',{}).get('nombre')

                if idDueno_dic is None:
                    pass
                elif restaurante_dic is None:
                    pass
                else:
                    idDuenoValue = idDueno_dic.get('stringValue')
                    nombre = restaurante_dic.get('stringValue')

                    if idDuenoValue == self.uid:
                        print(f'nombre: {nombre}')
                        self.restauranteValores += [nombre]

            self.data.append(self.ordenesValores)
            self.data.append(self.bebidasValores)
            self.data.append(self.platillosValores)
            self.data.append(self.restauranteValores)

            print(self.data)

        return self.data
'''
[CLASE]
errorFireBaseHandling

[PARAMETROS]
ninguno

[INFO]
esta clase permite retornar un mensaje
segun el error ocurrido

'''

class errorFirebaseHandling():
    msg = ''

    def __init__(self, msg):
        self.msg = msg

    def getMessageError(self):
        if(self.msg == 'INVALID_EMAIL'):

            _message = """ [INVALID_EMAIL]: El correo no coincide o esta mal escrito.\n
[FORMATO EJEMPLO]: example@email.com
            """

            return _message

        elif(self.msg == 'WEAK_PASSWORD : Password should be at least 6 characters'):

            _message = """
[WEAK_PASSWORD]: La contraseña es demasiado debil
[RECOMENDACIONES]:\n
    * Una longitud de 6 caracteres
    * Utilizar numeros y letras
    * Utilizar letras mayusculas y minusculas
    * Utilizar guiones (_) (-)
"""

            return _message
        elif self.msg == "EMAIL_EXISTS":

            _message="""
[EMAIL_EXISTS]: Este correo ya esta en uso
            """

            return _message

        elif self.msg == "INVALID_PASSWORD":

            _message= """
[INVALID_PASSWORD]: Contraseña incorrecta
            """

            return  _message

        else:
            _message = 'error desconocido'
            return _message

    pass

'''
[CLASE]
LoginScreen

[PARAMETROS]
Screen -> nombre del formulario

[INFO]
Esta clase permite iniciar sesion
a los usuarios

'''

class LoginScreen(Screen):
    main = None
    stats = None

    def __init__(self,**kw):
        super().__init__(**kw)
        self.db = FirestoreHandling()

    def btnLoginInputs(self):
        _NombreUsuario = self.ids['txtUsuario'].text
        _Contrasena = self.ids['txtContrasena'].text

        if not(_NombreUsuario and _Contrasena):
            self.dialog = MDDialog(
                title='Error al iniciar sesion',
                text='Rellenar todos los campos',
                buttons=[MDFlatButton(text='Cerrar', on_release=self.dialogClose)]
            )
            self.dialog.open()
        else:
            try:
                _usuario = _authfirebase.sign_in_with_email_and_password(_NombreUsuario, _Contrasena)

                self.ids['txtUsuario'].text = ''
                self.ids['txtContrasena'].text = ''
                
                self.db.uid = _usuario['localId']

                #obteniendo la data de su respectivo usuario
                self.data = self.db.getData()

                self.main.update(self.data)

                self.manager.current='main'

            except requests.exceptions.HTTPError as error:
                print(error)
                _errorJson = error.args[1]
                _errorCode = json.loads(_errorJson)['error']['message']
                _errorHandling = errorFirebaseHandling(_errorCode)
                _errorMessage = _errorHandling.getMessageError()
                self.dialog = MDDialog(
                    title='Error al iniciar session',
                    text=_errorMessage,
                    buttons=[MDFlatButton(text='cerrar',on_release=self.dialogClose)]
                )
                self.dialog.open()

                self.ids['txtUsuario'].text = ''
                self.ids['txtContrasena'].text = ''

        pass

    def dialogClose(self, obj):
        self.dialog.dismiss()
        pass

'''
[CLASE]
MainScreen

[PARAMETROS]
Screen -> nombre del formulario

[INFO]
Esta ventana va despues del login

'''

class MainScreen(Screen):

    def closeMessage(self, app):
        self.app = app
        self.dialogCloseLogin = \
            MDDialog(
                title='Cerrar Aplicacion',
                text='Desea cerrar sesion y salir de la aplicacion?',
                buttons=[
                    MDFlatButton(text='Cancelar', on_release=self.cancelLogin),
                    MDFlatButton(text='Aceptar', on_release=self.closeLogin)   
                ]
            )
        
        return self.dialogCloseLogin

    def cancelLogin(self, obj):
        self.dialogCloseLogin.dismiss()

    def closeLogin(self, obj):
        self.dialogCloseLogin.dismiss()
        _authfirebase.current_user = None
        self.app.stop()
    
    def btnDatosGeneralesInputs(self):
        if self.manager.current != 'main':
            self.manager.current = 'main'

    def btnEstadisticasInputs(self):
        if self.manager.current != 'stats':
            self.manager.current = 'stats'
            self.manager.stats.update(self.manager.login.data)
            
    def update(self, data):
        self.data = data

        ordenesArray = self.data[0]
        bebidasArray = self.data[1]
        platillosArray = self.data[2]
        restauranteNombre = self.data[3]

        dialogMessage = "No se pudo encontrar el contenido de las siguientes colecciones: "

        warningMessage = False

        if len(ordenesArray) == 0:
            warningMessage = True
            dialogMessage += "ordenes, "
            self.ids['lblVentasTotales'].text = 'Sin Datos'
        else:
            fechaActual = datetime.today()
            length = len(ordenesArray)
            montoTotal = 0

            for i in range(0,length,3):
                montoOrden = ordenesArray[i]
                fechaOrden = ordenesArray[i + 1]

                if fechaOrden.day == fechaActual.day and fechaOrden.month == fechaActual.month and fechaOrden.year == fechaActual.year:
                    montoTotal += montoOrden

            self.ids['lblVentasTotales'].text = f'Ventas Totales: ${montoTotal}'

        if len(bebidasArray) == 0:
            warningMessage = True
            dialogMessage += 'bebidas, '
            self.ids['lblBebida'].text = 'Sin Datos'
        else: 
            length = len(bebidasArray)
            bebidaMasVendida = ''
            mayor = 0
            primeraBebida = True

            for i in range(0,length,3):
                nombre = bebidasArray[i]
                contador = bebidasArray[i + 2]

                if contador > mayor:
                    bebidaMasVendida = ''
                    bebidaMasVendida = nombre
                    mayor = contador
                elif contador == mayor and not primeraBebida:
                    bebidaMasVendida += f', {nombre}'
                elif primeraBebida:
                    bebidaMasVendida += nombre

                primeraBebida = False
                
            self.ids['lblBebida'].text = bebidaMasVendida


        if len(platillosArray) == 0:
            warningMessage = True
            dialogMessage += 'platillos, '
            self.ids['lblPlatillo'].text = 'Sin Datos'
        else:
            length = len(platillosArray)
            platilloMasVendido = ''
            mayor = 0
            primerPlatillo = True

            for i in range(0,length,3):
                nombre = platillosArray[i]
                contador = platillosArray[i + 2]

                if contador > mayor:
                    platilloMasVendido = ''
                    platilloMasVendido = nombre
                    mayor = contador
                elif contador == mayor and not primerPlatillo:
                    platilloMasVendido += f', {nombre}'
                elif primerPlatillo:
                    platilloMasVendido += nombre

                primerPlatillo = False
                
            self.ids['lblPlatillo'].text = platilloMasVendido


        if len(restauranteNombre) == 0:
            warningMessage = True
            self.ids['lblTitulo'].text = 'Sin Nombre'
        else:
            self.ids['lblTitulo'].text = restauranteNombre[0]

        if warningMessage:
            self.dialog = MDDialog(
                title = 'Informacion no encontrada',
                text = dialogMessage,
                buttons = [
                    MDFlatButton(text='Cerrar', on_release=self.close)
                ]
            )
            self.dialog.open()

    def updateDay(self):
        ordenesArray = self.data[0]
        warningMessage = False
        montoTotal = 0

        dialogMessage = "No se pudo encontrar el contenido de las siguientes colecciones: "

        if len(ordenesArray) == 0:
            warningMessage = True
            dialogMessage += "ordenes, "
            self.ids['lblVentasTotales'].text = 'Sin Datos'
        else:
            fechaActual = datetime.today()
            length = len(ordenesArray)

            for i in range(0,length,3):
                montoOrden = ordenesArray[i]
                fechaOrden = ordenesArray[i + 1]

                if fechaOrden.day == fechaActual.day and fechaOrden.month == fechaActual.month and fechaOrden.year == fechaActual.year:
                    montoTotal += montoOrden

            self.ids['lblVentasTotales'].text = f'Ventas Totales: ${montoTotal}'
            
        if warningMessage:
            self.dialog = MDDialog(
                title = 'Informacion no encontrada',
                text = dialogMessage,
                buttons = [
                    MDFlatButton(text='Cerrar', on_release=self.close)
                ]
            )
            self.dialog.open()
 
    def updateWeek(self):
        ordenesArray = self.data[0]
        length = len(ordenesArray)
        dia_actual = datetime.today()
        calendario_actual = calendar.monthcalendar(dia_actual.year, dia_actual.month)
        calendario_siguiente = calendar.monthcalendar(dia_actual.year, dia_actual.month + 1)
        montoTotal = 0
        warningMessage = False

        dialogMessage = "No se pudo encontrar el contenido de las siguientes colecciones: "

        if len(ordenesArray) == 0:
            warningMessage = True
            dialogMessage += 'ordenes, '
            self.ids['lblVentasTotales'].text = 'Sin Datos'
        else:

            for semana_actual in calendario_actual:
                primer_dia = min(semana_actual)
                ultimo_dia = max(semana_actual)

                if primer_dia != 0:
                    for i in range(0,length,3):
                        montoOrden = ordenesArray[i]
                        fechaOrden = ordenesArray[i+1]

                        if fechaOrden.month == dia_actual.month and fechaOrden.day >= primer_dia and fechaOrden.day <= ultimo_dia:
                            montoTotal += montoOrden

                else:
                    semana_siguiente = calendario_siguiente[0]

                    for i in range(0, len(semana_siguiente)):
                        if semana_siguiente[i] == 0:
                            semana_siguiente[i] = semana_actual[i]

                    primer_dia_siguiente = min(semana_siguiente)
                    ultimo_dia_siguiente = max(semana_siguiente)
                
                    for i in range(0,length,3):
                        montoOrden = ordenesArray[i]
                        fechaOrden = ordenesArray[i+1]                    

                        if fechaOrden.month == dia_actual.month and fechaOrden.day >= primer_dia_siguiente or fechaOrden.day <= ultimo_dia_siguiente:
                            montoTotal += montoOrden

            self.ids['lblVentasTotales'].text = f'Ventas Totales: ${montoTotal}'

        if warningMessage:
            self.dialog = MDDialog(
                title = 'Informacion no encontrada',
                text = dialogMessage,
                buttons = [
                    MDFlatButton(text='Cerrar', on_release=self.close)
                ]
            )
            self.dialog.open()

    def close(self, obj):
        self.dialog.dismiss()

'''
[CLASE]
StatsScreen

[PARAMETROS]
Screen -> nombre del formulario

[INFO]
Esta clase permite mostrar
las estadisticas

'''

class StatsScreen(Screen):
    checklinearGrafic = False
    checkPieBbdGrafic = False
    checkPiePltGrafic = False
    linearGraficConfig = None
    PieBbdGraficConfig = None
    PiePltGraficConfig = None
    semana_actual = None

    def btnDatosGeneralesInputs(self):
        if self.manager.current != 'main':
            self.manager.current = 'main'

    def btnEstadisticasInputs(self):
        if self.manager.current != 'stats':
            self.manager.current = 'stats'

    def update(self, data):
        self.data = data

        ordenesArray = self.data[0]
        bebidasArray = self.data[1]
        platillosArray = self.data[2]
        restauranteNombre = self.data[3]

        dialogMessage = "No se pudo encontrar el contenido de las siguientes colecciones: "

        warningMessage = False

        length = len(ordenesArray)
        dia_actual = datetime.today()
        calendario_anterior = calendar.monthcalendar(dia_actual.year, dia_actual.month - 1)
        calendario_actual = calendar.monthcalendar(dia_actual.year, dia_actual.month)
        calendario_siguiente = calendar.monthcalendar(dia_actual.year, dia_actual.month + 1)
        montoTotal = 0

        x = [1,2,3,4,5,6,7]
        y = [0,0,0,0,0,0,0]

        plt.figure(dpi=80)

        if self.checklinearGrafic:
            plt.close(1)
            vt = self.ids.bxlVentasTotales
            vt.remove_widget(self.linearGraficConfig)

        if self.checkPiePltGrafic:
            plt.close(2)
            Pla = self.ids.bxlPlatillos
            Pla.remove_widget(self.PiePltGraficConfig)

        if self.checkPieBbdGrafic:
            plt.close(3)
            bbd = self.ids.bxlBebidas
            bbd.remove_widget(self.PieBbdGraficConfig)


        ################################################################

        if len(ordenesArray) == 0:
            warningMessage = True
            dialogMessage += "ordenes, "

            x = [1,2,3,4]
            y = [1,2,3,4]
            names = ['vacio','vacio','vacio','vacio']

            plt.figure(1)
            plt.plot(x,y)
            plt.xticks(x,names)
            plt.xlabel('Vacio')
            plt.xlabel('Vacio')

            self.linearGraficConfig = FigureCanvasKivyAgg(plt.gcf())
            vt = self.ids.bxlVentasTotales
            vt.add_widget(self.linearGraficConfig)

            if self.linearGraficConfig in vt.children:
                self.checklinearGrafic = True
            else:
                self.checklinearGrafic = False
        else:
            semana_actual = None
            aux = False

            for semana in calendario_actual:

                for i in range(0,len(semana)):

                    if dia_actual.day == semana[i]:
                        self.semana_actual = semana
                        aux = True
                        break

                if aux:
                    break

            if min(semana) == 0:
                semana_anterior = calendario_anterior[4]

                for i in range(0, len(semana)):
                    if semana[i] == 0:
                        semana[i] = semana_anterior[i]
            elif max(semana) == 0:
                semana_siguiente = calendario_siguiente[0]
                
                for i in range(0, len(semana)):
                    if semana[i] == 0:
                        semana[i] = semana_siguiente[i]

                pass

            for i in range(0, length, 3):
                monto = ordenesArray[i]
                fecha = ordenesArray[i+1]

                for i in range(0, len(semana)):
                    if fecha.day == semana[i]:
                        y[i] += monto

            names = ['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']

            plt.figure(1)
            plt.plot(x,y)
            plt.xticks(x,names,fontsize=7.0)
            plt.xlabel('Vacio')
            plt.xlabel('Vacio')

            self.linearGraficConfig = FigureCanvasKivyAgg(plt.gcf())
            vt = self.ids.bxlVentasTotales
            vt.add_widget(self.linearGraficConfig)

            if self.linearGraficConfig in vt.children:
                self.checklinearGrafic = True
            else:
                self.checklinearGrafic = False
        

        if len(platillosArray) == 0:
            warningMessage = True
            dialogMessage += 'bebidas, '

            a = [1]
            b = ['Vacio']

            plt.figure(2)
            plt.pie(a,labels=b)

            self.PieBbdGraficConfig = FigureCanvasKivyAgg(plt.gcf())

            bbd = self.ids.bxlBebidas
            bbd.add_widget(self.PieBbdGraficConfig)

            if self.PieBbdGraficConfig in bbd.children:
                self.checkPieBbdGrafic = True
            else:
                self.checkPieBbdGrafic = False

        else:
        
            a = [0,0,0,0]
            b = ['','','','']

            for i in range(0,len(platillosArray),3):
                nombre = platillosArray[i]
                contador = platillosArray[i+2]

                if nombre == 'Pollo en salsa de hongos':
                    nombre = 'Pollo en salsa\n de hongos'

                for j in range(0, len(a)):
                    if j == len(a) - 1 and a[j] == 0:
                        a[j] = contador
                        b[j] = nombre
                        break
                    elif j == len(a) - 1 and a[j] != 0 and contador > a[j]:
                        a[j] = contador
                        b[j] = nombre
                        break
                    elif a[j] == 0 and a[j+1] == 0:
                        a[j] = contador
                        b[j] = nombre
                        break
                    elif a[j] != 0 and a[j+1] == 0:
                        a[j+1] = contador
                        b[j+1] = nombre
                        break
                    elif a[j] != 0 and a[j+1] != 0 and a[j+2] == 0:
                        a[j+2] = contador
                        b[j+2] = nombre
                        break
                    elif a[j] != 0 and a[j+1] != 0 and a[j+2] != 0 and contador > a[j]:
                        a[j] = contador
                        b[j] = nombre
                        break
            
            plt.figure(2)
            plt.pie(a,labels=b,textprops={'fontsize':7.5},radius=0.7)

            self.PiePltGraficConfig = FigureCanvasKivyAgg(plt.gcf())

            Pla = self.ids.bxlPlatillos
            Pla.add_widget(self.PiePltGraficConfig)

            if self.PiePltGraficConfig in Pla.children:
                self.checkPiePltGrafic = True
            else:
                self.checkPiePltGrafic = False

        if len(bebidasArray) == 0:
            warningMessage = True
            dialogMessage += 'platillos, '

            a = [1]
            b = ['Vacio']

            plt.figure(2)
            plt.pie(a,labels=b)

            self.PieBbdGraficConfig = FigureCanvasKivyAgg(plt.gcf())

            bbd = self.ids.bxlBebidas
            bbd.add_widget(self.PieBbdGraficConfig)

            if self.PieBbdGraficConfig in bbd.children:
                self.checkPieBbdGrafic = True
            else:
                self.checkPieBbdGrafic = False
        else:

            c = [0,0,0,0]
            d = ['','','','']

            for i in range(0,len(bebidasArray),3):
                nombre = bebidasArray[i]
                contador = bebidasArray[i+2]

                for j in range(0, len(c)):
                    if j == len(c) - 1 and c[j] == 0:
                        c[j] = contador
                        d[j] = nombre
                        break
                    elif j == len(c) - 1 and c[j] != 0 and contador > c[j]:
                        c[j] = contador
                        d[j] = nombre
                        break
                    elif c[j] == 0 and c[j+1] == 0:
                        c[j] = contador
                        d[j] = nombre
                        break
                    elif c[j] != 0 and c[j+1] == 0:
                        c[j+1] = contador
                        d[j+1] = nombre
                        break
                    elif c[j] != 0 and c[j+1] != 0 and c[j+2] == 0:
                        c[j+2] = contador
                        d[j+2] = nombre
                        break
                    elif c[j] != 0 and c[j+1] != 0 and c[j+2] != 0 and c[j+3] != 0 and contador > c[j]:
                        c[j] = contador
                        d[j] = nombre
                        break

            print(c)
            plt.figure(3)
            plt.pie(c,labels=d,textprops={'fontsize':7.5},radius=0.7,autopct='%1.1f%%')

            self.PieBbdGraficConfig = FigureCanvasKivyAgg(plt.gcf())

            bbd = self.ids.bxlBebidas
            bbd.add_widget(self.PieBbdGraficConfig)

            if self.PieBbdGraficConfig in bbd.children:
                self.checkPieBbdGrafic = True
            else:
                self.checkPieBbdGrafic = False                

        if len(restauranteNombre) == 0:
            warningMessage = True
            dialogMessage += 'nombre, '
            self.ids['lblTitulo'].text = 'Sin Nombre'
        else:
            self.ids['lblTitulo'].text = restauranteNombre[0]

        if warningMessage:
            self.dialog = MDDialog(
                title = 'Informacion no encontrada',
                text = dialogMessage,
                buttons = [
                    MDFlatButton(text='Cerrar', on_release=self.close)
                ]
            )
            self.dialog.open()

    def close(self, obj):
        self.dialog.dismiss()
'''
[CLASE]
ManagerSC

[PARAMETROS]
ScreenManager -> obtejo de kivymd

[INFO]
Esta clase permite administrar cada
formulario que se utilizara dentro de la
app

'''

class ManagerSC(ScreenManager):

    def buildScreens(self):
        
        self.login = LoginScreen(name='login')
        self.main = MainScreen(name='main')
        self.stats = StatsScreen(name='stats')

        self.login.main = self.main
        self.login.stats = self.stats

        self.add_widget(self.login)
        self.add_widget(self.main)
        self.add_widget(self.stats)

    def setScreen(self, name):
        self.current = name

    def getScreen(self):
        return self.current

'''
[CLASE]
App

[PARAMETROS]
MDApp -> objeto de kivy

[INFO]
permite construir y ejecutar 
la aplicacion

'''

class App(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = Builder.load_file("desing.kv")
        self._screen=ManagerSC()
        Window.bind(on_keyboard=self.keyEvents)


    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.accent_palette = 'Gray'
        self._screen = ManagerSC()

        self._screen.buildScreens()

        return self._screen

    def keyEvents(self, window, key, *largs):
        if key == 27:
            if self._screen.getScreen() == 'login':
                self.stop()
            elif self._screen.getScreen() == 'main':
                dialog = self._screen.main.closeMessage(self)
                dialog.open()
            elif self._screen.getScreen() == 'stats':
                self._screen.setScreen('main')

if __name__ == '__main__':
    App().run()