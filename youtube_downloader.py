import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import yt_dlp
from moviepy.editor import VideoFileClip
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class YouTubeDownloader:
    def __init__(self):
        self.desktop_path = Path.home() / "Desktop"
        self.base_folder = self.desktop_path / "Youtube-Videos"
        self.base_folder.mkdir(exist_ok=True)
        
    def extract_topic_from_title(self, title):
        """Extract topic from video title (1-2 words)"""
        # Common programming topics and keywords
        topics = [
            # Frontend Technologies
            'react', 'vue', 'angular', 'svelte', 'nextjs', 'nuxt', 'gatsby', 'remix',
            'javascript', 'typescript', 'html', 'css', 'sass', 'scss', 'tailwind', 'bootstrap',
            'webpack', 'vite', 'parcel', 'rollup', 'babel', 'eslint', 'prettier', 'jest',
            'cypress', 'playwright', 'selenium', 'puppeteer', 'storybook', 'styled components',
            'material ui', 'ant design', 'chakra ui', 'mantine', 'react query', 'redux',
            'mobx', 'zustand', 'context api', 'hooks', 'components', 'frontend',
            
            # Backend Technologies
            'node', 'express', 'fastify', 'nestjs', 'koa', 'hapi', 'python', 'django',
            'flask', 'fastapi', 'spring boot', 'spring', 'java', 'ruby', 'rails', 'sinatra',
            'php', 'laravel', 'symfony', 'codeigniter', 'go', 'gin', 'echo', 'fiber',
            'rust', 'actix', 'rocket', 'axum', 'c#', 'asp.net', 'dotnet', 'elixir',
            'phoenix', 'scala', 'play', 'akka', 'backend', 'api', 'rest', 'graphql',
            'grpc', 'websocket', 'microservices', 'monolith', 'serverless', 'lambda',
            
            # Database Technologies
            'postgresql', 'mysql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server',
            'cassandra', 'dynamodb', 'firestore', 'supabase', 'prisma', 'sequelize',
            'typeorm', 'mongoose', 'sqlalchemy', 'hibernate', 'jpa', 'database', 'sql',
            'nosql', 'orm', 'migrations', 'seeding', 'indexing', 'query optimization',
            
            # DevOps & Infrastructure
            'docker', 'kubernetes', 'k8s', 'helm', 'terraform', 'ansible', 'puppet',
            'chef', 'jenkins', 'github actions', 'gitlab ci', 'circleci', 'travis ci',
            'aws', 'azure', 'gcp', 'google cloud', 'digitalocean', 'heroku', 'vercel',
            'netlify', 'cloudflare', 'nginx', 'apache', 'load balancer', 'cdn',
            'monitoring', 'prometheus', 'grafana', 'elasticsearch', 'kibana', 'logstash',
            'splunk', 'datadog', 'new relic', 'sentry', 'devops', 'ci cd', 'cicd',
            'infrastructure', 'deployment', 'scaling', 'performance', 'optimization',
            
            # Security & Authentication
            'jwt', 'oauth', 'saml', 'ldap', 'ssl', 'tls', 'https', 'encryption',
            'hashing', 'bcrypt', 'security', 'authentication', 'authorization', 'csrf',
            'xss', 'sql injection', 'vulnerability', 'penetration testing', 'audit',
            
            # Testing & Quality
            'testing', 'unit testing', 'integration testing', 'e2e testing', 'tdd',
            'bdd', 'mocking', 'stubbing', 'coverage', 'quality assurance', 'qa',
            
            # Version Control & Collaboration
            'git', 'github', 'gitlab', 'bitbucket', 'version control', 'code review',
            'pull request', 'merge request', 'branching', 'merging', 'conflicts',
            
            # Cloud Architecture
            'serverless', 'functions', 'faas', 'containers', 'orchestration', 'service mesh',
            'istio', 'linkerd', 'microservices', 'soa', 'event driven', 'message queue',
            'rabbitmq', 'kafka', 'sqs', 'pubsub', 'event sourcing', 'cqrs',
            
            # Development Tools & Practices
            'agile', 'scrum', 'kanban', 'lean', 'devops', 'code review', 'refactoring',
            'clean code', 'design patterns', 'architecture', 'system design', 'scaling',
            
            # Machine Learning & Data
            'machine learning', 'ai', 'data science', 'deep learning', 'neural networks',
            'tensorflow', 'pytorch', 'keras', 'scikit learn', 'pandas', 'numpy',
            'jupyter', 'data analysis', 'data engineering', 'etl', 'data pipeline',
            
            # Mobile Development
            'react native', 'flutter', 'swift', 'kotlin', 'android', 'ios', 'mobile',
            'xamarin', 'ionic', 'cordova', 'pwa', 'progressive web app',
            
            # Networking & Web Servers
            'http', 'https', 'tcp', 'udp', 'dns', 'dhcp', 'ftp', 'sftp', 'ssh', 'telnet',
            'smtp', 'pop3', 'imap', 'web server', 'apache', 'nginx', 'iis', 'caddy',
            'nginx reverse proxy', 'apache tomcat', 'jetty', 'undertow', 'lighttpd',
            'nodejs server', 'express server', 'fastapi server', 'django server', 'flask server',
            'networking', 'computer networks', 'network protocols', 'ip addressing', 'subnetting',
            'vlan', 'vpn', 'proxy server', 'reverse proxy', 'load balancer', 'cdn',
            'cloudflare', 'fastly', 'akamai', 'maxcdn', 'jsdelivr', 'unpkg',
            
            # Web Technologies & Protocols
            'websockets', 'socket.io', 'signalr', 'web rtc', 'webrtc', 'sip', 'rtp',
            'http2', 'http3', 'quic', 'grpc', 'rest api', 'soap', 'xml rpc',
            'json rpc', 'graphql', 'openapi', 'swagger', 'postman', 'insomnia',
            'curl', 'wget', 'httpie', 'axios', 'fetch api', 'xhr', 'ajax',
            
            # Web Performance & Optimization
            'web performance', 'optimization', 'caching', 'browser caching', 'server caching',
            'redis cache', 'memcached', 'varnish', 'cloudflare cache', 'cdn caching',
            'minification', 'compression', 'gzip', 'brotli', 'image optimization',
            'lazy loading', 'code splitting', 'tree shaking', 'bundle optimization',
            
            # Web Security & Protocols
            'cors', 'csp', 'hsts', 'xss protection', 'csrf protection', 'same site',
            'content security policy', 'https everywhere', 'ssl termination', 'certificate',
            'lets encrypt', 'wildcard ssl', 'multi domain ssl', 'certificate authority',
            
            # API & Integration
            'api gateway', 'microgateway', 'kong', 'apigee', 'aws api gateway',
            'webhook', 'callback', 'oauth2', 'openid connect', 'saml2', 'ldap',
            'active directory', 'authentication server', 'identity provider', 'federation',
            
            # Real-time & Streaming
            'streaming', 'live streaming', 'video streaming', 'audio streaming',
            'rtmp', 'hls', 'dash', 'mpeg dash', 'web streaming', 'media server',
            'wowza', 'ant media server', 'nginx rtmp', 'ffmpeg streaming',
            'real time', 'realtime', 'event streaming', 'data streaming',
            
            # Network Infrastructure
            'router', 'switch', 'firewall', 'intrusion detection', 'ids', 'ips',
            'network monitoring', 'wireshark', 'nmap', 'metasploit', 'penetration testing',
            'network security', 'cybersecurity', 'ethical hacking', 'security audit',
            
            # Cloud Networking
            'vpc', 'virtual private cloud', 'cloud networking', 'aws vpc', 'azure vnet',
            'gcp vpc', 'cloud firewall', 'network acl', 'security groups', 'nat gateway',
            'internet gateway', 'transit gateway', 'direct connect', 'expressroute',
            
            # DNS & Domain Management
            'dns management', 'domain registration', 'name servers', 'dns records',
            'a record', 'cname', 'mx record', 'txt record', 'ns record',
            'dns propagation', 'domain transfer', 'whois', 'dns lookup', 'dig',
            
            # Email & Communication
            'email server', 'mail server', 'exchange server', 'postfix', 'sendmail',
            'email protocols', 'smtp auth', 'spf', 'dkim', 'dmarc', 'email security',
            'mail relay', 'smtp gateway', 'email filtering', 'spam protection',
            
            # Monitoring & Analytics
            'network monitoring', 'server monitoring', 'uptime monitoring', 'performance monitoring',
            'google analytics', 'mixpanel', 'segment', 'hotjar', 'fullstory',
            'log analysis', 'siem', 'splunk', 'elk stack', 'graylog', 'fluentd',
            
            # Other Technologies
            'blockchain', 'bitcoin', 'ethereum', 'web3', 'smart contracts', 'nft',
            'metaverse', 'ar', 'vr', 'gaming', 'unity', 'unreal engine', 'iot',
            'raspberry pi', 'arduino', 'embedded', 'system programming'
        ]
        
        title_lower = title.lower()
        
        # Check for multi-word topics first
        for topic in sorted(topics, key=len, reverse=True):
            if topic in title_lower:
                return topic.replace(' ', '_')
        
        # If no specific topic found, try to extract first 1-2 meaningful words
        words = re.findall(r'\b[a-zA-Z]+\b', title)
        if len(words) >= 2:
            # Check if first two words form a common topic
            two_word_topic = f"{words[0]}_{words[1]}".lower()
            two_word_topics = [
                'machine_learning', 'data_science', 'web_development', 'artificial_intelligence',
                'react_native', 'next_js', 'vue_js', 'angular_js', 'spring_boot', 'asp_net',
                'node_js', 'express_js', 'django_rest', 'flask_api', 'fast_api', 'graphql_api',
                'rest_api', 'docker_compose', 'kubernetes_cluster', 'terraform_infra', 'ci_cd',
                'github_actions', 'gitlab_ci', 'aws_lambda', 'azure_functions', 'gcp_cloud',
                'microservices', 'serverless', 'dev_ops', 'full_stack', 'front_end', 'back_end',
                'data_pipeline', 'etl_pipeline', 'event_driven', 'message_queue', 'service_mesh',
                'load_balancer', 'content_delivery', 'database_design', 'api_gateway', 'security_testing',
                'penetration_testing', 'unit_testing', 'integration_testing', 'e2e_testing', 'code_review',
                'version_control', ' agile_development', 'scrum_master', 'kanban_board', 'lean_methodology',
                
                # Networking & Web Technologies
                'web_server', 'reverse_proxy', 'load_balancer', 'content_delivery', 'network_protocols',
                'computer_networks', 'network_security', 'web_performance', 'api_gateway', 'web_sockets',
                'web_rtc', 'http_protocol', 'dns_server', 'email_server', 'vpn_server',
                'proxy_server', 'firewall_config', 'network_monitoring', 'ssl_certificate', 'domain_registration',
                
                # Cloud & Infrastructure
                'cloud_networking', 'virtual_private_cloud', 'aws_vpc', 'azure_vnet', 'gcp_vpc',
                'cdn_caching', 'browser_caching', 'server_caching', 'redis_cache', 'memcached_cache',
                'nginx_server', 'apache_server', 'iis_server', 'caddy_server', 'tomcat_server',
                
                # Security & Protocols
                'cors_policy', 'csp_policy', 'hsts_policy', 'xss_protection', 'csrf_protection',
                'oauth2_auth', 'openid_connect', 'saml2_auth', 'ldap_server', 'active_directory',
                'ssl_termination', 'https_everywhere', 'certificate_authority', 'email_security',
                
                # Real-time & Streaming
                'live_streaming', 'video_streaming', 'audio_streaming', 'rtmp_streaming',
                'hls_streaming', 'dash_streaming', 'web_streaming', 'media_server',
                'real_time', 'event_streaming', 'data_streaming', 'realtime_communication',
                
                # Monitoring & Analytics
                'network_monitoring', 'server_monitoring', 'uptime_monitoring', 'performance_monitoring',
                'google_analytics', 'log_analysis', 'siem_system', 'elk_stack', 'dns_management',
                'domain_transfer', 'email_filtering', 'spam_protection', 'intrusion_detection'
            ]
            if two_word_topic in two_word_topics:
                return two_word_topic
        
        # Return first word as topic if nothing else matches
        if words:
            return words[0].lower()
        
        return 'general'
    
    def get_video_info(self, url):
        """Get video information including title and size"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'filesize': info.get('filesize', 0)
            }
    
    def download_video(self, url, output_path):
        """Download video from YouTube"""
        ydl_opts = {
            'outtmpl': str(output_path / '%(title)s.%(ext)s'),
            'format': 'worst[height<=720]/worst',
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'ignoreerrors': True,
            'retries': 3,
            'fragment_retries': 3,
        }
        
        try:
            logger.info("Starting download...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            logger.info("Download completed successfully!")
            return True
        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            return False
    
    def reduce_video_quality(self, video_path, max_size_mb=480):
        """Reduce video quality to meet size requirements"""
        video = VideoFileClip(str(video_path))
        
        # Try different quality settings
        quality_settings = [
            {'height': 480, 'bitrate': '500k'},
            {'height': 360, 'bitrate': '300k'},
            {'height': 240, 'bitrate': '200k'},
        ]
        
        for settings in quality_settings:
            temp_path = video_path.parent / f"temp_{video_path.name}"
            
            try:
                # Resize and compress
                resized_video = video.resize(height=settings['height'])
                resized_video.write_videofile(
                    str(temp_path),
                    bitrate=settings['bitrate'],
                    audio_bitrate='64k',
                    codec='libx264',
                    audio_codec='aac',
                    verbose=False,
                    logger=None
                )
                
                # Check file size
                temp_size_mb = temp_path.stat().st_size / (1024 * 1024)
                
                if temp_size_mb <= max_size_mb:
                    # Replace original with compressed version
                    video_path.unlink()
                    temp_path.rename(video_path)
                    logger.info(f"Reduced video quality to {settings['height']}p, size: {temp_size_mb:.1f}MB")
                    break
                else:
                    temp_path.unlink()
                    
            except Exception as e:
                logger.error(f"Error reducing quality: {e}")
                if temp_path.exists():
                    temp_path.unlink()
                continue
        
        video.close()
    
    def increase_video_speed(self, video_path, speed_factor=1.5):
        """Increase video playback speed"""
        try:
            video = VideoFileClip(str(video_path))
            
            # Increase speed
            sped_up_video = video.fl_time(lambda t: t / speed_factor, apply_to=['video', 'audio'])
            sped_up_video.fps = video.fps
            
            temp_path = video_path.parent / f"sped_up_{video_path.name}"
            
            # Write sped up video
            sped_up_video.write_videofile(
                str(temp_path),
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Replace original
            video_path.unlink()
            temp_path.rename(video_path)
            
            video.close()
            sped_up_video.close()
            
            logger.info(f"Increased video speed by {speed_factor}x")
            
        except Exception as e:
            logger.error(f"Error increasing video speed: {e}")
    
    def process_video(self, url):
        """Process a single video URL"""
        try:
            logger.info(f"Processing video: {url}")
            
            # Get video info
            info = self.get_video_info(url)
            title = info['title']
            logger.info(f"Video title: {title}")
            
            # Extract topic and create folder
            topic = self.extract_topic_from_title(title)
            topic_folder = self.base_folder / topic
            topic_folder.mkdir(exist_ok=True)
            
            # Download video
            logger.info("Downloading video...")
            self.download_video(url, topic_folder)
            
            # Find downloaded video file (allow more time for download to complete)
            import time
            time.sleep(2)  # Wait for file system to update
            
            video_files = list(topic_folder.glob("*.mp4")) + list(topic_folder.glob("*.webm")) + list(topic_folder.glob("*.mkv"))
            if not video_files:
                video_files = list(topic_folder.glob("*"))
                video_files = [f for f in video_files if f.is_file() and f.suffix in ['.mp4', '.webm', '.mkv', '.flv', '.avi', '.mov']]
            
            if not video_files:
                logger.error(f"No video file found for {title}")
                logger.info(f"Files in folder: {list(topic_folder.glob('*'))}")
                return False
            
            video_path = video_files[0]  # Take the first (should be only one)
            
            # Check file size
            file_size_mb = video_path.stat().st_size / (1024 * 1024)
            logger.info(f"Downloaded video size: {file_size_mb:.1f}MB")
            
            # Reduce quality if too large
            if file_size_mb > 500:
                logger.info("Video is too large, reducing quality...")
                self.reduce_video_quality(video_path)
                
                # Check new size
                new_size_mb = video_path.stat().st_size / (1024 * 1024)
                if new_size_mb > 480:
                    logger.warning(f"Could not reduce video below 480MB. Current size: {new_size_mb:.1f}MB")
            
            # Increase speed
            logger.info("Increasing video speed...")
            self.increase_video_speed(video_path)
            
            logger.info(f"Successfully processed: {title} -> {topic}/{video_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing video {url}: {e}")
            return False
    
    def process_urls_from_file(self, file_path):
        """Process all URLs from a text file"""
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        logger.info(f"Found {len(urls)} URLs to process")
        
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls, 1):
            logger.info(f"Processing URL {i}/{len(urls)}")
            if self.process_video(url):
                successful += 1
            else:
                failed += 1
        
        logger.info(f"Processing complete. Successful: {successful}, Failed: {failed}")

def main():
    # Check for FFmpeg (required for moviepy)
    import sys
    import os
    
    ffmpeg_found = False
    
    # First try to use bundled FFmpeg (in PyInstaller temp directory)
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        bundle_dir = sys._MEIPASS
        ffmpeg_path = os.path.join(bundle_dir, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            # Add bundle directory to PATH for this session
            os.environ['PATH'] = bundle_dir + os.pathsep + os.environ.get('PATH', '')
            ffmpeg_found = True
    
    # If not found in bundle, try system PATH
    if not ffmpeg_found:
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            ffmpeg_found = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            ffmpeg_found = False
    
    if not ffmpeg_found:
        logger.error("FFmpeg not found. Please install FFmpeg to use this script.")
        logger.error("Download from: https://ffmpeg.org/download.html")
        sys.exit(1)
    
    downloader = YouTubeDownloader()
    
    # Look for URLs file in current directory
    urls_file = "youtube_urls.txt"
    
    if len(sys.argv) > 1:
        urls_file = sys.argv[1]
    
    if not os.path.exists(urls_file):
        logger.error(f"URLs file not found: {urls_file}")
        logger.info("Please create a file with YouTube URLs (one per line)")
        logger.info("Or specify the file path as an argument")
        sys.exit(1)
    
    downloader.process_urls_from_file(urls_file)

if __name__ == "__main__":
    main()
