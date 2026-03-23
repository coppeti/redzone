import re
from urllib.parse import unquote

from django import template

register = template.Library()


@register.filter
def embed_url(url):
    """Converts a YouTube, Vimeo or Odysee watch URL to an embed URL."""
    if not url:
        return ""

    decoded = unquote(url)

    # YouTube: https://www.youtube.com/watch?v=ID or https://youtu.be/ID
    yt_match = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})", decoded)
    if yt_match:
        return f"https://www.youtube.com/embed/{yt_match.group(1)}"

    # Vimeo: https://vimeo.com/ID
    vimeo_match = re.search(r"vimeo\.com/(\d+)", decoded)
    if vimeo_match:
        return f"https://player.vimeo.com/video/{vimeo_match.group(1)}"

    # Odysee embed URL déjà formatée (copiée depuis le bouton Partager → Intégrer)
    if "odysee.com" in decoded and "/embed/" in decoded:
        return decoded

    # Odysee URL normale: https://odysee.com/@Channel:hash/video:hash
    odysee_match = re.search(r"odysee\.com/(@[^/]+/[^/?#]+)", decoded)
    if odysee_match:
        return f"https://odysee.com/$/embed/{odysee_match.group(1)}"

    return url
