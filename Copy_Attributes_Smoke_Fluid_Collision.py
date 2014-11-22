import bpy

bl_info = {
    "name": "Copy Attributes Smoke Collision and Fluid Obstacle",
    "description": "Copy Attributes from Smoke Collision and Fluid Obstacle from active to selected objects",
    "author": "Tiago Werner Schreiner",
    "version": (1,0),
    "blender": (2, 71, 0),
    "location": "View3D > Toolbar > Physics",    
    "category": "3D View"
}

# Copia os atributos de colisao de Smoke
def copySmokeCollision():
    ind = 0
    #verifica em que inidice o modificador Smoke esta
    for mod in bpy.context.object.modifiers:
        if mod.name == 'Smoke':
            indMod = ind
            #salva o tipo de colisao que o objecto ativo tem
            tipoColl = bpy.context.object.modifiers[ind].coll_settings.collision_type
        ind = ind + 1 
    
    #percorre os objetos selecionados
    for obj in bpy.context.selected_objects:
        #torna o objeto selecionado no objeto ativo
        bpy.context.scene.objects.active = obj
        #adiciona o modificador Smoke    
        bpy.ops.object.modifier_add(type='SMOKE')
        #adiciona a colisao
        obj.modifiers[indMod].smoke_type = 'COLLISION'
        #adiciona o tipo de colisao
        bpy.context.object.modifiers[indMod].coll_settings.collision_type = tipoColl
        

# Copia os atributos dos obstaculos dos Fluidos
def copyFluidCollision():
    ind = 0
    #verifica em que indice o modificador Fluid esta
    for mod in bpy.context.object.modifiers:
        if mod.name == 'Fluidsim':
            indMod = ind
            #salva as info do modificador
            volumeIni = bpy.context.object.modifiers[ind].settings.volume_initialization
            AnimMesh  = bpy.context.object.modifiers[ind].settings.use_animated_mesh
            if AnimMesh == False:
                slipType = bpy.context.object.modifiers[ind].settings.slip_type
                if slipType == 'PARTIALSLIP': 
                    amountPartial = bpy.context.object.modifiers[ind].settings.partial_slip_factor
            impactFactor = bpy.context.object.modifiers[ind].settings.impact_factor
        ind = ind + 1
    
    #percorre os objetos selecionados
    for obj in bpy.context.selected_objects:
        #torna o objecto selecionado em objeto ativo
        bpy.context.scene.objects.active = obj
        #adiciona o modificador Fluid
        bpy.ops.object.modifier_add(type='FLUID_SIMULATION')
        #adiciona o obstaculo
        obj.modifiers[indMod].settings.type = 'OBSTACLE'
        #insere as informacoes salvas do objeto ativo por primero
        bpy.context.object.modifiers[indMod].settings.volume_initialization = volumeIni 
        bpy.context.object.modifiers[indMod].settings.use_animated_mesh = AnimMesh
        if AnimMesh == False:
            bpy.context.object.modifiers[indMod].settings.slip_type = slipType
            if slipType == 'PARTIALSLIP':
                bpy.context.object.modifiers[indMod].settings.partial_slip_factor = amountPartial
        bpy.context.object.modifiers[indMod].settings.impact_factor = impactFactor


#Cria o operador para copiar os atributos do Smoke
class CopySmokeCollOp(bpy.types.Operator):
    bl_idname = "object.copy_smoke_coll"
    bl_label  = "Copy Smoke Collision Attribut"
    bl_description = "Copy Attributes Smoke Collision from Active to Selected"
    
    def execute(self, context):
        copySmokeCollision()
        return {'FINISHED'}

#Cria o operador para copiar os atributos do Fluid
class CopyFluidObst(bpy.types.Operator):
    bl_idname = "object.copy_fluid_obst"
    bl_label  = "Copy Fluid Obstacle Attribut" 
    bl_description = "Copy Attributes Fluid Obstacle from Active to Selected"
    
    def execute(self, context):
        copyFluidCollision()
        return {'FINISHED'}

#Cria o Painel
class CopyPhysicsAtt(bpy.types.Panel):
    bl_label = "Copy Attribute from Smoke or Fluid Collision"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Physics'  

    #Desenha o layout
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Copy Selected from Active:")

        split = layout.split()
        col = split.column(align=True)

        col.operator("object.copy_smoke_coll", text="Copy Smoke Collision Atttributes", icon='MOD_SMOKE')
        col.operator("object.copy_fluid_obst", text="Copy Fluid Obstacle Attributes", icon='MOD_FLUIDSIM')

#Registra o Painel e os operadores Criados
def register():
    bpy.utils.register_class(CopyPhysicsAtt)
    bpy.utils.register_class(CopySmokeCollOp)
    bpy.utils.register_class(CopyFluidObst)

def unregister():
    bpy.utils.unregister_class(CopyPhysics)

if __name__ == "__main__":
    register()






