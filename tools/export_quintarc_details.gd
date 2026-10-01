extends SceneTree

# Run against the game project to preserve its exact labels, values and ordering.
func _initialize() -> void:
 var output = OS.get_cmdline_user_args()[0]
 var details = {}
 for key in QuintarcRecipes.keys():
  details[key] = QuintarcSkills.details(key)
 var file = FileAccess.open(output, FileAccess.WRITE)
 file.store_string(JSON.stringify(details))
 file.close()
 quit()
