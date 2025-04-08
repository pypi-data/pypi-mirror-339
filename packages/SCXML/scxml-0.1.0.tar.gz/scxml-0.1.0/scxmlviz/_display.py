import uuid
from IPython.display import display, HTML
import os

def display_scxml(scxml: str, current_state: str = None, height: int = 500):
    div_id = f"scxml-{uuid.uuid4().hex}"

    bundle_path = os.path.join(os.path.dirname(__file__), 'static', 'scxml-bundle.js')
    with open(bundle_path, 'r', encoding='utf-8') as f:
        js_bundle = f.read()

    escaped = scxml.replace("\\", "\\\\").replace("`", "\\`")

    html = f"""
    <div id="{div_id}" style="height:{height}px; border:1px solid #ccc;"></div>
    <script>
    {js_bundle}
    </script>
    <script>
      (function() {{
        const scxml = `{escaped}`;
        const currentState = {f'"{current_state}"' if current_state else 'null'};
        const container = document.getElementById("{div_id}");

        function tryRender() {{
          if (typeof window.scxmlviz?.renderScxml === 'function') {{
            window.scxmlviz.renderScxml(container, scxml, currentState);
          }} else {{
            setTimeout(tryRender, 100);
          }}
        }}

        tryRender();
      }})();
    </script>
    """
    display(HTML(html))


# Shared helper to build the HTML
def _build_scxml_html(scxml: str, current_state: str = None, height: int = 500):
    div_id = f"scxml-{uuid.uuid4().hex}"
    bundle_path = os.path.join(os.path.dirname(__file__), 'static', 'scxml-bundle.js')
    
    with open(bundle_path, 'r', encoding='utf-8') as f:
        js_bundle = f.read()

    escaped = scxml.replace("\\", "\\\\").replace("`", "\\`")

    html = f"""
    <div id="{div_id}" style="height:{height}px; border:1px solid #ccc;"></div>
    <script>
    {js_bundle}
    </script>
    <script>
      (function() {{
        const scxml = `{escaped}`;
        const currentState = {f'"{current_state}"' if current_state else 'null'};
        const container = document.getElementById("{div_id}");

        function tryRender() {{
          if (typeof window.scxmlviz?.renderScxml === 'function') {{
            window.scxmlviz.renderScxml(container, scxml, currentState);
          }} else {{
            setTimeout(tryRender, 100);
          }}
        }}

        tryRender();
      }})();
    </script>
    """
    return html

def save_scxml(scxml: str, current_state: str = None, height: int = 500, output_path: str = "scxml_output.html"):
    html = _build_scxml_html(scxml, current_state, height)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'></head><body>\n")
        f.write(html)
        f.write("\n</body></html>")

    print(f"✅ SCXML visualization saved to: {os.path.abspath(output_path)}")