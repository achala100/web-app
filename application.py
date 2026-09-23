```python
from flask import Flask, render_template_string, jsonify
from datetime import datetime, timezone
import os

# ============================================================
# CONFIGURATION
# ============================================================

GITHUB_REPO_URL = "https://github.com/your-username/your-repo-name"

application = Flask(__name__)

# ============================================================
# HTML TEMPLATE
# ============================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>AURA // Cloud Deployment</title>

    <script src="https://cdn.tailwindcss.com"></script>

    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        mono: ['JetBrains Mono', 'monospace'],
                        sans: ['Inter', 'sans-serif']
                    },
                    animation: {
                        'float': 'float 6s ease-in-out infinite',
                        'pulse-slow': 'pulse 3s ease-in-out infinite',
                        'spin-slow': 'spin 12s linear infinite'
                    },
                    keyframes: {
                        float: {
                            '0%, 100%': { transform: 'translateY(0px)' },
                            '50%': { transform: 'translateY(-10px)' }
                        }
                    }
                }
            }
        }
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: 'Inter', sans-serif;
            background:
                radial-gradient(circle at 15% 20%, rgba(0, 180, 255, 0.12), transparent 30%),
                radial-gradient(circle at 85% 70%, rgba(120, 60, 255, 0.12), transparent 30%),
                #030712;
            color: #e5e7eb;
            overflow-x: hidden;
        }

        .mono {
            font-family: 'JetBrains Mono', monospace;
        }

        /* Background grid */

        .grid-bg {
            position: fixed;
            inset: 0;
            z-index: -3;

            background-image:
                linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);

            background-size: 50px 50px;

            mask-image: linear-gradient(
                to bottom,
                black 0%,
                rgba(0,0,0,.7) 50%,
                transparent 100%
            );
        }

        /* Glow orbs */

        .orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(90px);
            pointer-events: none;
            z-index: -2;
        }

        .orb-blue {
            width: 350px;
            height: 350px;
            background: rgba(0, 160, 255, 0.10);
            top: 10%;
            left: -100px;
        }

        .orb-purple {
            width: 400px;
            height: 400px;
            background: rgba(120, 60, 255, 0.10);
            right: -150px;
            bottom: 5%;
        }

        /* Glass */

        .glass {
            background: rgba(8, 15, 30, 0.72);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);

            border: 1px solid rgba(148, 163, 184, 0.12);

            box-shadow:
                0 20px 60px rgba(0,0,0,.35),
                inset 0 1px 0 rgba(255,255,255,.03);
        }

        .glass:hover {
            border-color: rgba(56, 189, 248, 0.25);
            transition: .3s ease;
        }

        /* Status pulse */

        .status-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: #22c55e;
            box-shadow:
                0 0 0 5px rgba(34,197,94,.10),
                0 0 18px rgba(34,197,94,.8);
        }

        /* Gradient text */

        .gradient-text {
            background: linear-gradient(
                90deg,
                #67e8f9,
                #60a5fa,
                #a78bfa
            );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Animated border */

        .animated-border {
            position: relative;
        }

        .animated-border::before {
            content: "";
            position: absolute;
            inset: -1px;

            border-radius: inherit;

            background: linear-gradient(
                90deg,
                transparent,
                rgba(56,189,248,.5),
                transparent
            );

            background-size: 200% 100%;

            animation: borderMove 4s linear infinite;

            z-index: -1;
        }

        @keyframes borderMove {
            0% {
                background-position: 200% 0;
            }

            100% {
                background-position: -200% 0;
            }
        }

        /* Terminal */

        .terminal {
            background: #020617;
            border: 1px solid rgba(148,163,184,.10);
        }

        .terminal-line {
            opacity: .85;
        }

        .terminal-line::before {
            content: "› ";
            color: #22d3ee;
        }

        /* Progress */

        .progress-track {
            height: 6px;
            border-radius: 999px;
            background: rgba(255,255,255,.06);
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(
                90deg,
                #06b6d4,
                #3b82f6,
                #8b5cf6
            );
            box-shadow: 0 0 14px rgba(59,130,246,.5);
        }

        /* AWS icon */

        .aws-logo {
            font-weight: 800;
            letter-spacing: -1px;
        }

        /* Scanline */

        .scanline {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 50;

            background: repeating-linear-gradient(
                to bottom,
                transparent 0px,
                transparent 3px,
                rgba(255,255,255,.008) 4px
            );
        }

        /* Mobile */

        @media(max-width: 768px) {

            .hero-title {
                font-size: 42px;
                line-height: 1;
            }

        }

    </style>

    <script>

        function updateClock() {

            const now = new Date();

            const utc =
                now.getUTCFullYear() + "-" +
                String(now.getUTCMonth() + 1).padStart(2, "0") + "-" +
                String(now.getUTCDate()).padStart(2, "0") + " " +
                String(now.getUTCHours()).padStart(2, "0") + ":" +
                String(now.getUTCMinutes()).padStart(2, "0") + ":" +
                String(now.getUTCSeconds()).padStart(2, "0");

            document.getElementById("server-time").innerText =
                utc + " UTC";
        }

        setInterval(updateClock, 1000);

        window.onload = updateClock;

        async function checkHealth() {

            const badge = document.getElementById("health-badge");
            const text = document.getElementById("health-text");

            text.innerText = "CHECKING...";
            badge.classList.remove("bg-green-500/10");
            badge.classList.add("bg-yellow-500/10");

            try {

                const response = await fetch("/health");

                if (response.ok) {

                    text.innerText = "OPERATIONAL";

                    badge.classList.remove("bg-yellow-500/10");
                    badge.classList.add("bg-green-500/10");

                } else {

                    text.innerText = "DEGRADED";
                }

            } catch {

                text.innerText = "OFFLINE";
            }
        }

    </script>

</head>


<body>

<div class="grid-bg"></div>

<div class="orb orb-blue"></div>
<div class="orb orb-purple"></div>

<div class="scanline"></div>


<!-- ========================================================= -->
<!-- NAVIGATION -->
<!-- ========================================================= -->

<header class="relative z-20 border-b border-white/5">

    <div class="max-w-7xl mx-auto px-6 py-5">

        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-5">

            <div class="flex items-center gap-4">

                <div class="w-11 h-11 rounded-xl
                            bg-gradient-to-br from-cyan-400/20 to-blue-500/10
                            border border-cyan-400/20
                            flex items-center justify-center">

                    <span class="text-cyan-300 text-xl font-bold">A</span>

                </div>

                <div>

                    <div class="flex items-center gap-3">

                        <h1 class="font-bold tracking-wide text-white">
                            AURA CLOUD
                        </h1>

                        <span class="text-[10px] px-2 py-1 rounded-full
                                     bg-cyan-400/10
                                     border border-cyan-400/20
                                     text-cyan-300 mono">
                            v1.0.0
                        </span>

                    </div>

                    <p class="text-xs text-slate-500 mono mt-1">
                        CLOUD DEPLOYMENT CONTROL CENTER
                    </p>

                </div>

            </div>


            <div class="flex items-center gap-3">

                <div class="px-4 py-2 rounded-xl
                            bg-white/[0.03]
                            border border-white/10">

                    <span class="text-[10px] text-slate-500 block mono">
                        REGION
                    </span>

                    <span class="text-sm text-cyan-300 mono">
                        {{ aws_region }}
                    </span>

                </div>


                <div id="health-badge"
                     class="px-4 py-2 rounded-xl
                            bg-green-500/10
                            border border-green-500/20">

                    <div class="flex items-center gap-2">

                        <span class="status-dot"></span>

                        <span id="health-text"
                              class="text-xs text-green-400 font-semibold">
                            OPERATIONAL
                        </span>

                    </div>

                </div>

            </div>

        </div>

    </div>

</header>


<!-- ========================================================= -->
<!-- MAIN -->
<!-- ========================================================= -->

<main class="relative z-10 max-w-7xl mx-auto px-6 py-12">


    <!-- HERO -->

    <section class="mb-10">

        <div class="grid lg:grid-cols-3 gap-8 items-center">


            <div class="lg:col-span-2">

                <div class="inline-flex items-center gap-2
                            px-3 py-1.5 rounded-full
                            bg-cyan-400/5
                            border border-cyan-400/10
                            text-cyan-300 text-xs mono mb-6">

                    <span class="status-dot"></span>

                    LIVE DEPLOYMENT ENVIRONMENT

                </div>


                <h2 class="hero-title text-6xl md:text-7xl
                           font-extrabold tracking-tight
                           text-white leading-none">

                    DEPLOYMENT

                    <br>

                    <span class="gradient-text">
                        SUCCESSFUL.
                    </span>

                </h2>


                <p class="mt-6 text-slate-400 max-w-2xl
                          text-base md:text-lg leading-relaxed">

                    Your Flask application is running successfully
                    on AWS Elastic Beanstalk with Gunicorn.
                    The deployment pipeline has completed
                    successfully and the application is responding
                    to health checks.

                </p>


                <div class="flex flex-wrap gap-3 mt-8">

                    <button onclick="checkHealth()"
                            class="px-5 py-3 rounded-xl
                                   bg-cyan-500 hover:bg-cyan-400
                                   text-slate-950
                                   font-bold text-sm
                                   transition
                                   shadow-lg shadow-cyan-500/20">

                        RUN HEALTH CHECK

                    </button>


                    <a href="{{ github_url }}"
                       target="_blank"
                       class="px-5 py-3 rounded-xl
                              bg-white/[0.03]
                              hover:bg-white/[0.07]
                              border border-white/10
                              text-white
                              font-semibold text-sm
                              transition">

                        VIEW SOURCE →

                    </a>

                </div>

            </div>


            <!-- SYSTEM CORE -->

            <div class="glass animated-border
                        rounded-3xl p-7
                        relative overflow-hidden">

                <div class="absolute -top-20 -right-20
                            w-40 h-40
                            bg-cyan-500/10
                            blur-3xl rounded-full">
                </div>


                <div class="relative">

                    <div class="flex justify-between items-center mb-8">

                        <span class="text-xs text-slate-500 mono">
                            SYSTEM_CORE
                        </span>

                        <span class="text-[10px] px-2 py-1
                                     rounded bg-green-500/10
                                     text-green-400">
                            ACTIVE
                        </span>

                    </div>


                    <div class="flex justify-center mb-8">

                        <div class="w-36 h-36 rounded-full
                                    border border-cyan-400/20
                                    flex items-center justify-center
                                    relative">

                            <div class="absolute inset-3 rounded-full
                                        border border-blue-400/20
                                        border-dashed animate-spin-slow">
                            </div>

                            <div class="absolute inset-8 rounded-full
                                        bg-cyan-400/10
                                        blur-xl">
                            </div>

                            <div class="relative text-center">

                                <div class="text-4xl font-black
                                            gradient-text">
                                    A
                                </div>

                                <div class="text-[9px]
                                            text-slate-500 mono">
                                    CORE
                                </div>

                            </div>

                        </div>

                    </div>


                    <div class="text-center">

                        <h3 class="font-bold text-white">
                            AURA_CORE_1
                        </h3>

                        <p class="text-xs text-slate-500 mono mt-1">
                            {{ env_name }}
                        </p>

                    </div>

                </div>

            </div>

        </div>

    </section>


    <!-- ========================================================= -->
    <!-- METRICS -->
    <!-- ========================================================= -->

    <section class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">


        <div class="glass rounded-2xl p-5">

            <div class="text-xs text-slate-500 mono">
                PLATFORM
            </div>

            <div class="mt-3 text-xl font-bold text-white">
                AWS EB
            </div>

            <div class="text-xs text-green-400 mt-1">
                Elastic Beanstalk
            </div>

        </div>


        <div class="glass rounded-2xl p-5">

            <div class="text-xs text-slate-500 mono">
                RUNTIME
            </div>

            <div class="mt-3 text-xl font-bold text-white">
                Python
            </div>

            <div class="text-xs text-cyan-400 mt-1">
                Flask + Gunicorn
            </div>

        </div>


        <div class="glass rounded-2xl p-5">

            <div class="text-xs text-slate-500 mono">
                DEPLOYMENT
            </div>

            <div class="mt-3 text-xl font-bold text-white">
                GitHub
            </div>

            <div class="text-xs text-purple-400 mt-1">
                Actions Pipeline
            </div>

        </div>


        <div class="glass rounded-2xl p-5">

            <div class="text-xs text-slate-500 mono">
                STATUS
            </div>

            <div class="mt-3 text-xl font-bold text-green-400">
                100%
            </div>

            <div class="text-xs text-slate-500 mt-1">
                Healthy
            </div>

        </div>


    </section>


    <!-- ========================================================= -->
    <!-- DASHBOARD -->
    <!-- ========================================================= -->

    <section class="grid lg:grid-cols-3 gap-6">


        <!-- DEPLOYMENT PIPELINE -->

        <div class="glass rounded-2xl p-6 lg:col-span-2">

            <div class="flex justify-between items-center mb-7">

                <div>

                    <h3 class="font-bold text-white">
                        Deployment Pipeline
                    </h3>

                    <p class="text-xs text-slate-500 mt-1 mono">
                        GITHUB ACTIONS → AWS ELASTIC BEANSTALK
                    </p>

                </div>

                <span class="text-xs text-green-400 mono">
                    COMPLETED
                </span>

            </div>


            <div class="space-y-7">


                <!-- STEP -->

                <div class="flex gap-4">

                    <div class="flex flex-col items-center">

                        <div class="w-8 h-8 rounded-full
                                    bg-green-500/10
                                    border border-green-500/30
                                    flex items-center justify-center">

                            <span class="text-green-400 text-sm">
                                ✓
                            </span>

                        </div>

                        <div class="w-px h-full bg-white/10 mt-2"></div>

                    </div>

                    <div class="pb-3">

                        <h4 class="text-sm font-semibold text-white">
                            Source Repository
                        </h4>

                        <p class="text-xs text-slate-500 mt-1">
                            Repository successfully validated
                        </p>

                    </div>

                </div>


                <!-- STEP -->

                <div class="flex gap-4">

                    <div class="flex flex-col items-center">

                        <div class="w-8 h-8 rounded-full
                                    bg-green-500/10
                                    border border-green-500/30
                                    flex items-center justify-center">

                            <span class="text-green-400 text-sm">
                                ✓
                            </span>

                        </div>

                        <div class="w-px h-full bg-white/10 mt-2"></div>

                    </div>

                    <div class="pb-3">

                        <h4 class="text-sm font-semibold text-white">
                            Build & Dependencies
                        </h4>

                        <p class="text-xs text-slate-500 mt-1">
                            requirements.txt verified successfully
                        </p>

                    </div>

                </div>


                <!-- STEP -->

                <div class="flex gap-4">

                    <div class="flex flex-col items-center">

                        <div class="w-8 h-8 rounded-full
                                    bg-green-500/10
                                    border border-green-500/30
                                    flex items-center justify-center">

                            <span class="text-green-400 text-sm">
                                ✓
                            </span>

                        </div>

                        <div class="w-px h-full bg-white/10 mt-2"></div>

                    </div>

                    <div class="pb-3">

                        <h4 class="text-sm font-semibold text-white">
                            Gunicorn Application Server
                        </h4>

                        <p class="text-xs text-slate-500 mt-1">
                            Application server initialized
                        </p>

                    </div>

                </div>


                <!-- STEP -->

                <div class="flex gap-4">

                    <div>

                        <div class="w-8 h-8 rounded-full
                                    bg-cyan-500/10
                                    border border-cyan-500/30
                                    flex items-center justify-center">

                            <span class="text-cyan-300 text-sm">
                                ✓
                            </span>

                        </div>

                    </div>

                    <div>

                        <h4 class="text-sm font-semibold text-white">
                            Production Environment
                        </h4>

                        <p class="text-xs text-green-400 mt-1">
                            Deployment successful
                        </p>

                    </div>

                </div>

            </div>

        </div>


        <!-- SYSTEM INFORMATION -->

        <div class="glass rounded-2xl p-6">

            <h3 class="font-bold text-white mb-6">
                System Information
            </h3>


            <div class="space-y-5">


                <div>

                    <div class="flex justify-between text-xs mb-2">

                        <span class="text-slate-500">
                            Application
                        </span>

                        <span class="text-cyan-300">
                            Flask
                        </span>

                    </div>

                    <div class="progress-track">
                        <div class="progress-fill" style="width:100%">
                        </div>
                    </div>

                </div>


                <div>

                    <div class="flex justify-between text-xs mb-2">

                        <span class="text-slate-500">
                            Environment
                        </span>

                        <span class="text-green-400">
                            Healthy
                        </span>

                    </div>

                    <div class="progress-track">
                        <div class="progress-fill" style="width:96%">
                        </div>
                    </div>

                </div>


                <div>

                    <div class="flex justify-between text-xs mb-2">

                        <span class="text-slate-500">
                            Deployment
                        </span>

                        <span class="text-purple-400">
                            Complete
                        </span>

                    </div>

                    <div class="progress-track">
                        <div class="progress-fill" style="width:100%">
                        </div>
                    </div>

                </div>


            </div>


            <div class="mt-8 pt-6 border-t border-white/5">

                <div class="text-xs text-slate-500 mono mb-2">
                    SERVER_TIME
                </div>

                <div id="server-time"
                     class="text-sm text-cyan-300 mono">
                    {{ current_time }}
                </div>

            </div>


            <div class="mt-6">

                <div class="text-xs text-slate-500 mono mb-2">
                    AWS_REGION
                </div>

                <div class="text-sm text-white mono">
                    {{ aws_region }}
                </div>

            </div>

        </div>

    </section>


    <!-- ========================================================= -->
    <!-- TERMINAL -->
    <!-- ========================================================= -->

    <section class="glass rounded-2xl mt-6 overflow-hidden">

        <div class="px-5 py-3
                    border-b border-white/5
                    flex items-center justify-between">

            <div class="flex items-center gap-2">

                <span class="w-3 h-3 rounded-full bg-red-400/70"></span>
                <span class="w-3 h-3 rounded-full bg-yellow-400/70"></span>
                <span class="w-3 h-3 rounded-full bg-green-400/70"></span>

                <span class="ml-3 text-xs text-slate-500 mono">
                    aura@aws:~$
                </span>

            </div>

            <span class="text-[10px] text-slate-600 mono">
                LIVE TERMINAL
            </span>

        </div>


        <div class="terminal p-6 mono text-xs md:text-sm
                    space-y-2">

            <div class="terminal-line text-slate-400">
                initializing AURA_CORE_1...
            </div>

            <div class="terminal-line text-green-400">
                AWS Elastic Beanstalk environment detected
            </div>

            <div class="terminal-line text-green-400">
                Gunicorn application server: ONLINE
            </div>

            <div class="terminal-line text-green-400">
                Flask application: RUNNING
            </div>

            <div class="terminal-line text-cyan-300">
                Health endpoint: /health
            </div>

            <div class="terminal-line text-cyan-300">
                Environment: {{ env_name }}
            </div>

            <div class="terminal-line text-purple-300">
                Region: {{ aws_region }}
            </div>

            <div class="terminal-line text-green-400">
                deployment pipeline validation: PASSED
            </div>

            <div class="terminal-line text-white mt-4">
                SYSTEM READY_
            </div>

        </div>

    </section>


</main>


<!-- ========================================================= -->
<!-- FOOTER -->
<!-- ========================================================= -->

<footer class="relative z-10 border-t border-white/5 mt-4">

    <div class="max-w-7xl mx-auto px-6 py-6
                flex flex-col md:flex-row
                justify-between gap-3">

        <div class="text-xs text-slate-600 mono">
            AURA_CORE_1 // CLOUD PLATFORM
        </div>

        <div class="text-xs text-slate-600 mono">
            AWS ELASTIC BEANSTALK · FLASK · GUNICORN
        </div>

    </div>

</footer>


</body>
</html>
"""


# ============================================================
# ROUTES
# ============================================================

@application.route("/")
def home():

    now = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    env_name = os.environ.get(
        "AWS_EB_ENVIRONMENT_NAME",
        "LOCAL_DEBUG"
    )

    aws_region = os.environ.get(
        "AWS_REGION",
        "us-east-1"
    )

    return render_template_string(
        HTML_TEMPLATE,
        current_time=now,
        github_url=GITHUB_REPO_URL,
        env_name=env_name,
        aws_region=aws_region
    )


@application.route("/health")
def health_check():

    return jsonify({
        "status": "nominal",
        "service_id": "aura-core-1",
        "environment": os.environ.get(
            "AWS_EB_ENVIRONMENT_NAME",
            "LOCAL_DEBUG"
        ),
        "region": os.environ.get(
            "AWS_REGION",
            "us-east-1"
        ),
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat()
    }), 200


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":

    application.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
```
