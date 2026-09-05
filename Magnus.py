Web VPython 3.2

scene.width = 700
scene.height = 500
scene.background = vector(1, 1, 1)
scene.ambient = vector(0.4, 0.4, 0.4)
scene.title = "Magnus Effect Simulation"
scene.range = 40
scene.center = vector(20, 10, 0)

dt = 0.005
vx, vy, vz = 25.0, 20.0, 5.0
rx, ry, rz = 0.0, 0.0, 40.0   # rad/s (rz > 0 produces topspin/backspin effects)

ballCd = 0.54
ballCl = 0.25
ballmass = 0.6237
ballr = 0.5
airD = 1.225
ballCSA = 0.046
g = vector(0, -9.8, 0)

running = False

sloc = vector(0, 0, 0)
ball = sphere(pos=sloc, radius=ballr, color=vector(0.94, 0.45, 0.1), make_trail=True, retain=200)
analytic = curve(color=color.red)

floor = box(pos=vector(20, -ballr, 0), size=vector(150, 0.2, 80), color=vector(0.8, 0.7, 0.6))
varrow = arrow(pos=sloc, axis=vector(vx, vy, vz) * 0.2, shaftwidth=0.2, color=color.blue)

scene.append_to_caption("\n<b>Launch Controls</b>\n")

def launch_action():
    global running
    if not running:
        running = True
        run_simulation()

button(text="Launch Ball", bind=launch_action)

def set_vx(s):
    global vx
    vx = s.value
    lbl_vx.text = " vx: " + str(round(vx, 1)) + " m/s |"
    varrow.axis = vector(vx, vy, vz) * 0.2

def set_vy(s):
    global vy
    vy = s.value
    lbl_vy.text = " vy: " + str(round(vy, 1)) + " m/s |"
    varrow.axis = vector(vx, vy, vz) * 0.2

def set_rz(s):
    global rz
    rz = s.value
    lbl_rz.text = " rz (spin): " + str(round(rz, 1)) + " rad/s\n"

scene.append_to_caption("\n\n")
slider(min=0, max=50, value=vx, bind=set_vx)
lbl_vx = wtext(text=" vx: " + str(vx) + " m/s |")

slider(min=0, max=50, value=vy, bind=set_vy)
lbl_vy = wtext(text=" vy: " + str(vy) + " m/s |")

slider(min=-100, max=100, value=rz, bind=set_rz)
lbl_rz = wtext(text=" rz (spin): " + str(rz) + " rad/s\n")

def run_simulation():
    global running
    varrow.visible = False
    ball.pos = vector(sloc.x, sloc.y, sloc.z)
    ball.velocity = vector(vx, vy, vz)
    ball.clear_trail()
    analytic.clear()
    
    omega = vector(rx, ry, rz)
    sim_time = 0.0

    while ball.pos.y >= 0:
        rate(1 / dt)
        
        v = ball.velocity
        v_mag = mag(v)
        
        if v_mag > 0:
            # Aerodynamic Drag: Fd = -0.5 * Cd * rho * A * v^2 * v_hat
            fd = -0.5 * ballCd * airD * ballCSA * (v_mag**2) * norm(v)
            
            # Magnus Force: Fm = 0.5 * Cl * rho * A * r * (omega x v)
            fm = 0.5 * ballCl * airD * ballCSA * ballr * cross(omega, v)
        else:
            fd = vector(0, 0, 0)
            fm = vector(0, 0, 0)

        # Net Acceleration
        a = g + (fd + fm) / ballmass
        ball.velocity += a * dt
        ball.pos += ball.velocity * dt
        
        # Ball Rotation
        ball.rotate(angle=mag(omega) * dt, axis=norm(omega) if mag(omega) > 0 else vector(1, 0, 0))
        
        # Analytic comparison (vacuum trajectory)
        analytic.append(pos=sloc + vector(vx, vy, vz) * sim_time + 0.5 * g * (sim_time**2))
        
        sim_time += dt

    varrow.pos = ball.pos
    varrow.visible = True
    running = False
