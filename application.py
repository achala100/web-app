from flask import Flask, render_template_string, jsonify
from datetime import datetime
import os

# Specify your actual GitHub repository URL here
GITHUB_REPO_URL = "https://github.com/your-username/your-repo-name" 

application = Flask(__name__)

# HTML template styled with Tailwind CSS (Cyber-Tech Theme)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project: AURA | AWS Elastic Beanstalk</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        // Simulate a running server clock
        function updateClock() {
            const now = new Date();
            document.getElementById('server-time').textContent = now.toISOString().replace('T', ' ').substr(0, 19) + ' UTC';
        }
        setInterval(updateClock, 1000);
    </script>
    <style>
        /* Custom font and scanline effect */
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        body {
            font-family: 'Share+Tech+Mono', monospace;
        }
        .scanlines::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                to bottom,
                transparent,
                transparent 2px,
                rgba(0, 0, 0, 0.15) 3px,
                transparent 3px
            );
            pointer-events: none;
            z-index: 10;
        }
    </style>
</head>
<body class="bg-black text-cyan-400 min-h-screen flex flex-col justify-between scanlines overflow-hidden">
    
    <!-- Background grid effect -->
    <div class="fixed inset-0 opacity-10 bg-[url('https://www.transparenttextures.com/patterns/dark-dotted-squares.png')]"></div>

    <!-- Header / Navbar -->
    <header class="relative z-20 w-full py-4 px-6 border-b border-cyan-950 flex justify-between items-center max-w-7xl mx-auto bg-black/50 backdrop-blur-sm">
        <div class="flex items-center space-x-3">
            <div class="relative h-3 w-3 flex items-center justify-center">
                <div class="absolute h-full w-full bg-cyan-500 rounded-full animate-ping opacity-75"></div>
                <div class="relative h-2 w-2 bg-cyan-300 rounded-full"></div>
            </div>
            <span class="font-bold text-sm tracking-widest uppercase text-cyan-300">SYS_ID: AURA_CORE_1</span>
        </div>
        <div class="text-xs px-3 py-1 rounded border border-cyan-900 bg-cyan-950/50 text-cyan-500">
            AWS_REGION: {{ aws_region }}
        </div>
    </header>

    <!-- Main Content Grid -->
    <main class="flex-grow flex items-center justify-center px-6 py-8 relative z-20">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 w-full max-w-7xl h-auto md:h-[70vh]">
            
            <!-- Left Panel: Status -->
            <div class="md:col-span-3 bg-black border border-cyan-900 p-8 rounded-lg shadow-inner flex flex-col justify-between">
                <div class="space-y-4">
                    <div class="flex items-center justify-between border-b border-cyan-900 pb-2 mb-4">
                        <h1 class="text-4xl md:text-6xl font-extrabold text-white tracking-tight uppercase">DEPLOYMENT_</h1>
                        <span class="text-5xl font-black text-green-400">SUCCESS</span>
                    </div>

                    <div class="text-cyan-600 text-lg leading-relaxed max-w-3xl">
                        <p class="animate-pulse">/// STATUS: CORE NODE OPERATIONAL. DEPLOYMENT PIPELINE [GITHUB_ACTIONS] VALIDATED.</p>
                        <p class="mt-2">AWS Elastic Beanstalk successfully initialized with Python/Gunicorn runtime.</p>
                        <p class="mt-2 text-white">ENVIRONMENT: {{ env_name }}</p>
                    </div>
                </div>

                <!-- Data Terminal -->
                <div class="bg-gray-950 p-5 rounded font-mono text-xs mt-8 border border-gray-800 text-cyan-300 space-y-2 overflow-auto h-32">
                    <p>> INITIALIZING EB DEPLOYMENT... [OK]</p>
                    <p>> VERIFYING REQUIREMENTS.TXT... [OK]</p>
                    <p>> STARTING GUNICORN... [OK]</p>
                    <p>> APPLICATION HEALTH CHECK: ACTIVE... [OK]</p>
                    <p class="text-green-400">> > > SYSTEM READY.</p>
                </div>
            </div>

            <!-- Right Panel: System Info & Links -->
            <div class="bg-black border border-cyan-900 p-6 rounded-lg shadow-inner space-y-6 flex flex-col justify-between">
                
                <div>
                    <h2 class="text-xl font-bold text-cyan-200 uppercase border-b border-cyan-900 pb-2 mb-4">SYSTEM_STATS</h2>
                    
                    <div class="space-y-4">
                        <div class="bg-cyan-950 p-4 rounded border border-cyan-900">
                            <p class="text-xs text-cyan-600 uppercase tracking-wider">SERVER_TIME_UTC</p>
                            <p id="server-time" class="text-lg text-white font-bold mt-1 font-mono">{{ current_time }}</p>
                        </div>

                        <div class="bg-cyan-950 p-4 rounded border border-cyan-900">
                            <p class="text-xs text-cyan-600 uppercase tracking-wider">ENV_HEALTH</p>
                            <p class="text-green-400 font-bold mt-1 text-lg flex items-center space-x-2">
                                <span class="relative flex h-3 w-3">
                                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                    <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                                </span>
                                <span>NOMINAL</span>
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Link Section -->
                <div class="space-y-3 pt-6 border-t border-cyan-900">
                    <a href="/health" class="block w-full text-center px-6 py-3 rounded bg-cyan-900 hover:bg-cyan-800 text-white font-bold text-sm transition uppercase tracking-wider shadow-lg shadow-cyan-900/20">
                        RUN HEALTH CHECK
                    </a>
                    <a href="{{ github_url }}" target="_blank" class="block w-full text-center px-6 py-3 rounded bg-gray-900 hover:bg-gray-800 text-cyan-300 font-bold text-sm border border-gray-700 transition uppercase tracking-wider flex items-center justify-center space-x-2">
                        <svg height="20" width="20" class="fill-current" viewBox="0 0 16 16" version="1.1" aria-hidden="true"><path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path></svg>
                        <span>SOURCE_CODE_REPO</span>
                    </a>
                </div>
            </div>

        </div>
    </main>

    <!-- Footer -->
    <footer class="relative z-20 py-4 text-center text-xs text-cyan-900 border-t border-cyan-950 max-w-7xl mx-auto w-full bg-black/50">
        [AURA_SYSTEM_RUNNING] >> AWS Elastic Beanstalk >> Flask v3.x
    </footer>

</body>
</html>
"""

@application.route('/')
def home():
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    # Get environment name from AWS metadata if available, else default
    env_name = os.environ.get('AWS_EB_ENVIRONMENT_NAME', 'LOCAL_DEBUG')
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    
    return render_template_string(
        HTML_TEMPLATE, 
        current_time=now,
        github_url=GITHUB_REPO_URL,
        env_name=env_name,
        aws_region=aws_region
    )

@application.route('/health')
def health_check():
    return jsonify({
        "status": "nominal",
        "service_id": "aura-core-1",
        "timestamp_utc": datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    # Local development server execution
    application.run(host='0.0.0.0', port=5000)