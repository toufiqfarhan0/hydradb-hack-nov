"""
Generate high-fidelity Swiss Modernist console preview image for assets/console-preview.png
Renders the real interactive HydraDB GraphBLAS Matrix Viewer with swimlanes, active nodes,
glowing traversed paths, and OpenCypher telemetry HUD.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

WIDTH = 1280
HEIGHT = 760

im = Image.new("RGB", (WIDTH, HEIGHT), "#0E1117")
draw = ImageDraw.Draw(im)

def get_font(size: int, bold: bool = False):
    try:
        # Windows system fonts
        font_name = "arialbd.ttf" if bold else "arial.ttf"
        font_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", font_name)
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
        mono_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "consola.ttf")
        if os.path.exists(mono_path):
            return ImageFont.truetype(mono_path, size)
    except Exception:
        pass
    return ImageFont.load_default()

f_title = get_font(18, bold=True)
f_sub = get_font(11, bold=False)
f_col = get_font(12, bold=True)
f_node = get_font(12, bold=True)
f_node_sub = get_font(10, bold=False)
f_badge = get_font(11, bold=True)
f_code = get_font(11, bold=False)

# 1. Subtle background grid
for x in range(0, WIDTH, 40):
    draw.line([(x, 50), (x, HEIGHT - 110)], fill="#161B22", width=1)
for y in range(50, HEIGHT - 110, 40):
    draw.line([(0, y), (WIDTH, y)], fill="#161B22", width=1)

# 2. Window Chrome & Top Header
draw.rectangle([(0, 0), (WIDTH, 48)], fill="#1A1F26", outline="#2D333B", width=1)

# Window buttons
draw.ellipse([(16, 18), (28, 30)], fill="#EF4444")
draw.ellipse([(36, 18), (48, 30)], fill="#F59E0B")
draw.ellipse([(56, 18), (68, 30)], fill="#10B981")

# Title & subtitle
draw.text((85, 14), "HydraDB GraphBLAS Matrix Viewer", fill="#FFFFFF", font=f_title)
draw.text((410, 18), "// Interactive Context Visualizer (localhost:3000/console)", fill="#8B949E", font=f_sub)

# Right-side status pills
draw.rectangle([(WIDTH - 430, 11), (WIDTH - 250, 37)], fill="#1F2937", outline="#374151", width=1)
draw.ellipse([(WIDTH - 420, 20), (WIDTH - 412, 28)], fill="#10B981")
draw.text((WIDTH - 404, 16), "730 NODES  ·  2,421 EDGES", fill="#E5E7EB", font=f_badge)

draw.rectangle([(WIDTH - 240, 11), (WIDTH - 120, 37)], fill="#3B1214", outline="#D82C2C", width=1)
draw.text((WIDTH - 228, 16), "0.72ms LATENCY", fill="#FCA5A5", font=f_badge)

draw.rectangle([(WIDTH - 110, 11), (WIDTH - 16, 37)], fill="#D82C2C")
draw.text((WIDTH - 96, 16), "ACTIVE", fill="#FFFFFF", font=f_badge)

# 3. Swimlane Column Headers
cols = [
    ("TIER 1: MCP SERVERS (50)", 160, "#60A5FA"),
    ("TIER 2: CAPABILITY RESOLVERS (100)", 460, "#FBBF24"),
    ("TIER 3: ISOLATED TOOLS (500)", 780, "#D82C2C"),
    ("TIER 4: BOUND ENTITIES (80)", 1100, "#34D399")
]

for title, cx, color in cols:
    draw.line([(cx - 130, 56), (cx + 130, 56)], fill=color, width=2)
    draw.rectangle([(cx - 130, 60), (cx + 130, 86)], fill="#161B22", outline="#2D333B", width=1)
    draw.text((cx - 115, 66), title, fill=color, font=f_col)

# 4. Swimlane Nodes
servers = [
    ("mcp_postgres", "Database", True, 130),
    ("mcp_slack", "Alerting", True, 220),
    ("mcp_docker", "Container", False, 310),
    ("mcp_aws_rds", "Cloud", False, 400),
    ("mcp_k8s", "Orchestrator", False, 490),
    ("mcp_sentry", "Observability", False, 580)
]

capabilities = [
    ("cap_db_diagnostics", "Pool & slow queries", True, 150),
    ("cap_incident_alerting", "War-room broadcast", True, 250),
    ("cap_container_ops", "Lifecycle & restarts", False, 370),
    ("cap_cloud_telemetry", "RDS IOPS & metrics", False, 480),
    ("cap_security_audit", "Dynamic leases", False, 580)
]

tools = [
    ("pg_check_connection_pool", "Isolated (480 tok)", True, 140),
    ("slack_post_incident_bulletin", "Isolated (520 tok)", True, 240),
    ("docker_restart_container", "Pruned (99.6%)", False, 340),
    ("aws_fetch_rds_metrics", "Pruned (99.6%)", False, 430),
    ("k8s_describe_pod", "Pruned (99.6%)", False, 510),
    ("sentry_fetch_trace", "Pruned (99.6%)", False, 590)
]

entities = [
    ("pg-cluster-prod.internal:5432", "conns: 387/400 (P0)", True, 140),
    ("Slack #incident-critical-ops", "channel: C08A91KL2", True, 240),
    ("container-prod-core-api", "docker://c10928a", False, 370),
    ("rds-aurora-cluster-prod", "iops: 12,400", False, 500)
]

# Background edges (dimmed)
def draw_curved_line(p1, p2, color, width=1):
    x1, y1 = p1
    x2, y2 = p2
    points = []
    for step in range(25):
        t = step / 24.0
        # Cubic bezier with horizontal handles
        cx1 = x1 + (x2 - x1) * 0.5
        cy1 = y1
        cx2 = x1 + (x2 - x1) * 0.5
        cy2 = y2
        bx = (1-t)**3 * x1 + 3*(1-t)**2 * t * cx1 + 3*(1-t)*t**2 * cx2 + t**3 * x2
        by = (1-t)**3 * y1 + 3*(1-t)**2 * t * cy1 + 3*(1-t)*t**2 * cy2 + t**3 * y2
        points.append((bx, by))
    draw.line(points, fill=color, width=width)

# Draw non-active dimmed background paths
for s in servers:
    if not s[2]:
        for c in capabilities[2:4]:
            draw_curved_line((240, s[3] + 18), (350, c[3] + 18), "#21262D", width=1)
for c in capabilities:
    if not c[2]:
        for t in tools[2:5]:
            draw_curved_line((560, c[3] + 18), (670, t[3] + 18), "#21262D", width=1)

# Active Traversed Paths (Glowing Red #D82C2C)
# 1. mcp_postgres -> cap_db_diagnostics -> pg_check_connection_pool -> pg-cluster-prod
draw_curved_line((240, 130 + 18), (350, 150 + 18), "#D82C2C", width=3)
draw_curved_line((560, 150 + 18), (670, 140 + 18), "#D82C2C", width=3)
draw_curved_line((890, 140 + 18), (990, 140 + 18), "#D82C2C", width=3)

# 2. mcp_slack -> cap_incident_alerting -> slack_post_incident_bulletin -> Slack channel
draw_curved_line((240, 220 + 18), (350, 250 + 18), "#D82C2C", width=3)
draw_curved_line((560, 250 + 18), (670, 240 + 18), "#D82C2C", width=3)
draw_curved_line((890, 240 + 18), (990, 240 + 18), "#D82C2C", width=3)

# Path Edge Labels
draw.rectangle([(270, 130), (330, 146)], fill="#1E293B", outline="#475569")
draw.text((275, 132), "PROVIDES", fill="#94A3B8", font=f_node_sub)

draw.rectangle([(585, 132), (655, 148)], fill="#3B1214", outline="#D82C2C")
draw.text((590, 134), "PREFERS 2.70", fill="#FCA5A5", font=f_node_sub)

draw.rectangle([(910, 130), (975, 146)], fill="#1E293B", outline="#475569")
draw.text((915, 132), "REQUIRES", fill="#94A3B8", font=f_node_sub)

# Draw Node Boxes
def draw_node(x, y, w, h, title, sub, color, border, active=False):
    fill_col = "#1E232B" if active else "#161B22"
    border_col = border if active else "#2D333B"
    draw.rectangle([(x, y), (x + w, y + h)], fill=fill_col, outline=border_col, width=2 if active else 1)
    if active:
        # Glow accent bar
        draw.rectangle([(x, y), (x + 4, y + h)], fill=border)
    draw.text((x + 12, y + 6), title, fill=color, font=f_node)
    draw.text((x + 12, y + 22), sub, fill="#8B949E", font=f_node_sub)

for s in servers:
    draw_node(50, s[3], 190, 38, s[0], s[1], "#FFFFFF" if s[2] else "#6E7681", "#60A5FA", active=s[2])

for c in capabilities:
    draw_node(350, c[3], 210, 38, c[0], c[1], "#FFFFFF" if c[2] else "#6E7681", "#FBBF24", active=c[2])

for t in tools:
    draw_node(670, t[3], 220, 38, t[0], t[1], "#FFFFFF" if t[2] else "#484F58", "#D82C2C", active=t[2])

for e in entities:
    draw_node(990, e[3], 240, 38, e[0], e[1], "#FFFFFF" if e[2] else "#6E7681", "#34D399", active=e[2])

# 5. Bottom Telemetry & OpenCypher Terminal HUD
draw.rectangle([(0, HEIGHT - 110), (WIDTH, HEIGHT)], fill="#161B22", outline="#2D333B", width=1)

# Task prompt bar
draw.rectangle([(16, HEIGHT - 98), (WIDTH - 16, HEIGHT - 68)], fill="#0E1117", outline="#30363D", width=1)
draw.text((28, HEIGHT - 91), "ACTIVE TASK PROMPT:", fill="#D82C2C", font=f_badge)
draw.text((170, HEIGHT - 91), '"Production PostgreSQL database is exhausting connection pool and throwing 500s. Inspect pool & war-room."', fill="#FFFFFF", font=f_code)

# Traversal stats readout
draw.text((28, HEIGHT - 54), "OPENCYPHER TRAVERSAL:", fill="#8B949E", font=f_node_sub)
draw.text((170, HEIGHT - 54), "MATCH (c:Capability WHERE c.id IN [...]) MATCH (t:Tool)-[:PROVIDES]->(c) OPTIONAL MATCH (t)-[:REQUIRES_ENTITY]->(e:Entity)", fill="#60A5FA", font=f_code)

draw.rectangle([(WIDTH - 380, HEIGHT - 58), (WIDTH - 20, HEIGHT - 30)], fill="#1F2937", outline="#374151")
draw.text((WIDTH - 368, HEIGHT - 51), "CONTEXT: 1,214 TOKENS (-99.6%)  ·  2 TOOLS  ·  2 BOUND ENTITIES", fill="#34D399", font=f_badge)

# Save high-res PNG
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "console-preview.png")
im.save(output_path, "PNG", optimize=True)
print(f"SUCCESS: Generated {output_path} ({os.path.getsize(output_path):,} bytes)")
