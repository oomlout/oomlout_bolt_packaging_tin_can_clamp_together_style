import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    oomp_mode = "project"
    #oomp_mode = "oobb"

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr", "laser", "true"]
    elif typ == "fast":
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 3
        kwargs["height"] = 3
        kwargs["thickness"] = 12
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        #names = ["base","top","bottom","clip"]
        extras = ["", "middle", "top","sides"]

        for ex in extras:
            part = copy.deepcopy(part_default)
            p3 = copy.deepcopy(kwargs)
            p3["width"] = 3
            p3["height"] = 3
            #p3["thickness"] = 6
            if ex != "":
                p3["extra"] = ex
            part["kwargs"] = p3
            nam = "base"
            part["name"] = nam
            if oomp_mode == "oobb":
                p3["oomp_size"] = nam
            parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        scad_help.generate_navigation(sort = sort)


def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    depth_top_plate = 3
    depth_can_top = 3

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    if extra == "middle":
        p3["depth"] = depth - depth_top_plate
    if extra == "top":
        p3["depth"] = depth_top_plate + depth_can_top
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos) 
    pos1[2] += -depth + depth_top_plate 
    if extra == "middle":
        pos1[2] += -3  
    if extra == "top":
        pos1[2] += 6
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add cans
    if True:
        
        clearance_can_thickness = 0.5
        poss = []
        shift_x = 37.5
        shift_y = 37.5
        shift_z = 0
        poss.append([shift_x, shift_y, shift_z])
        poss.append([-shift_x, shift_y, shift_z])
        poss.append([shift_x, -shift_y, shift_z])
        poss.append([-shift_x, -shift_y, shift_z])
        #poss.append([0, 0])
        diameter_can_top = 75
        diameter_can_main = 73
        #depth_can_top = 3
        depth_can_bottom = 3
        depth_can_lid = 1
        depth_can_total = 109
        depth_can_main = depth_can_total - depth_can_top - depth_can_bottom
        #ty = "positive"
        ty = "negative"
        
    
        for pos_shift in poss:            
            #top tube
            p3 = copy.deepcopy(kwargs)
            p3["type"] = ty
            p3["shape"] = f"oobb_tube_new"

            p3["depth"] = depth_can_top
            p3["radius"] = (diameter_can_top+clearance_can_thickness)/2
            p3["wall_thickness"] = 1
            #p3["m"] = "#"
            pos1 = copy.deepcopy(pos)
            pos1[0] += pos_shift[0]
            pos1[1] += pos_shift[1]
            pos1[2] += -depth_can_top + pos_shift[2]
            p3["pos"] = pos1
            oobb_base.append_full(thing,**p3)
            
            #tube lid inset
            current_z = 0
            p3 = copy.deepcopy(kwargs)
            p3["type"] = ty
            p3["shape"] = f"oobb_tube_new"
            p3["depth"] = depth_can_lid
            p3["radius"] = (diameter_can_main+clearance_can_thickness)/2
            p3["wall_thickness"] = 3
            #p3["m"] = "#"
            pos1 = copy.deepcopy(pos)
            pos1[0] += pos_shift[0]
            pos1[1] += pos_shift[1]
            current_z += -depth_can_top
            pos1[2] += current_z + pos_shift[2]
            p3["pos"] = pos1
            oobb_base.append_full(thing,**p3)

            #main tube
            current_z += -depth_can_main
            if extra == "middle":
                #main tube
                p3 = copy.deepcopy(kwargs)
                p3["type"] = ty
                p3["shape"] = f"oobb_cylinder"
                dep = depth_can_main
                p3["depth"] = dep
                p3["radius"] = (diameter_can_main+clearance_can_thickness)/2
                #p3["wall_thickness"] = 1
                #p3["m"] = "#"
                pos1 = copy.deepcopy(pos)
                pos1[0] += pos_shift[0]
                pos1[1] += pos_shift[1]
                pos1[2] += current_z + pos_shift[2] + depth_can_main/2                
                p3["pos"] = pos1
                oobb_base.append_full(thing,**p3)
            else:
                p3 = copy.deepcopy(kwargs)
                p3["type"] = ty
                p3["shape"] = f"oobb_tube_new"
                dep = depth_can_main
                p3["depth"] = dep
                p3["radius"] = (diameter_can_main+clearance_can_thickness)/2
                p3["wall_thickness"] = 1
                #p3["m"] = "#"
                pos1 = copy.deepcopy(pos)
                pos1[0] += pos_shift[0]
                pos1[1] += pos_shift[1]                
                pos1[2] += current_z + pos_shift[2]
                p3["pos"] = pos1
                oobb_base.append_full(thing,**p3)

            #bottom flat
            p3 = copy.deepcopy(kwargs)
            p3["type"] = ty
            p3["shape"] = f"oobb_cylinder"
            p3["depth"] = depth_can_lid
            p3["radius"] = (diameter_can_main+clearance_can_thickness)/2
            #p3["m"] = "#"
            pos1 = copy.deepcopy(pos)
            pos1[0] += pos_shift[0]
            pos1[1] += pos_shift[1]
            #current_z += -depth_can_lid 
            pos1[2] += current_z + pos_shift[2]
            p3["pos"] = pos1
            oobb_base.append_full(thing,**p3)

            #bottom tube
            p3 = copy.deepcopy(kwargs)
            p3["type"] = ty
            p3["shape"] = f"oobb_tube_new"
            p3["depth"] = depth_can_bottom
            p3["radius"] = (diameter_can_main+clearance_can_thickness)/2
            p3["wall_thickness"] = 1
            #p3["m"] = "#"
            pos1 = copy.deepcopy(pos)
            pos1[0] += pos_shift[0]
            pos1[1] += pos_shift[1]
            current_z += -depth_can_bottom
            pos1[2] += current_z + pos_shift[2]
            p3["pos"] = pos1
            oobb_base.append_full(thing,**p3)
            
                


    


    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    dep = 250
    p3["depth"] = dep
    p3["holes"] = "single"
    locs = []
    single_mm = 1.5/15
    locs.append([1-single_mm,1-single_mm])
    locs.append([width+single_mm,1-single_mm])
    locs.append([1-single_mm,height+single_mm])
    locs.append([width+single_mm,height+single_mm])
    locs.append([2,2])
    p3["locations"] = locs
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[2] += -dep/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    
    if extra == "sides":
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += 0
        pos1[2] += -depth_can_top
        p3["pos"] = pos1
        p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

    if prepare_print:        
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        components_third = copy.deepcopy(thing["components"])
        components_fourth = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 150
        pos1[2] += 0
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

        #add third copy        
        return_value_3 = {}
        return_value_3["type"]  = "rotation"
        return_value_3["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 150
        pos1[1] += 150
        pos1[2] += -depth_top_plate
        return_value_3["pos"] = pos1
        return_value_3["rot"] = [180,0,0]
        return_value_3["objects"] = components_third
        thing["components"].append(return_value_3)

        #add fourth copy
        return_value_4 = {}
        return_value_4["type"]  = "rotation"
        return_value_4["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[1] += 150
        pos1[2] += 3.5
        return_value_4["pos"] = pos1
        return_value_4["rot"] = [0,0,0]
        return_value_4["objects"] = components_fourth
        thing["components"].append(return_value_4)

        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += 0
        pos1[2] += -500
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
    
if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)