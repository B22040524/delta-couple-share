import os
from urllib.parse import quote

from flask import Flask, render_template

app = Flask(__name__)

DELTA_PACKAGE = "com.tencent.tmgp.dfm"
DELTA_ACTIVITY = "com.epicgames.ue4.SplashActivity"
STORE_URL = f"https://sj.qq.com/appdetail/{DELTA_PACKAGE}"


def public_base_url() -> str:
    return os.getenv("PUBLIC_BASE_URL", "").strip().rstrip("/")


def explicit_intent_url() -> str:
    # 显式 Intent 仅做最佳努力启动。QQ/浏览器可能基于安全策略拦截。
    fallback = quote(STORE_URL, safe="")
    component = f"{DELTA_PACKAGE}/{DELTA_ACTIVITY}"

    return (
        "intent:#Intent;"
        "action=android.intent.action.MAIN;"
        "category=android.intent.category.LAUNCHER;"
        f"component={component};"
        f"package={DELTA_PACKAGE};"
        f"S.browser_fallback_url={fallback};"
        "end"
    )


@app.get("/")
def index():
    return {
        "status": "ok",
        "page": "/couple",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/couple")
def couple():
    base = public_base_url()
    page_url = f"{base}/couple" if base else ""
    image_url = (
        f"{base}/static/couple_card.png"
        if base
        else "/static/couple_card.png"
    )

    return render_template(
        "couple.html",
        page_url=page_url,
        image_url=image_url,
        intent_url=explicit_intent_url(),
        store_url=STORE_URL,
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
