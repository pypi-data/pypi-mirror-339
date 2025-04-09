from .get_b_vars import get_data

def append_node_tree (filepath, node_group_name = ''):
  with get_data().libraries.load(filepath, link = False) as (data_from, data_to):
    if node_group_name:
      data_to.node_groups.append(node_group_name)
    else:
      # 原来的节点组不会消失
      data_to.node_groups = data_from.node_groups
