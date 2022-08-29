import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# base de datos de mis voces:
# id1 español femenino, debo cambiarlo a español masculino
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
# id2 inglés masculino
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'

lista_de_campeones = ['atrox', 'ahri', 'ari', 'akali', 'acali', 'acshan', 'akshan', 'alistar', 'amumu',
                      'anivia', 'ani', 'anni', 'anie', 'aphelios', 'afelios', 'ashe', 'aye', 'aurelion sol',
                      'azir', 'asir', 'bardo', 'belvet', 'velvet', 'belbet', 'blitscrank', 'blitzcrank',
                      'blits', 'brand', 'bran', 'braum', 'caitlyn', 'caitlin', 'camil', 'camille',
                      'casiopeia', 'casio', 'cassiopeia', 'chogat', 'talon', 'talón', 'zed', 'sed']


# escuchar microfono y guardarlo en texto
def transformar_audio_en_texto():
    # almacenar recognizer en una variable
    r = sr.Recognizer()

    # configurar microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzó la grabación
        print('ya puedes hablar.')

        # guardar lo que escuche como audio en una variable
        audio = r.listen(origen)

        try:
            # intentará buscar en google
            pedido = r.recognize_google(audio, language='es-ar')

            # prueba de que pudo ingresar
            print('dijiste: ' + pedido)

            # devolver pedido
            return pedido

        # en caso de que no se comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print('no funciona')

            # devolver error
            return 'sigo esperando el audio'

        # en caso de no resolver el pedido
        except sr.RequestError:

            # prueba de que no comprendio el audio
            print('no entendí')

            # devolver error
            return 'sigo esperando el audio'

        # error inesperado
        except:
            # prueba de que no comprendio el audio
            print('no se escucha')

            # devolver error
            return 'sigo esperando el audio'


# función para que el asistente pueda ser escuchado
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar día de la semana
def pedir_dia():
    # crear variable con datos de hoy
    dia = datetime.date.today()

    # crear variable par el día de la semana
    dia_semana = dia.weekday()

    # diccionario con nombres de los días
    calendario = {0: 'lunes',
                  1: 'martes',
                  2: 'miércoles',
                  3: 'jueves',
                  4: 'viernes',
                  5: 'sábado',
                  6: 'domingo'}

    # decir el día de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# informar qué hora es
def pedir_hora():
    # crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} y {hora.minute}.'

    # decir la hora
    hablar(hora)


# función de saludo inicial
def saludo_inicial():
    # crear variable con datos de datetime
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'buen día'
    else:
        momento = 'buenas tardes'

    # decir el saludo
    hablar(f'Hola {momento}, soy Jarvis. ¿En qué te puedo ayudar?')


# función central
def pedir_cosas():
    # activar el saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # activar el micrófono y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        # DAILY QUESTIONS
        if 'abrir youtube' in pedido:
            hablar('Estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir google' in pedido:
            hablar('Estoy iniciando el navegador')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Esto encontré en wikipedia:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Ahora lo pongo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'El precio de {accion} es {precio_actual}')
                continue
            except:
                hablar(f'Perdón, no he encontrado el precio de {accion}')
                continue
        elif 'gracias' in pedido:
            hablar('De nada, avisame cualquier cosa.')
            break

        # LEAGUE OF LEGENDS
        elif 'objetos de' in pedido \
                or 'objetos en' in pedido \
                or 'chetos de' in pedido \
                or 'chetos en' in pedido:
            campeon = pedido.split('de')[-1].strip()

            if campeon in lista_de_campeones:
                if campeon == 'atrox':
                    hablar('Los objetos de Aatrox con mayor porcentaje de victoria son: Eclipse, Cuchilla Oscura '
                           'y Serylda. Usa Botas Blindadas, pero si tu oponente en línea tiene dapo A-P, te '
                           'recomiendo las Botas de Mercurio.')
                    continue
                if campeon == 'ahri' or campeon == 'ari':
                    hablar('Según el porcentaje de victoria, los mejores objetos para Ahri son: Escarcha Eterna, '
                           'Llamasombría y Reloj de Zhonya. ')
                    continue
                if campeon == 'akali' or campeon == 'acali':
                    hablar('Los mejores objetos de Akali son: Cintomisil, Llamasombría y el Reloj de Arena de Zhonya. ')
                    continue
                if campeon == 'akshan' or campeon == 'acshan':
                    hablar('Los objetos más ganadores de Akshan son: Verdugo de Krakens, Hoja del Rey Arruinado '
                           'y Recuerdos de Lord Dominik.')
                    continue
                if campeon == 'alistar':
                    hablar('Los objetos más ganadores de Akshan son: Verdugo de Krakens, Hoja del Rey Arruinado '
                           'y Recuerdos de Lord Dominik.')
                    continue
                if campeon == 'amumu':
                    hablar('Los objetos que más victorias te darán si juegas Amumu son: Égida de Fuego Solar, '
                           'Abrazo Demoníaco y Malla de Espinas.')
                    continue
                if campeon == 'anivia':
                    hablar('Los mejores objetos en Anivia son: Desconsuelo de Liandry, Bastón del Arcángel y '
                           'el Reloj de Arena de Zhonya. ')
                    continue
                if campeon == 'ani' or campeon == 'anni' or campeon == 'anie':
                    hablar('Los objetos ganadores en Annie son: Eco de Luden, Llamasombría y el Reloj de Arena de '
                           'Zhonya.')
                    continue
                if campeon == 'aphelios' or campeon == 'afelios':
                    hablar('Los mejores objetos de Aphelios son: Viento Huracanado, Sanguinaria y Filo del Infinito.')
                    continue
                if campeon == 'ashe' or campeon == 'aye':
                    hablar('En Ashe, los mejores objetos son: Arcoescudo Inmortal, Hoja de Furia de Guinsoo y el '
                           'Huracán de Runaan.')
                    continue
                if campeon == 'aurelion sol':
                    hablar('Según el porcentaje de victoria, los objetos de Aurelion Sol deben ser: Escarcha Eterna, '
                           'Cetro de Cristal de Rilay y el Reloj de Arena de Zhonya.')
                    continue
                if campeon == 'azir' or campeon == 'asir':
                    hablar('Los mejores objetos en Azir son: Eco de Luden, Llamasombría y el Reloj de Arena de Zhonya. '
                           'Si la partida se alarga no olvides comprar el Sombrero Mortal de Rabadón.')
                    continue
                if campeon == 'bardo':
                    hablar('Los objetos para ganar con Bardo son: Medallón de los Solari de Hierro, '
                           'Coraza del Muerto y Putrificador Tecnoquímico.')
                    continue
                if campeon == 'belbet' or campeon == 'belvet' or campeon == 'velvet':
                    hablar('En este nuevo campeón, los mejores objetos son: Verdugo de Krakens, Hoja del Rey '
                           'Arruinado y la Hoja de Furia de Guinsoo. Las mejores botas suelen ser las Blindadas '
                           'a menos que tu oponente en línea tenga daño mágico, en este caso debes usar las '
                           'Botas de Mercurio.')
                    continue
                if campeon == 'blitscrank' or campeon == 'blitzcrank' or campeon == 'blits':
                    hablar('Los objetos más útiles en Blitzcranck son el Medallón de los Solari de Hierro, '
                           'Promesa del Caballero y Convergencia de Zeke.')
                    continue
                if campeon == 'brand' or campeon == 'bran':
                    hablar('Los mejores objetos de Brand son: Desconsuelo de Liandry, el Reloj de Arena de Zhonya '
                           'y el Cetro de Cristal de Rilay.')
                    continue
                if campeon == 'braum':
                    hablar('Según los porcentajes de victoria, los mejores objetos de Braum son: Medalón de los Solari '
                           'de Hierro, Promesa de Caballero y Malla de Espinas.')
                    continue
                if campeon == 'caitlyn' or campeon == 'caitlin':
                    hablar(
                        'Los objetos más fuertes en Caitlyn son: Viento Huracanado, Recaudadora y Filo del Infinito.')
                    continue
                if campeon == 'camil' or campeon == 'camille':
                    hablar('En Camille te recomiendo comprar siempre Desgarrador Divino, Baile de la Muerte y '
                           'la Hidra Voraz. Si tu oponente tiene daño mágico compra Botas de Mercurio, si tiene '
                           'daño físico compra Botas Blindadas.')
                    continue
                if campeon == 'cassiopeia' or campeon == 'casiopeia' or campeon == 'casio':
                    hablar('Los objetos más fuertes en Cassiopeia son: Desconsuelo de Liandry, Bastón del Arcángel '
                           'y Cetro de Cristal de Rilay. No hace falta que compres Botas con este campeón.')
                    continue
                if campeon == 'chogat':
                    hablar('Los objetos más fuertes de Cho’gath son: Guantelete de Fuego Escarchado, Malla de Espinas '
                           'y Corazón de Hielo.')
                    continue
                if campeon == 'talon' or campeon == 'talón':
                    hablar('Los objetos más fuertes en Talon son: Youmuu, Draktharr y Filo de la Noche. Las botas '
                           'más usadas son las Jonias de Lucidez.')
                    continue
            else:
                hablar('Perdón, no escuché el nombre del campeón. ¿Podrías repetirme el pedido?')
                continue
        elif 'counter de' in pedido:
            campeon = pedido.split('de')[-1].strip()
            if campeon in lista_de_campeones:
                if campeon == 'zed' or campeon == 'sed':
                    hablar('Los mejores counters de Zed son: Anivia, Swain y Gangplank. ')
                    continue
                elif campeon == 'ahri' or campeon == 'ari':
                    hablar('Los mejores counters de Ahri son: VelKoz, Zed y Talon.')
                    continue
            else:
                hablar('Perdón, no escuché el nombre del campeón. ¿Podrías repetirme el pedido?')
                continue
        elif 'cómo le gano a' in pedido \
                or 'cómo ganarle a' in pedido \
                or 'como le hago counter a' in pedido \
                or 'como counterear a' in pedido:
            campeon = pedido.split('a')[-1].strip()
            if campeon in lista_de_campeones:
                if campeon == 'zed' or campeon == 'sed':
                    hablar('Comprate Zhonya, recuerda que después de ultear aparecerá atrás tuyo y, si puedes, '
                           'compra objetos que te den escudos o armadura.')
                    continue
                else:
                    hablar('Perdón, no escuché el nombre del campeón. ¿Podrías repetirme el pedido?')
                    continue
