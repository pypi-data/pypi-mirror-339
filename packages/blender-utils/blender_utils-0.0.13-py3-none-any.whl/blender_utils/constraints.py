from math import radians

from .bone import get_pose_bone
from .get_b_vars import get_active_object 

def add_stretch_to_constraint (
  bone, 
  subtarget, 
  head_tail = 0, 
  target = None
):
  pose_bone = get_pose_bone(bone)
  
  if pose_bone:
    constraint = pose_bone.constraints.new('STRETCH_TO')
    constraint.target = target or get_active_object()
    constraint.subtarget = subtarget
    constraint.head_tail = head_tail

def add_ik_constraint (
  bone, 
  subtarget, 
  chain_count, 
  pole_subtarget = '', 
  target = None
):
  pose_bone = get_pose_bone(bone)

  if pose_bone:
    constraint = pose_bone.constraints.new('IK')
    constraint.target = target or get_active_object()
    constraint.subtarget = subtarget
    constraint.chain_count = chain_count
    constraint.pole_target = get_active_object()
    constraint.pole_subtarget = pole_subtarget

def add_copy_rotation_constraint (
  bone, 
  subtarget, 
  use_x = True,
  use_y = True, 
  use_z = True,
  invert_x = False,
  invert_y = False,
  invert_z = False,
  target_space = 'WORLD',
  owner_space = 'WORLD',
  influence = 1,
  target = None
):
  pose_bone = get_pose_bone(bone)

  if pose_bone:
    constraint = pose_bone.constraints.new('COPY_ROTATION')
    constraint.target = target or get_active_object()
    constraint.subtarget = subtarget
    constraint.target_space = target_space
    constraint.owner_space = owner_space
    constraint.use_x = use_x
    constraint.use_y = use_y
    constraint.use_z = use_z
    constraint.invert_x = invert_x
    constraint.invert_y = invert_y
    constraint.invert_z = invert_z
    constraint.influence = influence

def add_copy_location_constraint (
  bone, 
  subtarget, 
  target_space = 'WORLD',
  owner_space = 'WORLD',
  target = None
):
  pose_bone = get_pose_bone(bone)

  if pose_bone:
    constraint = pose_bone.constraints.new('COPY_LOCATION')
    constraint.target = target or get_active_object()
    constraint.subtarget = subtarget
    constraint.target_space = target_space
    constraint.owner_space = owner_space

def add_limit_rotation_constraint (
  bone, 
  owner_space = 'WORLD',
  use_legacy_behavior = False,
  use_limit_x = False,
  min_x = 0, 
  max_x = 0,
  use_limit_y = False,
  min_y = 0, 
  max_y = 0,
  use_limit_z = False,
  min_z = 0, 
  max_z = 0
):
  pose_bone = get_pose_bone(bone)

  if pose_bone:
    constraint = pose_bone.constraints.new('LIMIT_ROTATION')
    constraint.owner_space = owner_space
    constraint.use_limit_x = use_limit_x
    constraint.min_x = radians(min_x)
    constraint.max_x = radians(max_x)
    constraint.use_limit_y = use_limit_y
    constraint.min_y = radians(min_y)
    constraint.max_y = radians(max_y)
    constraint.use_limit_z = use_limit_z
    constraint.min_z = radians(min_z)
    constraint.max_z = radians(max_z)
    constraint.use_legacy_behavior = use_legacy_behavior

def add_copy_transforms_constraint (
  bone_name, 
  subtarget, 
  target_space = 'WORLD', 
  owner_space = 'WORLD', 
  influence = 1,
  target = None
):
  pose_bone = get_pose_bone(bone_name)

  if pose_bone:
    constraint = pose_bone.constraints.new('COPY_TRANSFORMS')
    constraint.target = target or get_active_object()
    constraint.subtarget = subtarget
    constraint.target_space = target_space
    constraint.owner_space = owner_space
    constraint.influence = influence
     
def add_copy_scale_constraint (
  bone, 
  subtarget, 
  target_space = 'WORLD', 
  owner_space = 'WORLD',
  target = None
):
  pose_bone = get_pose_bone(bone)

  if pose_bone:
    constraint = pose_bone.constraints.new('COPY_SCALE')
    constraint.target = target or get_active_object()
    constraint.subtarget = subtarget
    constraint.target_space = target_space
    constraint.owner_space = owner_space

def add_damped_track_constraint (
  bone, 
  subtarget, 
  track_axis = 'TRACK_Y',
  head_tail = 0,
  influence = 1,
  target = None
):
  pose_bone = get_pose_bone(bone)

  if pose_bone:
    constraint = pose_bone.constraints.new('DAMPED_TRACK')
    constraint.target = target or get_active_object()
    constraint.subtarget = subtarget
    constraint.track_axis = track_axis
    constraint.head_tail = head_tail
    constraint.influence = influence

def add_armature_constraint (bone, subtarget, target = None):
  pose_bone = get_pose_bone(bone)

  if pose_bone:
    constraint = pose_bone.constraints.new('ARMATURE')
    target = target or get_active_object()

    for _subtarget in subtarget:
      _target = constraint.targets.new()
      _target.target = target
      _target.subtarget = _subtarget

def add_limit_location_constraint (
  bone, 
  owner_space = 'WORLD',
  use_min_x = False,
  min_x = 0,
  use_min_y = False,
  min_y = 0,
  use_min_z = False,
  min_z = 0,
  use_max_x = False,
  max_x = 0,
  use_max_y = False,
  max_y = 0,
  use_max_z = False,
  max_z = 0,
  influence = 1
):
  pose_bone = get_pose_bone(bone)

  if pose_bone:
    constraint = pose_bone.constraints.new('LIMIT_LOCATION')
    constraint.owner_space = owner_space
    constraint.use_min_x = use_min_x
    constraint.use_min_y = use_min_y
    constraint.use_min_z = use_min_z
    constraint.use_max_x = use_max_x
    constraint.use_max_y = use_max_y
    constraint.use_max_z = use_max_z
    constraint.min_x = min_x
    constraint.min_y = min_y
    constraint.min_z = min_z
    constraint.max_x = max_x
    constraint.max_y = max_y
    constraint.max_z = max_z
    constraint.influence = influence
