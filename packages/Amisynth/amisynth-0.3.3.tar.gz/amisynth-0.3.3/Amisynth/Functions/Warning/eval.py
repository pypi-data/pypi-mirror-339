import xfox
import discord
import Amisynth.utils as utils
from Amisynth.utils import utils as utils_func
from Amisynth.utils import buttons as but, embeds as emb

@xfox.addfunc(xfox.funcs, name="eval")
async def eval_command(code=None, *args, **kwargs):
    # ✅ Verificación para evitar que 'code' sea None
    if code is None:
        return ""

    context = utils.ContextAmisynth()
    channel = context.obj_channel

    try:
        code = await xfox.parse(code)

    except ValueError as e:
        return f"{e}"


    texto = code

    botones, embeds = await utils_func()

    view = discord.ui.View()
    if botones:
        for boton in botones:
            view.add_item(boton)

    await channel.send(
        content=texto if texto else "",
        view=view,
        embeds=embeds if embeds else []
    )
    but.clear()
    emb.clear()

    return ""

