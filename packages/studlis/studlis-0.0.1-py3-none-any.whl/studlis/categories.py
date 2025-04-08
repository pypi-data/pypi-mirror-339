def parse_category_tree(categories):
    """
    
    """
    tree=[]
    tree_dict = {}
    for category in categories:
        walk_category_tree(category,tree,tree_dict)
    return tree,tree_dict



def walk_category_tree(config_node,tree,tree_dict,parent_node=None):
    """
    
    """
    
    if not "name" in config_node:
        raise ValueError("Category does not have a name")
    caption = config_node["name"] if not "caption" in config_node else config_node["caption"]
    if parent_node is not None:
        path = parent_node["path"]+"/"+config_node["name"]
    else:
        path = "/"+config_node["name"]

    permission_group_filter = [] if not "permission_group_filter" in config_node else config_node["permission_group_filter"]
    if len(permission_group_filter) ==0:
        if parent_node is not None:
            permission_group_filter = parent_node["permission_group_filter"]
        else:
            print("Warning: Category %s does not have any allowed permission groups. Set to ':everyone' to allow everyone." % caption)
    
    
    item = {"name":config_node["name"],"caption":caption,"path":path,"children":[],"permission_group_filter":permission_group_filter}
    tree.append(item)
    tree_dict[path]=item
    if "children" in config_node:
        for config_child in config_node["children"]:
            walk_category_tree(config_child,item["children"],tree_dict,item)

   


