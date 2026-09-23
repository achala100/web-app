from flask import Flask, render_template_string, jsonify
from datetime import datetime

application = Flask(__name__)

# Modern HTML template styled with Tailwind CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS Elastic Beanstalk - Python App</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between font-sans">
    
    <!-- Header / Navbar -->
    <header class="w-full py-6 px-8 border-b border-slate-800 flex justify-between items-center max-w-6xl mx-auto">
        <div class="flex items-center space-x-3">
            <div class="h-3 w-3 bg-emerald-500 rounded-full animate-pulse"></div>
            <span class="font-bold tracking-wider text-sm uppercase text-slate-400">AWS Elastic Beanstalk</span>
        </div>
        <span class="text-xs bg-slate-900 border border-slate-800 text-slate-400 px-3 py-1 rounded-full">Python / Flask</span>
    </header>

    <!-- Main Content Hero Section -->
    <main class="flex-grow flex items-center justify-center px-6 py-12">
        <div class="max-w-3xl w-full bg-slate-900/60 border border-slate-800/80 backdrop-blur-xl rounded-2xl p-8 md:p-12 shadow-2xl text-center space-y-6">
            
            <div class="inline-flex p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-400 mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
            </div>

            <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight text-white">
                Deployment <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Successful!</span>
            </h1>
            
            <p class="text-slate-400 text-lg max-w-xl mx-auto">
                Your Python application is live and running smoothly on AWS Elastic Beanstalk via automated GitHub pipelines.
            </p>

            <!-- Dynamic Server Status Box -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-left pt-4">
                <div class="bg-slate-950/50 border border-slate-800/60 rounded-xl p-4">
                    <p class="text-xs text-slate-500 uppercase tracking-wider font-semibold">Server Time (UTC)</p>
                    <p class="text-slate-200 font-mono mt-1 text-sm">{{ current_time }}</p>
                </div>
                <div class="bg-slate-950/50 border border-slate-800/60 rounded-xl p-4">
                    <p class="text-xs text-slate-500 uppercase tracking-wider font-semibold">Environment Status</p>
                    <p class="text-emerald-400 font-mono mt-1 text-sm flex items-center space-x-2">
                        <span class="h-2 w-2 bg-emerald-400 rounded-full"></span>
                        <span>Healthy & Active</span>
                    </p>
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="pt-4 flex flex-wrap justify-center gap-4">
                <a href="/health" class="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition shadow-lg shadow-indigo-600/20">
                    Check Health Endpoint
                </a>
                <a href="https://github.com" target="_blank" class="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium text-sm border border-slate-700 transition">
                    View GitHub Repo
                </a>
            </div>

        </div>
    </main>

    <!-- Footer -->
    <footer class="py-6 text-center text-xs text-slate-600 border-t border-slate-900 max-w-6xl mx-auto w-full">
        Powered by AWS Elastic Beanstalk & Flask. Built for modern cloud infrastructure.
    </footer>

</body>
</html>
"""

@application.route('/')
def home():
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    return render_template_string(HTML_TEMPLATE, current_time=now)

@application.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "aws-elastic-beanstalk-python",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)