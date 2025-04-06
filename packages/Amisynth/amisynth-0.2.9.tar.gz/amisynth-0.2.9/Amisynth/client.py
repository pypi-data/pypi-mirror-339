

import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import xfox
import Amisynth.Handler
import Amisynth.utils as utils
from typing import List, Dict, Optional, Any
import os
import importlib.util

# Registrar todas las funciones automáticamente
Amisynth.Handler.register_all()

class AmiClient(commands.Bot):
    def __init__(self, prefix, cogs=None, variables_json=False, case_insensitive:bool=False):
        super().__init__(command_prefix=prefix, intents=discord.Intents.all(), case_insensitive=case_insensitive)
        
        self.prefix = prefix
        self.servicios_prefijos = {}  # Diccionario para guardar los prefijos por servidor
        self._cogs = cogs or []
        self.comandos_personalizados = {}
        self.eventos_personalizados = {
            "$onMessage": [],
            "$onReady": [],
            "$onReactionAdd": [],
            "$onReactionRemove": [],
            "$onInteraction": [],
            "$onMessageEdit": [],
            "$onMessageDelete": [],
            "$onJoinMember": [],
            "$onLeaveMember": [],
            "$onMessagesPurged": [],
            "$onMessageTyping": []
        }

        if variables_json:
            utils.VariableManager()

        utils.bot_inst = self

    async def get_prefix(self, msg):
        """Obtiene el prefijo de acuerdo con el servidor o usa el prefijo general."""
        if msg.guild:
            # Si el servidor tiene un prefijo personalizado, lo devuelve
            return self.servicios_prefijos.get(msg.guild.id, self.prefix)
        return self.prefix  # Usa el prefijo general si no es un servidor
    
    def set_prefijo_servidor(self, servidor_id, nuevo_prefijo):
        """Permite cambiar el prefijo para un servidor específico."""
        self.servicios_prefijos[servidor_id] = nuevo_prefijo


    async def setup_hook(self):
        """Cargar todos los cogs de forma asincrónica."""
        if self._cogs:  # Verificar si se pasó una carpeta de cogs
            await self.load_cogs(self._cogs)

    async def load_cogs(self, carpeta):
        """Cargar cogs de forma asincrónica."""
        for filename in os.listdir(carpeta):
            if filename.endswith(".py"):
                cog_path = os.path.join(carpeta, filename)

                # Cargar módulo dinámicamente
                spec = importlib.util.spec_from_file_location(filename[:-3], cog_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Si el cog tiene una función setup(bot), la ejecutamos
                if hasattr(module, "setup"):
                    await module.setup(self)  # Ejecutar setup(bot) si es async


    def new_command(self, name, type, code):
        async def custom_command(ctx_command):
            utils.ContextAmisynth(ctx=ctx_command)

            try:
              
                result = await xfox.parse(code, del_empty_lines=True)
             
            except ValueError as e:
                result = e
        
            texto = result
            botones, embeds = await utils.utils()
            # Construir el View si hay botones
            view = discord.ui.View()
            if botones:
                for boton in botones:  # Extraer la fila y el botón
                    view.add_item(boton)

            

            # Enviar mensaje con el tipo adecuado
            try:
                await ctx_command.send(
                content=texto if texto else None,  # Si hay texto, se agrega
                view=view if botones else None,    # Si hay botones, se agrega el View
                embeds=embeds if embeds else None  # Si hay embeds, se agregan
                )
            except discord.HTTPException as e:
                if e.code == 50006:
                    print(f"[DEBUG AMISYNTH] SE ENVIO UN MENSAJE VACIO EN  EL TIPO COMANDO.")
                else:
                    pass



        self.comandos_personalizados[name] = {"type": type, "code": code}
        self.add_command(commands.Command(custom_command, name=name))
    
    
    def new_slash(
        self,
        name: str,
        description: str,
        code: str = "",
        options: Optional[List[Dict[str, Any]]] = None
    ):
        parameters = ["interaction: discord.Interaction"]
        choices_kwargs = {}



        def remp(valor):
            if valor == "Texto":
                return "str"  # Devuelve el tipo de texto (string)
            elif valor == "Integer":
                return "int"  # Devuelve el tipo entero
            elif valor == "Archivo":
                return "discord.Attachment"  # Devuelve el tipo de archivo adjunto
            elif valor == "Canal":
                return "discord.TextChannel"  # Devuelve el tipo de canal de texto
            elif valor == "Mencionable":
                return "discord.Member" # Devuelve el tipo de miembro mencionable (puede ser un usuario o rol)
            elif valor == "Rol":
                return "discord.Role"  # Devuelve el tipo de rol
            elif valor == "Number":
               return "float"  # Devuelve el tipo de número (puede ser entero o flotante)
            else:
               raise ValueError("[DEBUG SLASH] OPCION DE SLASH INVALIDA")


        if options:
            for option in options:
                option_name = option.get("name_option")
                param_name = option_name.replace(" ", "_")
                option_type = remp(valor=option["type"])
                option_required = option.get("required", False)
                
                if option_required:
                    parameters.append(f"{param_name}: {option_type}")
                else:
                    parameters.append(f"{param_name}: {option_type} = None")

                if "choices" in option and isinstance(option["choices"], list):
                    choices_kwargs[param_name] = [
                        app_commands.Choice(name=choice["name_choice"], value=choice["value_choice"])
                        for choice in option["choices"]
                    ]

        params_str = ", ".join(parameters)

        func_code = f"""async def slash_command({params_str}):
        kwargs = {{"ctx_slash_env": interaction}}
        utils.ContextAmisynth(interaction)

        result = await xfox.parse({repr(code)}, del_empty_lines=True, **kwargs)
        botones, embeds = await utils.utils()
           
        view = discord.ui.View()
        if botones:
            for boton in botones: 
                view.add_item(boton)

        await interaction.response.send_message(
            content=result if result else None,
            view=view,
            embeds=embeds if embeds else [],
            ephemeral=False
        )"""

        exec(func_code, globals(), locals())
        command_func = locals()["slash_command"]
        decorated_func = self.tree.command(name=name, description=description)(command_func)
        
        for key, choices in choices_kwargs.items():
            decorated_func = app_commands.choices(**{key: choices})(decorated_func)
        
        self.comandos_personalizados[name] = {"type": "slash", "code": code}





    def new_event(self, 
                  tipo, 
                  codigo, 
                  overwrite=False):
        
        if tipo not in self.eventos_personalizados or overwrite:
            self.eventos_personalizados[tipo] = []  # Reiniciar si se sobrescribe
        self.eventos_personalizados[tipo].append(codigo)

    async def ejecutar_eventos(self, tipo, 
                               ctx_message_env=None, 
                               ctx_reaction_env=None, 
                               ctx_reaction_remove_env=None, 
                               ctx_interaction_env=None, 
                               ctx_message_edit_env=None, 
                               ctx_message_delete_env=None,
                               ctx_join_member_env=None,
                               ctx_remove_member_env=None,
                               ctx_bulk_message_delete_env=None,
                               ctx_typing_env=None):
        

        if tipo in self.eventos_personalizados:
            for codigo in self.eventos_personalizados[tipo]:
                kwargs = {
                    "ctx_message_env": ctx_message_env,
                    "ctx_reaction_env": ctx_reaction_env,
                    "ctx_reaction_remove_env": ctx_reaction_remove_env,
                    "ctx_interaction_env": ctx_interaction_env,  # 👈 Agregado aquí
                    "ctx_message_edit_env": ctx_message_edit_env,
                    "ctx_message_delete_env": ctx_message_delete_env,
                    "ctx_join_member_env": ctx_join_member_env,
                    "ctx_remove_member_env": ctx_remove_member_env,
                    "ctx_bulk_message_delete_env": ctx_bulk_message_delete_env,
                    "ctx_typing_env": ctx_typing_env
                }
                try:
                    result = await xfox.parse(codigo, del_empty_lines=True, **kwargs)
                except ValueError as e:
                    result = e

                botones, embeds = await utils.utils()
                view=None
                if botones:
                    # Crear un View para los botones
                    view = discord.ui.View()
                    for boton in botones:
                        view.add_item(boton)  # Agregar los botones al View
                
                try:
                    if ctx_message_env:
                        await ctx_message_env.channel.send(result, 
                                                        view=view if view else None,  
                                                        embeds=embeds if embeds else [])

                    elif ctx_reaction_env:
                        channel = self.get_channel(ctx_reaction_env.channel_id, )
                        if channel:
                            await channel.send(result, 
                                            view=view if view else None,
                                            embeds=embeds if embeds else [])


                    elif ctx_reaction_remove_env:
                        channel = self.get_channel(ctx_reaction_remove_env.channel_id)
                        if channel:
                            await channel.send(result, 
                                            view=view,
                                            embeds=embeds if embeds else [])

                    elif ctx_interaction_env:
                        await ctx_interaction_env.response.edit_message(content=result, 
                                                                    view=view,
                                                                    embeds=embeds)

                    elif ctx_message_edit_env:
                        before, after = ctx_message_edit_env
                        await before.channel.send(content=result, 
                                              view=view, 
                                              embeds=embeds)

                    elif ctx_message_delete_env:
                        await ctx_message_delete_env.channel.send(content=result, 
                                                                    view=view,
                                                                    embeds=embeds)
                    
                    elif ctx_bulk_message_delete_env:
                        
                        await ctx_bulk_message_delete_env.channel.send(content=result, 
                                                                    view=view,
                                                                    embeds=embeds)
                        
                    elif ctx_typing_env:
                        
                        await ctx_typing_env[0].send(content=result, 
                                                                    view=view,
                                                                    embeds=embeds)

                except Exception as e:
                    print(f"[DEBUG ERROR]: ERROR: {e}")
    


    async def on_message(self, ctx_message_env):
        if ctx_message_env.author.bot:
            return
        
        utils.ContextAmisynth(ctx_message_env)

        await self.ejecutar_eventos("$onMessage", ctx_message_env)
        await self.process_commands(ctx_message_env)  # Permite que otros comandos de discord.py sigan funcionando




    async def on_ready(self):
        print(f"[DEBUG CLIENT] USER:{self.user}")
        utils.bot_id = self.user.id
        await self.ejecutar_eventos("$onReady")
        try:
            synced = await self.tree.sync()
            
        except Exception as e:
            print(f"Error al sincronizar slash commands: {e}")



    async def on_member_join(self, member: discord.Member):
        utils.ContextAmisynth(member)
        await self.ejecutar_eventos("$onJoinMember", ctx_join_member_env=member)
    
    async def on_member_remove(self, member: discord.Member):
        utils.ContextAmisynth(member)
        await self.ejecutar_eventos("$onLeaveMember", ctx_remove_member_env=member)


        
    async def on_raw_reaction_add(self, ctx_reaction_env: discord.RawReactionActionEvent):
        utils.ContextAmisynth(ctx_reaction_env)
        """Maneja cuando un usuario añade una reacción."""
        await self.ejecutar_eventos("$onReactionAdd", ctx_reaction_env=ctx_reaction_env)



    async def on_raw_reaction_remove(self, ctx_reaction_remove_env: discord.RawReactionActionEvent):
        """Maneja cuando un usuario remueve una reacción."""
        utils.ContextAmisynth(ctx_reaction_remove_env)
        await self.ejecutar_eventos("$onReactionRemove", ctx_reaction_remove_env=ctx_reaction_remove_env)



    async def on_interaction(self, ctx_interaction_env: discord.Interaction):
        """Maneja interacciones como botones y menús."""
        if ctx_interaction_env.user.bot:
            return
        utils.ContextAmisynth(ctx_interaction_env)
        await self.ejecutar_eventos("$onInteraction", ctx_interaction_env=ctx_interaction_env)



    async def on_message_edit(self, before, after):
        utils.ContextAmisynth(before)
        if before.author.bot:  # Evita que el bot procese sus propios mensajes
            return
        await self.ejecutar_eventos("$onMessageEdit", ctx_message_edit_env=(before, after))
        

    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        utils.ContextAmisynth(message)
        await self.ejecutar_eventos("$onMessageDelete", ctx_message_delete_env=message)



    async def on_bulk_message_delete(self, ctx_bulk_message_delete_env: discord.Message):
        utils.ContextAmisynth(ctx_bulk_message_delete_env)
        await self.ejecutar_eventos("$onMessagesPurged", ctx_bulk_message_delete_env=ctx_bulk_message_delete_env[0])

    async def on_typing(self, channel, user, when):
        utils.ContextAmisynth(channel)
        await self.ejecutar_eventos("$onMessageTyping", ctx_typing_env=(channel, user, when))

