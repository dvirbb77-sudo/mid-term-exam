import os
import sys
import socket
from flask import Flask, jsonify, render_template_string, redirect, request

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))
VERSION = os.environ.get("VERSION", "1.0.0")
API_KEY = os.environ.get("API_KEY")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Fortress Status</title>
    <style>
        :root {
            color-scheme: dark;
            --cape: #c8102e;
            --sky: #1666c1;
            --gold: #ffd447;
            --ink: #0a1733;
            --cloud: #f7fbff;
        }

        * {
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            margin: 0;
            display: grid;
            place-items: center;
            overflow: hidden;
            background:
                radial-gradient(circle at 18% 16%, rgba(255, 255, 255, 0.92) 0 7%, transparent 8%),
                radial-gradient(circle at 84% 18%, rgba(255, 255, 255, 0.7) 0 5%, transparent 6%),
                linear-gradient(145deg, #55b7ff 0%, var(--sky) 52%, #081b49 100%);
            color: var(--cloud);
            font-family: "Trebuchet MS", Arial, sans-serif;
        }

        main {
            width: min(920px, calc(100vw - 32px));
            display: grid;
            grid-template-columns: minmax(220px, 0.8fr) minmax(280px, 1fr);
            align-items: center;
            gap: 32px;
            padding: 32px;
            border: 3px solid rgba(255, 255, 255, 0.35);
            border-radius: 8px;
            background: rgba(8, 27, 73, 0.82);
            box-shadow: 0 28px 80px rgba(0, 0, 0, 0.38);
        }

        .hero {
            position: relative;
            min-height: 420px;
            display: grid;
            place-items: end center;
        }

        .cape {
            position: absolute;
            width: 220px;
            height: 360px;
            bottom: 12px;
            left: 16px;
            background: linear-gradient(120deg, #8e071c, var(--cape));
            clip-path: polygon(45% 0, 82% 6%, 100% 100%, 18% 92%, 0 20%);
            transform: skewX(-7deg);
            filter: drop-shadow(0 18px 18px rgba(0, 0, 0, 0.35));
        }

        .superman {
            position: relative;
            width: 210px;
            height: 390px;
        }

        .head {
            width: 86px;
            height: 94px;
            margin: 0 auto;
            border-radius: 44% 44% 48% 48%;
            background: #ffd0a6;
            border: 4px solid #06152f;
            position: relative;
            z-index: 2;
        }

        .hair {
            position: absolute;
            inset: -8px 10px auto 8px;
            height: 34px;
            border-radius: 50% 48% 42% 42%;
            background: #101010;
        }

        .curl {
            position: absolute;
            width: 22px;
            height: 30px;
            left: 42px;
            top: 18px;
            border-radius: 50%;
            border-left: 8px solid #101010;
            transform: rotate(-26deg);
        }

        .eye {
            position: absolute;
            width: 10px;
            height: 6px;
            top: 45px;
            border-radius: 999px;
            background: #06152f;
        }

        .eye.left {
            left: 23px;
        }

        .eye.right {
            right: 23px;
        }

        .smile {
            position: absolute;
            width: 28px;
            height: 13px;
            left: 27px;
            bottom: 17px;
            border-bottom: 4px solid #7c2430;
            border-radius: 50%;
        }

        .body {
            width: 154px;
            height: 178px;
            margin: -6px auto 0;
            border: 4px solid #06152f;
            border-radius: 34px 34px 18px 18px;
            background: linear-gradient(90deg, #115ecf, #1887f0);
            position: relative;
            z-index: 1;
        }

        .shield {
            position: absolute;
            width: 78px;
            height: 64px;
            left: 50%;
            top: 28px;
            display: grid;
            place-items: center;
            transform: translateX(-50%);
            clip-path: polygon(8% 0, 92% 0, 100% 36%, 50% 100%, 0 36%);
            background: var(--gold);
            border: 4px solid var(--cape);
            color: var(--cape);
            font-size: 42px;
            font-weight: 900;
            line-height: 1;
            text-shadow: 1px 1px 0 #06152f;
        }

        .belt {
            position: absolute;
            width: 100%;
            height: 18px;
            left: 0;
            bottom: 24px;
            background: var(--gold);
            border-block: 3px solid #06152f;
        }

        .arm {
            position: absolute;
            width: 42px;
            height: 146px;
            top: 112px;
            background: #1476df;
            border: 4px solid #06152f;
            border-radius: 24px;
            z-index: 0;
        }

        .arm.left {
            left: 5px;
            transform: rotate(20deg);
        }

        .arm.right {
            right: 5px;
            transform: rotate(-20deg);
        }

        .legs {
            width: 136px;
            height: 110px;
            margin: -4px auto 0;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .leg {
            background: #104db8;
            border: 4px solid #06152f;
            border-radius: 0 0 22px 22px;
        }

        .boot {
            height: 32px;
            margin-top: 70px;
            border-radius: 0 0 18px 18px;
            background: var(--cape);
        }

        .panel {
            display: grid;
            gap: 18px;
        }

        h1 {
            margin: 0;
            color: var(--gold);
            font-size: clamp(2.1rem, 7vw, 4.8rem);
            line-height: 0.92;
            text-transform: uppercase;
        }

        .tagline {
            max-width: 36rem;
            margin: 0;
            color: #dbeeff;
            font-size: 1.08rem;
        }

        .speech {
            position: relative;
            min-height: 82px;
            margin: 0;
            padding: 18px 20px;
            border: 4px solid #06152f;
            border-radius: 8px;
            background: var(--cloud);
            color: var(--ink);
            font-size: clamp(1.5rem, 4vw, 2.5rem);
            font-weight: 900;
            line-height: 1.05;
            text-transform: uppercase;
            box-shadow: 8px 8px 0 var(--gold);
        }

        .speech::before {
            content: "";
            position: absolute;
            left: -23px;
            top: 34px;
            border: 14px solid transparent;
            border-right-color: #06152f;
        }

        .speech::after {
            content: "";
            position: absolute;
            left: -16px;
            top: 38px;
            border: 10px solid transparent;
            border-right-color: var(--cloud);
        }

        button {
            width: fit-content;
            min-height: 48px;
            padding: 0 22px;
            border: 3px solid #06152f;
            border-radius: 6px;
            background: var(--cape);
            color: #fff;
            font: inherit;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
            cursor: pointer;
            box-shadow: 5px 5px 0 var(--gold);
        }

        button:hover {
            transform: translate(-1px, -1px);
        }

        button:active {
            transform: translate(3px, 3px);
            box-shadow: 2px 2px 0 var(--gold);
        }

        pre {
            min-height: 118px;
            margin: 0;
            padding: 16px;
            overflow: auto;
            border: 2px solid rgba(255, 255, 255, 0.28);
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.28);
            color: #ecf6ff;
            font-size: 0.95rem;
            white-space: pre-wrap;
        }

        @media (max-width: 740px) {
            body {
                overflow: auto;
                padding: 16px 0;
            }

            main {
                grid-template-columns: 1fr;
                gap: 16px;
                padding: 22px;
            }

            .hero {
                min-height: 350px;
            }

            .speech::before,
            .speech::after {
                display: none;
            }
        }
    </style>
</head>
<body>
    <main>
        <section class="hero" aria-label="Superman status mascot">
            <div class="cape"></div>
            <div class="superman">
                <div class="head">
                    <div class="hair"></div>
                    <div class="curl"></div>
                    <div class="eye left"></div>
                    <div class="eye right"></div>
                    <div class="smile"></div>
                </div>
                <div class="arm left"></div>
                <div class="arm right"></div>
                <div class="body">
                    <div class="shield">S</div>
                    <div class="belt"></div>
                </div>
                <div class="legs">
                    <div class="leg"><div class="boot"></div></div>
                    <div class="leg"><div class="boot"></div></div>
                </div>
            </div>
        </section>
        <section class="panel">
            <h1>Fortress Status</h1>
            <p class="tagline">A hero-grade pulse check for this tiny Flask universe.</p>
            <p class="speech" id="superman-line">Awaiting status...</p>
            <button onclick="fetchStatus()">Check Status</button>
            <pre id="output">No signal yet.</pre>
        </section>
    </main>
    <script>
        async function fetchStatus() {
            const line = document.getElementById('superman-line');
            const output = document.getElementById('output');

            try {
                const res = await fetch('/api/v1/status');
                const data = await res.json();
                const isOk = res.ok && data.status === 'ok';

                line.innerText = isOk ? 'I shit you not' : 'I shit you yes';
                output.innerText = JSON.stringify(data, null, 2);
            } catch (error) {
                line.innerText = 'I shit you yes';
                output.innerText = JSON.stringify({ error: error.message }, null, 2);
            }
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/status")
def status_redirect():
    return redirect("/api/v1/status", code=302)


@app.route("/api/v1/status")
def status_v1():
    return jsonify(
        {"status": "ok", "hostname": socket.gethostname(), "version": VERSION}
    )


@app.route("/api/v1/secret")
def secret():
    key = request.headers.get("X-API-Key")
    # Explicit check for security routes
    if not key or key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"message": "you found the secret"})


def main():
    """Entry point for the automation service."""
    if not API_KEY:
        print("FATAL: API_KEY is mandatory and must be set.", file=sys.stderr)
        sys.exit(1)
    app.run(host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()

#### I had the strange issue where if you switch out of main when it's empty the brnach is erased (ubuntu 24.4) so fabricating the pull request by deleting the comment#####
