from django.core.management.base import BaseCommand
from backend1.models import Hashtag

class Command(BaseCommand):
    help = 'Add predefined hashtags'

    def handle(self, *args, **kwargs):
        hashtags = [
            "web-development", "mobile-development", "game-development", "blockchain", "automatization",
            "databases", "data-science", "ai", "systems", "courses", "full-projects", "backend", "frontend", 
            "wordpress", "django", "flask", "node-js", "express-js", "php", "html-css", "javascript", 
            "react-js", "next-js", "vue-js", "bootstrap", "tailwind", "three-js", "vite", "java", "kotlin", 
            "flutter", "react-native", "unity", "unreal-engine", "rpg-maker", "godot", "phaser", "solidity", 
            "dao", "nft", "dapps", "defi", "web3-tools", "bots", "scripting-and-automation", "workflow-automation", 
            "robotic-process-automation", "email-automation", "data-automation", "automated-reporting", 
            "home-automation", "mysql", "postgresql", "sqlite", "realm", "firebase", "ipfs", "Data-Manipulation-Analysis",
            "machine-learning", "deep-learning", "data-visualization", "natural-language-processing", 
            "big-data-frameworks", "workflow-experiment-managment", "others", "Natural-Language-Processing-Generative-Models", 
            "computer-vision", "Machine-Learning-Frameworks", "reinforcement-learning", "ai-in-audio-music", 
            "auto-ml-ai-platforms", "ai-chatbots-assistants", "home-ai", "other-tools", "ubuntu", "ubuntu-server", 
            "windows", "linux-mint", "python", "docker", "c++", "video-graphic", "news", "article"
        ]

        for tag in sorted(hashtags, key=str.casefold):
            Hashtag.objects.get_or_create(name=tag)
            self.stdout.write(self.style.SUCCESS(f'Successfully added/checked hashtag {tag}'))
