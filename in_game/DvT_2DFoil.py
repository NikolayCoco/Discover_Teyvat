# @Saltfish 2025/11/17 update
# This Python script is used for:
# 1. Generate unspecified portrait:
#     Don't forget tell me your trigger (`'''+modprefix+'''_portrait_trigger`) 
# 2. Generate specified portrait:
#     Use `var:portrait_locked ?= flag:%s` instead
#     %s is your flag value assigned from Clausewitz script
# 3. Generate both unspecified and specified as same time:
#    Use `trigger_if = { limit = { has_variable = portrait_locked } var:portrait_locked ?= flag:%s }` instead
#    %s is your flag value assigned from Clausewitz script
import os

gfxmodpath = r"C:\Users\MicHB\Documents\Paradox Interactive\Europa Universalis V\mod\Discover_Teyvat\in_game"
modprefix = "DvT"

assetpath = os.path.join(gfxmodpath, "gfx\\models\\props", modprefix)
accessorypath = os.path.join(gfxmodpath, "gfx\\portraits\\accessories\\"+modprefix+"_props.txt")
genepath = os.path.join(gfxmodpath, "common\\genes\\"+modprefix+"_genes_special_accessories_misc.txt")
gfxmodifierpath = os.path.join(gfxmodpath, "gfx\\portraits\\portrait_modifiers\\"+modprefix+"_portrait.txt")
encoding = "utf_8_sig"

output_asset = open(os.path.join(assetpath, "00_"+modprefix+".asset"), "w", encoding=encoding)
output_accessory = open(accessorypath, "w", encoding=encoding)
output_gene = open(genepath, "w", encoding=encoding)
output_gfxmodifier = open(gfxmodifierpath, "w", encoding=encoding)
output_gfxmodifier.write(modprefix+"_portrait = {\n\tusage = game\n\tpriority = 100\n")
id = 0
slices = 1

output_gene.write('''accessory_genes = {
\t'''+modprefix+'''props_'''+str(slices)+''' = {
\t\tgene_'''+modprefix+'''_blank_'''+str(slices)+''' = {
\t\t\tindex = 0
\t\t}''')
for root, dirs, files in os.walk(gfxmodpath):
    for file in files:
        if file[-12:] == '_diffuse.dds':
            name = file[:-12]
            id = id + 1
            if id == 256:
                id = 1
                slices += 1
                output_gene.write('''\n\t}\n\t'''+modprefix+'''props_'''+str(slices)+''' = {\t
\t\tgene_'''+modprefix+'''_blank_'''+str(slices)+''' = {
\t\t\tindex = 0
\t\t}''')
            shortname = file[:-12]
            if int(shortname.split("_")[-1]) <= 50:
                output_gfxmodifier.write('''
\t'''+shortname+''' = {
\t\tdna_modifiers = {
\t\t\taccessory = {
\t\t\t\tmode = replace
\t\t\t\tgene = '''+modprefix+'''props_'''+str(slices)+'''
\t\t\t\ttemplate = '''+shortname+'''
\t\t\t\tvalue = 0.5
\t\t\t}
\t\t}
\t\tweight = {
\t\t\tbase = 0
\t\t\tmodifier = {
\t\t\t\tadd = 255''')
                output_gfxmodifier.write('''
\t\t\t\t'''+modprefix+'''_2D_portrait_trigger = yes
\t\t\t\thas_trait = '''+modprefix+'''_'''+shortname+'''_trait
\t\t\t}
\t\t}
\t}''')
            output_accessory.write(name+" = { entity = { required_tags = \"\" shared_pose_entity = head entity = \""+name+"_entity\" } }\n")
            output_gene.write('''
\t\t'''+shortname+''' = {
\t\t\tindex = '''+str(id)+'''
\t\t\tmale = { 1 = '''+shortname+''' }
\t\t\tfemale = male
\t\t\tboy = male
\t\t\tgirl = male
\t\t\tadolescent_boy = male
\t\t\tadolescent_girl = male
\t\t\tinfant = male
\t\t}''')
            output_asset.write('''
pdxmesh = {
\tname = "'''+name+'''_mesh"
\tfile = "hm_prophet.mesh"
\tscale = 0.8
\tmeshsettings = {
\t\tname = "prophet_shieldShape"
\t\tindex = 0
\t\ttexture_diffuse = "'''+name+'''_diffuse.dds"
\t\ttexture_specular = "'''+name+'''_diffuse.dds"
\t\tshader = "portrait_attachment_alpha_to_coverage"
\t\tshader_file = "gfx/hmportrait.shader"
\t}
}
entity = {
\tname = "'''+name+'''_entity"
\tpdxmesh = "'''+name+'''_mesh"
}
''')

output_gene.write("\n\t}\n}")
output_gfxmodifier.write("\n}")
output_gene.close()
output_gfxmodifier.close()
output_asset.close()
output_accessory.close()
