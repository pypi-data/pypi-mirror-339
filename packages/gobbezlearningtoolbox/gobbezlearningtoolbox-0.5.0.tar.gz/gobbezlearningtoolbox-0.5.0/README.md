# PYPI PYTHON STUDY RESOURCES
This is a simple idea of grouping my notes and study material in a single space, 
thus creating a PyPi module where everyone can access these.
Also, the print-text is colored!

## Installation and Use
Install the module from PIP:
```bash
pip install gobbezlearningtoolbox
```

Check all the materials in the module:
```bash
from gobbezlearningtoolbox.listall import ListAll
print(ListAll())
```

Use the material you want to study and find all the contents (example code):
```bash
from gobbezlearningtoolbox.datascience import DataScience

ds = DataScience()
print(ds.help())
```

Pick a content and start studying (example code):
```bash
from gobbezlearningtoolbox.datascience import DataScience

ds = DataScience()
print(ds.machinelearning())
```

## List of materials:
#### DataScience: 
Methods and most common functions for Data Science, DataFrame manipulation and Machine Learning.
* imports_dataframe():
* imports_machinelearning(): 

* eda(): 
* operations():


#### DeepLearning:
Most common Keras Deep Learning models.
* imports(): Common imports for Keras

* common_path(): Simple step-by-step schema when dealing with Deep Learning 

* dense(): A densely connected network is a pile of Dense layers to elaborate vector data. 
* convnet(): Convolutions layers search local patterns, applying the same transformation to different (patch).
* rnn(): Recurrent Neural Network elaborates a single timestep input at time while keeping a state.

* pre_elaboration(): List the most used data pre-elaboration techniques

* callbacks(): Explain how to configure Keras Callbacks for different advanced techniques
* dropout(): Explain how to set a simple DropOut
* learning_rate_scheduler(): Explain how to modify learning rate based on epochs
* mixed_precision(): Explain how to setup a mixed_precision training
* gradient_accumulation(): Explain how to use gradient accumulation to increase batch size

* TensorBoard(): Show how to use Tensorflow TensorBoard to gain insights of your neural network
* plot_model(): Show how to use Keras plot_model to create an image of the layers of your neural network

* compile(): Explain how to compile a model
* train(): Explain how to train a model
* train_with_gradient_accumulation(): Explain advanced techniques for training a model
* predict_regression(): Explain how to make regression predictions with the model
* predict_classification(): Explain how to make classification predictions with the model
* evaluate(): Explain how to evaluate the model

* plot(): Explain how to plot results of the model

#### TelegramBot:
Simple quick-start guide for the python-telegram-bot module to create your own Telegram Bot.
* imports(): Find the most common imports to start 

* quick_start(): Quick setup explanations

#### Django:
Simple quick-start guide to configure and create your Django backend server and database.
* imports_project(): Most common imports for your main project
* imports_application(): Find the most common imports to use in your applications 

* example_main_urls(): Example of Urls of the main project 
* example_model(): Example of Model for your application 
* example_view(): Example of View for your application 
* example_urls(): Example of Urls for your application
        
* settings(): Django settings file explanations 
* commands(): Most important Django commands

#### Cookiecutter
Simple quick-start to build a pre-configured Django project.
* commands(): Cookiecutter commands

#### CreatePyPiModule
Simple commands to create your own PyPi Python module.
* details(): Get step-by-step details
* commands(): Commands to create your Python module

#### Ollama
Chat with an AI LLM model from Ollama directly in your Python code.
* imports(): Ollama imports
* commands(): Ollama shell commands to install a model
* chat(): Example code to configure and use a LLM model


## Contribute
You can contribute to the GitHub Repository or use it locally:
```bash
git clone https://github.com/gobbez/gobbezlearningtoolbox.git
```

## Notes
Please note that this module isn't complete, and it only gives a basic entry-level to start.
For more information contact me.
You can find the PyPi module here: https://pypi.org/project/gobbezlearningtoolbox


## Updates
* improved deeplearning (05/04/2025)
* added ollama (18/03/2025)
* added createpypimodule (18/03/2025)
* added cookiecutter (18/03/2025)
* added django (18/03/2025)
* added telegrambot (18/03/2025)
* added listall (15/03/2025)
* added deeplearning (15/03/2025)
* added datascience (15/03/2025)

