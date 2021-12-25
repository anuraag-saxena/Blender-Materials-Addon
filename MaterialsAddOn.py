bl_info = {
    "name" : "Materials AddOn",
    "author" : "Anuraag",
    "version" : (0, 1, 0),
    "blender" : (2, 93, 6),
    "location" : "View3d > Toolshelf",
    "desciption" : "Includes various materials",
    "warning" : "",
    "wiki_url" : "",
    "category" : "Add Shader",
}


### Precious Metals
# Gold - # metal, rusty, nugget 
# silver - # metal, rusty, nugget 
###
# Metal - # metal, damaged, galvanized, nugget, rusty, scratched
###
# winter - # candy, snow, Gingerbread



import bpy


def hex_to_rgb( hex_value ):
    b = (hex_value & 0xFF) / 255.0
    g = ((hex_value >> 8) & 0xFF) / 255.0
    r = ((hex_value >> 16) & 0xFF) / 255.0
    return r, g, b


###################### PANELS ############################
class PRECIOUS_METALS(bpy.types.Panel):
    bl_label = "Precious Metals"
    bl_idname = "SHADER_PT_PRECIOUS_METALS"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Materials"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        row.label(text="Gold")
        row = layout.row()
        row.operator("shader.gold_metal_operator")
        row.operator("shader.gold_rusted_operator")
        row.operator("shader.gold_nugget_operator")
        row = layout.row()
        row.label(text="Silver")
        row = layout.row()
        row.operator("shader.silver_metal_operator")
        row.operator("shader.silver_rusted_operator")
        row.operator("shader.silver_nugget_operator")
        

class GENERAL_METAL(bpy.types.Panel):
    bl_label = "General Metal"
    bl_idname = "SHADER_PT_GENERAL_METAL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Materials"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        row.operator("shader.general_metal_operator")
        row.operator("shader.metal_rusty_operator")
        row.operator("shader.metal_nugget_operator")
        row = layout.row()
        row.operator("shader.metal_galvanized_operator")
        row.operator("shader.chrome_operator")
        row = layout.row()
        row.operator("shader.metal_damaged_operator")
        row.operator("shader.metal_scratched_operator")
        

class WINTER(bpy.types.Panel):
    bl_label = "Winter"
    bl_idname = "SHADER_PT_WINTER"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Materials"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        row.operator("shader.candy_operator")
        row.operator("shader.snow_operator")
        row = layout.row()
        row.operator("shader.gingerbread_operator")



###################### GOLD ######################
class SHADER_OT_GOLD_METAL(bpy.types.Operator):
    bl_label = "Metal"
    bl_idname = "shader.gold_metal_operator"
    
    def execute(self, context):
        material_gold_metal = bpy.data.materials.new(name="Gold Metal")
        material_gold_metal.use_nodes = True
        
        prinicpled_bsdf = material_gold_metal.node_tree.nodes.get("Principled BSDF")
        prinicpled_bsdf.inputs[4].default_value = 1
        prinicpled_bsdf.inputs[7].default_value = 0.27
        
        material_output = material_gold_metal.node_tree.nodes.get("Material Output")
        
        colorramp1_node = material_gold_metal.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-400, 200)
        colorramp1_node.color_ramp.elements[0].color = (0.610, 0.337, 0.084, 1)
        colorramp1_node.color_ramp.elements[1].color = (0.279, 0.098, 0.025, 1)
        
        musgrave1_node = material_gold_metal.node_tree.nodes.new("ShaderNodeTexMusgrave")
        musgrave1_node.location = (-700, 200)
        musgrave1_node.inputs[2].default_value = 400
        musgrave1_node.inputs[3].default_value = 16
        musgrave1_node.inputs[4].default_value = 0
        
        mapping1_node = material_gold_metal.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-1000, 200)
        
        texcoord1_node = material_gold_metal.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-1300, 200)
        
        noise1_node = material_gold_metal.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-700, -200)
        noise1_node.inputs[2].default_value = 12
        noise1_node.inputs[3].default_value = 16
        noise1_node.inputs[4].default_value = 0.45
        
        bump1_node = material_gold_metal.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (-400, -200)
        bump1_node.inputs[0].default_value = 0.008
        
        material_gold_metal.node_tree.links.new(colorramp1_node.outputs[0], prinicpled_bsdf.inputs[0])
        material_gold_metal.node_tree.links.new(musgrave1_node.outputs[0], colorramp1_node.inputs[0])
        material_gold_metal.node_tree.links.new(mapping1_node.outputs[0], musgrave1_node.inputs[0])
        material_gold_metal.node_tree.links.new(mapping1_node.outputs[0], noise1_node.inputs[0])
        material_gold_metal.node_tree.links.new(texcoord1_node.outputs[3], mapping1_node.inputs[0])
        material_gold_metal.node_tree.links.new(noise1_node.outputs[0], bump1_node.inputs[2])
        material_gold_metal.node_tree.links.new(bump1_node.outputs[0], prinicpled_bsdf.inputs[20])
        
        bpy.context.object.active_material = material_gold_metal
        return {"FINISHED"}
    
    


class SHADER_OT_GOLD_RUSTED(bpy.types.Operator):
    bl_label = "Rusty"
    bl_idname = "shader.gold_rusted_operator"
    
    def execute(self, context):
        material_gold_rusted = bpy.data.materials.new(name="Gold Rusted")
        material_gold_rusted.use_nodes = True
        
        material_output = material_gold_rusted.node_tree.nodes.get("Material Output")
        material_output.location = (300, 200)
        
        mixshader1_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeMixShader")        
        mixshader1_node.location = (100, 200)
        
        colorramp1_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-900, 200)
        colorramp1_node.color_ramp.elements[0].position = 0.520
        colorramp1_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp1_node.color_ramp.elements[1].position = 0.644
        colorramp1_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        noise1_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-1500, 200)
        noise1_node.inputs[2].default_value = 1.3
        noise1_node.inputs[3].default_value = 16
        noise1_node.inputs[4].default_value = 0.615
        noise1_node.inputs[5].default_value = 0
        
        principled_bsdf1 = material_gold_rusted.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (-300, -200)
        principled_bsdf1.inputs[4].default_value = 1
        
        colorramp2_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp2_node.location = (-900, -180)
        colorramp2_node.color_ramp.elements[0].position = 0.362
        colorramp2_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp2_node.color_ramp.elements[1].position = 0.513
        colorramp2_node.color_ramp.elements[1].color = (0.799, 0.558, 0.133, 1)
        
        colorramp3_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp3_node.location = (-900, -450)
        colorramp3_node.color_ramp.elements[0].position = 0.468
        colorramp3_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp3_node.color_ramp.elements[1].position = 0.827
        colorramp3_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        bump1_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (-600, -750)
        bump1_node.inputs[0].default_value = 0.518
        bump1_node.inputs[1].default_value = 1
        
        colorramp4_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp4_node.location = (-900, -750)
        colorramp4_node.color_ramp.elements[0].position = 0
        colorramp4_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp4_node.color_ramp.elements[1].position = 0.506
        colorramp4_node.color_ramp.elements[1].color = (1, 1, 1, 1)
          
        bump2_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeBump")
        bump2_node.location = (-900, -1100)
        bump2_node.inputs[0].default_value = 0.106
        bump2_node.inputs[1].default_value = 1
        
        noise2_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeTexNoise")
        noise2_node.location = (-1500, -450)
        noise2_node.inputs[2].default_value = 1
        noise2_node.inputs[3].default_value = 16
        noise2_node.inputs[4].default_value = 0.708
        noise2_node.inputs[5].default_value = 0
        
        noise3_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeTexNoise")
        noise3_node.location = (-1500, -1100)
        noise3_node.inputs[2].default_value = 1
        noise3_node.inputs[3].default_value = 16
        noise3_node.inputs[4].default_value = 0.9
        noise3_node.inputs[5].default_value = 0
        
        principled_bsdf2 = material_gold_rusted.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        principled_bsdf2.location = (-300, -1350)
        principled_bsdf2.inputs[7].default_value = 1
        
        colorramp5_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp5_node.location = (-900, -1350)
        colorramp5_node.color_ramp.elements[0].position = 0.141
        colorramp5_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp5_node.color_ramp.elements[1].position = 0.734
        colorramp5_node.color_ramp.elements[1].color = (0.694, 0.279, 0, 1)
        
        bump3_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeBump")
        bump3_node.location = (-900, -1650)
        bump3_node.inputs[0].default_value = 1
        bump3_node.inputs[1].default_value = 1
        
        mapping1_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-1800, -450)
        
        textcoord1_node = material_gold_rusted.node_tree.nodes.new("ShaderNodeTexCoord")
        textcoord1_node.location = (-2000, -450)
        
        material_gold_rusted.node_tree.links.new(mixshader1_node.outputs[0], material_output.inputs[0])
        material_gold_rusted.node_tree.links.new(colorramp1_node.outputs[0], mixshader1_node.inputs[0])
        material_gold_rusted.node_tree.links.new(principled_bsdf1.outputs[0], mixshader1_node.inputs[1])
        material_gold_rusted.node_tree.links.new(noise1_node.outputs[0], colorramp1_node.inputs[0])
        material_gold_rusted.node_tree.links.new(colorramp2_node.outputs[0], principled_bsdf1.inputs[0])
        material_gold_rusted.node_tree.links.new(colorramp3_node.outputs[0], principled_bsdf1.inputs[7])
        material_gold_rusted.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])
        material_gold_rusted.node_tree.links.new(colorramp4_node.outputs[0], bump1_node.inputs[2])
        material_gold_rusted.node_tree.links.new(noise2_node.outputs[0], colorramp2_node.inputs[0])
        material_gold_rusted.node_tree.links.new(noise2_node.outputs[0], colorramp3_node.inputs[0])
        material_gold_rusted.node_tree.links.new(noise2_node.outputs[0], colorramp4_node.inputs[0])
        material_gold_rusted.node_tree.links.new(bump2_node.outputs["Normal"], bump1_node.inputs["Normal"])
        material_gold_rusted.node_tree.links.new(noise3_node.outputs[0], bump2_node.inputs[2])
        material_gold_rusted.node_tree.links.new(principled_bsdf2.outputs[0], mixshader1_node.inputs[2])
        material_gold_rusted.node_tree.links.new(colorramp5_node.outputs[0], principled_bsdf2.inputs[0])
        material_gold_rusted.node_tree.links.new(bump3_node.outputs[0], principled_bsdf2.inputs[19])
        material_gold_rusted.node_tree.links.new(noise1_node.outputs[0], colorramp5_node.inputs[0])
        material_gold_rusted.node_tree.links.new(noise1_node.outputs[0], bump3_node.inputs[2])
        material_gold_rusted.node_tree.links.new(mapping1_node.outputs[0], noise1_node.inputs["Vector"])
        material_gold_rusted.node_tree.links.new(mapping1_node.outputs[0], noise2_node.inputs["Vector"])
        material_gold_rusted.node_tree.links.new(mapping1_node.outputs[0], noise3_node.inputs["Vector"])
        material_gold_rusted.node_tree.links.new(textcoord1_node.outputs[3], mapping1_node.inputs[0])
        
        bpy.context.object.active_material = material_gold_rusted
        return {"FINISHED"}




class SHADER_OT_GOLD_NUGGET(bpy.types.Operator):
    bl_label = "Nugget"
    bl_idname = "shader.gold_nugget_operator"
    
    def execute(self, context):
        material_gold_nugget = bpy.data.materials.new(name="Gold Nugget")
        material_gold_nugget.use_nodes = True

        material_output = material_gold_nugget.node_tree.nodes.get("Material Output")
        material_output.location = (300, 200)        

        principled_bsdf1 = material_gold_nugget.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (0, 200)
        principled_bsdf1.inputs[4].default_value = 1
        principled_bsdf1.inputs[7].default_value = 0.380

        colorramp1_node = material_gold_nugget.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-300, 200)
        colorramp1_node.color_ramp.elements[0].position = 0
        colorramp1_node.color_ramp.elements[0].color = (0.610, 0.337, 0.084, 1)
        colorramp1_node.color_ramp.elements[1].position = 1
        colorramp1_node.color_ramp.elements[1].color = (0.279, 0.098, 0.025, 1)
        
        bump1_node = material_gold_nugget.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (-300, -200)
        bump1_node.inputs[0].default_value = 0.5
        bump1_node.inputs[1].default_value = 1
        
        musgrave1_node = material_gold_nugget.node_tree.nodes.new("ShaderNodeTexMusgrave")
        musgrave1_node.location = (-600, 200)
        musgrave1_node.inputs[2].default_value = 400
        musgrave1_node.inputs[3].default_value = 16
        musgrave1_node.inputs[4].default_value = 0
        musgrave1_node.inputs[5].default_value = 2
        
        noise1_node = material_gold_nugget.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-600, -200)
        noise1_node.inputs[2].default_value = 10
        noise1_node.inputs[3].default_value = 8
        noise1_node.inputs[4].default_value = 0.45
        noise1_node.inputs[5].default_value = 0              
        
        mapping1_node = material_gold_nugget.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-900, 100)
        
        texcoord1_node = material_gold_nugget.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-1200, 100)
        
        material_gold_nugget.node_tree.links.new(texcoord1_node.outputs[3], mapping1_node.inputs[0])     
        material_gold_nugget.node_tree.links.new(mapping1_node.outputs["Vector"], musgrave1_node.inputs["Vector"])
        material_gold_nugget.node_tree.links.new(mapping1_node.outputs["Vector"], noise1_node.inputs["Vector"])
        material_gold_nugget.node_tree.links.new(musgrave1_node.outputs[0], colorramp1_node.inputs[0])
        material_gold_nugget.node_tree.links.new(noise1_node.outputs[0], bump1_node.inputs[2])
        material_gold_nugget.node_tree.links.new(colorramp1_node.outputs[0], principled_bsdf1.inputs[0])
        material_gold_nugget.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])

        bpy.context.object.active_material = material_gold_nugget
        return {"FINISHED"}






###################### SILVER ######################
class SHADER_OT_SILVER_METAL(bpy.types.Operator):
    bl_label = "Metal"
    bl_idname = "shader.silver_metal_operator"
    
    def execute(self, context):
        material_silver_metal = bpy.data.materials.new(name="Silver Metal")
        material_silver_metal.use_nodes = True
        
        prinicpled_bsdf = material_silver_metal.node_tree.nodes.get("Principled BSDF")
        prinicpled_bsdf.inputs[4].default_value = 1
        prinicpled_bsdf.inputs[7].default_value = 0.27
        
        material_output = material_silver_metal.node_tree.nodes.get("Material Output")
        
        colorramp1_node = material_silver_metal.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-400, 200)
        colorramp1_node.color_ramp.elements[0].color = (0.651, 0.651, 0.651, 1)
        colorramp1_node.color_ramp.elements[1].color = (0.527, 0.527, 0.527, 1)
        
        musgrave1_node = material_silver_metal.node_tree.nodes.new("ShaderNodeTexMusgrave")
        musgrave1_node.location = (-700, 200)
        musgrave1_node.inputs[2].default_value = 400
        musgrave1_node.inputs[3].default_value = 16
        musgrave1_node.inputs[4].default_value = 0
        
        mapping1_node = material_silver_metal.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-1000, 200)
        
        texcoord1_node = material_silver_metal.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-1300, 200)
        
        noise1_node = material_silver_metal.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-700, -200)
        noise1_node.inputs[2].default_value = 12
        noise1_node.inputs[3].default_value = 16
        noise1_node.inputs[4].default_value = 0.45
        
        bump1_node = material_silver_metal.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (-400, -200)
        bump1_node.inputs[0].default_value = 0.008
        
        material_silver_metal.node_tree.links.new(colorramp1_node.outputs[0], prinicpled_bsdf.inputs[0])
        material_silver_metal.node_tree.links.new(musgrave1_node.outputs[0], colorramp1_node.inputs[0])
        material_silver_metal.node_tree.links.new(mapping1_node.outputs[0], musgrave1_node.inputs[0])
        material_silver_metal.node_tree.links.new(mapping1_node.outputs[0], noise1_node.inputs[0])
        material_silver_metal.node_tree.links.new(texcoord1_node.outputs[3], mapping1_node.inputs[0])
        material_silver_metal.node_tree.links.new(noise1_node.outputs[0], bump1_node.inputs[2])
        material_silver_metal.node_tree.links.new(bump1_node.outputs[0], prinicpled_bsdf.inputs[20])
        
        bpy.context.object.active_material = material_silver_metal
        return {"FINISHED"}
    
    


class SHADER_OT_SILVER_RUSTED(bpy.types.Operator):
    bl_label = "Rusty"
    bl_idname = "shader.silver_rusted_operator"
    
    def execute(self, context):
        material_silver_rusted = bpy.data.materials.new(name="Silver Rusted")
        material_silver_rusted.use_nodes = True
        
        material_output = material_silver_rusted.node_tree.nodes.get("Material Output")
        material_output.location = (300, 200)
        
        mixshader1_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeMixShader")        
        mixshader1_node.location = (100, 200)
        
        colorramp1_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-900, 200)
        colorramp1_node.color_ramp.elements[0].position = 0.520
        colorramp1_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp1_node.color_ramp.elements[1].position = 0.644
        colorramp1_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        noise1_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-1500, 200)
        noise1_node.inputs[2].default_value = 1.3
        noise1_node.inputs[3].default_value = 16
        noise1_node.inputs[4].default_value = 0.615
        noise1_node.inputs[5].default_value = 0
        
        principled_bsdf1 = material_silver_rusted.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (-300, -200)
        principled_bsdf1.inputs[4].default_value = 1
        
        colorramp2_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp2_node.location = (-900, -180)
        colorramp2_node.color_ramp.elements[0].position = 0.362
        colorramp2_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp2_node.color_ramp.elements[1].position = 0.513
        colorramp2_node.color_ramp.elements[1].color = (0.527, 0.527, 0.527, 1)
        
        colorramp3_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp3_node.location = (-900, -450)
        colorramp3_node.color_ramp.elements[0].position = 0.468
        colorramp3_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp3_node.color_ramp.elements[1].position = 0.827
        colorramp3_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        bump1_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (-600, -750)
        bump1_node.inputs[0].default_value = 0.518
        bump1_node.inputs[1].default_value = 1
        
        colorramp4_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp4_node.location = (-900, -750)
        colorramp4_node.color_ramp.elements[0].position = 0
        colorramp4_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp4_node.color_ramp.elements[1].position = 0.506
        colorramp4_node.color_ramp.elements[1].color = (1, 1, 1, 1)
          
        bump2_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeBump")
        bump2_node.location = (-900, -1100)
        bump2_node.inputs[0].default_value = 0.106
        bump2_node.inputs[1].default_value = 1
        
        noise2_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeTexNoise")
        noise2_node.location = (-1500, -450)
        noise2_node.inputs[2].default_value = 1
        noise2_node.inputs[3].default_value = 16
        noise2_node.inputs[4].default_value = 0.708
        noise2_node.inputs[5].default_value = 0
        
        noise3_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeTexNoise")
        noise3_node.location = (-1500, -1100)
        noise3_node.inputs[2].default_value = 1
        noise3_node.inputs[3].default_value = 16
        noise3_node.inputs[4].default_value = 0.9
        noise3_node.inputs[5].default_value = 0
        
        principled_bsdf2 = material_silver_rusted.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        principled_bsdf2.location = (-300, -1350)
        principled_bsdf2.inputs[7].default_value = 1
        
        colorramp5_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp5_node.location = (-900, -1350)
        colorramp5_node.color_ramp.elements[0].position = 0.141
        colorramp5_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp5_node.color_ramp.elements[1].position = 0.734
        colorramp5_node.color_ramp.elements[1].color = (0.376, 0.109, 0.036, 1)
        
        bump3_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeBump")
        bump3_node.location = (-900, -1650)
        bump3_node.inputs[0].default_value = 1
        bump3_node.inputs[1].default_value = 1
        
        mapping1_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-1800, -450)
        
        textcoord1_node = material_silver_rusted.node_tree.nodes.new("ShaderNodeTexCoord")
        textcoord1_node.location = (-2000, -450)
        
        material_silver_rusted.node_tree.links.new(mixshader1_node.outputs[0], material_output.inputs[0])
        material_silver_rusted.node_tree.links.new(colorramp1_node.outputs[0], mixshader1_node.inputs[0])
        material_silver_rusted.node_tree.links.new(principled_bsdf1.outputs[0], mixshader1_node.inputs[1])
        material_silver_rusted.node_tree.links.new(noise1_node.outputs[0], colorramp1_node.inputs[0])
        material_silver_rusted.node_tree.links.new(colorramp2_node.outputs[0], principled_bsdf1.inputs[0])
        material_silver_rusted.node_tree.links.new(colorramp3_node.outputs[0], principled_bsdf1.inputs[7])
        material_silver_rusted.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])
        material_silver_rusted.node_tree.links.new(colorramp4_node.outputs[0], bump1_node.inputs[2])
        material_silver_rusted.node_tree.links.new(noise2_node.outputs[0], colorramp2_node.inputs[0])
        material_silver_rusted.node_tree.links.new(noise2_node.outputs[0], colorramp3_node.inputs[0])
        material_silver_rusted.node_tree.links.new(noise2_node.outputs[0], colorramp4_node.inputs[0])
        material_silver_rusted.node_tree.links.new(bump2_node.outputs["Normal"], bump1_node.inputs["Normal"])
        material_silver_rusted.node_tree.links.new(noise3_node.outputs[0], bump2_node.inputs[2])
        material_silver_rusted.node_tree.links.new(principled_bsdf2.outputs[0], mixshader1_node.inputs[2])
        material_silver_rusted.node_tree.links.new(colorramp5_node.outputs[0], principled_bsdf2.inputs[0])
        material_silver_rusted.node_tree.links.new(bump3_node.outputs[0], principled_bsdf2.inputs[19])
        material_silver_rusted.node_tree.links.new(noise1_node.outputs[0], colorramp5_node.inputs[0])
        material_silver_rusted.node_tree.links.new(noise1_node.outputs[0], bump3_node.inputs[2])
        material_silver_rusted.node_tree.links.new(mapping1_node.outputs[0], noise1_node.inputs["Vector"])
        material_silver_rusted.node_tree.links.new(mapping1_node.outputs[0], noise2_node.inputs["Vector"])
        material_silver_rusted.node_tree.links.new(mapping1_node.outputs[0], noise3_node.inputs["Vector"])
        material_silver_rusted.node_tree.links.new(textcoord1_node.outputs[3], mapping1_node.inputs[0])
        
        bpy.context.object.active_material = material_silver_rusted
        return {"FINISHED"}




class SHADER_OT_SILVER_NUGGET(bpy.types.Operator):
    bl_label = "Nugget"
    bl_idname = "shader.silver_nugget_operator"
    
    def execute(self, context):
        material_silver_nugget = bpy.data.materials.new(name="Silver Nugget")
        material_silver_nugget.use_nodes = True

        material_output = material_silver_nugget.node_tree.nodes.get("Material Output")
        material_output.location = (300, 200)        

        principled_bsdf1 = material_silver_nugget.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (0, 200)
        principled_bsdf1.inputs[4].default_value = 1
        principled_bsdf1.inputs[7].default_value = 0.380

        colorramp1_node = material_silver_nugget.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-300, 200)
        colorramp1_node.color_ramp.elements[0].position = 0
        colorramp1_node.color_ramp.elements[0].color = (0.651, 0.651, 0.651, 1)
        colorramp1_node.color_ramp.elements[1].position = 1
        colorramp1_node.color_ramp.elements[1].color = (0.527, 0.527, 0.527, 1)
        
        bump1_node = material_silver_nugget.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (-300, -200)
        bump1_node.inputs[0].default_value = 0.5
        bump1_node.inputs[1].default_value = 1
        
        musgrave1_node = material_silver_nugget.node_tree.nodes.new("ShaderNodeTexMusgrave")
        musgrave1_node.location = (-600, 200)
        musgrave1_node.inputs[2].default_value = 400
        musgrave1_node.inputs[3].default_value = 16
        musgrave1_node.inputs[4].default_value = 0
        musgrave1_node.inputs[5].default_value = 2
        
        noise1_node = material_silver_nugget.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-600, -200)
        noise1_node.inputs[2].default_value = 10
        noise1_node.inputs[3].default_value = 8
        noise1_node.inputs[4].default_value = 0.45
        noise1_node.inputs[5].default_value = 0              
        
        mapping1_node = material_silver_nugget.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-900, 100)
        
        texcoord1_node = material_silver_nugget.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-1200, 100)
        
        material_silver_nugget.node_tree.links.new(texcoord1_node.outputs[3], mapping1_node.inputs[0])     
        material_silver_nugget.node_tree.links.new(mapping1_node.outputs["Vector"], musgrave1_node.inputs["Vector"])
        material_silver_nugget.node_tree.links.new(mapping1_node.outputs["Vector"], noise1_node.inputs["Vector"])
        material_silver_nugget.node_tree.links.new(musgrave1_node.outputs[0], colorramp1_node.inputs[0])
        material_silver_nugget.node_tree.links.new(noise1_node.outputs[0], bump1_node.inputs[2])
        material_silver_nugget.node_tree.links.new(colorramp1_node.outputs[0], principled_bsdf1.inputs[0])
        material_silver_nugget.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])

        bpy.context.object.active_material = material_silver_nugget
        return {"FINISHED"}






############################# METAL ##############################
class SHADER_OT_GENERAL_METAL(bpy.types.Operator):
    bl_label = "Metal"
    bl_idname = "shader.general_metal_operator"
    
    def execute(self, context):
        material_general_metal = bpy.data.materials.new(name="Metal")
        material_general_metal.use_nodes = True
        
        material_output = material_general_metal.node_tree.nodes.get("Material Output")
        material_output.location = (300, 200)
        
        principled_bsdf1 = material_general_metal.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (0, 200)
        principled_bsdf1.inputs[4].default_value = 1
        principled_bsdf1.inputs[7].default_value = 0.27
        
        colorramp1_node = material_general_metal.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-300, 200)
        colorramp1_node.color_ramp.elements[0].position = 0
        colorramp1_node.color_ramp.elements[0].color = (0.165, 0.191, 0.209, 1)
        colorramp1_node.color_ramp.elements[1].position = 1
        colorramp1_node.color_ramp.elements[1].color = (0.095, 0.095, 0.095, 1)
        
        bump1_node = material_general_metal.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (-300, -200)
        bump1_node.inputs[0].default_value = 0.008
        bump1_node.inputs[1].default_value = 1
        
        musgrave1_node = material_general_metal.node_tree.nodes.new("ShaderNodeTexMusgrave")
        musgrave1_node.location = (-600, 200)
        musgrave1_node.inputs[2].default_value = 400
        musgrave1_node.inputs[3].default_value = 16
        musgrave1_node.inputs[4].default_value = 0
        musgrave1_node.inputs[5].default_value = 2
        
        noise1_node = material_general_metal.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-600, -200)
        noise1_node.inputs[2].default_value = 12
        noise1_node.inputs[3].default_value = 16
        noise1_node.inputs[4].default_value = 0.45
        noise1_node.inputs[5].default_value = 0
        
        mapping1_node = material_general_metal.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-900, 200)
        
        texcoord1_node = material_general_metal.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-1200, 200)
        
        material_general_metal.node_tree.links.new(texcoord1_node.outputs[3], mapping1_node.inputs[0])        
        material_general_metal.node_tree.links.new(mapping1_node.outputs["Vector"], musgrave1_node.inputs["Vector"])
        material_general_metal.node_tree.links.new(mapping1_node.outputs["Vector"], noise1_node.inputs["Vector"])
        material_general_metal.node_tree.links.new(musgrave1_node.outputs[0], colorramp1_node.inputs[0])
        material_general_metal.node_tree.links.new(noise1_node.outputs[0], bump1_node.inputs[2])
        material_general_metal.node_tree.links.new(colorramp1_node.outputs[0], principled_bsdf1.inputs[0])
        material_general_metal.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])
        material_general_metal.node_tree.links.new(principled_bsdf1.outputs[0], material_output.inputs[0])
                
        bpy.context.object.active_material = material_general_metal
        return {"FINISHED"}





class SHADER_OT_METAL_GALVANIZED(bpy.types.Operator):
    bl_label = "Galvanized"
    bl_idname = "shader.metal_galvanized_operator"
    
    def execute(self, context):
        material_metal_galvanized = bpy.data.materials.new(name="Metal Galvanized")
        material_metal_galvanized.use_nodes = True
        
        material_output = material_metal_galvanized.node_tree.nodes.get("Material Output")
        material_output.location = (600, 200)
        
        principled_bsdf1 = material_metal_galvanized.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (300, 200)
        principled_bsdf1.inputs[0].default_value = (0.462, 0.462, 0.462, 1)
        principled_bsdf1.inputs[4].default_value = 1
        
        bump1_node = material_metal_galvanized.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (0, -200)
        bump1_node.inputs[0].default_value = 0.03
        bump1_node.inputs[1].default_value = 1
        
        bump2_node = material_metal_galvanized.node_tree.nodes.new("ShaderNodeBump")
        bump2_node.location = (-300, -100)
        bump2_node.inputs[0].default_value = 0.05
        bump2_node.inputs[1].default_value = 1
        
        colorramp1_node = material_metal_galvanized.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-600, 200)
        colorramp1_node.color_ramp.elements[0].position = 0
        colorramp1_node.color_ramp.elements[0].color = (0.192, 0.192, 0.192, 1)
        colorramp1_node.color_ramp.elements[1].position = 1
        colorramp1_node.color_ramp.elements[1].color = (0.349, 0.349, 0.349, 1)
        
        voronoi1_node = material_metal_galvanized.node_tree.nodes.new("ShaderNodeTexVoronoi")
        voronoi1_node.location = (-900, 200)
        voronoi1_node.distance = "MINKOWSKI"
        voronoi1_node.inputs[2].default_value = 60
        voronoi1_node.inputs[3].default_value = 0.5
        voronoi1_node.inputs[4].default_value = 1
        
        noise1_node = material_metal_galvanized.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-900, -200)
        noise1_node.inputs[2].default_value = 20
        noise1_node.inputs[3].default_value = 16
        noise1_node.inputs[4].default_value = 0.5
        noise1_node.inputs[5].default_value = 0
        
        texcoord1_node = material_metal_galvanized.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-1200, 200)
        
        material_metal_galvanized.node_tree.links.new(texcoord1_node.outputs[3], voronoi1_node.inputs["Vector"])
        material_metal_galvanized.node_tree.links.new(texcoord1_node.outputs[3], noise1_node.inputs["Vector"])
        material_metal_galvanized.node_tree.links.new(voronoi1_node.outputs[1], colorramp1_node.inputs[0])
        material_metal_galvanized.node_tree.links.new(noise1_node.outputs[0], bump1_node.inputs["Height"])
        material_metal_galvanized.node_tree.links.new(colorramp1_node.outputs["Color"], bump2_node.inputs["Height"])
        material_metal_galvanized.node_tree.links.new(bump2_node.outputs[0], bump1_node.inputs["Normal"])
        material_metal_galvanized.node_tree.links.new(colorramp1_node.outputs["Color"], principled_bsdf1.inputs[7])
        material_metal_galvanized.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])
        material_metal_galvanized.node_tree.links.new(principled_bsdf1.outputs[0], material_output.inputs[0])
        
        bpy.context.object.active_material = material_metal_galvanized
        return {"FINISHED"}





class SHADER_OT_METAL_DAMAGED(bpy.types.Operator):
    bl_label = "Damaged"
    bl_idname = "shader.metal_damaged_operator"
    
    def execute(self, context):
        material_metal_damaged = bpy.data.materials.new(name="Metal Damaged")
        material_metal_damaged.use_nodes = True
    
        material_output = material_metal_damaged.node_tree.nodes.get("Material Output")
        material_output.location = (600, 200)
    
        principled_bsdf1 = material_metal_damaged.node_tree.nodes.get("Principled BSDF")    
        principled_bsdf1.location = (300, 200)
        
        mix1_node = material_metal_damaged.node_tree.nodes.new("ShaderNodeMixRGB")
        mix1_node.location = (0, 200)
        mix1_node.blend_type = "MIX"
        mix1_node.inputs[1].default_value = (0.100, 0.019, 0.007, 1)
        
        bump1_node = material_metal_damaged.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (0, -200)
        bump1_node.inputs[0].default_value = 0.250
        bump1_node.inputs[1].default_value = 1
        
        bump2_node = material_metal_damaged.node_tree.nodes.new("ShaderNodeBump")
        bump2_node.location = (-250, -400)
        bump2_node.inputs[0].default_value = 0.200
        bump2_node.inputs[1].default_value = 1
        
        colorramp1_node = material_metal_damaged.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-600, 500)
        colorramp1_node.color_ramp.elements[0].position = 0
        colorramp1_node.color_ramp.elements[0].color = (1, 1, 1, 1)
        colorramp1_node.color_ramp.elements[1].position = 0.721
        colorramp1_node.color_ramp.elements[1].color = (0, 0, 0, 1)
    
        colorramp2_node = material_metal_damaged.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp2_node.location = (-600, 200)
        colorramp2_node.color_ramp.elements.new(0)
        colorramp2_node.color_ramp.elements.new(0)
        colorramp2_node.color_ramp.elements[0].position = 0.395
        colorramp2_node.color_ramp.elements[0].color = (0.032, 0.025, 0.020, 1)
        colorramp2_node.color_ramp.elements[1].position = 0.409
        colorramp2_node.color_ramp.elements[1].color = (0.279, 0.275, 0.270, 1)    
        colorramp2_node.color_ramp.elements[2].position = 0.522
        colorramp2_node.color_ramp.elements[2].color = (0.441, 0.439, 0.437, 1)
        colorramp2_node.color_ramp.elements[3].position = 0.634
        colorramp2_node.color_ramp.elements[3].color = (0.604, 0.604, 0.604, 1)    
        
        colorramp3_node = material_metal_damaged.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp3_node.location = (-600, -100)
        colorramp3_node.color_ramp.elements[0].position = 0.366
        colorramp3_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp3_node.color_ramp.elements[1].position = 0.451
        colorramp3_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        colorramp4_node = material_metal_damaged.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp4_node.location = (-600, -400)
        colorramp4_node.color_ramp.elements[0].position = 0
        colorramp4_node.color_ramp.elements[0].color = (0.503, 0.503, 0.503, 1)
        colorramp4_node.color_ramp.elements[1].position = 1
        colorramp4_node.color_ramp.elements[1].color = (0.133, 0.133, 0.133, 1)
        
        bump3_node = material_metal_damaged.node_tree.nodes.new("ShaderNodeBump")
        bump3_node.location = (-600, -700)
        bump3_node.inputs[0].default_value = 0.080
        bump3_node.inputs[1].default_value = 1
        
        musgrave1_node = material_metal_damaged.node_tree.nodes.new("ShaderNodeTexMusgrave")
        musgrave1_node.location = (-900, 400)
        musgrave1_node.inputs[2].default_value = 3
        musgrave1_node.inputs[3].default_value = 16
        musgrave1_node.inputs[4].default_value = 0.4
        musgrave1_node.inputs[5].default_value = 2
        
        noise1_node = material_metal_damaged.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-900, -100)
        noise1_node.inputs[2].default_value = 3.3
        noise1_node.inputs[3].default_value = 16
        noise1_node.inputs[4].default_value = 0.55
        noise1_node.inputs[5].default_value = 0
        
        texcoord1_node = material_metal_damaged.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-1200, 200)
        
        material_metal_damaged.node_tree.links.new(texcoord1_node.outputs[3], musgrave1_node.inputs["Vector"])
        material_metal_damaged.node_tree.links.new(texcoord1_node.outputs[3], noise1_node.inputs["Vector"])
        material_metal_damaged.node_tree.links.new(musgrave1_node.outputs[0], colorramp1_node.inputs[0])
        material_metal_damaged.node_tree.links.new(noise1_node.outputs[0], colorramp2_node.inputs[0])
        material_metal_damaged.node_tree.links.new(noise1_node.outputs[0], colorramp3_node.inputs[0])
        material_metal_damaged.node_tree.links.new(noise1_node.outputs[0], colorramp4_node.inputs[0])
        material_metal_damaged.node_tree.links.new(noise1_node.outputs[0], bump3_node.inputs[2])
        material_metal_damaged.node_tree.links.new(colorramp1_node.outputs[0], mix1_node.inputs[0])
        material_metal_damaged.node_tree.links.new(colorramp1_node.outputs[0], bump1_node.inputs[2])
        material_metal_damaged.node_tree.links.new(colorramp2_node.outputs[0], mix1_node.inputs[2])
        material_metal_damaged.node_tree.links.new(colorramp3_node.outputs[0], principled_bsdf1.inputs[4])
        material_metal_damaged.node_tree.links.new(colorramp3_node.outputs[0], bump2_node.inputs[2])
        material_metal_damaged.node_tree.links.new(colorramp4_node.outputs[0], principled_bsdf1.inputs[7])
        material_metal_damaged.node_tree.links.new(bump3_node.outputs[0], bump2_node.inputs["Normal"])
        material_metal_damaged.node_tree.links.new(bump2_node.outputs[0], bump1_node.inputs["Normal"])
        material_metal_damaged.node_tree.links.new(mix1_node.outputs[0], principled_bsdf1.inputs[0])
        material_metal_damaged.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])
        
        bpy.context.object.active_material = material_metal_damaged
        return {"FINISHED"}






class SHADER_OT_METAL_NUGGET(bpy.types.Operator):
    bl_label = "Nugget"
    bl_idname = "shader.metal_nugget_operator"
    
    def execute(self, context):
        material_metal_nugget = bpy.data.materials.new(name="Metal Nugget")
        material_metal_nugget.use_nodes = True
        
        material_output = material_metal_nugget.node_tree.nodes.get("Material Output")
        material_output.location = (600, 200)
        
        principled_bsdf1 = material_metal_nugget.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (300, 200)
        principled_bsdf1.inputs[4].default_value = 1
        principled_bsdf1.inputs[7].default_value = 0.380
        
        colorramp1_node = material_metal_nugget.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (0, 200)
        colorramp1_node.color_ramp.elements[0].position = 0
        colorramp1_node.color_ramp.elements[0].color = (0.165, 0.191, 0.209, 1)
        colorramp1_node.color_ramp.elements[1].position = 1
        colorramp1_node.color_ramp.elements[1].color = (0.095, 0.095, 0.095, 1)
        
        bump1_node = material_metal_nugget.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (0, -200)
        bump1_node.inputs[0].default_value = 0.5
        bump1_node.inputs[1].default_value = 1
        
        musgrave1_node = material_metal_nugget.node_tree.nodes.new("ShaderNodeTexMusgrave")
        musgrave1_node.location = (-300, 200)
        musgrave1_node.inputs[2].default_value = 400
        musgrave1_node.inputs[3].default_value = 16
        musgrave1_node.inputs[4].default_value = 0
        musgrave1_node.inputs[5].default_value = 2
        
        noise1_node = material_metal_nugget.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-300, -200)
        noise1_node.inputs[2].default_value = 10
        noise1_node.inputs[3].default_value = 8
        noise1_node.inputs[4].default_value = 0.45
        noise1_node.inputs[5].default_value = 0
        
        mapping1_node = material_metal_nugget.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-600, 200)
        
        texcoord1_node = material_metal_nugget.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-900, 200)
        
        material_metal_nugget.node_tree.links.new(texcoord1_node.outputs[3], mapping1_node.inputs[0])
        material_metal_nugget.node_tree.links.new(mapping1_node.outputs[0], musgrave1_node.inputs["Vector"])
        material_metal_nugget.node_tree.links.new(mapping1_node.outputs[0], noise1_node.inputs["Vector"])
        material_metal_nugget.node_tree.links.new(musgrave1_node.outputs[0], colorramp1_node.inputs[0])
        material_metal_nugget.node_tree.links.new(noise1_node.outputs[0], bump1_node.inputs[2])
        material_metal_nugget.node_tree.links.new(colorramp1_node.outputs[0], principled_bsdf1.inputs[0])
        material_metal_nugget.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])
        
        bpy.context.object.active_material = material_metal_nugget
        return {"FINISHED"}






class SHADER_OT_METAL_RUSTY(bpy.types.Operator):
    bl_label = "Rusty"
    bl_idname = "shader.metal_rusty_operator"
    
    def execute(self, context):
        material_metal_rusty = bpy.data.materials.new(name="Metal Rusty")
        material_metal_rusty.use_nodes = True
    
        material_output = material_metal_rusty.node_tree.nodes.get("Material Output")
        material_output.location = (1000, -600)
        
        mix1_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeMixShader")
        mix1_node.location = (800, -600)
    
        principled_bsdf1 = material_metal_rusty.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (300, 200)
        
        principled_bsdf2 = material_metal_rusty.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        principled_bsdf2.location = (300, -1000)
        principled_bsdf2.inputs[0].default_value = (0.165, 0.191, 0.205, 1)
        principled_bsdf2.inputs[4].default_value = 1
        
        bump1_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (0, -200)
        bump1_node.inputs[0].default_value = 1
        bump1_node.inputs[1].default_value = 1
        
        bump2_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeBump")
        bump2_node.location = (-300, -200)
        bump2_node.inputs[0].default_value = 0.160
        bump2_node.inputs[1].default_value = 1
        
        bump3_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeBump")
        bump3_node.location = (-300, -1000)
        bump3_node.inputs[0].default_value = 0.015
        bump3_node.inputs[1].default_value = 1
        
        colorramp1_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-300, 200)
        colorramp1_node.color_ramp.elements[0].position = 0
        colorramp1_node.color_ramp.elements[0].color = (1, 1, 1, 1)
        colorramp1_node.color_ramp.elements[1].position = 0.077
        colorramp1_node.color_ramp.elements[1].color = (0, 0, 0, 1)
        
        colorramp2_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp2_node.location = (-300, -600)
        colorramp2_node.color_ramp.elements[0].position = 0.464
        colorramp2_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp2_node.color_ramp.elements[1].position = 0.528
        colorramp2_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        colorramp3_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp3_node.location = (-700, 400)
        colorramp3_node.color_ramp.elements.new(0)
        colorramp3_node.color_ramp.elements[0].position = 0.160
        colorramp3_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp3_node.color_ramp.elements[1].position = 0.577
        colorramp3_node.color_ramp.elements[1].color = (0.038, 0.014, 0.007, 1)
        colorramp3_node.color_ramp.elements[2].position = 0.853
        colorramp3_node.color_ramp.elements[2].color = (0.080, 0.044, 0.023, 1)
        
        noise1_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-900, 400)
        noise1_node.inputs[2].default_value = 60
        noise1_node.inputs[3].default_value = 16
        noise1_node.inputs[4].default_value = 0.6
        noise1_node.inputs[5].default_value = 0
        
        noise2_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeTexNoise")
        noise2_node.location = (-900, -600)
        noise2_node.inputs[2].default_value = 5
        noise2_node.inputs[3].default_value = 16
        noise2_node.inputs[4].default_value = 0.9
        noise2_node.inputs[5].default_value = 0
        
        noise3_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeTexNoise")
        noise3_node.location = (-900, -1000)
        noise3_node.inputs[2].default_value = 6
        noise3_node.inputs[3].default_value = 2
        noise3_node.inputs[4].default_value = 0.5
        noise3_node.inputs[5].default_value = 0
        
        mapping1_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-1200, -600)
        
        texcoord1_node = material_metal_rusty.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-1500, -600)
    
        material_metal_rusty.node_tree.links.new(mix1_node.outputs[0], material_output.inputs[0])
        material_metal_rusty.node_tree.links.new(principled_bsdf1.outputs[0], mix1_node.inputs[1])
        material_metal_rusty.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])
        material_metal_rusty.node_tree.links.new(colorramp1_node.outputs[0], principled_bsdf1.inputs[7])
        material_metal_rusty.node_tree.links.new(bump2_node.outputs[0], bump1_node.inputs["Normal"])
        material_metal_rusty.node_tree.links.new(colorramp2_node.outputs[0], bump1_node.inputs[2])
        material_metal_rusty.node_tree.links.new(colorramp2_node.outputs[0], mix1_node.inputs[0])
        material_metal_rusty.node_tree.links.new(principled_bsdf2.outputs[0], mix1_node.inputs[2])
        material_metal_rusty.node_tree.links.new(bump3_node.outputs[0], principled_bsdf2.inputs[20])
        material_metal_rusty.node_tree.links.new(colorramp3_node.outputs[0], principled_bsdf1.inputs[0])
        material_metal_rusty.node_tree.links.new(colorramp3_node.outputs[0], colorramp1_node.inputs[0])
        material_metal_rusty.node_tree.links.new(colorramp3_node.outputs[0], bump2_node.inputs[2])
        material_metal_rusty.node_tree.links.new(noise1_node.outputs[0], colorramp3_node.inputs[0])
        material_metal_rusty.node_tree.links.new(noise2_node.outputs[0], colorramp2_node.inputs[0])
        material_metal_rusty.node_tree.links.new(noise3_node.outputs[0], bump3_node.inputs[2])
        material_metal_rusty.node_tree.links.new(mapping1_node.outputs[0], noise1_node.inputs["Vector"])
        material_metal_rusty.node_tree.links.new(mapping1_node.outputs[0], noise2_node.inputs["Vector"])
        material_metal_rusty.node_tree.links.new(mapping1_node.outputs[0], noise3_node.inputs["Vector"])
        material_metal_rusty.node_tree.links.new(texcoord1_node.outputs[3], mapping1_node.inputs[0])
        
        bpy.context.object.active_material = material_metal_rusty
        return {"FINISHED"}





class SHADER_OT_METAL_SCRATCHED(bpy.types.Operator):
    bl_label = "Scratched"
    bl_idname = "shader.metal_scratched_operator"
    
    def execute(self, context):
        material_metal_scratched = bpy.data.materials.new(name="Metal Scratched")
        material_metal_scratched.use_nodes = True
        
        texcoord1_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-1200, 0)
        
        mapping1_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-900, 0)
        
        wave1_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeTexWave")
        wave1_node.location = (-600, 600)
        wave1_node.inputs[1].default_value = 0.1
        wave1_node.inputs[2].default_value = 78
        wave1_node.inputs[3].default_value = 16
        wave1_node.inputs[4].default_value = 1
        wave1_node.inputs[5].default_value = 0.75
        wave1_node.inputs[6].default_value = 0
        
        noise1_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-600, 200)
        noise1_node.inputs[2].default_value = 1
        noise1_node.inputs[3].default_value = 10
        noise1_node.inputs[4].default_value = 0.8
        noise1_node.inputs[5].default_value = 12
        
        wave2_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeTexWave")
        wave2_node.location = (-600, -200)
        wave2_node.inputs[1].default_value = 4
        wave2_node.inputs[2].default_value = 4.5
        wave2_node.inputs[3].default_value = 2
        wave2_node.inputs[4].default_value = 1
        wave2_node.inputs[5].default_value = 0.5
        wave2_node.inputs[6].default_value = 0
        
        separateXYZ1_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeSeparateXYZ")
        separateXYZ1_node.location = (-600, -600)
        
        colorramp1_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-300, 800)
        colorramp1_node.color_ramp.elements[0].position = 0
        colorramp1_node.color_ramp.elements[0].color = (0.235, 0.231, 0.235, 1) 
        colorramp1_node.color_ramp.elements[1].position = 1
        colorramp1_node.color_ramp.elements[1].color = (0.533, 0.527, 0.533, 1) 
        
        colorramp2_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp2_node.location = (-300, 500)
        colorramp2_node.color_ramp.elements[0].position = 0
        colorramp2_node.color_ramp.elements[0].color = (1, 1, 1, 1) 
        colorramp2_node.color_ramp.elements[1].position = 0.764
        colorramp2_node.color_ramp.elements[1].color = (0, 0, 0, 1)
        
        colorramp3_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp3_node.location = (-300, 200)
        colorramp3_node.color_ramp.elements[0].position = 0.442
        colorramp3_node.color_ramp.elements[0].color = (0, 0, 0, 1) 
        colorramp3_node.color_ramp.elements[1].position = 0.449
        colorramp3_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        combineXYZ1_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeCombineXYZ")
        combineXYZ1_node.location = (-300, -400)
        
        bump1_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (0, 500)
        bump1_node.inputs[0].default_value = 0.07
        bump1_node.inputs[1].default_value = 1
        
        musgrave1_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeTexMusgrave")
        musgrave1_node.location = (0, -300)
        musgrave1_node.inputs[2].default_value = 3
        musgrave1_node.inputs[3].default_value = 14
        musgrave1_node.inputs[4].default_value = 0.56
        musgrave1_node.inputs[5].default_value = 2.5
        
        bump2_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeBump")
        bump2_node.location = (300, 400)
        bump2_node.inputs[0].default_value = 0.3
        bump2_node.inputs[1].default_value = 1
        
        colorramp4_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp4_node.location = (300, -200)
        colorramp4_node.color_ramp.elements[0].position = 0.692
        colorramp4_node.color_ramp.elements[0].color = (1, 1, 1, 1) 
        colorramp4_node.color_ramp.elements[1].position = 0.783
        colorramp4_node.color_ramp.elements[1].color = (0, 0, 0, 1)
        
        bump3_node = material_metal_scratched.node_tree.nodes.new("ShaderNodeBump")
        bump3_node.location = (600, 0)
        bump3_node.inputs[0].default_value = 0.387
        bump3_node.inputs[1].default_value = 1
         
        principled_bsdf1 = material_metal_scratched.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (900, 300)
        principled_bsdf1.inputs[4].default_value = 1
        principled_bsdf1.inputs[7].default_value = 0.198
        
        material_output = material_metal_scratched.node_tree.nodes.get("Material Output")
        material_output.location = (1200, 300)
        
        material_metal_scratched.node_tree.links.new(texcoord1_node.outputs[3], mapping1_node.inputs[0])
        material_metal_scratched.node_tree.links.new(mapping1_node.outputs[0], wave1_node.inputs[0])
        material_metal_scratched.node_tree.links.new(mapping1_node.outputs[0], noise1_node.inputs[1])
        material_metal_scratched.node_tree.links.new(mapping1_node.outputs[0], wave2_node.inputs[0])
        material_metal_scratched.node_tree.links.new(mapping1_node.outputs[0], separateXYZ1_node.inputs[0])
        material_metal_scratched.node_tree.links.new(wave1_node.outputs[0], colorramp1_node.inputs[0])
        material_metal_scratched.node_tree.links.new(wave1_node.outputs[0], colorramp2_node.inputs[0])
        material_metal_scratched.node_tree.links.new(noise1_node.outputs[0], colorramp3_node.inputs[0])
        material_metal_scratched.node_tree.links.new(wave2_node.outputs[0], combineXYZ1_node.inputs[1])
        material_metal_scratched.node_tree.links.new(separateXYZ1_node.outputs[0], combineXYZ1_node.inputs[0])
        material_metal_scratched.node_tree.links.new(separateXYZ1_node.outputs[2], combineXYZ1_node.inputs[2])
        material_metal_scratched.node_tree.links.new(colorramp2_node.outputs[0], bump1_node.inputs[2])
        material_metal_scratched.node_tree.links.new(combineXYZ1_node.outputs[0], musgrave1_node.inputs["Vector"])
        material_metal_scratched.node_tree.links.new(colorramp3_node.outputs[0], bump2_node.inputs[2])
        material_metal_scratched.node_tree.links.new(bump1_node.outputs[0], bump2_node.inputs["Normal"])
        material_metal_scratched.node_tree.links.new(musgrave1_node.outputs[0], colorramp4_node.inputs[0])
        material_metal_scratched.node_tree.links.new(colorramp4_node.outputs[0], bump3_node.inputs[2])
        material_metal_scratched.node_tree.links.new(bump2_node.outputs[0], bump3_node.inputs["Normal"])
        material_metal_scratched.node_tree.links.new(colorramp1_node.outputs[0], principled_bsdf1.inputs[0])
        material_metal_scratched.node_tree.links.new(bump3_node.outputs[0], principled_bsdf1.inputs[20])
        
        bpy.context.object.active_material = material_metal_scratched
        return {"FINISHED"}





class SHADER_OT_CHROME(bpy.types.Operator):
    bl_label = "Chrome"
    bl_idname = "shader.chrome_operator"
    
    def execute(self, context):
        material_chrome = bpy.data.materials.new(name="Chrome")
        material_chrome.use_nodes = True
        
        principled_bsdf1 = material_chrome.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (0, 0)
        principled_bsdf1.inputs[4].default_value = 1
        principled_bsdf1.inputs[5].default_value = 0
        principled_bsdf1.inputs[7].default_value = 0.08
        
        glossy_bsdf1 = material_chrome.node_tree.nodes.new("ShaderNodeBsdfGlossy")
        glossy_bsdf1.location = (0, 200)
        glossy_bsdf1.inputs[0].default_value = (0, 0, 0, 1)
        glossy_bsdf1.inputs[1].default_value = 0.580
        
        layer_weight1 = material_chrome.node_tree.nodes.new("ShaderNodeLayerWeight")
        layer_weight1.location = (0, 500)
        
        mix1_node = material_chrome.node_tree.nodes.new("ShaderNodeMixShader")
        mix1_node.location = (300, 200)
        
        material_output = material_chrome.node_tree.nodes.get("Material Output")
        material_output.location = (600, 200)
        
        material_chrome.node_tree.links.new(layer_weight1.outputs[0], mix1_node.inputs[0])        
        material_chrome.node_tree.links.new(glossy_bsdf1.outputs[0], mix1_node.inputs[2])        
        material_chrome.node_tree.links.new(principled_bsdf1.outputs[0], mix1_node.inputs[1])        
        material_chrome.node_tree.links.new(mix1_node.outputs[0], material_output.inputs[0])        
        
        bpy.context.object.active_material = material_chrome
        return {"FINISHED"}





class SHADER_OT_GINGERBREAD(bpy.types.Operator):
    bl_label = "Gingerbread"
    bl_idname = "shader.gingerbread_operator"
    
    def execute(self, context):
        material_gingerbread = bpy.data.materials.new(name="Gingerbread")
        material_gingerbread.use_nodes = True 
    
        principled_bsdf1 = material_gingerbread.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (600, 200)
        principled_bsdf1.inputs[7].default_value = 0.8
        
        material_output = material_gingerbread.node_tree.nodes.get("Material Output")
        material_output.location = (900, 200)
    
        mix1_node = material_gingerbread.node_tree.nodes.new("ShaderNodeMixRGB")
        mix1_node.location = (300, 200)
        mix1_node.inputs[1].default_value = (0.929, 0.323, 0.106, 1)
        mix1_node.inputs[2].default_value = (0.539, 0.186, 0.059, 1)
        
        bump1_node = material_gingerbread.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (300, -200)
        bump1_node.inputs[0].default_value = 1
        bump1_node.inputs[1].default_value = 1
        
        colorramp1_node = material_gingerbread.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (0, 0)
        colorramp1_node.color_ramp.elements[0].position = 0.330
        colorramp1_node.color_ramp.elements[0].color = (0, 0, 0, 1)
        colorramp1_node.color_ramp.elements[1].position = 0.431
        colorramp1_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        noise1_node = material_gingerbread.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-300, 0)
        noise1_node.inputs[2].default_value = 200
        noise1_node.inputs[3].default_value = 5.5
        noise1_node.inputs[4].default_value = 0.375
        noise1_node.inputs[5].default_value = 0
        
        mapping1_node = material_gingerbread.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-600, 0)
        
        texcoord1_node = material_gingerbread.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-900, 0)
        
        material_gingerbread.node_tree.links.new(texcoord1_node.outputs[3], mapping1_node.inputs[0])
        material_gingerbread.node_tree.links.new(mapping1_node.outputs[0], noise1_node.inputs["Vector"])
        material_gingerbread.node_tree.links.new(noise1_node.outputs[1], colorramp1_node.inputs[0])
        material_gingerbread.node_tree.links.new(colorramp1_node.outputs[0], mix1_node.inputs[0])
        material_gingerbread.node_tree.links.new(colorramp1_node.outputs[0], bump1_node.inputs[2])
        material_gingerbread.node_tree.links.new(mix1_node.outputs[0], principled_bsdf1.inputs[0])
        material_gingerbread.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])
        material_gingerbread.node_tree.links.new(principled_bsdf1.outputs[0], material_output.inputs[0])
    
        bpy.context.object.active_material = material_gingerbread
        return  {"FINISHED"}    
    
    



class SHADER_OT_CANDY(bpy.types.Operator):
    bl_label = "Candy"
    bl_idname = "shader.candy_operator"
    
    def execute(self, context):
        material_candy = bpy.data.materials.new(name="Candy")
        material_candy.use_nodes = True 
        
        material_output = material_candy.node_tree.nodes.get("Material Output")
        material_output.location = (1200, 200)
        
        principled_bsdf1 = material_candy.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (900, 200)
        principled_bsdf1.inputs[1].default_value = 0.3
        principled_bsdf1.inputs[3].default_value = (0.799, 0.068, 0.038, 1)
        principled_bsdf1.inputs[4].default_value = 0
        principled_bsdf1.inputs[7].default_value = 0.2
        
        colorramp1_node = material_candy.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (600, 200)
        colorramp1_node.color_ramp.elements.new(0)
        colorramp1_node.color_ramp.elements.new(0.1)
        colorramp1_node.color_ramp.elements.new(0.2)
        colorramp1_node.color_ramp.elements[0].position = 0.163
        colorramp1_node.color_ramp.elements[0].color = (1, 1, 1, 1)
        colorramp1_node.color_ramp.elements[1].position = 0.355
        colorramp1_node.color_ramp.elements[1].color = (1, 0.044, 0.058, 1)
        colorramp1_node.color_ramp.elements[2].position = 0.5
        colorramp1_node.color_ramp.elements[2].color = (0.768, 0, 0.002, 1)
        colorramp1_node.color_ramp.elements[3].position = 0.652
        colorramp1_node.color_ramp.elements[3].color = (1, 0.044, 0.058, 1)
        colorramp1_node.color_ramp.elements[4].position = 0.822
        colorramp1_node.color_ramp.elements[4].color = (1, 1, 1, 1)
        
        bump1_node = material_candy.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (600, -200)
        bump1_node.inputs[0].default_value = 0.02
        bump1_node.inputs[1].default_value = 1
        
        math1_node = material_candy.node_tree.nodes.new("ShaderNodeMath")
        math1_node.location = (300, 200)
        math1_node.operation = "FRACT"
        
        noise1_node = material_candy.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (300, -200)
        noise1_node.inputs[2].default_value = 2
        noise1_node.inputs[3].default_value = 15
        noise1_node.inputs[4].default_value = 0.5
        noise1_node.inputs[5].default_value = 0
        
        math2_node = material_candy.node_tree.nodes.new("ShaderNodeMath")
        math2_node.location = (0, 200)
        math2_node.operation = "MULTIPLY"
        math2_node.inputs[1].default_value = 13
        
        texcoord1_node = material_candy.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (0, -200)
        
        gradient1_node = material_candy.node_tree.nodes.new("ShaderNodeTexGradient")
        gradient1_node.location = (-300, 200)
        gradient1_node.gradient_type = "RADIAL"
        
        mapping1_node = material_candy.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-600, 200)
        
        combineXYZ1_node = material_candy.node_tree.nodes.new("ShaderNodeCombineXYZ")
        combineXYZ1_node.location = (-900, 0)
        
        math3_node = material_candy.node_tree.nodes.new("ShaderNodeMath")
        math3_node.location = (-1200, 0)
        math3_node.operation = "MULTIPLY"
        math3_node.inputs[1].default_value = 2
        
        gradient2_node = material_candy.node_tree.nodes.new("ShaderNodeTexGradient")
        gradient2_node.location = (-1500, 0)
        gradient2_node.gradient_type = "SPHERICAL"
                
        mapping2_node = material_candy.node_tree.nodes.new("ShaderNodeMapping")
        mapping2_node.location = (-1800, 0)        
        mapping2_node.inputs[3].default_value[2] = 0
        
        texcoord2_node = material_candy.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord2_node.location = (-2100, 200)
        
        material_candy.node_tree.links.new(mapping1_node.outputs[0], gradient1_node.inputs[0])
        material_candy.node_tree.links.new(gradient1_node.outputs[0], math2_node.inputs[0])
        material_candy.node_tree.links.new(math2_node.outputs[0], math1_node.inputs[0])
        material_candy.node_tree.links.new(math1_node.outputs[0], colorramp1_node.inputs[0])
        material_candy.node_tree.links.new(colorramp1_node.outputs[0], principled_bsdf1.inputs[0])
        material_candy.node_tree.links.new(principled_bsdf1.outputs[0], material_output.inputs[0])
        material_candy.node_tree.links.new(texcoord1_node.outputs[3], noise1_node.inputs["Vector"])
        material_candy.node_tree.links.new(noise1_node.outputs[0], bump1_node.inputs[2])
        material_candy.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])
        material_candy.node_tree.links.new(texcoord2_node.outputs[3], mapping2_node.inputs[0])
        material_candy.node_tree.links.new(texcoord2_node.outputs[3], mapping1_node.inputs[0])
        material_candy.node_tree.links.new(mapping2_node.outputs[0], gradient2_node.inputs["Vector"])
        material_candy.node_tree.links.new(gradient2_node.outputs[0], math3_node.inputs[0])
        material_candy.node_tree.links.new(math3_node.outputs[0], combineXYZ1_node.inputs[2])
        material_candy.node_tree.links.new(combineXYZ1_node.outputs[0], mapping1_node.inputs[2]) 
        
        bpy.context.object.active_material = material_candy
        return  {"FINISHED"}   





class SHADER_OT_SNOW(bpy.types.Operator):
    bl_label = "Snow"
    bl_idname = "shader.snow_operator"
    
    def execute(self, context):
        material_snow = bpy.data.materials.new(name="Snow")
        material_snow.use_nodes = True 

        material_output = material_snow.node_tree.nodes.get("Material Output")
        material_output.location = (1200, 200)

        principled_bsdf1 = material_snow.node_tree.nodes.get("Principled BSDF")
        principled_bsdf1.location = (900, 200)
        principled_bsdf1.inputs[3].default_value = (0.8, 0.8, 0.8, 1)
        principled_bsdf1.inputs[7].default_value = 0.1
        
        bump1_node = material_snow.node_tree.nodes.new("ShaderNodeBump")
        bump1_node.location = (600, -300)
        bump1_node.inputs[0].default_value = 0.2
        bump1_node.inputs[1].default_value = 1 
    
        bump2_node = material_snow.node_tree.nodes.new("ShaderNodeBump")
        bump2_node.location = (400, -200)
        bump2_node.inputs[0].default_value = 0.2
        bump2_node.inputs[1].default_value = 1 
        
        bump3_node = material_snow.node_tree.nodes.new("ShaderNodeBump")
        bump3_node.location = (200, -100)
        bump3_node.inputs[0].default_value = 0.1
        bump3_node.inputs[1].default_value = 1 

        colorramp1_node = material_snow.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp1_node.location = (-100, 200)
        colorramp1_node.color_ramp.elements[0].position = 0
        colorramp1_node.color_ramp.elements[0].color = (0.244, 0.378, 0.902, 1)
        colorramp1_node.color_ramp.elements[1].position = 1
        colorramp1_node.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        mix1_node = material_snow.node_tree.nodes.new("ShaderNodeMixRGB")
        mix1_node.location = (-300, 200)
        mix1_node.blend_type = "MIX"
        mix1_node.inputs[0].default_value = 0.5

        voronoi1_node = material_snow.node_tree.nodes.new("ShaderNodeTexVoronoi")
        voronoi1_node.location = (-600, 300)
        voronoi1_node.voronoi_dimensions = "3D"
        voronoi1_node.feature = "F1"
        voronoi1_node.distance = "EUCLIDEAN"
        voronoi1_node.inputs[2].default_value = 4.5
        voronoi1_node.inputs[3].default_value = 1
        
        voronoi2_node = material_snow.node_tree.nodes.new("ShaderNodeTexVoronoi")
        voronoi2_node.location = (-600, 0)
        voronoi2_node.voronoi_dimensions = "3D"
        voronoi2_node.feature = "F2"
        voronoi2_node.distance = "MANHATTAN"
        voronoi2_node.inputs[2].default_value = 50
        voronoi2_node.inputs[3].default_value = 1
        
        noise1_node = material_snow.node_tree.nodes.new("ShaderNodeTexNoise")
        noise1_node.location = (-600, -300)
        noise1_node.inputs[2].default_value = 4
        noise1_node.inputs[3].default_value = 2
        noise1_node.inputs[4].default_value = 0.5
        noise1_node.inputs[5].default_value = 0
        
        noise2_node = material_snow.node_tree.nodes.new("ShaderNodeTexNoise")
        noise2_node.location = (-600, -600)
        noise2_node.inputs[2].default_value = 170
        noise2_node.inputs[3].default_value = 16
        noise2_node.inputs[4].default_value = 0.5
        noise2_node.inputs[5].default_value = 0
        
        mapping1_node = material_snow.node_tree.nodes.new("ShaderNodeMapping")
        mapping1_node.location = (-900, -100)
        
        texcoord1_node = material_snow.node_tree.nodes.new("ShaderNodeTexCoord")
        texcoord1_node.location = (-1200, -100)

        material_snow.node_tree.links.new(texcoord1_node.outputs[3], mapping1_node.inputs[0])
        material_snow.node_tree.links.new(mapping1_node.outputs[0], voronoi1_node.inputs["Vector"])
        material_snow.node_tree.links.new(mapping1_node.outputs[0], voronoi2_node.inputs["Vector"])
        material_snow.node_tree.links.new(mapping1_node.outputs[0], noise1_node.inputs["Vector"])
        material_snow.node_tree.links.new(mapping1_node.outputs[0], noise2_node.inputs["Vector"])
        material_snow.node_tree.links.new(voronoi1_node.outputs[0], mix1_node.inputs[1])
        material_snow.node_tree.links.new(voronoi2_node.outputs[0], mix1_node.inputs[2])
        material_snow.node_tree.links.new(noise1_node.outputs[0], bump2_node.inputs[2])
        material_snow.node_tree.links.new(noise2_node.outputs[0], bump3_node.inputs[2])
        material_snow.node_tree.links.new(mix1_node.outputs[0], colorramp1_node.inputs[0])
        material_snow.node_tree.links.new(colorramp1_node.outputs[0], principled_bsdf1.inputs[0]) 
        material_snow.node_tree.links.new(colorramp1_node.outputs[0], bump3_node.inputs[2])
        material_snow.node_tree.links.new(bump3_node.outputs[0], bump2_node.inputs["Normal"])
        material_snow.node_tree.links.new(bump2_node.outputs[0], bump1_node.inputs["Normal"])
        material_snow.node_tree.links.new(bump1_node.outputs[0], principled_bsdf1.inputs[20])

        bpy.context.object.active_material = material_snow
        return  {"FINISHED"}   

        





def register():
    # Panels
    bpy.utils.register_class(PRECIOUS_METALS)
    bpy.utils.register_class(GENERAL_METAL)
    bpy.utils.register_class(WINTER)
    # Precious Metals
    bpy.utils.register_class(SHADER_OT_GOLD_METAL)
    bpy.utils.register_class(SHADER_OT_GOLD_RUSTED)
    bpy.utils.register_class(SHADER_OT_GOLD_NUGGET)
    bpy.utils.register_class(SHADER_OT_SILVER_METAL)
    bpy.utils.register_class(SHADER_OT_SILVER_RUSTED)
    bpy.utils.register_class(SHADER_OT_SILVER_NUGGET)
    # General Metal
    bpy.utils.register_class(SHADER_OT_GENERAL_METAL)
    bpy.utils.register_class(SHADER_OT_METAL_GALVANIZED)
    bpy.utils.register_class(SHADER_OT_METAL_DAMAGED)
    bpy.utils.register_class(SHADER_OT_METAL_NUGGET)
    bpy.utils.register_class(SHADER_OT_METAL_RUSTY)
    bpy.utils.register_class(SHADER_OT_METAL_SCRATCHED)
    bpy.utils.register_class(SHADER_OT_CHROME)
    # Winter
    bpy.utils.register_class(SHADER_OT_GINGERBREAD)
    bpy.utils.register_class(SHADER_OT_CANDY)
    bpy.utils.register_class(SHADER_OT_SNOW)
    
    
    
def unregister():
    # Panels
    bpy.utils.unregister_class(PRECIOUS_METALS)
    bpy.utils.unregister_class(GENERAL_METAL)
    bpy.utils.unregister_class(WINTER)
    # Precious Metals
    bpy.utils.unregister_class(SHADER_OT_GOLD_METAL)
    bpy.utils.unregister_class(SHADER_OT_GOLD_RUSTED)
    bpy.utils.unregister_class(SHADER_OT_GOLD_NUGGET)
    bpy.utils.unregister_class(SHADER_OT_SILVER_METAL)
    bpy.utils.unregister_class(SHADER_OT_SILVER_RUSTED)
    bpy.utils.unregister_class(SHADER_OT_SILVER_NUGGET)
    # General Metal
    bpy.utils.unregister_class(SHADER_OT_GENERAL_METAL)
    bpy.utils.unregister_class(SHADER_OT_METAL_GALVANIZED)
    bpy.utils.unregister_class(SHADER_OT_METAL_DAMAGED)
    bpy.utils.unregister_class(SHADER_OT_METAL_NUGGET)
    bpy.utils.unregister_class(SHADER_OT_METAL_RUSTY)
    bpy.utils.unregister_class(SHADER_OT_METAL_SCRATCHED)
    bpy.utils.unregister_class(SHADER_OT_CHROME)    
    # Winter
    bpy.utils.unregister_class(SHADER_OT_GINGERBREAD)
    bpy.utils.unregister_class(SHADER_OT_CANDY)
    bpy.utils.unregister_class(SHADER_OT_SNOW)
    

if __name__ == "__main__":
    register()
