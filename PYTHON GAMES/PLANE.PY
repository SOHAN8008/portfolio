from ursina import * 

app=Ursina()
me=Animation(
    'assets/players',
     collider='box',y=5
)
Sky()
camera.orthographic = True
camera.fov = 20

Entity(
    model='quad',
    texture='assets/BG',
    scale=36,z=1
)

fly= Entity(
    model='cube',
    Texture='assets//fly1',
    collider='box',
    scale=2,x=20,y=-10
)
flies = []
def newfly():
   new = duplicate(
     fly,
     y=-5+(5124*time.dt)%15
    )
   flies.append(new)
   invoke(newfly, delay=1)
newfly()


def update():
    for fly in flies:
        fly.x -=4*time.dt
    me.y +=held_keys['w']*6*time.dt 
    me.y -=held_keys['s']*6*time.dt  
    a= held_keys['w']*-20
    b= held_keys['s']*20
    if a != 0:
        me.rotation_z = a
    else:
     me.rotation_z = a

    for fly in flies :
        fly.x -= 4*time.dt 
        touch = fly.intersects()
        if touch.hit:
            flies.remove()
            destroy(fly)
        t = me.intersects()
        if t.hit and t.entity.scale==2:
            quit


def input(key):
    if key == 'space':
        e = Entity(
            y=me.y,
            x=me.x+2,
            model='cube',
            texture='assets/bullet',
            collider='cube'
        )
        e.animate_x(
         30,
         duration=2,
         curve=curve.linear
        )
        invoke(destroy, e,
                  delat=2)
app.run()