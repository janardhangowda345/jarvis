import pygame
import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import os 
import re
import requests
import random
import webbrowser
import threading
import math
import subprocess

try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    VOLUME_AVAILABLE = True
except:
    VOLUME_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except:
    PSUTIL_AVAILABLE = False


API_KEY = 'cfc02400bdaecbb945953165695b4b90'
CITY    = 'hoskote'

APPS = {
    'notepad'           : 'notepad.exe',
    'calculator'        : 'calc.exe',
    'paint'             : 'mspaint.exe',
    'word'              : 'winword',
    'excel'             : 'excel',
    'powerpoint'        : 'powerpnt',
    'task manager'      : 'taskmgr.exe',
    'file explorer'     : 'explorer.exe',
    'cmd'               : 'cmd.exe',
    'command prompt'    : 'cmd.exe',
    'vs code'           : 'code',
    'visual studio code': 'code',
    'chrome'            : 'chrome',
    'spotify'           : 'spotify',
}

WEBSITES = {
    'youtube'  : 'https://www.youtube.com',
    'instagram': 'https://www.instagram.com',
    'github'   : 'https://www.github.com',
    'spotify'  : 'https://open.spotify.com',
    'google'   : 'https://www.google.com',
    'linkedin' : 'https://www.linkedin.com',
    'netflix'  : 'https://www.netflix.com',
    'twitter'  : 'https://www.twitter.com',
    'reddit'   : 'https://www.reddit.com',
    'chatgpt'  : 'https://chat.openai.com',
}


pygame.init()
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ARIA — Voice Assistant")

try:
    FONT_TITLE  = pygame.font.SysFont("segoeui", 28, bold=True)
    FONT_STATUS = pygame.font.SysFont("segoeui", 18)
    FONT_MED    = pygame.font.SysFont("segoeui", 15)
    FONT_SMALL  = pygame.font.SysFont("segoeui", 13)
except:
    FONT_TITLE  = pygame.font.Font(None, 32)
    FONT_STATUS = pygame.font.Font(None, 22)
    FONT_MED    = pygame.font.Font(None, 18)
    FONT_SMALL  = pygame.font.Font(None, 16)


C_BG       = (13,  13,  15)
C_CARD     = (22,  22,  26)
C_BORDER   = (40,  40,  48)
C_WHITE    = (240, 240, 255)
C_DIMWHITE = (140, 140, 160)
C_DARK     = (80,  80,  95)

ORB_IDLE     = [(30,  80, 200), (100, 30, 220), (60,  20, 180)]   # blue-purple
ORB_LISTEN   = [(20, 180, 255), (60, 100, 255), (10, 140, 220)]   # bright blue
ORB_SPEAK    = [(220, 30, 180), (140, 20, 240), (180, 10, 160)]   # pink-purple
ORB_THINKING = [(255,140,  20), (220, 60, 20),  (200, 80,  10)]   # amber


state = {
    "listening" : False,
    "speaking"  : False,
    "thinking"  : False,
    "idle"      : True,
    "output"    : "Hi Janardhan! Press SPACE or click the orb to speak.",
    "history"   : [],
    "command_in": "",
    "orb_scale" : 1.0,
    "orb_target": 1.0,
}

recognizer = sr.Recognizer()
engine     = pyttsx3.init()
engine.setProperty('rate', 175)


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def draw_orb(cx, cy, radius, colors, t, active=False):
    c1, c2, cg = colors

    
    for i in range(10, 0, -1):
        r_glow = radius + i * 9
        alpha  = int(6 * i)
        s = pygame.Surface((r_glow*2+4, r_glow*2+4), pygame.SRCALPHA)
        pygame.draw.circle(s, (*cg, alpha), (r_glow+2, r_glow+2), r_glow)
        screen.blit(s, (cx - r_glow - 2, cy - r_glow - 2))

   
    base_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        ratio = r / radius
      
        dark = int(10 + (1 - ratio) * 30)
        pygame.draw.circle(base_surf, (dark, dark, dark+10, 255),
                           (radius, radius), r)
    screen.blit(base_surf, (cx - radius, cy - radius))

   
    streak_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    num_streaks = 6 if active else 3
    for i in range(num_streaks):
        angle  = t * (1.2 + i * 0.3) + i * (math.pi * 2 / num_streaks)
        length = radius * random.uniform(0.4, 0.75) if active else radius * 0.5
        sx     = radius + math.cos(angle) * length * 0.3
        sy     = radius + math.sin(angle) * length * 0.5
        ex     = radius + math.cos(angle + 0.6) * length
        ey     = radius + math.sin(angle + 0.6) * length * 0.8

        streak_color = c1 if i % 2 == 0 else c2
        alpha = int(180 + math.sin(t * 3 + i) * 60) if active else 120

        
        for w in range(6, 0, -2):
            a2 = int(alpha * (w / 6) * 0.6)
            pygame.draw.line(streak_surf, (*streak_color, a2),
                             (int(sx), int(sy)), (int(ex), int(ey)), w)

    
    mask = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255,255,255,255), (radius, radius), radius)
    streak_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(streak_surf, (cx - radius, cy - radius))

   
    bloom_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    bloom_r    = int(radius * (0.35 + math.sin(t * 2) * 0.06))
    bloom_col  = lerp_color(c1, (255, 255, 255), 0.4)
    for i in range(5, 0, -1):
        br = bloom_r + i * 8
        ba = int(20 * i)
        pygame.draw.circle(bloom_surf, (*bloom_col, ba), (radius, radius), br)
    pygame.draw.circle(bloom_surf, (*bloom_col, 180), (radius, radius), bloom_r)
    bloom_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(bloom_surf, (cx - radius, cy - radius))

  
    spec_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    spec_x = int(radius * 0.58)
    spec_y = int(radius * 0.42)
    for i in range(4, 0, -1):
        sr2 = int(radius * 0.18) + i * 4
        sa  = int(35 * i)
        pygame.draw.circle(spec_surf, (255, 255, 255, sa),
                           (spec_x, spec_y), sr2)
    pygame.draw.circle(spec_surf, (255, 255, 255, 160),
                       (spec_x, spec_y), int(radius * 0.10))
    spec_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(spec_surf, (cx - radius, cy - radius))

    rim_s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(rim_s, (*c2, 60), (radius, radius), radius, 3)
    screen.blit(rim_s, (cx - radius, cy - radius))



def speak(text):
    state["speaking"]  = True
    state["thinking"]  = False
    state["idle"]      = False
    state["orb_target"]= 1.15
    engine.say(text)
    engine.runAndWait()
    state["speaking"]  = False
    state["idle"]      = True
    state["orb_target"]= 1.0

def listen():
    state["listening"]  = True
    state["idle"]       = False
    state["orb_target"] = 1.2
    state["output"]     = "Listening..."
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.4)
        try:
            audio   = recognizer.listen(source, timeout=6, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            state["command_in"] = command
            state["listening"]  = False
            state["thinking"]   = True
            state["orb_target"] = 1.05
            state["output"]     = f'"{command}"'
            return command.lower()
        except sr.WaitTimeoutError:
            state["listening"]  = False
            state["orb_target"] = 1.0
            return ""
        except sr.UnknownValueError:
            state["listening"]  = False
            state["orb_target"] = 1.0
            return ""
        except sr.RequestError:
            state["listening"]  = False
            state["orb_target"] = 1.0
            return "service_error"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            desc = data['weather'][0]['description']
            temp = data['main']['temp']
            hum  = data['main']['humidity']
            return f"It's {temp}°C in {CITY} with {desc}. Humidity is {hum}%."
        return "Couldn't get the weather right now."
    except:
        return "Weather service unavailable."

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? They make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call fake spaghetti? An impasta!",
        "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "How many programmers to change a light bulb? None — that's a hardware problem.",
    ]
    return random.choice(jokes)

def calculator(command):
    try:
        match = re.search(
            r'(\d+(?:\.\d+)?)\s*(\+|-|\*|/|plus|minus|times|divided by)\s*(\d+(?:\.\d+)?)',
            command)
        if match:
            n1 = float(match.group(1))
            op = match.group(2)
            n2 = float(match.group(3))
            ops = {'+': n1+n2, 'plus': n1+n2,
                   '-': n1-n2, 'minus': n1-n2,
                   '*': n1*n2, 'times': n1*n2,
                   '/': (n1/n2 if n2 != 0 else None),
                   'divided by': (n1/n2 if n2 != 0 else None)}
            result = ops.get(op)
            if result is None:
                return "You can't divide by zero!"
            result = int(result) if result == int(result) else round(result, 4)
            return f"{n1} {op} {n2} = {result}"
        return "I couldn't parse that. Try: calculate 12 plus 5."
    except:
        return "Calculation error."

def open_app(command):
    for app_name, exe in APPS.items():
        if app_name in command:
            try:
                subprocess.Popen(exe, shell=True)
                return f"Opening {app_name}."
            except Exception as e:
                return f"Couldn't open {app_name}."
    return None

def open_website(command):
    for site, url in WEBSITES.items():
        if site in command:
            webbrowser.open(url)
            return f"Opening {site}."
    return None

def google_search(query):
    q = re.sub(r'(search for|search|google)', '', query).strip()
    if q:
        webbrowser.open(f"https://www.google.com/search?q={q.replace(' ', '+')}")
        return f"Searching for {q}."
    return "What should I search for?"

def adjust_volume(command):
    if not VOLUME_AVAILABLE:
        return "Volume control is unavailable on this system."
    try:
        if "increase" in command or "up" in command:
            volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel() + 2.0, None)
            return "Volume increased."
        elif "decrease" in command or "down" in command:
            volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel() - 2.0, None)
            return "Volume decreased."
        elif "mute" in command:
            volume.SetMute(1, None)
            return "Volume muted."
        elif "unmute" in command:
            volume.SetMute(0, None)
            return "Volume unmuted."
        return "Say increase, decrease, mute or unmute."
    except:
        return "Volume adjustment failed."

def get_system_info():
    if not PSUTIL_AVAILABLE:
        return "Please install psutil: pip install psutil"
    cpu  = psutil.cpu_percent(interval=0.5)
    ram  = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return (f"CPU is at {cpu}%. RAM usage is {ram.percent}% "
            f"({round(ram.used/1e9,1)} GB of {round(ram.total/1e9,1)} GB). "
            f"Disk is {disk.percent}% full.")

def get_wikipedia(command):
    query = re.sub(r'(wikipedia|tell me about|what is|who is|search wiki|wiki)', '', command).strip()
    if not query:
        return "What would you like to know about?"
    try:
        summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That's a bit ambiguous. Did you mean: {', '.join(e.options[:3])}?"
    except:
        return "I couldn't find that on Wikipedia."


def handle_command(command):
    command = command.strip().lower()
    if not command:
        return "I didn't catch that. Please try again."
    if command == "service_error":
        return "Speech service error. Check your internet connection."

    if any(w in command for w in ['hello', 'hi aria', 'hey aria', 'good morning', 'good evening']):
        hour  = datetime.datetime.now().hour
        greet = "Good morning" if hour < 12 else ("Good afternoon" if hour < 18 else "Good evening")
        return f"{greet}, Janardhan! How can I help you?"

    if 'time' in command and 'date' not in command:
        return "It's " + datetime.datetime.now().strftime("%I:%M %p")
    if 'date' in command or 'today' in command:
        return "Today is " + datetime.datetime.now().strftime("%A, %B %d %Y")

    if 'weather' in command:
        return get_weather()
    if 'joke' in command:
        return tell_joke()
    if 'calculat' in command or re.search(r'\d+\s*(plus|minus|times|divided|\+|-|\*|/)\s*\d+', command):
        return calculator(command)
    if any(w in command for w in ['system', 'cpu', 'ram', 'memory', 'disk']):
        return get_system_info()
    if 'volume' in command:
        return adjust_volume(command)
    if 'camera' in command:
        os.system("start microsoft.windows.camera:")
        return "Opening camera."

    result = open_app(command)
    if result:
        return result

    if 'open' in command or any(s in command for s in WEBSITES):
        result = open_website(command)
        if result:
            return result

    if 'search' in command or 'google' in command:
        return google_search(command)

    if any(w in command for w in ['wikipedia', 'tell me about', 'what is', 'who is', 'wiki']):
        return get_wikipedia(command)

    if any(w in command for w in ['bye', 'goodbye', 'exit', 'quit', 'shutdown']):
        speak("Goodbye Janardhan. Have a great day!")
        pygame.quit()
        exit()

    wiki = get_wikipedia(command)
    if "couldn't find" not in wiki.lower() and "what would" not in wiki.lower():
        return wiki

    return f"I'm not sure how to help with that yet."


def run_command_thread():
    command  = listen()
    response = handle_command(command) if command else "I didn't hear anything."
    state["output"]  = response
    state["thinking"]= False
    state["history"].insert(0, {"cmd": state["command_in"] or "—", "res": response})
    state["history"] = state["history"][:5]
    threading.Thread(target=speak, args=(response,), daemon=True).start()


def wrap_text(text, font, max_width):
    words  = text.split()
    lines, current = [], ""
    for word in words:
        test = current + (" " if current else "") + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_ui(t):
    screen.fill(C_BG)

    if state["listening"]:
        orb_colors = ORB_LISTEN
        status_txt = "Listening..."
        status_col = (100, 200, 255)
    elif state["speaking"]:
        orb_colors = ORB_SPEAK
        status_txt = "Speaking..."
        status_col = (255, 100, 200)
    elif state["thinking"]:
        orb_colors = ORB_THINKING
        status_txt = "Thinking..."
        status_col = (255, 180, 60)
    else:
        orb_colors = ORB_IDLE
        status_txt = "Tap to speak"
        status_col = C_DIMWHITE

    diff = state["orb_target"] - state["orb_scale"]
    state["orb_scale"] += diff * 0.08
    scale  = state["orb_scale"]
    ORB_R  = int(110 * scale)
    ORB_CX = WIDTH  // 2
    ORB_CY = HEIGHT // 2 - 30

    is_active = state["listening"] or state["speaking"] or state["thinking"]

    title = FONT_TITLE.render("Voice  Assistant", True, C_WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 38)))

    pygame.draw.line(screen, C_BORDER, (WIDTH//2 - 120, 58), (WIDTH//2 + 120, 58), 1)

    draw_orb(ORB_CX, ORB_CY, ORB_R, orb_colors, t, active=is_active)

    if state["idle"]:
        hint_r = ORB_R + int(math.sin(t * 1.5) * 4) + 16
        hs = pygame.Surface((hint_r*2+4, hint_r*2+4), pygame.SRCALPHA)
        pygame.draw.circle(hs, (255,255,255, 18), (hint_r+2, hint_r+2), hint_r, 1)
        screen.blit(hs, (ORB_CX - hint_r - 2, ORB_CY - hint_r - 2))

    st = FONT_STATUS.render(status_txt, True, status_col)
    screen.blit(st, st.get_rect(center=(WIDTH // 2, ORB_CY + ORB_R + 26)))

    out_y = ORB_CY + ORB_R + 55
    lines = wrap_text(state["output"], FONT_MED, WIDTH - 120)[:3]
    for i, line in enumerate(lines):
        col  = C_WHITE if i == 0 else C_DIMWHITE
        surf = FONT_MED.render(line, True, col)
        screen.blit(surf, surf.get_rect(center=(WIDTH // 2, out_y + i * 22)))

    if state["history"]:
        hist_y = HEIGHT - 78
        pygame.draw.line(screen, C_BORDER, (40, hist_y - 10), (WIDTH - 40, hist_y - 10), 1)
        label = FONT_SMALL.render("Recent", True, C_DARK)
        screen.blit(label, (44, hist_y - 8))
        for i, entry in enumerate(state["history"][:3]):
            cmd_short = entry["cmd"][:30] + ("…" if len(entry["cmd"]) > 30 else "")
            res_short = entry["res"][:48] + ("…" if len(entry["res"]) > 48 else "")
            x_pos = 44 + i * 210
            if x_pos + 200 > WIDTH - 20:
                break
            pygame.draw.rect(screen, C_CARD, (x_pos, hist_y + 4, 200, 52), border_radius=8)
            pygame.draw.rect(screen, C_BORDER, (x_pos, hist_y + 4, 200, 52), 1, border_radius=8)
            cs = FONT_SMALL.render(cmd_short, True, C_DIMWHITE)
            rs = FONT_SMALL.render(res_short[:28], True, C_DARK)
            screen.blit(cs, (x_pos + 8, hist_y + 10))
            screen.blit(rs, (x_pos + 8, hist_y + 28))

   
    clock_s = FONT_SMALL.render(datetime.datetime.now().strftime("%H:%M:%S"), True, C_DARK)
    screen.blit(clock_s, (WIDTH - clock_s.get_width() - 16, 16))

    
    hint = FONT_SMALL.render("SPACE to speak  ·  ESC to quit", True, C_DARK)
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 12)))

    pygame.display.flip()

def main():
    clock   = pygame.time.Clock()
    t       = 0.0
    running = True

    threading.Thread(
        target=speak,
        args=("Hello Janardhan! I am ARIA. How can I help you today?",),
        daemon=True
    ).start()

    while running:
        dt = clock.tick(60) / 1000.0
        t += dt

        ORB_CX = WIDTH  // 2
        ORB_CY = HEIGHT // 2 - 30
        ORB_R  = int(110 * state["orb_scale"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                dist = math.hypot(mx - ORB_CX, my - ORB_CY)
                if dist <= ORB_R + 20:
                    if not state["listening"] and not state["speaking"]:
                        threading.Thread(target=run_command_thread, daemon=True).start()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not state["listening"] and not state["speaking"]:
                        threading.Thread(target=run_command_thread, daemon=True).start()
                if event.key == pygame.K_ESCAPE:
                    running = False

        draw_ui(t)

    pygame.quit()

if __name__ == "__main__":
    main()
