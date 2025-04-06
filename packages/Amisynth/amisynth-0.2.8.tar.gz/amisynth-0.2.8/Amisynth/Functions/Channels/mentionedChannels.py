import xfox
import discord
import Amisynth.utils as utils
@xfox.addfunc(xfox.funcs, name="mentionedChannels")
async def mentioned_channels(numero: str = None, *args, **kwargs):
    context = utils.ContextAmisynth()
    channels = context.get_channel_mentions()  # Obtener menciones de roles

    if not channels:
        print("[DEBUG MENTIONEDCHANNELS]: No se encontraron menciones de canales")
        return ""
    # Si no se proporciona un índice o selector, devolver el primer canal mencionado
    if numero is None:
        return str(channels[0])

    # Si el argumento es un número, obtener la mención en ese índice
    if numero.isdigit():  
        indice = int(numero) - 1  # Convertir a índice basado en 1
        if 0 <= indice < len(channels):
            return str(channels[indice])
        else:
            print("[DEBUG MENTIONED_CHANNELS]: No hay suficiente cantidad de canales mencionados.")
            return ""

    # Mayor y menor ID de canal
    if numero == ">":
        return str(max(channels, key=lambda channel: channel.id))  # Mayor ID
    
    if numero == "<":
        return str(min(channels, key=lambda channel: channel.id))  # Menor ID
    
    print(f"[DEBUG MENTIONED_CHANNELS]: Parámetro no válido: {numero}")
    raise ValueError(f":x: No pusiste el parámetro adecuado: `{numero}`, en `$mentionedChannels[{numero}]`")
