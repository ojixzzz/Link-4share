from flask import Flask
app = Flask(__name__)

import link4share.views.home
import link4share.views.download