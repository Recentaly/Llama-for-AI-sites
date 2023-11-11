# Llama-for-AI-sites

Welcome to Llama-for-AI-sites, a Flask-based application designed to host multiple models from the Llama series, including "llama-2-7b," "llama-2-13b," and "llama-2-70b." It provides these models entirely free of charge for integration into various AI-driven sites and is specifically designed for [Venus Chub Ai](https://venus.chub.ai)

## Features

### Supported Models
- **llama-2-7b**: A powerful model designed for specific AI tasks.
- **llama-2-13b**: A larger version for more complex AI processing.
- **llama-2-70b**: The most extensive model for comprehensive AI capabilities.

### Routes
- `/chat/completions`: Use this route to facilitate chat completions powered by the Llama models.
- `/models`: Explore the available models and their specific functionalities.

## Usage
This Flask app is designed to be seamlessly integrated into various AI sites. It provides an API for accessing the mentioned Llama models, allowing developers to leverage its capabilities for different AI-driven purposes.

Because of it's routes, it can be used as a base for OpenAI proxies.

## Getting Started

### Prerequisites
- Python = 3.10
- Flask

### Installation
1. Clone the repository.
2. Install the required dependencies: `pip install -r requirements.txt`.
3. Run the Flask app: `python main.py`.

## Contributions
Contributions are welcome! If you have suggestions, bug reports, or enhancements, feel free to create issues or submit pull requests.

## Acknowledgments
- Thanks to the developers behind the Llama models for their incredible work.

<table>
  <tr>
     <td>
       <p align="center"> <img src="https://de.wikipedia.org/wiki/Datei:AGPLv3_Logo.svg" width="80%"></img>
    </td>
    <td> 
      <img src="https://img.shields.io/badge/License-GNU_GPL_v3.0-red.svg"/> <br> 
This project is licensed under the<a href="./LICENSE">AGNU_GPL_v3.0</a>. <img width=2300/>
    </td>
  </tr>
</table>
