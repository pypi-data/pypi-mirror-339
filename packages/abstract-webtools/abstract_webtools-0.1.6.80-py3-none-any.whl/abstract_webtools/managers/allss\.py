allss = """BASE_DIR = Path('/var/www/clownworld')
TEMPLATES_DIR = BASE_DIR / 'templates'
TEMPLATES_FOLDER_PATH = TEMPLATES_DIR / 'videos'
FLASK_APP_DIR = BASE_DIR  / 'video_player'
VIDEO_REACT = BASE_DIR / 'bolshevid'
BUILD_DIR = VIDEO_REACT / 'build'
STATIC_DIR = BUILD_DIR / 'static'
IMGS_DIR = STATIC_DIR / 'imgs'
CSS_DIR = STATIC_DIR / 'css'
JS_DIR = STATIC_DIR / 'js'
DATA_DIR = BASE_DIR / 'data'
VIDEOS_DIR = DATA_DIR / 'videos'
USERS_DIR = DATA_DIR / 'users'
DOWNLOADS_DIR = DATA_DIR / 'downloads'
DOWNLOADS_VIDS_DIR = DOWNLOADS_DIR / 'videos'"""
ste = ''
for alls in allss.split('\n'):
    ste+=f"{alls.split(' ')[0]},"
input(ste)
