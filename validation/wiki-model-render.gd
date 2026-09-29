extends SceneTree
var camera: Camera3D
var subject: Node3D
var outputs: Array = []
func _initialize():
 call_deferred("run")
func run():
 root.size = Vector2i(512,512)
 root.position = Vector2i(1800,80)
 var environment = WorldEnvironment.new()
 environment.environment = Environment.new()
 environment.environment.background_mode = Environment.BG_COLOR
 environment.environment.background_color = Color("141c30")
 environment.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
 environment.environment.ambient_light_color = Color("dce7ff")
 environment.environment.ambient_light_energy = .75
 root.add_child(environment)
 var light = DirectionalLight3D.new()
 light.rotation_degrees = Vector3(-32,-28,0)
 light.light_energy = 1.4
 root.add_child(light)
 var fill = DirectionalLight3D.new()
 fill.rotation_degrees = Vector3(-15,145,0)
 fill.light_energy = .45
 root.add_child(fill)
 camera = Camera3D.new()
 camera.projection = Camera3D.PROJECTION_ORTHOGONAL
 camera.near = .01
 camera.far = 1000
 root.add_child(camera)
 Glyphs.setup()
 DirAccess.make_dir_recursive_absolute("/tmp/justpolygames-site/assets/item-images")
 DirAccess.make_dir_recursive_absolute("/tmp/justpolygames-site/assets/mob-images")
 for id in Glyphs.items:
  subject = PencilArt.item(id)
  if id == "hole":
   # Hole has no loose-item mesh: render its actual circle-and-X recipe strokes.
   for stroke in Glyphs.items[id].strokes:
    for i in range(1,stroke.size()):
     var a: Vector2 = stroke[i-1]
     var b: Vector2 = stroke[i]
     PencilArt.rod(subject,Vector3(a.x-.5,.5-a.y,0),Vector3(b.x-.5,.5-b.y,0),.016,Glyphs.PAPER)
  root.add_child(subject)
  await capture("/tmp/justpolygames-site/assets/item-images/"+id+".png")
 for kind in ["wraith","skitter","spitter","brute","sentinel","thorn","eraser"]:
  subject = PencilArt.monster(kind)
  root.add_child(subject)
  await capture("/tmp/justpolygames-site/assets/mob-images/project-pencil-"+kind+".png")
 for kind in QuintarcEnemyAppearance.MODELS:
  subject = Node3D.new()
  root.add_child(subject)
  QuintarcEnemyAppearance.build(subject,kind,2.0)
  await capture("/tmp/justpolygames-site/assets/mob-images/quintarc-"+kind+".png")
 var f = FileAccess.open("/tmp/wiki-model-render/results.json",FileAccess.WRITE)
 f.store_string(JSON.stringify(outputs,"  "))
 print("WIKI_RENDERS_COMPLETE: ",outputs.size())
 quit()
func capture(path: String):
 await process_frame
 await process_frame
 var points: Array[Vector3] = []
 for mesh in subject.find_children("*","MeshInstance3D",true,false):
  if not mesh.visible: continue
  var box: AABB = mesh.get_aabb()
  for i in range(8): points.append(mesh.global_transform*box.get_endpoint(i))
 assert(points.size()>0,"No renderable meshes for "+path)
 var bounds = AABB(points[0],Vector3.ZERO)
 for point in points: bounds = bounds.expand(point)
 var center = bounds.get_center()
 camera.position = center+Vector3(.45,.22,1).normalized()*maxf(10,bounds.size.length()*2)
 camera.look_at(center)
 var right = camera.global_basis.x
 var up = camera.global_basis.y
 var half = .01
 for point in points: half = maxf(half,maxf(absf((point-center).dot(right)),absf((point-center).dot(up))))
 camera.size = half*2.4
 for i in range(4): await process_frame
 await RenderingServer.frame_post_draw
 var picture = root.get_texture().get_image()
 assert(picture.save_png(path)==OK)
 outputs.append({"path":path,"meshes":points.size()/8,"width":picture.get_width(),"height":picture.get_height()})
 print("CAPTURED: ",path)
 subject.queue_free()
 await process_frame
