import requests, numpy as np, matplotlib.pyplot as plt, re, pandas as pd
from bs4 import BeautifulSoup
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1>Hello world.</h1>"

