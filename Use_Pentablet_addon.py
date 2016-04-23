# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


# ##### COMIENZO LICENCIA GPL ESPAÑOL #####
#
# Este programa es sofware libre; puedes redistribuirlo y/o
# Modificarlo bajo los terminos de la Licencia Publica General GNU
# Publicada por la Fundación para el Software Libre; ya sea la versión 2
# De la Licencia, o (a su elección) cualquier versión posterior.
#
# Este programa se distribuye con la esperanza de que sea útil,
# Pero SIN NINGUNA GARANTÍA; ni siquiera la garantía implícita de
# COMERCIALIZACIÓN o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Vea el
# Licencia Pública General GNU para más detalles.
#
# Debería haber recibido una copia de la Licencia Pública General GNU
# Junto a este programa; si no, escriba a la Free Software Foundation,
# Inc., 51 Franklin Street, Quinto Piso, Boston, MA 02110-1301, EE.UU..
#
# ##### FIN LICENCIA GPL ESPAÑOL #####

bl_info = {
    'name': 'Use Pentablet',
    'author': 'Harold Tovar',
    'version': (1, 1),
    "blender": (2, 6, 8),
    "api": 36157,
    'description': 'Enable some options inside Blender to work with Pentablets',
    "wiki_url": ""\
        "",
    "tracker_url": "estacion3d.com/descargas"\
        "",
    'category': '3D View'}
    
   
import bpy  
import os
from bpy import context

#----------------------- Variables ---------------------------------------------------------------
    
bpy.types.Scene.use_pentablet = bpy.props.BoolProperty(description = "Use Pentablet", default=False) 
bpy.types.Scene.pentablet_group = bpy.props.BoolProperty(description = "Pentablet Groups", default=False) 
theme = bpy.context.user_preferences.themes['Default']
userpref = context.user_preferences
inputs = userpref.inputs


#---------------------- Operadores ------------------------------------

# ubica el centro de masa/pivote en la posicion del cursor 3D

class SetORG_Cursor_OBJ(bpy.types.Operator):
    bl_idname = "center.cursor3d" 
    bl_label = "Origin to 3D Cursor"
    bl_description = "Set the origin to 3D Cursor Position"

    def execute(self, context):
     
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        
        return {'FINISHED'}


#coloca el centro de masa en la posicion del cursor 3D en modo edicion

class SetORG_Cursor_EDIT(bpy.types.Operator):
    bl_idname = "set.origentocursor3d"
    bl_label = "Origin to 3D Cursor"
    bl_description = "Set origin to 3D Cursor in Edit Mode"

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}
    

# Coloca el centro de masa en la seleccion activa en modo edicion, funciona en todos los modos de edicion incluso en armatures :)
 
class SetORG_SELEC(bpy.types.Operator):
    bl_idname = "set.origenaselection"
    bl_label = "Origin to Active Selection"
    bl_description = "Set origin to Active Selection in Edit Mode"

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'} 
         
# Coloca el pivote en el centro de masa :) en modo objeto funciona en armatures tambien
    
class SetORGN_GEO(bpy.types.Operator):
    bl_idname = "set.origentogeo"
    bl_label = "Origin to 3D Cursor"
    bl_description = "Set origin to 3D Cursor in Edit Mode"

    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        return {'FINISHED'}
    
    
# coloca la opcion de tweak threshold al minimo para agilizar el arrastre con el mouse y/o Pentablet en modo edicion

class Drag_Min(bpy.types.Operator):
    bl_idname = "min.dragoffset"
    bl_label = "Minimal Drag Offset Value"
    bl_description = "Set Minimal Drag Offset"

    def execute(self, context):
        
         
        bpy.context.user_preferences.inputs.tweak_threshold=3
        
        return {'FINISHED'}
    
    
# coloca la opcion de tweak threshold al maximo para evitar el arrastre con el mouse y/o Pentablet
# Util en modo objeto para seleccionar y mover los objetos sin errores accidentales XD XD XD suele pasar...

class Drag_Max(bpy.types.Operator):
    bl_idname = "max.dragoffset"
    bl_label = "Maximum Drag Offset Value"
    bl_description = "Set Maximum Drag Offset"

    def execute(self, context):
        
         
        bpy.context.user_preferences.inputs.tweak_threshold=1024
        
        return {'FINISHED'}

class Drag_DEF(bpy.types.Operator):
    bl_idname = "default.dragoffset"
    bl_label = "Normal Drag Offset Value"
    bl_description = "Set Default Drag Offset"

    def execute(self, context):
        
         
        bpy.context.user_preferences.inputs.tweak_threshold=10
        
        return {'FINISHED'}


# habilita la opcion set border render

class SetBorder_R(bpy.types.Operator):
    bl_idname = "set.camrenderborder"
    bl_label = "Use Render Border"
    bl_description = "Set Render Border"

    def execute(self, context):
        
         
        bpy.context.scene.render.use_border = True
        
        return {'FINISHED'}
    
class UnsetBorder_R(bpy.types.Operator):
    bl_idname = "unset.camrenderborder"
    bl_label = "Clear Render Border"
    bl_description = "Clear Render Border"

    def execute(self, context):
        
         
        bpy.context.scene.render.use_border = False
        
        return {'FINISHED'}

# Doble click Presets
    
class H_DoubleClick_P(bpy.types.Operator):
    bl_idname = "double.clickpreset"
    bl_label = "Set Double Click Speed"
    bl_description = "Slow double click speed "

    def execute(self, context):
        
         
        bpy.context.user_preferences.inputs.mouse_double_click_time = 340
        
        return {'FINISHED'}

class H_DoubleClick_P1(bpy.types.Operator):
    bl_idname = "double.clickpreset1"
    bl_label = "Set Double Click Speed"
    bl_description = "Fast double click speed"

    def execute(self, context):
        
         
        bpy.context.user_preferences.inputs.mouse_double_click_time = 380
        
        return {'FINISHED'}

class H_DoubleClick_D(bpy.types.Operator):
    bl_idname = "double.clickdefault"
    bl_label = "Set Default Click Speed"
    bl_description = "Default double click speed"

    def execute(self, context):
        
         
        bpy.context.user_preferences.inputs.mouse_double_click_time = 350
        
        return {'FINISHED'}



# Calcula las Normales en Modo Objeto funciona en multiples objetos a la vez

class Fix_NRMLS_OBJ(bpy.types.Operator):
    bl_idname = "fixnormals.inobjectmode"
    bl_label = "Fix Normals"
    bl_description = "Recalculate Normals in Object Mode"
    
    @classmethod
    def poll(cls, context):
        # regresa si el objetos se tiene al menos un objeto seleccionado sino no hace nada XD
        
        return bpy.context.mode == 'OBJECT' and len(context.selected_objects) > 0
    
    
    def execute(self, context):
        
        scn = bpy.context.scene
        sel = bpy.context.selected_objects
        meshes = [obj for obj in sel if obj.type == 'MESH']#Con esto se asegura que el operador se ejecute unicamente en objetos tipo Mesh y no arroje errores molestos :)

        for obj in meshes:
            scn.objects.active = obj
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')

         
        self.report({'INFO'}, "Normals were fixed in all Selected Objects") 
        return {"FINISHED"} # listo, ya termine la tarea encomendada XD




#Crea un Grupo de objetos Temporal y lo hace inseleccionable
class Set_Pentablet_GRP(bpy.types.Operator):

    bl_idname = "set.pentabletgroup"
    bl_label = "Lock Objects"
    bl_description = "Make objects unselectable temporarily"

    @classmethod
    def poll(cls, context):
        # regresa si el objetos se tiene al menos un objeto seleccionado sino no hace nada XD
        
        return len(context.selected_objects) > 0
    
    
    def execute(self, context):
        #if not 'Use_Pentablet_Group' in bpy.data.groups:
            #bpy.ops.group.create(name="Use_Pentablet_Group")
            
        bpy.context.scene.pentablet_group= True
        
        sel = context.selected_objects
        
        for obj in sel:
            # Coloca los objetos uno por uno como activos
            bpy.context.scene.objects.active = obj
        
        
            #Estas dos opciones funcionan en nuevas versiones de blender "2.73.3" por ahora deshabilitadas :)
            #bpy.context.object.show_wire_color= True
            #bpy.context.object.color = (0.043617, 0.206792, 0.603817, 1.000000)
            if not 'Use_Pentablet_Group' in bpy.data.groups:
                bpy.ops.group.create(name="Use_Pentablet_Group")
        
            bpy.context.scene.objects.active = obj 
            bpy.ops.object.group_link(group='Use_Pentablet_Group')
            obj.select= True
            bpy.context.scene.objects.active = obj
            #hide_render = True
    
        for object in bpy.data.groups['Use_Pentablet_Group'].objects:
            object.hide_select = True
            object.select= True
            bpy.context.scene.objects.active = object
        
        bpy.ops.object.select_all(action='DESELECT') 
        self.report({'INFO'}, "All selected objects are Locked")  
        return {'FINISHED'}

#Restaura la opcion de seleccion de los objetos dentro del grupo temporal
class Unset_Pentablet_GRP(bpy.types.Operator):
    """Make objects selectable again"""
    bl_idname = "unset.pentabletgroup"
    bl_label = "Unlock Objects"
    
    @classmethod
    def poll(cls, context):
        # regresa si el objetos se tiene al menos un objeto seleccionado sino no hace nada XD
        
        return bpy.context.scene.pentablet_group == True
  
    def execute(self, context):
        
        bpy.ops.object.select_all(action='DESELECT')

        for object in bpy.data.groups['Use_Pentablet_Group'].objects:
            
            #Estas dos opciones funcionan en nuevas versiones de blender "2.73.3" por ahora deshabilitadas :)
            #object.show_wire_color= False
            #object.color = (1, 1, 1, 1)
            object.hide_select = False
            object.select= True
            bpy.context.scene.objects.active = object

        bpy.ops.object.select_same_group(group="Use_Pentablet_Group")
        bpy.ops.group.objects_remove(group='Use_Pentablet_Group')
        bpy.context.scene.pentablet_group= False
        
        bpy.ops.object.select_all(action='DESELECT')
        #bpy.context.scene.objects.active = object
        #object.select= True
        self.report({'INFO'}, "All objects were Unlocked")
        return {'FINISHED'}
       
#Usese solo en caso de emergencia, porque algunas veces las cosas no funcionan como deberian funcionar...
class Set_Selectable_OBJ(bpy.types.Operator):
    """Make all objects in the scene selectable again"""
    bl_idname = "selectable.again"
    bl_label = "Make All Objects Selectable"

    def execute(self, context):
        
        for object in bpy.data.scenes['Scene'].objects:
            object.hide_select = False
            object.select= True
            bpy.context.scene.objects.active = object

        self.report({'INFO'}, "All Objects Are Now Selectable")  
        return {'FINISHED'}
    
#Habilita las opciones hidden wire y x-ray para trabajar mejor cuando se esta haciendo retopologia :)
class Retopo_HelperON(bpy.types.Operator):
    """Set hidden wire and x-ray turned on"""
    bl_idname = "retopo.helperon"
    bl_label = "Hidden Wire and X-Ray ON"
    
  
    def execute(self, context):

        bpy.context.space_data.show_occlude_wire = True
        bpy.context.object.show_x_ray = True

        self.report({'INFO'}, "X-Ray Settings ON")
        return {'FINISHED'}

#Deshabilita las opciones hidden wire y x-ray 
class Retopo_HelperOFF(bpy.types.Operator):
    """Set hidden wire and x-ray turned off"""
    bl_idname = "retopo.helperoff"
    bl_label = "Hidden Wire and X-Ray ON"
    
  
    def execute(self, context):

        bpy.context.space_data.show_occlude_wire = False
        bpy.context.object.show_x_ray = False

        self.report({'INFO'}, "X-Ray Settings OFF")
        return {'FINISHED'}
    
    
    
    
#------------------ Temporal Vertex size Edit Mode ----------------------------------------

# Presets para cambiar temporalmente el tamaño de los vertices en modo edicion, se dice temporal porque no se guardan estos ajustes en ninguna parte




class vertex_3(bpy.types.Operator):
    bl_idname = "vertex.sizetres"
    bl_label = "vertex size = 3"
    bl_description = "Set Vertex size to 3px in edit mode"

    def execute(self, context):
        
        bpy.context.user_preferences.themes['Default'].view_3d.vertex_size = 3
        
        return {'FINISHED'}


class vertex_4(bpy.types.Operator):
    bl_idname = "vertex.sizecuatro"
    bl_label = "vertex size = 4"
    bl_description = "Set Vertex size to 4px in edit mode"

    def execute(self, context):
        
         
        bpy.context.user_preferences.themes['Default'].view_3d.vertex_size = 4
        
        return {'FINISHED'}


class vertex_6(bpy.types.Operator):
    bl_idname = "vertex.sizeseis"
    bl_label = "vertex size = 6"
    bl_description = "Set Vertex size to 6px in edit mode"

    def execute(self, context):
        
         
        bpy.context.user_preferences.themes['Default'].view_3d.vertex_size = 6
        
        return {'FINISHED'}


class vertex_8(bpy.types.Operator):
    bl_idname = "vertex.sizeocho"
    bl_label = "vertex size = 8"
    bl_description = "Set Vertex size to 8px in edit mode"

    def execute(self, context):
        
         
        bpy.context.user_preferences.themes['Default'].view_3d.vertex_size = 8
        
        return {'FINISHED'}

class vertex_10(bpy.types.Operator):
    bl_idname = "vertex.sizediez"
    bl_label = "vertex size = 10"
    bl_description = "Set Vertex size to 10px in edit mode"

    def execute(self, context):
        
         
        bpy.context.user_preferences.themes['Default'].view_3d.vertex_size = 10
        
        return {'FINISHED'}



#-------------- Temporal Wireframe Color Edit Mode ----------------------

# Presets para cambiar temporalmente el color de las aristas "wireframe" de la malla en modo edicion

class wire_blue(bpy.types.Operator):
    bl_idname = "wire.blue"
    bl_label = "Set Wireframe Blue in Editmode"
    bl_description = "Set Wireframe Blue in Editmode"

    def execute(self, context):
        
         
        bpy.context.user_preferences.themes['Default'].view_3d.wire_edit = (0, 0.09, 0.671)
        bpy.context.user_preferences.themes['Default'].view_3d.vertex = (0.051, 0.055, 0.212)
        
        return {'FINISHED'}

class wire_LBlue(bpy.types.Operator):
    bl_idname = "wire.lightblue"
    bl_label = "Set Wireframe Light Blue in Editmode"
    bl_description = "Set Wireframe Light Blue  in Editmode"

    def execute(self, context):
        
         
        bpy.context.user_preferences.themes['Default'].view_3d.wire_edit = (0.188235,0.219608,0.321569)
        bpy.context.user_preferences.themes['Default'].view_3d.vertex = (0.211765,0.454902,0.556863)
        
        return {'FINISHED'}

class wire_gray(bpy.types.Operator):
    bl_idname = "wire.gray"
    bl_label = "Set Wireframe Gray in Editmode"
    bl_description = "Set Wireframe Gray in Editmode"

    def execute(self, context):
        
        
        bpy.context.user_preferences.themes['Default'].view_3d.wire_edit = (0.3, 0.3, 0.3)
        bpy.context.user_preferences.themes['Default'].view_3d.vertex = (0.211765,0.454902,0.556863) #0.37 #0.270588, 0.411765, 0.478431
        
        return {'FINISHED'}

class wire_black(bpy.types.Operator):
    bl_idname = "wire.black"
    bl_label = "Set Wireframe Black in Editmode"
    bl_description = "Set Wireframe Black in Editmode"

    def execute(self, context):
        
         
        bpy.context.user_preferences.themes['Default'].view_3d.wire_edit = (0.0,0.0, 0.0)
        bpy.context.user_preferences.themes['Default'].view_3d.vertex = (0.0, 0.0, 0.0)
        
        return {'FINISHED'}


#--------------------------------- Nuevos Operadores :) ----------------------------------------------------------    
    
# Experimental Keymaps
    
addon_keymapstemp = [] 

#Agrega Experimental shorcuts   

class Add_keymapstemp(bpy.types.Operator):
    """Use Experimental Pentablet Shortcuts"""
    bl_idname = "add.experimentalkeymap"
    bl_label = "Add Pentablet keyMaps"

    def execute(self, context):

        wm = bpy.context.window_manager
        
        #Este shorcut permite extruir nuevos vertices haciendo una pequeña linea en la pentablet, el motivo por el cual es experimental
        #es debido a que algunas veces se activa el seleccionador de ruta corta :/ sin embargo pese a esto funciona muy bien :) cuando se usa con cuidado
        
        km= wm.keyconfigs.addon.keymaps.new(name="Mesh")
        kmi = km.keymap_items.new('mesh.dupli_extrude_cursor', 'EVT_TWEAK_S', 'ANY', ctrl=True)
        addon_keymapstemp.append((km, kmi)) 
        
        self.report({'INFO'}, "Experimental Pentablet Shortcuts Enabled") 
        #print(tuple(addon_keymapstemp))
        return {'FINISHED'}
    
    
#Remueve Experimental shorcuts 
       
class Remove_keymapstemp(bpy.types.Operator): 
    """Remove Experimental Pentablet Shortcuts"""
    bl_idname = "remove.experimentalkeymap"
    bl_label = "Remove Pentablet keyMaps" 

    def execute(self, context):

        for km, kmi in addon_keymapstemp:
            
            wm = bpy.context.window_manager
            
            km.keymap_items.remove(kmi)

        addon_keymapstemp.clear()
        self.report({'INFO'}, "Experimental Pentablet Shortcuts Disabled")
        #print(addon_keymapstemp)
        return {'FINISHED'}   


#Controlar texturas estencils con teclado en modo Texture Paint

addon_keymap_estencil_temp = [] 

class Add_keymap_estencil_normal(bpy.types.Operator):
    """Control Stencils with keyboard"""
    bl_idname = "add.estencilkeymap"
    bl_label = "Enable Stencil Shotcuts"
    
    # Con estas lineas evaluamos si estamos en modo Texture Paint  :)  
    @classmethod
    def poll(cls, context):
        return bpy.context.mode == 'PAINT_TEXTURE'

    #Si estamos en modo Texture Paint entonces continuemos :)
    def execute(self, context):

        wm = bpy.context.window_manager
        
        for km, kmi in addon_keymap_estencil_temp:
            
            wm = bpy.context.window_manager
            
            km.keymap_items.remove(kmi)

        addon_keymap_estencil_temp.clear()
        
        
        #Controles estencil normal :)
        
        km= wm.keyconfigs.addon.keymaps.new(name="Image Paint")
        kmi = km.keymap_items.new('brush.stencil_control', 'Q', 'PRESS')
        kmi.properties.mode= 'TRANSLATION'
        addon_keymap_estencil_temp.append((km, kmi))
        
        km= wm.keyconfigs.addon.keymaps.new(name="Image Paint")
        kmi = km.keymap_items.new('brush.stencil_control', 'W', 'PRESS')
        kmi.properties.mode= 'SCALE'
        addon_keymap_estencil_temp.append((km, kmi))
        
        km= wm.keyconfigs.addon.keymaps.new(name="Image Paint")
        kmi = km.keymap_items.new('brush.stencil_control', 'Q', 'PRESS', shift=True)
        kmi.properties.mode= 'ROTATION'
        addon_keymap_estencil_temp.append((km, kmi))
        
        self.report({'INFO'}, "Stencil Shortcuts Enabled") 
        #print(tuple(addon_keymapstemp))
        return {'FINISHED'}


class Add_keymap_estencil_mask(bpy.types.Operator):
    """Control Stencils Mask with keyboard"""
    bl_idname = "add.estencilmaskkeymap"
    bl_label = "Enable Stencil Mask Shortcuts"
    
    # Con estas lineas evaluamos si estamos en modo Texture Paint :) 
    @classmethod
    def poll(cls, context):
        return bpy.context.mode == 'PAINT_TEXTURE'

    #Si estamos en modo texture paint entonces continuemos :)
    
    def execute(self, context):

        wm = bpy.context.window_manager
        
        for km, kmi in addon_keymap_estencil_temp:
            
            wm = bpy.context.window_manager
            
            km.keymap_items.remove(kmi)

        addon_keymap_estencil_temp.clear()
        
        
        #Controles estencil Mask :)
        
        km= wm.keyconfigs.addon.keymaps.new(name="Image Paint")
        kmi = km.keymap_items.new('brush.stencil_control', 'Q', 'PRESS')
        kmi.properties.mode= 'TRANSLATION'
        kmi.properties.texmode= 'SECONDARY'## Changed 2016
        addon_keymap_estencil_temp.append((km, kmi))
        
        km= wm.keyconfigs.addon.keymaps.new(name="Image Paint")
        kmi = km.keymap_items.new('brush.stencil_control', 'W', 'PRESS')
        kmi.properties.mode= 'SCALE'
        kmi.properties.texmode= 'SECONDARY'## Changed 2016
        addon_keymap_estencil_temp.append((km, kmi))
        
        km= wm.keyconfigs.addon.keymaps.new(name="Image Paint")
        kmi = km.keymap_items.new('brush.stencil_control', 'Q', 'PRESS', shift=True)
        kmi.properties.mode= 'ROTATION'
        kmi.properties.texmode= 'SECONDARY'## Changed 2016
        addon_keymap_estencil_temp.append((km, kmi))
        
        self.report({'INFO'}, "Stencil Mask Shortcuts Enabled") 
        #print(tuple(addon_keymapstemp))
        return {'FINISHED'}
    
    

#Remueve los atajos para controlar las texturas stencil con el teclado :)  
       
class Remove_allestencilkeymaps(bpy.types.Operator): 
    """Remove Stencil all Shortcuts"""
    bl_idname = "remove.estencilkeymaps"
    bl_label = "Remove All Stencil Shorcuts" 

    # Con estas lineas evaluamos si estamos en modo Texture Paint :)
    @classmethod
    def poll(cls, context):
        return bpy.context.mode == 'PAINT_TEXTURE'

    #Si estamos en modo texture paint entonces continuemos :)
    
    def execute(self, context):

        for km, kmi in addon_keymap_estencil_temp:
            
            wm = bpy.context.window_manager
            
            km.keymap_items.remove(kmi)

        addon_keymap_estencil_temp.clear()
        self.report({'INFO'}, "All Stencil Shorcuts Disabled")
        #print(addon_keymapstemp)
        return {'FINISHED'}   
    
    
    
#Project Paint Options ON 

class ProjectPaintOptions_ON(bpy.types.Operator):
    """Enable Occlude, Cull, Normal Options in Texture Paint Mode""" 
    bl_idname = "projectpaint.optionson"
    bl_label = "Project Paint Options ON"

    def execute(self, context):

        bpy.context.scene.tool_settings.image_paint.use_occlude = True
        bpy.context.scene.tool_settings.image_paint.use_backface_culling = True
        bpy.context.scene.tool_settings.image_paint.use_normal_falloff = True

        self.report({'INFO'}, "Project Paint Options ON")
        
        return {'FINISHED'} 
    

#Project Paint Options OFF

class ProjectPaintOptions_OFF(bpy.types.Operator):
    """Disable Occlude, Cull, Normal Options in Texture Paint Mode""" 
    bl_idname = "projectpaint.optionsoff"
    bl_label = "Project Paint Options OFF"

    def execute(self, context):

        bpy.context.scene.tool_settings.image_paint.use_occlude = False
        bpy.context.scene.tool_settings.image_paint.use_backface_culling = False
        bpy.context.scene.tool_settings.image_paint.use_normal_falloff = False

        self.report({'INFO'}, "Project Paint Options OFF")
        return {'FINISHED'} 
    

#Project Paint Bleed Option = 8px

class TexturePaint_Bleed10(bpy.types.Operator):
    """Set Texture Paint Bleed Option to 10px""" 
    bl_idname = "texturepaint.bleed10"
    bl_label = "Set Texture Paint Bleed 10px"

    def execute(self, context):

        bpy.context.scene.tool_settings.image_paint.seam_bleed = 10 

        self.report({'INFO'}, "Bleed Option Changed to 10px")
        return {'FINISHED'} 
    
    
    
    
    
#---------------- Draw the Panel -------------------------

# Clase que define en que lugares mostrar el panel Pentablet Tools

class VerPanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Pentablet"

    @classmethod
    def poll(cls, context):
        return (bpy.context.mode == 'OBJECT' or bpy.context.mode == 'EDIT_MESH' or bpy.context.mode == 'PAINT_TEXTURE' or bpy.context.mode == 'SCULPT')# Muestra el panel Pentablet Tools unicamente en modo objeto,modo edicion y texture paint


# dibujando el panel

class H_pentablet(VerPanel,bpy.types.Panel):
    bl_label = "Pentablet Tools"
    bl_idname = "use.pentablet"
    
    def draw(self,context):
        
        layout = self.layout
        
        #if bpy.context.mode == 'OBJECT':
        layout.prop(bpy.context.scene, "use_pentablet", text="Use Pentablet", icon="GREASEPENCIL")
        
  
        layout.label(".............................................................................................................................................................................")

        if bpy.context.scene.use_pentablet == True:
            bpy.context.user_preferences.inputs.select_mouse='LEFT'
            bpy.context.user_preferences.inputs.use_mouse_emulate_3_button= True 
            bpy.context.user_preferences.edit.use_drag_immediately= True
         
            
        if bpy.context.scene.use_pentablet == False:
            bpy.context.user_preferences.inputs.select_mouse='RIGHT'
            bpy.context.user_preferences.inputs.use_mouse_emulate_3_button= False 
            bpy.context.user_preferences.edit.use_drag_immediately= False # 
                
        
        
        if bpy.context.mode == 'PAINT_TEXTURE':
            #layout.label("......................................................................................................................................................")
            
            col = layout.column(align=True)
            
            col.label("Enable Stencil Shorcuts:")
            
            row = col.row(align=True) 
            row.operator("add.estencilkeymap", text="Texture")
            row.operator("add.estencilmaskkeymap", text="Texture Mask")
            col.operator("remove.estencilkeymaps", text="Disable Stencil Shortcuts")
            col.separator()
            
            col.label("Project Paint Options:")
            row = col.row(align=True) 
            row.operator("projectpaint.optionson", text="ON")
            row.operator("projectpaint.optionsoff", text="OFF")
            
            col.separator()
            
            #col.label("Poject Paint Options:")
            col.operator("texturepaint.bleed10", text="Set Bleed to 10px")
            #col.separator()
            col.operator("image.save_dirty", text="Save All Images")
            
            col.label("............................................................................................................................................................")
            

        if bpy.context.mode == 'OBJECT' or bpy.context.mode == 'EDIT_MESH':
            #layout.label("......................................................................................................................................................")
            
            col = layout.column(align=True)
            
            col.label("Custom Drag Offset:")
            col.prop(inputs, "tweak_threshold",  text= "Drag Value")
            row = col.row(align=True)
            row.operator("min.dragoffset", text="Min")#icon="EDIT"
            row.operator("max.dragoffset", text="Max")#icon="FREEZE"
            col.operator("default.dragoffset", icon="BLANK1", text="Default")
        
        
        if bpy.context.mode == 'EDIT_MESH':
            
            #col.label("..........................................................................................................................................................")
            
            layout = self.layout            
            col = layout.column(align=True)

            col.label(text="Double Click:")
            
            col.prop(inputs, "mouse_double_click_time", text="Speed")
            
            row = col.row(align=True)
            row.operator("double.clickpreset", text="Slow")
            row.operator("double.clickpreset1", text="Fast")
            col.operator("double.clickdefault", text="Default", icon="BLANK1")
            
            #col.separator()
            #col.label(text="Drag value:")
            #col.prop(inputs, "drag_threshold", slider= True)
            
        if bpy.context.mode == 'EDIT_MESH':
            
            # Vertices Color ------------------------
            col.separator()
            col.label("Vertex Size:")
               
            
            row = col.row(align=True)
            row.operator("vertex.sizetres", text="3")
            row.operator("vertex.sizecuatro", text="4")
            row.operator("vertex.sizeseis", text="6")
            #row = col.row(align=True)
            row.operator("vertex.sizeocho", text="8")
            row.operator("vertex.sizediez", text="10")
            
            # Wireframe Color ------------------------
            col.separator()
            col.label("Wireframe Color:")
            row = col.row(align=True)
                        
            row.operator("wire.blue", text="Blue")
            row.operator("wire.black", text="Black")
            row = col.row(align=True)
            row.operator("wire.lightblue", text="Light Blue")
            row.operator("wire.gray", text="Gray")
            
            #Experimental Keymaps
            
            layout = self.layout            
            col = layout.column(align=True)

            col.label(text="Pentablet Shortcuts:")
            row = col.row(align=True)
            row.operator("add.experimentalkeymap", text="ON")
            row.operator("remove.experimentalkeymap", text="OFF")
            
            
            
            
            
            
            col.label(".......................................................................................................................................................................................................................")



#------------------------- Lock and Unlock Objects ----------------------------------------------------

        if bpy.context.mode == 'OBJECT':
            
            col.label(".......................................................................................................................................................................................................................")
            
            layout.label("Object Tools:")
            
            col = layout.column(align=True)
            row = col.row(align=True)
            row.operator("set.pentabletgroup", text= "Lock Objects")
            
            
            row = col.row(align=True)
            row.operator("unset.pentabletgroup", text= "Unlock Objects")
            col.separator()
            col.operator("fixnormals.inobjectmode", text="Fix Normals")

#------------------------- X-Ray options ----------------------------------------------------        
        if bpy.context.mode == 'OBJECT' or bpy.context.mode == 'EDIT_MESH':
                    
            col.separator()
            col.label(text="Set X-Ray:")
            row = col.row(align=True)
            row = col.row(align=True)
            row.operator("retopo.helperon", text="ON")
            row.operator("retopo.helperoff", text="OFF")


        if bpy.context.mode == 'OBJECT' or bpy.context.mode == 'EDIT_MESH' or bpy.context.mode == 'PAINT_TEXTURE' or bpy.context.mode == 'SCULPT':
#---------------------- Opciones para cambiar tema y atajos de teclado ------------------------------------
       
            layout.label("Change Keymap:") 

            
            row = layout.row()
            layout = self.layout
            theme = context.user_preferences.themes[0] 
            split_themes = layout.split()
            sub = split_themes.column()
            subrow = sub.row(align=True)
            #text= USERPREF_MT_interface_theme_presets.bl_label
            
           
            subrow = sub.row(align=True)
            subrow.menu("USERPREF_MT_interface_theme_presets",text="Change Theme")#Lista todos los temas disponibles

            wm = context.window_manager
            kc = wm.keyconfigs.user
            spref = context.space_data
            text = bpy.path.display_name(wm.keyconfigs.active.name)


            row.menu("USERPREF_MT_keyconfigs", text=text) #Lista todos las configuraciones de teclado disponibles
            
            sub.separator() 


# --------------- --------- Dibujando Algunos Menus --------------------------------------------------


# estructura de menu para operadores de snap y camara :) 
    
def menu_snaper(self, context):
    
    if bpy.context.object.mode == 'EDIT':
        
        obj = bpy.context.active_object.data
        
        layout = self.layout
        layout.separator()
        layout.operator("set.origenaselection", text="Origin to Selection")
        layout.operator("set.origentocursor3d", text="Origin to 3D Cursor")
        
    
    elif bpy.context.object.mode == 'OBJECT':
        layout = self.layout
        layout.separator()
        layout.operator("center.cursor3d", text="Origin to 3D Cursor")
        layout.operator("set.origentogeo", text="Origin to Geometry")



def Camera_Ops(self, context):
    
    view3d = context.space_data.region_3d
    view = context.space_data
    ob = context.active_object
    
    if view3d.view_perspective == 'CAMERA':
        layout = self.layout
        layout.separator()
        layout.operator("set.camrenderborder", text="Camera Render Border", icon="RENDER_REGION")
        layout.operator("unset.camrenderborder", text="Clear Camera Render Border", icon="X")
        layout.prop(view, "lock_camera")
        #layout.prop(ob, "name", text="", icon='OBJECT_DATA')


# estructura de menu de opciones adicionales en el menu Specials de los objetos 'w' :) 
        
def Object_Ops(self, context):
    
    ob = context.active_object

    if bpy.context.object.type == 'MESH' and bpy.context.object.mode == 'OBJECT':
        layout = self.layout
        layout.separator()
        layout.operator("fixnormals.inobjectmode", text="Fix Normals")
        

    if bpy.context.object.mode == 'OBJECT':
        layout = self.layout
        layout.separator()
        ob = context.active_object
        layout.operator("set.pentabletgroup", text= "Lock Objects")
        
        #if bpy.context.scene.pentablet_group == True:
        layout.operator("unset.pentabletgroup", text= "Unlock Objects")
            
        layout.separator()
        ob = context.active_object    
        layout.prop(ob, "name", text="", icon='OBJECT_DATA')


        
addon_keymaps = [] # almacena los atajos de teclado que se crean mas adelante

# --------------- --------- Registro del Addon -------------------------------------------------- 
            
def register():
    bpy.utils.register_class(H_pentablet)
    bpy.utils.register_class(SetORG_Cursor_OBJ)
    bpy.utils.register_class(SetORG_Cursor_EDIT)
    bpy.utils.register_class(SetORG_SELEC)
    bpy.utils.register_class(SetORGN_GEO)
    bpy.utils.register_class(Drag_Min)
    bpy.utils.register_class(Drag_Max)
    bpy.utils.register_class(Drag_DEF)
    bpy.utils.register_class(Fix_NRMLS_OBJ)
    bpy.utils.register_class(SetBorder_R)
    bpy.utils.register_class(UnsetBorder_R)
    bpy.utils.register_class(H_DoubleClick_D)
    bpy.utils.register_class(H_DoubleClick_P)
    bpy.utils.register_class(H_DoubleClick_P1)
    
    bpy.utils.register_class(vertex_3)
    bpy.utils.register_class(vertex_4)
    bpy.utils.register_class(vertex_6)
    bpy.utils.register_class(vertex_8)
    bpy.utils.register_class(vertex_10)
    bpy.utils.register_class(wire_blue)
    bpy.utils.register_class(wire_LBlue)
    bpy.utils.register_class(wire_gray)
    bpy.utils.register_class(wire_black)   
    
    bpy.utils.register_class(Set_Pentablet_GRP)
    bpy.utils.register_class(Unset_Pentablet_GRP)
    bpy.utils.register_class(Retopo_HelperON)
    bpy.utils.register_class(Retopo_HelperOFF)
    bpy.utils.register_class(Set_Selectable_OBJ)
    
    # Nuevos Addons
    bpy.utils.register_class(Add_keymapstemp)
    bpy.utils.register_class(Remove_keymapstemp)
    bpy.utils.register_class(ProjectPaintOptions_ON)
    bpy.utils.register_class(ProjectPaintOptions_OFF)
    bpy.utils.register_class(TexturePaint_Bleed10)
    
    #modificaciones 2016     
    
    bpy.utils.register_class(Add_keymap_estencil_normal)
    bpy.utils.register_class(Add_keymap_estencil_mask)
    bpy.utils.register_class(Remove_allestencilkeymaps)
    
    
    #importa los menus
    bpy.types.VIEW3D_MT_snap.append(menu_snaper)
    bpy.types.VIEW3D_MT_object_specials.append(Camera_Ops)
    bpy.types.VIEW3D_MT_object_specials.append(Object_Ops)



#------------- ----------- Creacion Atajos de Teclado--------------- ------- --------------------------

    wm = bpy.context.window_manager

    km= wm.keyconfigs.addon.keymaps.new(name="Mesh")
    kmi = km.keymap_items.new('mesh.loop_select', 'SELECTMOUSE', 'DOUBLE_CLICK')
    kmi.properties.extend= False
    kmi.properties.deselect= False
    kmi.properties.toggle= False
    addon_keymaps.append((km, kmi))

    km= wm.keyconfigs.addon.keymaps.new(name="Mesh")
    kmi = km.keymap_items.new('mesh.loop_select', 'SELECTMOUSE', 'DOUBLE_CLICK', shift=True)
    kmi.properties.extend= True
    kmi.properties.deselect= False
    kmi.properties.toggle= False
    addon_keymaps.append((km, kmi))

    km= wm.keyconfigs.addon.keymaps.new(name="Mesh")
    kmi = km.keymap_items.new('mesh.loop_select', 'SELECTMOUSE', 'DOUBLE_CLICK', ctrl= True, shift=True)
    kmi.properties.extend= False
    kmi.properties.deselect= True
    kmi.properties.toggle= False
    addon_keymaps.append((km, kmi))

    km= wm.keyconfigs.addon.keymaps.new(name="Mesh")
    kmi = km.keymap_items.new('view3d.select_lasso', 'EVT_TWEAK_S', 'ANY', shift=True, ctrl=True)
    addon_keymaps.append((km, kmi))

    km= wm.keyconfigs.addon.keymaps.new(name="Curve")
    kmi = km.keymap_items.new('curve.vertex_add', 'EVT_TWEAK_S', 'ANY', ctrl=True)
    addon_keymaps.append((km, kmi))

    km= wm.keyconfigs.addon.keymaps.new(name="Object Mode")
    kmi = km.keymap_items.new('view3d.select_lasso', 'EVT_TWEAK_S', 'ANY', shift=True, ctrl=True)
    addon_keymaps.append((km, kmi))

    km= wm.keyconfigs.addon.keymaps.new(name="UV Editor")
    kmi = km.keymap_items.new('uv.select_loop', 'SELECTMOUSE', 'DOUBLE_CLICK')
    kmi.properties.extend= True
    addon_keymaps.append((km, kmi))

    km= wm.keyconfigs.addon.keymaps.new(name="UV Editor")
    kmi = km.keymap_items.new('uv.select_lasso', 'EVT_TWEAK_S', 'ANY', shift=True, ctrl=True)
    kmi.properties.extend= True
    addon_keymaps.append((km, kmi))


    
    
    
    

#---------------------- Borra todos los operadores cuando se desactiva el addon --------------------------

def unregister():
    bpy.utils.unregister_class(H_pentablet)
    bpy.utils.unregister_class(SetORG_Cursor_OBJ)
    bpy.utils.unregister_class(SetORG_Cursor_EDIT)
    bpy.utils.unregister_class(SetORG_SELEC)
    bpy.utils.unregister_class(SetORGN_GEO)
    bpy.utils.unregister_class(Drag_Min)
    bpy.utils.unregister_class(Drag_Max)
    bpy.utils.unregister_class(Drag_DEF)
    bpy.utils.unregister_class(Fix_NRMLS_OBJ)
    bpy.utils.unregister_class(SetBorder_R)
    bpy.utils.unregister_class(UnsetBorder_R)
    bpy.utils.unregister_class(H_DoubleClick_D)
    bpy.utils.unregister_class(H_DoubleClick_P)
    bpy.utils.unregister_class(H_DoubleClick_P1)
    bpy.utils.unregister_class(vertex_3)
    bpy.utils.unregister_class(vertex_4)
    bpy.utils.unregister_class(vertex_6)
    bpy.utils.unregister_class(vertex_8)
    bpy.utils.unregister_class(vertex_10)
    bpy.utils.unregister_class(wire_blue)
    bpy.utils.unregister_class(wire_LBlue)
    bpy.utils.unregister_class(wire_gray)
    bpy.utils.unregister_class(wire_black)
    
    bpy.utils.unregister_class(Set_Pentablet_GRP)
    bpy.utils.unregister_class(Unset_Pentablet_GRP)
    bpy.utils.unregister_class(Retopo_HelperON)
    bpy.utils.unregister_class(Retopo_HelperOFF)
    bpy.utils.unregister_class(Set_Selectable_OBJ)
    
    # Nuevos Addons
    bpy.utils.unregister_class(Add_keymapstemp)
    bpy.utils.unregister_class(Remove_keymapstemp)
    bpy.utils.unregister_class(ProjectPaintOptions_ON)
    bpy.utils.unregister_class(ProjectPaintOptions_OFF)
    bpy.utils.unregister_class(TexturePaint_Bleed10)
    
    #modificaciones 2016     
    
    bpy.utils.unregister_class(Add_keymap_estencil_normal)
    bpy.utils.unregister_class(Add_keymap_estencil_mask)
    bpy.utils.unregister_class(Remove_allestencilkeymaps)

    #remueve los menus
    bpy.types.VIEW3D_MT_snap.remove(menu_snaper)
    bpy.types.VIEW3D_MT_object_specials.remove(Camera_Ops)
    bpy.types.VIEW3D_MT_object_specials.remove(Object_Ops)


    #Remueve los atajos de teclado Nuevos
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear() 


if __name__ == "__main__":
    register()  

# Fin? XD 
# Geek Blenderiano \(ᶺ__ᶺ)/
